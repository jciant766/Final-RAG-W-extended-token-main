"""
Legal Corrective RAG (CRAG) System for Malta Law
=================================================

A production-ready CRAG pipeline with built-in validation to prevent hallucinations
in legal document retrieval and answer generation.

Key Features:
- Document relevance grading (RELEVANT/IRRELEVANT/PARTIAL)
- Answer validation against source documents
- Strict citation requirements
- Confidence scoring
- Legal-specific validation (articles, numbers, dates)
"""

import os
import re
import json
from typing import List, Dict, Tuple, Optional, Literal
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv


class GradeLevel(Enum):
    """Document relevance grades"""
    RELEVANT = "RELEVANT"
    IRRELEVANT = "IRRELEVANT"
    PARTIAL = "PARTIAL"


@dataclass
class DocumentGrade:
    """Grading result for a retrieved document"""
    document_id: str
    grade: GradeLevel
    reasoning: str
    confidence: float


@dataclass
class ValidationResult:
    """Answer validation result"""
    grounded: bool
    confidence: float
    issues: List[str]
    citation_accuracy: float


@dataclass
class CRAGResponse:
    """Complete CRAG pipeline response"""
    question: str
    answer: str
    confidence: float
    grounded: bool
    relevant_docs: List[Dict]
    validation_result: ValidationResult
    grade_details: List[DocumentGrade]

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
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
                {
                    'doc_id': g.document_id,
                    'grade': g.grade.value,
                    'confidence': g.confidence
                }
                for g in self.grade_details
            ]
        }


class LegalCRAG:
    """
    Corrective RAG System for Legal Documents

    This class implements a multi-stage pipeline:
    1. Document Retrieval (from vector DB)
    2. Document Grading (relevance assessment)
    3. Answer Generation (using only relevant docs)
    4. Answer Validation (grounding check)

    The system enforces strict legal citation requirements and prevents
    hallucinations through validation.
    """

    # Confidence threshold for accepting answers
    CONFIDENCE_THRESHOLD = 0.85

    # Prompts for each stage
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
        """
        Initialize the CRAG system

        Args:
            llm_provider: Which LLM to use ("openai" or "anthropic")
            model_name: Specific model (defaults to gpt-4 or claude-3-sonnet)
            api_key: API key (if not in environment)
        """
        load_dotenv()
        if os.path.exists('env'):
            load_dotenv('env', override=True)

        self.llm_provider = llm_provider

        # Initialize LLM client
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
        """
        Call the configured LLM with a prompt

        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens in response

        Returns:
            The LLM's response text
        """
        try:
            if self.llm_provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.0  # Deterministic for legal use
                )
                return response.choices[0].message.content.strip()
            else:  # anthropic
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=0.0,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}")

    def grade_documents(
        self,
        question: str,
        documents: List[Dict]
    ) -> List[DocumentGrade]:
        """
        Grade each retrieved document for relevance

        This is the key CRAG innovation: we validate document relevance
        BEFORE using them for generation, filtering out irrelevant results.

        Args:
            question: The user's legal question
            documents: Retrieved documents from vector DB

        Returns:
            List of DocumentGrade objects
        """
        grades = []

        for doc in documents:
            # Extract document content and ID
            doc_id = doc.get('id', 'unknown')
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})

            # Truncate very long documents for grading
            content_preview = content[:2000] if len(content) > 2000 else content

            # Build grading prompt
            prompt = self.GRADING_PROMPT.format(
                question=question,
                document=f"[{metadata.get('citation', 'Unknown')}]\n{content_preview}"
            )

            # Get grade from LLM
            response = self._call_llm(prompt, max_tokens=50)

            # Parse response
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
                # Fallback: assume partial if unclear
                grade = GradeLevel.PARTIAL
                confidence = 0.50

            grades.append(DocumentGrade(
                document_id=doc_id,
                grade=grade,
                reasoning=response,
                confidence=confidence
            ))

        return grades

    def generate_answer(
        self,
        question: str,
        relevant_docs: List[Dict]
    ) -> str:
        """
        Generate an answer using only relevant documents

        Enforces strict citation requirements and prevents use of
        LLM's general knowledge.

        Args:
            question: The legal question
            relevant_docs: Filtered list of relevant documents

        Returns:
            Generated answer with citations
        """
        if not relevant_docs:
            return "Insufficient information in retrieved documents to answer this question about Malta law."

        # Format documents for the prompt
        docs_text = ""
        for i, doc in enumerate(relevant_docs, 1):
            metadata = doc.get('metadata', {})
            citation = metadata.get('citation', f'Document {i}')
            content = doc.get('content', '')
            docs_text += f"\n--- Document {i}: {citation} ---\n{content}\n"

        # Build generation prompt
        prompt = self.GENERATION_PROMPT.format(
            question=question,
            docs=docs_text
        )

        # Generate answer
        answer = self._call_llm(prompt, max_tokens=2000)

        return answer

    def validate_answer(
        self,
        answer: str,
        source_docs: List[Dict]
    ) -> ValidationResult:
        """
        Validate the generated answer against source documents

        This prevents hallucinations by checking:
        - All claims are in source docs
        - Citations are accurate
        - Numbers/dates match exactly

        Args:
            answer: The generated answer
            source_docs: The documents used for generation

        Returns:
            ValidationResult with grounding assessment
        """
        # Format source documents
        docs_text = ""
        for i, doc in enumerate(source_docs, 1):
            metadata = doc.get('metadata', {})
            citation = metadata.get('citation', f'Document {i}')
            content = doc.get('content', '')
            docs_text += f"\n--- {citation} ---\n{content}\n"

        # Build validation prompt
        prompt = self.VALIDATION_PROMPT.format(
            docs=docs_text,
            answer=answer
        )

        # Get validation from LLM
        response = self._call_llm(prompt, max_tokens=500)

        # Parse validation response
        grounded = self._parse_grounded(response)
        confidence = self._parse_confidence(response)
        issues = self._parse_issues(response)

        # Check citation accuracy
        citation_accuracy = self._check_citations(answer, source_docs)

        # Adjust confidence based on citation accuracy
        final_confidence = min(confidence, citation_accuracy)

        return ValidationResult(
            grounded=grounded,
            confidence=final_confidence,
            issues=issues,
            citation_accuracy=citation_accuracy
        )

    def _parse_grounded(self, response: str) -> bool:
        """Parse GROUNDED field from validation response"""
        if "GROUNDED:" in response.upper():
            grounded_line = [
                line for line in response.split('\n')
                if 'GROUNDED:' in line.upper()
            ][0]
            return "YES" in grounded_line.upper()
        return False

    def _parse_confidence(self, response: str) -> float:
        """Parse CONFIDENCE field from validation response"""
        if "CONFIDENCE:" in response.upper():
            conf_line = [
                line for line in response.split('\n')
                if 'CONFIDENCE:' in line.upper()
            ][0]
            # Extract number
            match = re.search(r'(\d+\.?\d*)', conf_line)
            if match:
                return float(match.group(1))
        return 0.5  # Default medium confidence

    def _parse_issues(self, response: str) -> List[str]:
        """Parse ISSUES field from validation response"""
        if "ISSUES:" in response.upper():
            issues_line = [
                line for line in response.split('\n')
                if 'ISSUES:' in line.upper()
            ]
            if issues_line:
                issues_text = issues_line[0].split(':', 1)[1].strip()
                if "NONE" in issues_text.upper() or issues_text == "[]":
                    return []
                # Parse list
                issues = [
                    i.strip().strip('[]"\'')
                    for i in issues_text.split(',')
                ]
                return [i for i in issues if i]
        return []

    def _check_citations(self, answer: str, source_docs: List[Dict]) -> float:
        """
        Check that all citations in the answer exist in source documents

        Returns a score from 0.0 to 1.0 representing citation accuracy
        """
        # Extract citations from answer (format: [Document, Article X])
        citation_pattern = r'\[([^\]]+)\]'
        citations = re.findall(citation_pattern, answer)

        if not citations:
            # No citations found - this is bad for legal answers
            return 0.5

        # Get all available citations from source docs
        available_citations = set()
        for doc in source_docs:
            metadata = doc.get('metadata', {})
            citation = metadata.get('citation', '')
            article = metadata.get('article', '')
            if citation:
                available_citations.add(citation)
            if article:
                available_citations.add(f"Article {article}")

        # Check each citation
        valid_citations = 0
        for citation in citations:
            citation = citation.strip()
            # Check if citation matches any source
            is_valid = any(
                avail.lower() in citation.lower() or citation.lower() in avail.lower()
                for avail in available_citations
            )
            if is_valid:
                valid_citations += 1

        # Calculate accuracy
        accuracy = valid_citations / len(citations) if citations else 0.0
        return accuracy

    def answer_legal_question(
        self,
        question: str,
        retrieved_docs: List[Dict],
        verbose: bool = False
    ) -> CRAGResponse:
        """
        Complete CRAG pipeline: grade, generate, validate

        This is the main entry point that orchestrates all stages.

        Args:
            question: The legal question
            retrieved_docs: Documents from vector database
            verbose: Whether to print progress

        Returns:
            CRAGResponse with complete pipeline results
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"CRAG Pipeline: {question}")
            print(f"{'='*60}")

        # Stage 1: Grade documents
        if verbose:
            print(f"\n[1/4] Grading {len(retrieved_docs)} retrieved documents...")

        grades = self.grade_documents(question, retrieved_docs)

        # Filter to relevant and partial documents
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
            print(f"\n[3/4] Validating answer against source documents...")

        validation = self.validate_answer(answer, relevant_docs)

        if verbose:
            print(f"  Grounded: {validation.grounded}")
            print(f"  Confidence: {validation.confidence:.2f}")
            print(f"  Citation accuracy: {validation.citation_accuracy:.2f}")
            if validation.issues:
                print(f"  Issues: {', '.join(validation.issues)}")

        # Stage 4: Apply confidence threshold
        if verbose:
            print(f"\n[4/4] Applying confidence threshold ({self.CONFIDENCE_THRESHOLD})...")

        if validation.confidence < self.CONFIDENCE_THRESHOLD:
            if verbose:
                print(f"  ⚠ Answer rejected (confidence too low)")
            answer = f"[LOW CONFIDENCE - {validation.confidence:.2f}] " + answer
        else:
            if verbose:
                print(f"  ✓ Answer accepted")

        # Build response
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
            print(f"\n{'='*60}")
            print(f"Pipeline Complete")
            print(f"{'='*60}\n")

        return response


class SimpleVectorDB:
    """
    Simple in-memory vector database for testing

    This is a minimal implementation that can be swapped out for
    production vector databases like ChromaDB, Pinecone, etc.
    """

    def __init__(self):
        """Initialize empty document store"""
        self.documents: List[Dict] = []
        self.embeddings: List[List[float]] = []

        # Initialize OpenAI for embeddings
        load_dotenv()
        if os.path.exists('env'):
            load_dotenv('env', override=True)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = "text-embedding-3-large"

    def add_documents(self, documents: List[Dict]):
        """
        Add documents to the database

        Args:
            documents: List of dicts with 'id', 'content', 'metadata'
        """
        for doc in documents:
            # Generate embedding
            embedding = self._embed_text(doc['content'])

            self.documents.append(doc)
            self.embeddings.append(embedding)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant documents

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of documents with similarity scores
        """
        if not self.documents:
            return []

        # Embed query
        query_embedding = self._embed_text(query)

        # Calculate cosine similarity
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            similarities.append((i, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top-k
        results = []
        for i, score in similarities[:top_k]:
            doc = self.documents[i].copy()
            doc['score'] = score
            results.append(doc)

        return results

    def _embed_text(self, text: str) -> List[float]:
        """Generate embedding for text"""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        return dot_product / (norm1 * norm2) if norm1 and norm2 else 0.0
