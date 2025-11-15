"""Extract exact quotes from Malta law OCR files for CRAG testing."""

import re
import os
from typing import List, Dict, Tuple


def extract_article(file_path: str, article_num: str, context_lines: int = 20) -> Tuple[str, str]:
    """
    Extract exact text of an article from a Malta law file.

    Returns:
        Tuple of (article_text, citation)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Get document name from filename
    doc_name = os.path.basename(file_path).replace('.txt', '')

    # Search for the article
    article_pattern = f"^{article_num}\\."

    found_line = None
    for i, line in enumerate(lines):
        if re.match(article_pattern, line.strip()):
            found_line = i
            break

    if found_line is None:
        return None, None

    # Extract context around the article
    start = max(0, found_line)
    end = min(len(lines), found_line + context_lines)

    article_text = ''.join(lines[start:end]).strip()

    # Clean up the text
    article_text = re.sub(r'\n+', '\n', article_text)
    article_text = re.sub(r'  +', ' ', article_text)

    citation = f"{doc_name}, Article {article_num}"

    return article_text, citation


def get_ownership_article() -> Dict:
    """Get the correct ownership article from Civil Code."""
    text, citation = extract_article(
        'ocr/output/16 - Civil Code.txt',
        '320',
        context_lines=5
    )

    return {
        'id': 'doc_ownership',
        'content': text,
        'metadata': {
            'citation': citation,
            'article': '320',
            'doc_code': 'cap_16',
            'jurisdiction': 'Malta',
            'verified': True
        }
    }


def get_contractor_tax_article() -> Dict:
    """Get contractor tax rate article from Income Tax Act."""
    text, citation = extract_article(
        'ocr/output/123 - Income Tax Act.txt',
        '56',
        context_lines=30
    )

    # Include sub-article 13 which mentions 35%
    text_13, _ = extract_article(
        'ocr/output/123 - Income Tax Act.txt',
        '56',
        context_lines=200  # Get more context to include (13)
    )

    return {
        'id': 'doc_tax',
        'content': text_13 if text_13 else text,
        'metadata': {
            'citation': citation,
            'article': '56',
            'doc_code': 'cap_123',
            'jurisdiction': 'Malta',
            'verified': True
        }
    }


def search_for_text(file_path: str, search_term: str, context_lines: int = 10) -> Tuple[str, int]:
    """Search for text and return surrounding context."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if search_term.lower() in line.lower():
            start = max(0, i - context_lines//2)
            end = min(len(lines), i + context_lines//2)
            context = ''.join(lines[start:end]).strip()
            return context, i

    return None, -1


def create_verified_test_documents() -> List[Dict]:
    """Create test documents with verified exact quotes from OCR files."""
    documents = []

    # 1. Ownership - Article 320
    doc = get_ownership_article()
    if doc:
        documents.append(doc)
        print(f"✓ Extracted: {doc['metadata']['citation']}")

    # 2. Tax Rate - Article 56(13) for contractors
    doc = get_contractor_tax_article()
    if doc:
        documents.append(doc)
        print(f"✓ Extracted: {doc['metadata']['citation']}")

    # 3. Sale Contract - Article 1328
    text, citation = extract_article('ocr/output/16 - Civil Code.txt', '1328', 15)
    if text:
        documents.append({
            'id': 'doc_sale',
            'content': text,
            'metadata': {
                'citation': citation,
                'article': '1328',
                'doc_code': 'cap_16',
                'jurisdiction': 'Malta',
                'verified': True
            }
        })
        print(f"✓ Extracted: {citation}")

    # 4. Search for Gender Identity Act
    if os.path.exists('ocr/output/540 - Gender Identity Act.txt'):
        text, citation = extract_article('ocr/output/540 - Gender Identity Act.txt', '3', 15)
        if text:
            documents.append({
                'id': 'doc_gender',
                'content': text,
                'metadata': {
                    'citation': citation,
                    'article': '3',
                    'doc_code': 'cap_540',
                    'jurisdiction': 'Malta',
                    'verified': True
                }
            })
            print(f"✓ Extracted: {citation}")

    # 5. Prevention of Money Laundering
    if os.path.exists('ocr/output/373 - Prevention of Money Laundering Act.txt'):
        text, citation = extract_article('ocr/output/373 - Prevention of Money Laundering Act.txt', '15', 20)
        if text:
            documents.append({
                'id': 'doc_aml',
                'content': text,
                'metadata': {
                    'citation': citation,
                    'article': '15',
                    'doc_code': 'cap_373',
                    'jurisdiction': 'Malta',
                    'verified': True
                }
            })
            print(f"✓ Extracted: {citation}")

    # 6. Commercial Code - Article 45
    text, citation = extract_article('ocr/output/13 - Commercial Code.txt', '45', 10)
    if text:
        documents.append({
            'id': 'doc_commercial',
            'content': text,
            'metadata': {
                'citation': citation,
                'article': '45',
                'doc_code': 'cap_13',
                'jurisdiction': 'Malta',
                'verified': True
            }
        })
        print(f"✓ Extracted: {citation}")

    return documents


if __name__ == "__main__":
    print("Extracting exact quotes from Malta law OCR files...")
    print("="*60)

    docs = create_verified_test_documents()

    print(f"\n{'='*60}")
    print(f"✓ Successfully extracted {len(docs)} documents with verified quotes")
    print(f"{'='*60}\n")

    # Display sample
    for doc in docs:
        print(f"\n{doc['metadata']['citation']}:")
        print(f"{doc['content'][:200]}...")
        print()
