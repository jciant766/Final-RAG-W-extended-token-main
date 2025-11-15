"""
Example Usage of Legal CRAG System
===================================

This script demonstrates how to use the Legal CRAG system for Malta law questions.
It shows integration with both the simple in-memory vector DB and the existing
ChromaDB-based VectorStore.
"""

import os
from legal_crag import LegalCRAG, SimpleVectorDB, CRAGResponse


def example_1_simple_usage():
    """Example 1: Basic usage with simple vector database"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic CRAG Usage with Simple Vector DB")
    print("="*80)

    # Initialize CRAG system
    crag = LegalCRAG(llm_provider="openai")

    # Create sample documents
    documents = [
        {
            'id': 'doc_1',
            'content': """Article 965 of the Civil Code (Cap. 16) states that ownership
            is the right to enjoy and dispose of things in the most absolute manner,
            provided they are not used in a way prohibited by laws or regulations.""",
            'metadata': {
                'citation': 'Civil Code Cap. 16, Article 965',
                'article': '965',
                'doc_code': 'cap_16'
            }
        },
        {
            'id': 'doc_2',
            'content': """The Income Tax Act (Cap. 123) Article 56 establishes that
            companies registered in Malta are subject to a standard corporate tax rate
            of thirty-five per cent (35%).""",
            'metadata': {
                'citation': 'Income Tax Act Cap. 123, Article 56',
                'article': '56',
                'doc_code': 'cap_123'
            }
        }
    ]

    # Initialize vector DB and add documents
    vector_db = SimpleVectorDB()
    vector_db.add_documents(documents)
    print("✓ Vector database initialized with 2 documents")

    # Ask a question
    question = "What is the corporate tax rate in Malta?"
    print(f"\nQuestion: {question}")

    # Retrieve relevant documents
    retrieved_docs = vector_db.search(question, top_k=5)
    print(f"✓ Retrieved {len(retrieved_docs)} documents")

    # Run CRAG pipeline
    response = crag.answer_legal_question(
        question=question,
        retrieved_docs=retrieved_docs,
        verbose=True
    )

    # Display results
    print("\n" + "─"*80)
    print("FINAL ANSWER:")
    print("─"*80)
    print(response.answer)
    print(f"\nConfidence: {response.confidence:.2f}")
    print(f"Grounded: {response.grounded}")
    print(f"Citation Accuracy: {response.validation_result.citation_accuracy:.2f}")


def example_2_with_existing_vectorstore():
    """Example 2: Integration with existing ChromaDB VectorStore"""
    print("\n\n" + "="*80)
    print("EXAMPLE 2: Integration with Existing VectorStore")
    print("="*80)

    # Check if ChromaDB exists
    if not os.path.exists("./chroma_db"):
        print("\n⚠️  ChromaDB not found. Run this after building the vector database.")
        print("   See README.md for setup instructions.")
        return

    # Import existing VectorStore
    try:
        from vector_store import VectorStore
    except ImportError:
        print("\n⚠️  VectorStore module not found.")
        return

    # Initialize
    crag = LegalCRAG(llm_provider="openai")
    vector_store = VectorStore()
    print("✓ Loaded existing Malta legal document database")

    # Ask a question
    question = "What are the requirements for customer due diligence under Malta's money laundering laws?"
    print(f"\nQuestion: {question}")

    # Retrieve documents using existing search
    retrieved_docs = vector_store.search(question, n_results=10)
    print(f"✓ Retrieved {len(retrieved_docs)} documents from ChromaDB")

    # Run CRAG pipeline
    response = crag.answer_legal_question(
        question=question,
        retrieved_docs=retrieved_docs,
        verbose=True
    )

    # Display results
    print("\n" + "─"*80)
    print("FINAL ANSWER:")
    print("─"*80)
    print(response.answer)
    print(f"\nMetrics:")
    print(f"  Confidence: {response.confidence:.2f}")
    print(f"  Grounded: {response.grounded}")
    print(f"  Citation Accuracy: {response.validation_result.citation_accuracy:.2f}")
    print(f"  Relevant Docs Used: {len(response.relevant_docs)}")


def example_3_batch_questions():
    """Example 3: Processing multiple questions"""
    print("\n\n" + "="*80)
    print("EXAMPLE 3: Batch Processing Multiple Questions")
    print("="*80)

    # Initialize
    crag = LegalCRAG(llm_provider="openai")
    vector_db = SimpleVectorDB()

    # Add comprehensive documents
    documents = [
        {
            'id': 'doc_1',
            'content': """Article 965 of the Civil Code (Cap. 16) defines ownership as
            the right to enjoy and dispose of things in the most absolute manner, provided
            they are not used in a way prohibited by laws or regulations.""",
            'metadata': {
                'citation': 'Civil Code Cap. 16, Article 965',
                'article': '965'
            }
        },
        {
            'id': 'doc_2',
            'content': """The Income Tax Act (Cap. 123) Article 56 establishes a corporate
            tax rate of thirty-five per cent (35%) for companies registered in Malta.""",
            'metadata': {
                'citation': 'Income Tax Act Cap. 123, Article 56',
                'article': '56'
            }
        },
        {
            'id': 'doc_3',
            'content': """Article 4 of the Gender Identity Act (Cap. 540) states that
            persons over eighteen (18) years may apply for gender recognition. Minors aged
            sixteen (16) to eighteen (18) require parental consent.""",
            'metadata': {
                'citation': 'Gender Identity Act Cap. 540, Article 4',
                'article': '4'
            }
        }
    ]

    vector_db.add_documents(documents)
    print(f"✓ Vector database initialized with {len(documents)} documents\n")

    # Multiple questions
    questions = [
        "What is the corporate tax rate in Malta?",
        "What is the minimum age for gender recognition?",
        "How is ownership defined in Malta law?"
    ]

    results = []

    for i, question in enumerate(questions, 1):
        print(f"\n{'─'*80}")
        print(f"Question {i}/{len(questions)}: {question}")
        print("─"*80)

        # Retrieve and process
        retrieved_docs = vector_db.search(question, top_k=3)
        response = crag.answer_legal_question(
            question=question,
            retrieved_docs=retrieved_docs,
            verbose=False  # Quiet mode for batch
        )

        # Store result
        results.append({
            'question': question,
            'answer': response.answer,
            'confidence': response.confidence,
            'passed': response.confidence >= LegalCRAG.CONFIDENCE_THRESHOLD
        })

        # Print summary
        status = "✓ PASS" if results[-1]['passed'] else "✗ FAIL"
        print(f"\nAnswer: {response.answer[:200]}...")
        print(f"\nStatus: {status} | Confidence: {response.confidence:.2f}")

    # Overall summary
    print(f"\n{'='*80}")
    print("BATCH SUMMARY")
    print("="*80)
    passed = sum(1 for r in results if r['passed'])
    print(f"Processed: {len(questions)} questions")
    print(f"Passed: {passed}/{len(questions)} ({passed/len(questions)*100:.1f}%)")
    avg_conf = sum(r['confidence'] for r in results) / len(results)
    print(f"Average Confidence: {avg_conf:.2f}")


def example_4_validation_demonstration():
    """Example 4: Demonstrating the validation system"""
    print("\n\n" + "="*80)
    print("EXAMPLE 4: Answer Validation Demonstration")
    print("="*80)

    # Initialize
    crag = LegalCRAG(llm_provider="openai")

    # Create a document with specific facts
    documents = [
        {
            'id': 'doc_1',
            'content': """Article 15 of the Prevention of Money Laundering Act (Cap. 373)
            requires customer due diligence for transactions of €15,000 or more.
            Penalties for non-compliance may include fines up to €200,000 and imprisonment.""",
            'metadata': {
                'citation': 'Prevention of Money Laundering Act Cap. 373, Article 15',
                'article': '15'
            }
        }
    ]

    vector_db = SimpleVectorDB()
    vector_db.add_documents(documents)

    # Ask about specific numbers
    question = "What is the fine for money laundering violations in Malta?"
    print(f"\nQuestion: {question}")

    retrieved_docs = vector_db.search(question, top_k=1)
    response = crag.answer_legal_question(
        question=question,
        retrieved_docs=retrieved_docs,
        verbose=True
    )

    # Show validation details
    print("\n" + "="*80)
    print("VALIDATION DETAILS")
    print("="*80)
    print(f"Answer: {response.answer}")
    print(f"\nValidation Results:")
    print(f"  • Grounded: {response.validation_result.grounded}")
    print(f"  • Confidence: {response.validation_result.confidence:.2f}")
    print(f"  • Citation Accuracy: {response.validation_result.citation_accuracy:.2f}")

    if response.validation_result.issues:
        print(f"\n  Issues Found:")
        for issue in response.validation_result.issues:
            print(f"    - {issue}")
    else:
        print(f"\n  ✓ No validation issues found")

    # Show document grades
    print(f"\nDocument Grades:")
    for grade in response.grade_details:
        print(f"  • {grade.document_id}: {grade.grade.value} (confidence: {grade.confidence:.2f})")


def example_5_anthropic_provider():
    """Example 5: Using Anthropic Claude instead of OpenAI"""
    print("\n\n" + "="*80)
    print("EXAMPLE 5: Using Anthropic Claude Provider")
    print("="*80)

    # Check if Anthropic API key is available
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  ANTHROPIC_API_KEY not found in environment.")
        print("   Set it to run this example with Claude.")
        return

    try:
        # Initialize with Anthropic
        crag = LegalCRAG(
            llm_provider="anthropic",
            model_name="claude-3-5-sonnet-20241022"
        )
        print("✓ Initialized CRAG with Anthropic Claude")

        # Simple test
        vector_db = SimpleVectorDB()
        documents = [
            {
                'id': 'doc_1',
                'content': """Article 56 of the Income Tax Act (Cap. 123) establishes
                that companies in Malta are subject to a thirty-five per cent (35%) tax rate.""",
                'metadata': {
                    'citation': 'Income Tax Act Cap. 123, Article 56',
                    'article': '56'
                }
            }
        ]
        vector_db.add_documents(documents)

        question = "What is the Malta corporate tax rate?"
        retrieved_docs = vector_db.search(question, top_k=1)

        response = crag.answer_legal_question(
            question=question,
            retrieved_docs=retrieved_docs,
            verbose=True
        )

        print("\n✓ Successfully used Claude for CRAG pipeline")
        print(f"Answer: {response.answer}")

    except Exception as e:
        print(f"\n❌ Error using Anthropic: {e}")


if __name__ == "__main__":
    import sys

    # Run examples
    try:
        # Example 1: Always runs (uses simple in-memory DB)
        example_1_simple_usage()

        # Example 2: Only if ChromaDB exists
        if os.path.exists("./chroma_db"):
            example_2_with_existing_vectorstore()

        # Example 3: Batch processing
        example_3_batch_questions()

        # Example 4: Validation demonstration
        example_4_validation_demonstration()

        # Example 5: Anthropic (if available)
        if os.getenv("ANTHROPIC_API_KEY"):
            example_5_anthropic_provider()

        print("\n\n" + "="*80)
        print("✓ All examples completed successfully!")
        print("="*80)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
