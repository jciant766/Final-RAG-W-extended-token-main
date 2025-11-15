"""
Automated Malta Law Article Extractor

This tool automatically:
1. Reads raw text from PDFs or text files
2. Detects article numbers and sub-articles
3. Chunks articles properly (no token limits)
4. Generates metadata automatically
5. Adds to malta_law_database.py

Usage:
    python auto_extract_malta_law.py --input "path/to/file.pdf" --act "Civil Code" --chapter "Cap. 16"
    python auto_extract_malta_law.py --input "path/to/file.txt" --act "Civil Code" --chapter "Cap. 16"
"""

import re
import os
import sys
import argparse
from typing import List, Dict, Tuple
from pathlib import Path

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file."""
    try:
        import PyPDF2

        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

        return text
    except ImportError:
        print("⚠️  PyPDF2 not installed. Install with: pip install PyPDF2")
        print("   Alternatively, use pdftotext: pip install pdftotext")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error reading PDF: {str(e)}")
        sys.exit(1)

def read_text_file(file_path: str) -> str:
    """Read text from .txt file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"✗ Error reading text file: {str(e)}")
        sys.exit(1)

def detect_articles(text: str) -> List[Dict[str, str]]:
    """
    Detect articles and sub-articles in Malta law text.

    Article pattern: Number followed by period (e.g., "15.", "320.")
    Sub-article pattern: Number in parentheses (e.g., "(1)", "(2)", "(a)")
    """

    # Clean up text
    text = text.strip()

    # Remove common headers that aren't articles
    text = re.sub(r'CAP\.\s*\d+\.\]', '', text)
    text = re.sub(r'\[Cap\.\s*\d+\.', '', text)

    articles = []

    # Split by article number pattern
    # Pattern: start of line or newline, then number(s), then period, then space
    # Example: "15. " or "320. "
    article_pattern = r'\n(\d+)\.\s+'

    # Find all article starts
    article_matches = list(re.finditer(article_pattern, text))

    if not article_matches:
        print("⚠️  No articles detected. Text might need cleaning.")
        print("   First 200 chars of text:")
        print(f"   {text[:200]}")
        return []

    # Extract each article with its content
    for i, match in enumerate(article_matches):
        article_num = match.group(1)
        start_pos = match.end()

        # Find end position (start of next article or end of text)
        if i + 1 < len(article_matches):
            end_pos = article_matches[i + 1].start()
        else:
            end_pos = len(text)

        # Extract article content
        article_content = text[start_pos:end_pos].strip()

        # Full article text with number
        full_article = f"{article_num}. {article_content}"

        articles.append({
            'article_num': article_num,
            'content': full_article,
            'has_subarticles': bool(re.search(r'\(\d+\)', article_content))
        })

    return articles

def group_related_articles(articles: List[Dict], max_group_size: int = 4) -> List[List[Dict]]:
    """
    Group sequential articles that should be chunked together.

    Rules:
    - Sequential numbers (320, 321, 322)
    - Max 4 articles per group (unless very short)
    - Respect semantic breaks
    """

    if not articles:
        return []

    groups = []
    current_group = [articles[0]]

    for i in range(1, len(articles)):
        prev_article = articles[i-1]
        curr_article = articles[i]

        prev_num = int(prev_article['article_num'])
        curr_num = int(curr_article['article_num'])

        # Check if sequential
        is_sequential = (curr_num == prev_num + 1)

        # Check if group is getting too large
        group_too_large = len(current_group) >= max_group_size

        if is_sequential and not group_too_large:
            # Add to current group
            current_group.append(curr_article)
        else:
            # Start new group
            groups.append(current_group)
            current_group = [curr_article]

    # Add last group
    if current_group:
        groups.append(current_group)

    return groups

def generate_topic(article_content: str, article_num: str) -> str:
    """
    Generate a topic name from article content.
    Uses first sentence or key terms.
    """

    # Common legal terms to identify topics
    topic_keywords = {
        'ownership': 'Ownership',
        'property': 'Property Rights',
        'sale': 'Sale Contracts',
        'purchase': 'Purchase Agreements',
        'tax': 'Taxation',
        'insurance': 'Insurance Requirements',
        'notary': 'Notarial Procedures',
        'registry': 'Registry Procedures',
        'title': 'Title Examination',
        'transfer': 'Property Transfer',
        'contract': 'Contracts',
        'marriage': 'Marriage',
        'divorce': 'Divorce',
        'inheritance': 'Inheritance',
        'succession': 'Succession',
        'company': 'Corporate Law',
        'employment': 'Employment',
        'criminal': 'Criminal Law',
        'testament': 'Testamentary Provisions',
        'will': 'Wills and Testaments',
        'breach': 'Breach and Liability',
        'damages': 'Damages'
    }

    content_lower = article_content.lower()

    # Check for keyword matches
    for keyword, topic in topic_keywords.items():
        if keyword in content_lower:
            return topic

    # Fallback: use first few words or article number
    first_sentence = article_content.split('.')[0][:50]
    if len(first_sentence) > 5:
        return first_sentence.strip()

    return f"Article {article_num}"

def create_document_entry(article_group: List[Dict], act_name: str, chapter: str) -> Dict:
    """
    Create a database entry for a group of articles.
    """

    # Combine article content
    if len(article_group) == 1:
        # Single article
        article = article_group[0]
        article_range = article['article_num']
        content = article['content']
    else:
        # Multiple articles
        first_num = article_group[0]['article_num']
        last_num = article_group[-1]['article_num']
        article_range = f"{first_num}-{last_num}"
        content = "\n\n".join([a['content'] for a in article_group])

    # Generate topic
    topic = generate_topic(content, article_group[0]['article_num'])

    # Create ID
    chapter_id = chapter.replace(' ', '_').replace('.', '_')
    article_id_str = article_range.replace('-', '_')
    doc_id = f"doc_{chapter_id}_art_{article_id_str}"

    # Create citation
    citation = f"{act_name} {chapter}, Article {article_range}"

    # Create document entry
    doc = {
        'id': doc_id,
        'content': content,
        'metadata': {
            'citation': citation,
            'article': article_range,
            'chapter': chapter,
            'act_name': act_name,
            'topic': topic,
            'jurisdiction': 'Malta',
            'verified_source': 'legislation.mt',
            'auto_extracted': True
        }
    }

    return doc

def extract_articles_from_file(
    file_path: str,
    act_name: str,
    chapter: str,
    topic_override: str = None
) -> List[Dict]:
    """
    Main extraction function.

    Args:
        file_path: Path to PDF or TXT file
        act_name: Name of the act (e.g., "Civil Code")
        chapter: Chapter number (e.g., "Cap. 16")
        topic_override: Optional topic to override auto-detection

    Returns:
        List of document entries ready for database
    """

    print(f"📄 Reading file: {file_path}")

    # Read file based on extension
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        text = read_text_file(file_path)
    else:
        print(f"✗ Unsupported file type. Use .pdf or .txt")
        sys.exit(1)

    print(f"✓ File read successfully ({len(text)} characters)")

    # Detect articles
    print("🔍 Detecting articles and sub-articles...")
    articles = detect_articles(text)

    if not articles:
        print("✗ No articles detected. Check file format.")
        return []

    print(f"✓ Detected {len(articles)} articles")

    # Show detected articles
    print("\nDetected articles:")
    for article in articles[:10]:  # Show first 10
        sub_marker = " [has sub-articles]" if article['has_subarticles'] else ""
        print(f"  • Article {article['article_num']}{sub_marker}")
    if len(articles) > 10:
        print(f"  ... and {len(articles) - 10} more")

    # Group related articles
    print(f"\n📦 Grouping related articles...")
    groups = group_related_articles(articles)
    print(f"✓ Created {len(groups)} chunks")

    # Create document entries
    print("\n📝 Generating database entries...")
    documents = []
    for group in groups:
        doc = create_document_entry(group, act_name, chapter)
        documents.append(doc)

        # Show what was created
        article_range = doc['metadata']['article']
        topic = doc['metadata']['topic']
        token_count = len(doc['content']) // 4  # Rough estimate
        print(f"  ✓ Article {article_range}: {topic} (~{token_count} tokens)")

    print(f"\n✅ Generated {len(documents)} document entries")

    return documents

def append_to_database(documents: List[Dict], database_file: str = 'malta_law_database.py'):
    """
    Append new documents to the existing database file.
    """

    print(f"\n💾 Adding to database: {database_file}")

    # Read current database
    try:
        with open(database_file, 'r') as f:
            db_content = f.read()
    except FileNotFoundError:
        print(f"✗ Database file not found: {database_file}")
        return False

    # Find the insertion point (before the closing bracket of MALTA_LAW_DOCUMENTS)
    # Look for the last ']' which closes the list
    insertion_point = db_content.rfind(']')

    if insertion_point == -1:
        print("✗ Could not find database list in file")
        return False

    # Generate Python code for new documents
    new_entries = []
    for doc in documents:
        # Format as Python dict
        entry = f"""    {{
        'id': '{doc['id']}',
        'content': '''{doc['content']}''',
        'metadata': {{
            'citation': '{doc['metadata']['citation']}',
            'article': '{doc['metadata']['article']}',
            'chapter': '{doc['metadata']['chapter']}',
            'act_name': '{doc['metadata']['act_name']}',
            'topic': '{doc['metadata']['topic']}',
            'jurisdiction': '{doc['metadata']['jurisdiction']}',
            'verified_source': '{doc['metadata']['verified_source']}',
            'auto_extracted': {doc['metadata']['auto_extracted']}
        }}
    }}"""
        new_entries.append(entry)

    # Insert new entries
    new_code = ",\n\n".join(new_entries)

    # Insert before closing bracket
    updated_content = (
        db_content[:insertion_point-1] +  # -1 to remove last comma/newline
        ",\n\n" +
        new_code +
        "\n" +
        db_content[insertion_point:]
    )

    # Write back
    with open(database_file, 'w') as f:
        f.write(updated_content)

    print(f"✅ Added {len(documents)} documents to database")
    return True

def save_as_new_file(documents: List[Dict], output_file: str):
    """
    Save documents as a new Python file.
    """

    print(f"\n💾 Saving to new file: {output_file}")

    # Generate Python code
    code = f'''"""
Auto-extracted Malta Law Documents
Generated by auto_extract_malta_law.py
"""

EXTRACTED_DOCUMENTS = [
'''

    for doc in documents:
        code += f"""    {{
        'id': '{doc['id']}',
        'content': '''{doc['content']}''',
        'metadata': {{
            'citation': '{doc['metadata']['citation']}',
            'article': '{doc['metadata']['article']}',
            'chapter': '{doc['metadata']['chapter']}',
            'act_name': '{doc['metadata']['act_name']}',
            'topic': '{doc['metadata']['topic']}',
            'jurisdiction': '{doc['metadata']['jurisdiction']}',
            'verified_source': '{doc['metadata']['verified_source']}',
            'auto_extracted': {doc['metadata']['auto_extracted']}
        }}
    }},

"""

    code += "]\n"

    # Write file
    with open(output_file, 'w') as f:
        f.write(code)

    print(f"✅ Saved {len(documents)} documents to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Auto-extract Malta law articles')
    parser.add_argument('--input', '-i', required=True, help='Input PDF or TXT file')
    parser.add_argument('--act', '-a', required=True, help='Act name (e.g., "Civil Code")')
    parser.add_argument('--chapter', '-c', required=True, help='Chapter (e.g., "Cap. 16")')
    parser.add_argument('--topic', '-t', help='Optional topic override')
    parser.add_argument('--output', '-o', help='Save to new file instead of appending to database')
    parser.add_argument('--preview', '-p', action='store_true', help='Preview only, do not save')

    args = parser.parse_args()

    # Check input file exists
    if not os.path.exists(args.input):
        print(f"✗ File not found: {args.input}")
        sys.exit(1)

    # Extract articles
    documents = extract_articles_from_file(
        args.input,
        args.act,
        args.chapter,
        args.topic
    )

    if not documents:
        print("✗ No documents extracted")
        sys.exit(1)

    # Preview mode
    if args.preview:
        print("\n" + "="*60)
        print("PREVIEW MODE - Documents NOT saved")
        print("="*60)
        for i, doc in enumerate(documents, 1):
            print(f"\n[{i}] {doc['metadata']['citation']}")
            print(f"Topic: {doc['metadata']['topic']}")
            print(f"Content preview: {doc['content'][:200]}...")
        sys.exit(0)

    # Save documents
    if args.output:
        save_as_new_file(documents, args.output)
    else:
        append_to_database(documents)

    print("\n✅ Done!")
    print(f"\nNext steps:")
    print(f"1. Review the added documents in malta_law_database.py")
    print(f"2. Run: python test_expanded_crag.py")
    print(f"3. Add more documents or adjust as needed")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # No arguments - show usage
        print("="*60)
        print("Malta Law Auto-Extractor")
        print("="*60)
        print("\nUsage:")
        print("  python auto_extract_malta_law.py -i FILE -a ACT -c CHAPTER")
        print("\nExamples:")
        print("  # Extract from PDF")
        print('  python auto_extract_malta_law.py -i civil_code.pdf -a "Civil Code" -c "Cap. 16"')
        print("\n  # Extract from TXT")
        print('  python auto_extract_malta_law.py -i tax_act.txt -a "Income Tax Act" -c "Cap. 123"')
        print("\n  # Preview without saving")
        print('  python auto_extract_malta_law.py -i file.pdf -a "Civil Code" -c "Cap. 16" --preview')
        print("\n  # Save to separate file")
        print('  python auto_extract_malta_law.py -i file.pdf -a "Act" -c "Cap. X" -o extracted.py')
        print("\nOptions:")
        print("  -i, --input     Input PDF or TXT file (required)")
        print("  -a, --act       Act name (required)")
        print("  -c, --chapter   Chapter number (required)")
        print("  -t, --topic     Optional topic override")
        print("  -o, --output    Save to new file instead of appending")
        print("  -p, --preview   Preview only, do not save")
        print("\nFile locations:")
        print("  Place PDFs/TXT files in: ./pdf_inputs/")
        print("  Extracted data goes to: malta_law_database.py")
        print("="*60)
        sys.exit(0)

    main()
