"""Legal CRAG System for Malta Law - Production-ready pipeline with validation."""

import os
import re
from typing import List, Dict, Optional, Literal
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv


class GradeLevel(Enum):
    RELEVANT = "RELEVANT"
    IRRELEVANT = "IRRELEVANT"
    PARTIAL = "PARTIAL"


@dataclass
class DocumentGrade:
    document_id: str
    grade: GradeLevel
    reasoning: str
    confidence: float


@dataclass
class ValidationResult:
    grounded: bool
    confidence: float
    issues: List[str]
    citation_accuracy: float


@dataclass
class CRAGResponse:
    question: str
    answer: str
    confidence: float
    grounded: bool
    relevant_docs: List[Dict]
    validation_result: ValidationResult
    grade_details: List[DocumentGrade]

    def to_dict(self) -> Dict:
        return {
            'question': self.question,
            'answer': self.answer,
            'confidence': self.confidence,
            'grounded': self.grounded,
            'relevant_doc_count': len(self.relevant_docs),
            'validation': {
                'grounded': self.validation_result.grounded,
                'confidence': self.validation_result.confidence,
                'issues': self.validation_result.issues,
                'citation_accuracy': self.validation_result.citation_accuracy
            },
            'grades': [
                {'doc_id': g.document_id, 'grade': g.grade.value, 'confidence': g.confidence}
                for g in self.grade_details
            ]
        }


class LegalCRAG:
    """Corrective RAG pipeline: Retrieve → Grade → Generate → Validate"""

    CONFIDENCE_THRESHOLD = 0.85

    GRADING_PROMPT = """You are grading legal documents for relevance to a Malta law question.

Question: {question}

Document Content:
{document}

Does this document directly answer the question about Malta law?
Consider:
1. Is this about Malta jurisdiction (not other countries)?
2. Does it address the specific legal topic asked about?
3. Does it contain information that helps answer the question?

Respond with ONLY ONE WORD: RELEVANT, IRRELEVANT, or PARTIAL

Your response:"""

    GENERATION_PROMPT = """You are a legal research assistant for Malta law.

Question: {question}

Relevant Documents:
{docs}

CRITICAL INSTRUCTIONS:
1. Answer ONLY using the provided documents above
2. Cite ALL sources as [Document Title, Article X] or [Document Title, Page Y]
3. If documents don't fully answer the question, say "Based on available documents..."
4. NEVER use general legal knowledge or information not in the documents
5. If you cannot answer from the documents, say "Insufficient information in retrieved documents"
6. Include specific article numbers and exact quotes when possible

Your answer:"""

    VALIDATION_PROMPT = """Validate this legal answer strictly against source documents.

Source Documents:
{docs}

Generated Answer:
{answer}

Validation Checklist:
1. Is every claim in the answer found in the source documents?
2. Do all article citations actually exist in the documents?
3. Do all numbers (fines, percentages, dates) match exactly?
4. Are quotes accurate?
5. Is the jurisdiction (Malta) correct?

Respond in this EXACT format:
GROUNDED: YES or NO
CONFIDENCE: 0.0-1.0
ISSUES: [list specific problems, or write "None"]

Your validation:"""

    def __init__(
        self,
        llm_provider: Literal["openai", "anthropic"] = "openai",
        model_name: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        load_dotenv()
        if os.path.exists('env'):
            load_dotenv('env', override=True)

        self.llm_provider = llm_provider

        if llm_provider == "openai":
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found")
            self.client = OpenAI(api_key=api_key)
            self.model = model_name or "gpt-4"
        elif llm_provider == "anthropic":
            api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found")
            self.client = Anthropic(api_key=api_key)
            self.model = model_name or "claude-3-5-sonnet-20241022"
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")

    def _call_llm(self, prompt: str, max_tokens: int = 2000) -> str:
        try:
            if self.llm_provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.0
                )
                return response.choices[0].message.content.strip()
            else:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=0.0,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}")

    def grade_documents(self, question: str, documents: List[Dict]) -> List[DocumentGrade]:
        """Grade each retrieved document for relevance."""
        grades = []

        for doc in documents:
            doc_id = doc.get('id', 'unknown')
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})

            content_preview = content[:2000] if len(content) > 2000 else content

            prompt = self.GRADING_PROMPT.format(
                question=question,
                document=f"[{metadata.get('citation', 'Unknown')}]\n{content_preview}"
            )

            response = self._call_llm(prompt, max_tokens=50)

            response_upper = response.upper().strip()
            if "RELEVANT" in response_upper and "IRRELEVANT" not in response_upper:
                grade = GradeLevel.RELEVANT
                confidence = 0.95
            elif "IRRELEVANT" in response_upper:
                grade = GradeLevel.IRRELEVANT
                confidence = 0.90
            elif "PARTIAL" in response_upper:
                grade = GradeLevel.PARTIAL
                confidence = 0.70
            else:
                grade = GradeLevel.PARTIAL
                confidence = 0.50

            grades.append(DocumentGrade(
                document_id=doc_id,
                grade=grade,
                reasoning=response,
                confidence=confidence
            ))

        return grades

    def generate_answer(self, question: str, relevant_docs: List[Dict]) -> str:
        """Generate answer using only relevant documents."""
        if not relevant_docs:
            return "Insufficient information in retrieved documents to answer this question about Malta law."

        docs_text = ""
        for i, doc in enumerate(relevant_docs, 1):
            metadata = doc.get('metadata', {})
            citation = metadata.get('citation', f'Document {i}')
            content = doc.get('content', '')
            docs_text += f"\n--- Document {i}: {citation} ---\n{content}\n"

        prompt = self.GENERATION_PROMPT.format(question=question, docs=docs_text)
        answer = self._call_llm(prompt, max_tokens=2000)
        return answer

    def validate_answer(self, answer: str, source_docs: List[Dict]) -> ValidationResult:
        """Validate generated answer against source documents."""
        docs_text = ""
        for i, doc in enumerate(source_docs, 1):
            metadata = doc.get('metadata', {})
            citation = metadata.get('citation', f'Document {i}')
            content = doc.get('content', '')
            docs_text += f"\n--- {citation} ---\n{content}\n"

        prompt = self.VALIDATION_PROMPT.format(docs=docs_text, answer=answer)
        response = self._call_llm(prompt, max_tokens=500)

        grounded = self._parse_grounded(response)
        confidence = self._parse_confidence(response)
        issues = self._parse_issues(response)
        citation_accuracy = self._check_citations(answer, source_docs)

        final_confidence = min(confidence, citation_accuracy)

        return ValidationResult(
            grounded=grounded,
            confidence=final_confidence,
            issues=issues,
            citation_accuracy=citation_accuracy
        )

    def _parse_grounded(self, response: str) -> bool:
        if "GROUNDED:" in response.upper():
            grounded_line = [line for line in response.split('\n') if 'GROUNDED:' in line.upper()][0]
            return "YES" in grounded_line.upper()
        return False

    def _parse_confidence(self, response: str) -> float:
        if "CONFIDENCE:" in response.upper():
            conf_line = [line for line in response.split('\n') if 'CONFIDENCE:' in line.upper()][0]
            match = re.search(r'(\d+\.?\d*)', conf_line)
            if match:
                return float(match.group(1))
        return 0.5

    def _parse_issues(self, response: str) -> List[str]:
        if "ISSUES:" in response.upper():
            issues_line = [line for line in response.split('\n') if 'ISSUES:' in line.upper()]
            if issues_line:
                issues_text = issues_line[0].split(':', 1)[1].strip()
                if "NONE" in issues_text.upper() or issues_text == "[]":
                    return []
                issues = [i.strip().strip('[]"\'') for i in issues_text.split(',')]
                return [i for i in issues if i]
        return []

    def _check_citations(self, answer: str, source_docs: List[Dict]) -> float:
        """Check citation accuracy (0.0-1.0)."""
        citation_pattern = r'\[([^\]]+)\]'
        citations = re.findall(citation_pattern, answer)

        if not citations:
            return 0.5

        available_citations = set()
        for doc in source_docs:
            metadata = doc.get('metadata', {})
            citation = metadata.get('citation', '')
            article = metadata.get('article', '')
            if citation:
                available_citations.add(citation)
            if article:
                available_citations.add(f"Article {article}")

        valid_citations = 0
        for citation in citations:
            citation = citation.strip()
            is_valid = any(
                avail.lower() in citation.lower() or citation.lower() in avail.lower()
                for avail in available_citations
            )
            if is_valid:
                valid_citations += 1

        return valid_citations / len(citations) if citations else 0.0

    def answer_legal_question(
        self,
        question: str,
        retrieved_docs: List[Dict],
        verbose: bool = False
    ) -> CRAGResponse:
        """Complete CRAG pipeline: grade → generate → validate."""
        if verbose:
            print(f"\n{'='*60}\nCRAG Pipeline: {question}\n{'='*60}")

        # Stage 1: Grade documents
        if verbose:
            print(f"\n[1/4] Grading {len(retrieved_docs)} documents...")

        grades = self.grade_documents(question, retrieved_docs)

        relevant_docs = [
            doc for doc, grade in zip(retrieved_docs, grades)
            if grade.grade in [GradeLevel.RELEVANT, GradeLevel.PARTIAL]
        ]

        if verbose:
            relevant_count = sum(1 for g in grades if g.grade == GradeLevel.RELEVANT)
            partial_count = sum(1 for g in grades if g.grade == GradeLevel.PARTIAL)
            irrelevant_count = sum(1 for g in grades if g.grade == GradeLevel.IRRELEVANT)
            print(f"  ✓ Relevant: {relevant_count}")
            print(f"  ~ Partial: {partial_count}")
            print(f"  ✗ Irrelevant: {irrelevant_count}")

        # Stage 2: Generate answer
        if verbose:
            print(f"\n[2/4] Generating answer from {len(relevant_docs)} relevant docs...")

        answer = self.generate_answer(question, relevant_docs)

        if verbose:
            print(f"  Answer length: {len(answer)} chars")

        # Stage 3: Validate answer
        if verbose:
            print(f"\n[3/4] Validating answer...")

        validation = self.validate_answer(answer, relevant_docs)

        if verbose:
            print(f"  Grounded: {validation.grounded}")
            print(f"  Confidence: {validation.confidence:.2f}")
            print(f"  Citation accuracy: {validation.citation_accuracy:.2f}")
            if validation.issues:
                print(f"  Issues: {', '.join(validation.issues)}")

        # Stage 4: Apply confidence threshold
        if verbose:
            print(f"\n[4/4] Applying threshold ({self.CONFIDENCE_THRESHOLD})...")

        if validation.confidence < self.CONFIDENCE_THRESHOLD:
            if verbose:
                print(f"  ⚠ Low confidence")
            answer = f"[LOW CONFIDENCE - {validation.confidence:.2f}] " + answer
        else:
            if verbose:
                print(f"  ✓ Accepted")

        response = CRAGResponse(
            question=question,
            answer=answer,
            confidence=validation.confidence,
            grounded=validation.grounded,
            relevant_docs=relevant_docs,
            validation_result=validation,
            grade_details=grades
        )

        if verbose:
            print(f"\n{'='*60}\nComplete\n{'='*60}\n")

        return response


class SimpleVectorDB:
    """In-memory vector database for testing."""

    def __init__(self):
        self.documents: List[Dict] = []
        self.embeddings: List[List[float]] = []

        load_dotenv()
        if os.path.exists('env'):
            load_dotenv('env', override=True)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = "text-embedding-3-large"

    def add_documents(self, documents: List[Dict]):
        """Add documents to the database."""
        for doc in documents:
            embedding = self._embed_text(doc['content'])
            self.documents.append(doc)
            self.embeddings.append(embedding)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant documents."""
        if not self.documents:
            return []

        query_embedding = self._embed_text(query)

        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)

        results = []
        for i, score in similarities[:top_k]:
            doc = self.documents[i].copy()
            doc['score'] = score
            results.append(doc)

        return results

    def _embed_text(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        return dot_product / (norm1 * norm2) if norm1 and norm2 else 0.0
