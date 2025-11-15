"""Test suite for Malta Legal CRAG with EXPANDED document database."""

import json
import sys
import os
from legal_crag import LegalCRAG, VoyageVectorDB
from malta_law_database import MALTA_LAW_DOCUMENTS

# Set API keys
os.environ['VOYAGE_API_KEY'] = 'pa-1fb-bYoXcy9MYbKYkXhqSKGwJrcRX40hVVTLoa5FFA8'
os.environ['OPENROUTER_API_KEY'] = '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'

# Expanded test questions covering multiple legal areas
TEST_QUESTIONS = [
    # Property Law
    {
        'question': 'What is the definition of ownership according to Malta Civil Code?',
        'expected_citation': 'Civil Code Cap. 16, Article 320',
        'topic': 'Property Law - Ownership'
    },
    {
        'question': 'Can a person be forced to give up their property in Malta?',
        'expected_citation': 'Civil Code Cap. 16, Article 321',
        'topic': 'Property Law - Expropriation'
    },

    # Tax Law
    {
        'question': 'What is the tax rate for Contractors under Malta Income Tax Act Article 56(13)?',
        'expected_citation': 'Income Tax Act Cap. 123, Article 56(13)',
        'topic': 'Tax Law - Contractor Rate'
    },

    # Contract Law
    {
        'question': 'When does property transfer occur in a sale contract according to Malta law?',
        'expected_citation': 'Civil Code Cap. 16, Article 1347',
        'topic': 'Contract Law - Property Transfer'
    },
    {
        'question': 'What is the definition of a sale contract in Malta?',
        'expected_citation': 'Civil Code Cap. 16, Article 1346',
        'topic': 'Contract Law - Sale Definition'
    },

    # Notarial Regulations
    {
        'question': 'What is the minimum insurance coverage required for notaries in Malta?',
        'expected_citation': 'Notaries (Compulsory Insurance) Regulations Cap. 55.07, Article 3',
        'topic': 'Professional Regulation - Insurance'
    },
    {
        'question': 'What does "breach" mean in the context of notarial insurance regulations?',
        'expected_citation': 'Notaries (Compulsory Insurance) Regulations Cap. 55.07, Article 2',
        'topic': 'Professional Regulation - Definitions'
    },

    # Public Registry
    {
        'question': 'Where are the Public Registry offices located in Malta?',
        'expected_citation': 'Public Registry Act Cap. 56, Articles 1-2',
        'topic': 'Administrative Law - Public Registry'
    },
    {
        'question': 'Who manages the Public Registry Office and what oath must they take?',
        'expected_citation': 'Public Registry Act Cap. 56, Article 3',
        'topic': 'Administrative Law - Registry Management'
    },

    # Title Examination
    {
        'question': 'What exemptions exist for notaries from examining title to immovable property?',
        'expected_citation': 'Examination of Title Regulations Cap. 55.06, Article 4',
        'topic': 'Notarial Procedure - Title Exemptions'
    },
    {
        'question': 'What does "transferee" mean in title examination regulations?',
        'expected_citation': 'Examination of Title Regulations Cap. 55.06, Article 2',
        'topic': 'Notarial Procedure - Definitions'
    },

    # Deceased Notaries
    {
        'question': 'What happens to acts of deceased notaries that are not in conformity with the law?',
        'expected_citation': 'Acts of Deceased Notaries Regulations Cap. 55.05, Articles 1-2',
        'topic': 'Notarial Procedure - Deceased Notaries'
    }
]

def run_expanded_tests():
    """Run comprehensive tests on expanded Malta law database."""

    print("=" * 60)
    print("MALTA LEGAL CRAG - EXPANDED TEST SUITE")
    print("=" * 60)
    print(f"Documents in database: {len(MALTA_LAW_DOCUMENTS)}")
    print(f"Test questions: {len(TEST_QUESTIONS)}")
    print(f"Coverage: Property, Tax, Contract, Notarial, Public Registry Law")
    print("=" * 60)

    try:
        # Initialize CRAG system
        crag = LegalCRAG()
        print("✓ CRAG initialized with OpenRouter")

        # Initialize vector database with ALL Malta law documents
        vector_db = VoyageVectorDB()
        for doc in MALTA_LAW_DOCUMENTS:
            vector_db.add_document(
                doc_id=doc['id'],
                content=doc['content'],
                metadata=doc['metadata']
            )
        print(f"✓ VoyageVectorDB initialized with {len(MALTA_LAW_DOCUMENTS)} documents")
        print()

        # Track results
        results = []
        passed = 0
        failed = 0

        # Run each test
        for i, test in enumerate(TEST_QUESTIONS, 1):
            question = test['question']
            expected_citation = test['expected_citation']
            topic = test['topic']

            print(f"[Test {i}/{len(TEST_QUESTIONS)}] {topic}")
            print(f"Q: {question}")

            try:
                # Retrieve relevant documents
                retrieved_docs = vector_db.search(question, top_k=3)

                # Run CRAG pipeline
                response = crag.query(question, retrieved_docs)

                # Check results
                if response.grounded and response.confidence >= crag.CONFIDENCE_THRESHOLD:
                    print(f"  ✓ PASS (confidence: {response.confidence:.2f})")
                    print(f"  Answer: {response.answer[:150]}...")
                    passed += 1
                    status = "PASS"
                else:
                    print(f"  ✗ FAIL (confidence: {response.confidence:.2f})")
                    if not response.grounded:
                        print(f"    - Not grounded in sources")
                    if response.validation_result.issues:
                        for issue in response.validation_result.issues:
                            print(f"    - {issue}")
                    failed += 1
                    status = "FAIL"

                results.append({
                    'test_number': i,
                    'topic': topic,
                    'question': question,
                    'expected_citation': expected_citation,
                    'status': status,
                    'confidence': response.confidence,
                    'grounded': response.grounded,
                    'answer': response.answer,
                    'citations_found': [doc['metadata'].get('citation') for doc in response.relevant_docs],
                    'validation_issues': response.validation_result.issues
                })

            except Exception as e:
                print(f"  ✗ ERROR: {str(e)}")
                failed += 1
                results.append({
                    'test_number': i,
                    'topic': topic,
                    'question': question,
                    'status': 'ERROR',
                    'error': str(e)
                })

            print()

        # Print summary
        print("=" * 60)
        print(f"RESULTS: {passed}/{len(TEST_QUESTIONS)} passed")
        if passed > 0:
            print(f"Success rate: {(passed/len(TEST_QUESTIONS)*100):.1f}%")
            avg_confidence = sum(r['confidence'] for r in results if 'confidence' in r) / max(passed, 1)
            print(f"Avg confidence: {avg_confidence:.2f}")
        print("=" * 60)

        # Save detailed results
        with open('expanded_crag_test_results.json', 'w') as f:
            json.dump({
                'total_tests': len(TEST_QUESTIONS),
                'passed': passed,
                'failed': failed,
                'success_rate': passed/len(TEST_QUESTIONS) if len(TEST_QUESTIONS) > 0 else 0,
                'database_size': len(MALTA_LAW_DOCUMENTS),
                'results': results
            }, f, indent=2)

        print("\n✓ Detailed results saved to expanded_crag_test_results.json")

        return passed == len(TEST_QUESTIONS)

    except Exception as e:
        print(f"\n✗ Test suite failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_expanded_tests()
    sys.exit(0 if success else 1)
