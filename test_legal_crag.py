"""
Test Suite for Legal CRAG System
=================================

This script tests the CRAG pipeline with 5 known Malta law questions
and evaluates the system's performance.
"""

import json
from legal_crag import LegalCRAG, SimpleVectorDB


# Test documents - realistic Malta legal content
TEST_DOCUMENTS = [
    {
        'id': 'doc_1',
        'content': """Article 965 of the Civil Code (Cap. 16) of Malta

        Ownership is the right to enjoy and dispose of things in the most absolute manner,
        provided they are not used in a way prohibited by laws or regulations.

        The owner may dispose of his property by gratuitous or onerous title, or may dispose
        thereof by will in favour of such persons as he may deem fit.

        However, ownership is subject to expropriation for public utility in accordance with law.

        Article 966

        The owner of a thing possesses by the sole force of ownership even though he is not
        in actual possession thereof.""",
        'metadata': {
            'citation': 'Civil Code Cap. 16, Article 965-966',
            'article': '965',
            'doc_code': 'cap_16',
            'jurisdiction': 'Malta'
        }
    },
    {
        'id': 'doc_2',
        'content': """Article 56 of the Income Tax Act (Cap. 123) of Malta

        Every person carrying on a trade, business or profession in Malta shall be chargeable
        to tax in respect of the profits or gains arising from such trade, business or profession.

        The standard rate of tax for companies registered in Malta is thirty-five per cent (35%).

        Article 56A - Tax Refunds

        Shareholders may be entitled to a refund of six-sevenths (6/7) of the Malta tax paid
        on profits distributed as dividends, subject to certain conditions.""",
        'metadata': {
            'citation': 'Income Tax Act Cap. 123, Article 56',
            'article': '56',
            'doc_code': 'cap_123',
            'jurisdiction': 'Malta'
        }
    },
    {
        'id': 'doc_3',
        'content': """Article 3 of the Gender Identity Act (Cap. 540) of Malta

        Every person has the right to gender identity and to the free development of their
        person according to their gender identity.

        No person shall be subjected to clinical procedures or treatment as a precondition
        to legal gender recognition.

        Article 4 - Gender Recognition

        Any person over the age of eighteen (18) years may apply to have their gender identity
        recognized by submitting a declaration to the Director of Public Registry.

        For minors aged sixteen (16) to eighteen (18) years, parental consent is required.""",
        'metadata': {
            'citation': 'Gender Identity Act Cap. 540, Article 3-4',
            'article': '3',
            'doc_code': 'cap_540',
            'jurisdiction': 'Malta'
        }
    },
    {
        'id': 'doc_4',
        'content': """Article 1328 of the Civil Code (Cap. 16) of Malta

        A contract of sale is a contract whereby one party, called the seller, binds himself
        to deliver a thing and to transfer the ownership thereof, and the other party, called
        the buyer, binds himself to pay the price thereof in money.

        Article 1329

        The contract of sale is perfected by mere consent, even though the thing is not yet
        delivered or the price paid.

        The property passes to the buyer as soon as there is agreement on the thing and the
        price, even though delivery has not yet been made.""",
        'metadata': {
            'citation': 'Civil Code Cap. 16, Article 1328-1329',
            'article': '1328',
            'doc_code': 'cap_16',
            'jurisdiction': 'Malta'
        }
    },
    {
        'id': 'doc_5',
        'content': """Article 15 of the Prevention of Money Laundering Act (Cap. 373) of Malta

        Subject persons shall apply customer due diligence measures when:
        (a) establishing a business relationship;
        (b) carrying out an occasional transaction that amounts to €15,000 or more;
        (c) there is a suspicion of money laundering or terrorist financing.

        Article 16 - Customer Due Diligence

        Customer due diligence measures include:
        (i) identifying the customer and verifying the customer's identity;
        (ii) identifying the beneficial owner and taking reasonable measures to verify identity;
        (iii) obtaining information on the purpose and intended nature of the business relationship.

        Penalties for non-compliance may include fines up to €200,000 and imprisonment.""",
        'metadata': {
            'citation': 'Prevention of Money Laundering Act Cap. 373, Article 15-16',
            'article': '15',
            'doc_code': 'cap_373',
            'jurisdiction': 'Malta'
        }
    },
    {
        'id': 'doc_6',
        'content': """Article 45 of the Commercial Code (Cap. 13) of Malta

        Every merchant is obliged to keep orderly accounting books showing his commercial
        operations and the state of his assets and liabilities.

        These books must be kept for a period of ten (10) years from the date of the last entry.

        The books of merchants constitute evidence in commercial matters.""",
        'metadata': {
            'citation': 'Commercial Code Cap. 13, Article 45',
            'article': '45',
            'doc_code': 'cap_13',
            'jurisdiction': 'Malta'
        }
    },
    {
        'id': 'doc_7',
        'content': """Companies Act (Cap. 386) - French Law

        This is a French commercial law provision about company formation.
        Companies in France must register with the Registre du Commerce.
        Directors must be appointed according to French corporate governance standards.

        [Note: This is NOT Malta law - used for testing irrelevant document filtering]""",
        'metadata': {
            'citation': 'French Companies Act',
            'article': '1',
            'doc_code': 'france',
            'jurisdiction': 'France'
        }
    }
]


# Test cases with known answers
TEST_CASES = [
    {
        'id': 'test_1',
        'question': 'What is the corporate tax rate in Malta?',
        'expected_answer_contains': ['35%', 'thirty-five per cent', 'companies'],
        'expected_citations': ['Income Tax Act', 'Cap. 123', 'Article 56'],
        'should_pass': True,
        'description': 'Test basic factual question with specific number'
    },
    {
        'id': 'test_2',
        'question': 'What defines ownership according to Malta Civil Code?',
        'expected_answer_contains': ['enjoy', 'dispose', 'absolute manner'],
        'expected_citations': ['Civil Code', 'Cap. 16', 'Article 965'],
        'should_pass': True,
        'description': 'Test legal definition question'
    },
    {
        'id': 'test_3',
        'question': 'What is the minimum age for gender recognition in Malta without parental consent?',
        'expected_answer_contains': ['eighteen', '18'],
        'expected_citations': ['Gender Identity Act', 'Cap. 540'],
        'should_pass': True,
        'description': 'Test specific age requirement'
    },
    {
        'id': 'test_4',
        'question': 'When does property transfer occur in a sale contract in Malta?',
        'expected_answer_contains': ['agreement', 'thing and price', 'consent'],
        'expected_citations': ['Civil Code', 'Article 1329'],
        'should_pass': True,
        'description': 'Test procedural legal question'
    },
    {
        'id': 'test_5',
        'question': 'What is the penalty for money laundering violations in Malta?',
        'expected_answer_contains': ['200,000', 'imprisonment', 'fine'],
        'expected_citations': ['Prevention of Money Laundering Act', 'Cap. 373'],
        'should_pass': True,
        'description': 'Test penalty/enforcement question'
    }
]


def run_tests(llm_provider: str = "openai", verbose: bool = True):
    """
    Run all test cases and measure performance

    Args:
        llm_provider: Which LLM to use ("openai" or "anthropic")
        verbose: Whether to print detailed output

    Returns:
        Test results dictionary
    """
    if verbose:
        print("\n" + "="*80)
        print("LEGAL CRAG SYSTEM - TEST SUITE")
        print("="*80)
        print(f"\nLLM Provider: {llm_provider.upper()}")
        print(f"Test Cases: {len(TEST_CASES)}")
        print(f"Test Documents: {len(TEST_DOCUMENTS)}")
        print("="*80)

    # Initialize CRAG system
    try:
        crag = LegalCRAG(llm_provider=llm_provider)
    except Exception as e:
        print(f"\n❌ Failed to initialize CRAG system: {e}")
        print("Make sure you have set OPENAI_API_KEY or ANTHROPIC_API_KEY in your environment")
        return None

    # Initialize vector database
    vector_db = SimpleVectorDB()
    vector_db.add_documents(TEST_DOCUMENTS)

    if verbose:
        print(f"\n✓ Vector database initialized with {len(TEST_DOCUMENTS)} documents")

    # Run tests
    results = []
    passed = 0
    failed = 0

    for i, test_case in enumerate(TEST_CASES, 1):
        if verbose:
            print(f"\n{'='*80}")
            print(f"Test Case {i}/{len(TEST_CASES)}: {test_case['description']}")
            print(f"{'='*80}")
            print(f"Question: {test_case['question']}")

        # Retrieve documents
        retrieved_docs = vector_db.search(test_case['question'], top_k=5)

        # Run CRAG pipeline
        response = crag.answer_legal_question(
            question=test_case['question'],
            retrieved_docs=retrieved_docs,
            verbose=verbose
        )

        # Evaluate results
        passed_test = True
        issues = []

        # Check confidence threshold
        if response.confidence < LegalCRAG.CONFIDENCE_THRESHOLD:
            passed_test = False
            issues.append(f"Low confidence: {response.confidence:.2f}")

        # Check if answer contains expected content
        answer_lower = response.answer.lower()
        for expected in test_case['expected_answer_contains']:
            if expected.lower() not in answer_lower:
                passed_test = False
                issues.append(f"Missing expected content: '{expected}'")

        # Check citations
        for expected_citation in test_case['expected_citations']:
            if expected_citation.lower() not in answer_lower:
                passed_test = False
                issues.append(f"Missing citation: '{expected_citation}'")

        # Check grounded
        if not response.grounded:
            passed_test = False
            issues.append("Answer not grounded in sources")

        # Check validation issues
        if response.validation_result.issues:
            for issue in response.validation_result.issues:
                issues.append(f"Validation issue: {issue}")

        # Record result
        test_result = {
            'test_id': test_case['id'],
            'question': test_case['question'],
            'answer': response.answer,
            'confidence': response.confidence,
            'grounded': response.grounded,
            'citation_accuracy': response.validation_result.citation_accuracy,
            'passed': passed_test,
            'issues': issues,
            'relevant_doc_count': len(response.relevant_docs),
            'grade_summary': {
                'relevant': sum(1 for g in response.grade_details if g.grade.value == 'RELEVANT'),
                'partial': sum(1 for g in response.grade_details if g.grade.value == 'PARTIAL'),
                'irrelevant': sum(1 for g in response.grade_details if g.grade.value == 'IRRELEVANT')
            }
        }
        results.append(test_result)

        # Update counters
        if passed_test:
            passed += 1
        else:
            failed += 1

        # Print result
        if verbose:
            print(f"\n{'─'*80}")
            print(f"ANSWER:")
            print(f"{'─'*80}")
            print(response.answer)
            print(f"\n{'─'*80}")
            print(f"EVALUATION:")
            print(f"{'─'*80}")
            print(f"Status: {'✓ PASS' if passed_test else '✗ FAIL'}")
            print(f"Confidence: {response.confidence:.2f}")
            print(f"Grounded: {response.grounded}")
            print(f"Citation Accuracy: {response.validation_result.citation_accuracy:.2f}")
            print(f"Relevant Docs: {len(response.relevant_docs)}")
            if issues:
                print(f"\nIssues:")
                for issue in issues:
                    print(f"  • {issue}")

    # Summary
    if verbose:
        print(f"\n{'='*80}")
        print("TEST SUMMARY")
        print(f"{'='*80}")
        print(f"Total Tests: {len(TEST_CASES)}")
        print(f"Passed: {passed} ({passed/len(TEST_CASES)*100:.1f}%)")
        print(f"Failed: {failed} ({failed/len(TEST_CASES)*100:.1f}%)")
        print(f"\nMetrics:")
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        avg_citation_accuracy = sum(r['citation_accuracy'] for r in results) / len(results)
        grounded_rate = sum(1 for r in results if r['grounded']) / len(results)
        print(f"  Average Confidence: {avg_confidence:.2f}")
        print(f"  Average Citation Accuracy: {avg_citation_accuracy:.2f}")
        print(f"  Grounded Rate: {grounded_rate*100:.1f}%")
        print(f"{'='*80}\n")

    return {
        'passed': passed,
        'failed': failed,
        'total': len(TEST_CASES),
        'pass_rate': passed / len(TEST_CASES),
        'avg_confidence': avg_confidence,
        'avg_citation_accuracy': avg_citation_accuracy,
        'grounded_rate': grounded_rate,
        'detailed_results': results
    }


def save_results(results: dict, filename: str = "crag_test_results.json"):
    """Save test results to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Results saved to {filename}")


if __name__ == "__main__":
    import sys

    # Parse command line arguments
    llm_provider = "openai"
    if len(sys.argv) > 1 and sys.argv[1] in ["openai", "anthropic"]:
        llm_provider = sys.argv[1]

    # Run tests
    results = run_tests(llm_provider=llm_provider, verbose=True)

    # Save results
    if results:
        save_results(results)

        # Exit with appropriate code
        if results['failed'] == 0:
            print("\n🎉 All tests passed!")
            sys.exit(0)
        else:
            print(f"\n⚠️  {results['failed']} test(s) failed")
            sys.exit(1)
    else:
        print("\n❌ Test suite failed to run")
        sys.exit(1)
