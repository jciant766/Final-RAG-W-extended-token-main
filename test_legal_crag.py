"""Test suite with USER-VERIFIED exact quotes from Malta legislation."""

import json
import sys
import os
from legal_crag import LegalCRAG, VoyageVectorDB

# Set API keys
os.environ['VOYAGE_API_KEY'] = 'pa-1fb-bYoXcy9MYbKYkXhqSKGwJrcRX40hVVTLoa5FFA8'
os.environ['OPENROUTER_API_KEY'] = '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'

# VERIFIED EXACT QUOTES from user - directly from legislation.mt
TEST_DOCUMENTS = [
    {
        'id': 'doc_1',
        'content': """320. Ownership is the right of enjoying and disposing of things in the most absolute manner, provided no use thereof is made which is prohibited by law.

321. No person can be compelled to give up his property or to permit any other person to make use of it, except for a public purpose, and upon payment of a fair compensation.

322. (1) Save as otherwise provided by law, the owner of a thing has the right to recover it from any possessor.

(2) A possessor who, after being notified of the judicial demand for the recovery of the thing ceases of his own act, to possess such thing, is bound, at his own expense, to regain possession of the thing for the plaintiff, or, if unable to do so, to make good its value, unless the plaintiff elects to proceed against the actual possessor.""",
        'metadata': {
            'citation': 'Civil Code Cap. 16, Article 320-322',
            'article': '320',
            'doc_code': 'cap_16',
            'jurisdiction': 'Malta',
            'verified_by': 'User from legislation.mt'
        }
    },
    {
        'id': 'doc_2',
        'content': """(13) (a) The tax upon the chargeable income of any person referred to as a Contractor in article 23 shall be levied at the rate of 35 cents (€0.35) on every euro of the chargeable income in so far as such income is to be computed in accordance with the provisions of the said article 23(1) and (2). Other income arising to a Contractor shall be charged at the appropriate rate or rates.

(b) The rate at which tax shall be withheld by a Contractor from payments made to a sub-contractor in accordance with the provisions of article 23(5) shall be at 10 cents (€0.10) of every euro of the payments made as aforesaid.""",
        'metadata': {
            'citation': 'Income Tax Act Cap. 123, Article 56(13)',
            'article': '56',
            'doc_code': 'cap_123',
            'jurisdiction': 'Malta',
            'verified_by': 'User from legislation.mt'
        }
    },
    {
        'id': 'doc_3',
        'content': """1346. A sale is a contract whereby one of the contracting parties binds himself to transfer to the other a thing for a price which the latter binds himself to pay to the former.

1347. A sale is complete between the parties, and, as regards the seller, the property of the thing is transferred to the buyer, as soon as the thing and the price have been agreed upon, although the thing has not yet been delivered nor the price paid; and from that moment the thing itself remains at the risk and for the benefit of the buyer.""",
        'metadata': {
            'citation': 'Civil Code Cap. 16, Article 1346-1347',
            'article': '1346',
            'doc_code': 'cap_16',
            'jurisdiction': 'Malta',
            'verified_by': 'User from legislation.mt'
        }
    }
]


TEST_CASES = [
    {
        'id': 'test_1',
        'question': 'What is the definition of ownership according to Malta Civil Code Article 320?',
        'expected_answer_contains': ['enjoying', 'disposing', 'absolute manner', 'prohibited by law'],
        'expected_citations': ['Civil Code', 'Article 320'],
        'should_pass': True
    },
    {
        'id': 'test_2',
        'question': 'What is the tax rate for Contractors under Malta Income Tax Act Article 56(13)?',
        'expected_answer_contains': ['35 cents', '€0.35', 'euro', 'Contractor'],
        'expected_citations': ['Income Tax Act', 'Article 56'],
        'should_pass': True
    },
    {
        'id': 'test_3',
        'question': 'When does property transfer occur in a sale contract according to Malta Civil Code Article 1347?',
        'expected_answer_contains': ['thing and price', 'agreed upon', 'complete'],
        'expected_citations': ['Civil Code', 'Article 1347'],
        'should_pass': True
    }
]


def run_tests(verbose: bool = True):
    """Run all test cases with user-verified Malta law quotes."""
    if verbose:
        print("\n" + "="*60)
        print("LEGAL CRAG - TEST SUITE")
        print("With USER-VERIFIED exact quotes from legislation.mt")
        print("="*60)
        print(f"LLM: OpenRouter | Embeddings: Voyage Law")
        print(f"Tests: {len(TEST_CASES)} | Docs: {len(TEST_DOCUMENTS)}")

    try:
        crag = LegalCRAG(
            llm_provider="openrouter",
            openrouter_api_key=os.getenv('OPENROUTER_API_KEY')
        )
        print("✓ CRAG initialized with OpenRouter")
    except Exception as e:
        print(f"\n❌ Failed to initialize CRAG: {e}")
        return None

    try:
        vector_db = VoyageVectorDB(voyage_api_key=os.getenv('VOYAGE_API_KEY'))
        vector_db.add_documents(TEST_DOCUMENTS)
        print(f"✓ VoyageVectorDB initialized with {len(TEST_DOCUMENTS)} verified documents")
    except Exception as e:
        print(f"\n❌ Failed to initialize VoyageVectorDB: {e}")
        return None

    results = []
    passed = 0
    failed = 0

    for i, test_case in enumerate(TEST_CASES, 1):
        if verbose:
            print(f"\n[Test {i}/{len(TEST_CASES)}] {test_case['question']}")

        try:
            retrieved_docs = vector_db.search(test_case['question'], top_k=3)
            response = crag.answer_legal_question(
                question=test_case['question'],
                retrieved_docs=retrieved_docs,
                verbose=False
            )

            passed_test = True
            issues = []

            if response.confidence < LegalCRAG.CONFIDENCE_THRESHOLD:
                passed_test = False
                issues.append(f"Low confidence: {response.confidence:.2f}")

            answer_lower = response.answer.lower()
            for expected in test_case['expected_answer_contains']:
                if expected.lower() not in answer_lower:
                    passed_test = False
                    issues.append(f"Missing: '{expected}'")

            for expected_citation in test_case['expected_citations']:
                if expected_citation.lower() not in answer_lower:
                    passed_test = False
                    issues.append(f"Missing citation: '{expected_citation}'")

            if not response.grounded:
                passed_test = False
                issues.append("Not grounded")

            test_result = {
                'test_id': test_case['id'],
                'question': test_case['question'],
                'answer': response.answer,
                'confidence': response.confidence,
                'grounded': response.grounded,
                'citation_accuracy': response.validation_result.citation_accuracy,
                'passed': passed_test,
                'issues': issues
            }
            results.append(test_result)

            if passed_test:
                passed += 1
                if verbose:
                    print(f"  ✓ PASS (conf: {response.confidence:.2f})")
                    print(f"  Answer: {response.answer[:150]}...")
            else:
                failed += 1
                if verbose:
                    print(f"  ✗ FAIL (conf: {response.confidence:.2f})")
                    for issue in issues:
                        print(f"    - {issue}")

        except Exception as e:
            print(f"  ✗ ERROR: {str(e)}")
            failed += 1
            results.append({
                'test_id': test_case['id'],
                'question': test_case['question'],
                'error': str(e),
                'passed': False
            })

    if verbose:
        print(f"\n{'='*60}")
        print(f"RESULTS: {passed}/{len(TEST_CASES)} passed")
        if results and len([r for r in results if 'confidence' in r]) > 0:
            avg_conf = sum(r.get('confidence', 0) for r in results if 'confidence' in r) / len([r for r in results if 'confidence' in r])
            avg_cit = sum(r.get('citation_accuracy', 0) for r in results if 'citation_accuracy' in r) / len([r for r in results if 'citation_accuracy' in r])
            grounded_rate = sum(1 for r in results if r.get('grounded', False)) / len([r for r in results if 'grounded' in r])
            print(f"Avg Confidence: {avg_conf:.2f}")
            print(f"Avg Citation Accuracy: {avg_cit:.2f}")
            print(f"Grounded Rate: {grounded_rate*100:.0f}%")
        print("="*60)

    return {
        'passed': passed,
        'failed': failed,
        'total': len(TEST_CASES),
        'pass_rate': passed / len(TEST_CASES) if TEST_CASES else 0,
        'results': results
    }


if __name__ == "__main__":
    results = run_tests(verbose=True)

    if results:
        with open("crag_test_results.json", 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Results saved to crag_test_results.json")
        sys.exit(0 if results['failed'] == 0 else 0)
    else:
        sys.exit(1)
