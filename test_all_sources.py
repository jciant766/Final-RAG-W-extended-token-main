"""
Test script to verify all document sources are properly indexed in vector database
"""
import json
from collections import Counter

def test_sources():
    """Check which documents are indexed in processed_chunks.json"""

    print("=" * 70)
    print("TESTING VECTOR DATABASE SOURCES")
    print("=" * 70)

    try:
        with open('processed_chunks.json', 'r', encoding='utf-8') as f:
            chunks = json.load(f)

        print(f"\nLoaded {len(chunks)} total chunks")

        # Count documents
        doc_counter = Counter()
        doc_code_counter = Counter()

        for chunk in chunks:
            metadata = chunk.get('metadata', {})
            doc_name = metadata.get('document', 'Unknown')
            doc_code = metadata.get('doc_code', 'Unknown')

            doc_counter[doc_name] += 1
            doc_code_counter[doc_code] += 1

        print("\n" + "=" * 70)
        print("DOCUMENTS IN VECTOR DATABASE:")
        print("=" * 70)

        for doc_name, count in sorted(doc_counter.items()):
            print(f"  {doc_name}: {count} chunks")

        print("\n" + "=" * 70)
        print("DOCUMENT CODES:")
        print("=" * 70)

        for doc_code, count in sorted(doc_code_counter.items()):
            print(f"  {doc_code}: {count} chunks")

        print("\n" + "=" * 70)
        print("SUMMARY:")
        print("=" * 70)
        print(f"  Total unique documents: {len(doc_counter)}")
        print(f"  Total unique doc codes: {len(doc_code_counter)}")
        print(f"  Total chunks: {len(chunks)}")

        # Check for commercial code dominance
        commercial_code_chunks = doc_counter.get('Commercial Code (Cap. 13)', 0)
        if commercial_code_chunks > 0:
            percentage = (commercial_code_chunks / len(chunks)) * 100
            print(f"\nWARNING: Commercial Code represents {percentage:.1f}% of all chunks")
            if percentage > 50:
                print("     WARNING: Commercial Code is dominating the database!")

        # Check if Companies Act is present
        companies_act_count = sum(count for doc, count in doc_counter.items() if 'Companies Act' in doc or '386' in doc)
        if companies_act_count == 0:
            print("\nWARNING: No Companies Act chunks found!")
        else:
            print(f"\nCompanies Act present with {companies_act_count} chunks")

    except FileNotFoundError:
        print("\nERROR: processed_chunks.json not found!")
        print("   Run build_vector_db.py first to create the vector database")
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    test_sources()
