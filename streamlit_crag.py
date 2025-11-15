"""
Streamlit Interface for Legal CRAG System
==========================================
Interactive demo of Corrective RAG for Malta Law
"""

import streamlit as st
import os
from legal_crag import LegalCRAG, VoyageVectorDB
import json

# Set page config
st.set_page_config(
    page_title="Malta Legal CRAG System",
    page_icon="⚖️",
    layout="wide"
)

# Set API keys
os.environ['VOYAGE_API_KEY'] = 'pa-1fb-bYoXcy9MYbKYkXhqSKGwJrcRX40hVVTLoa5FFA8'
os.environ['OPENROUTER_API_KEY'] = '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'

# Verified test documents from Malta legislation
TEST_DOCUMENTS = [
    {
        'id': 'doc_1',
        'content': """320. Ownership is the right of enjoying and disposing of things in the most absolute manner, provided no use thereof is made which is prohibited by law.
321. No person can be compelled to give up his property or to permit any other person to make use of it, except for a public purpose, and upon payment of a fair compensation.
322. (1) Save as otherwise provided by law, the owner of a thing has the right to recover it from any possessor.""",
        'metadata': {
            'citation': 'Civil Code Cap. 16, Article 320-322',
            'article': '320',
            'doc_code': 'cap_16',
            'jurisdiction': 'Malta'
        }
    },
    {
        'id': 'doc_2',
        'content': """56. (1) Saving the other provisions of this article, the tax upon the chargeable income of every person shall be determined as follows:

- (13) (a) The tax upon the chargeable income of any person referred to as a Contractor in article 23 shall be levied at the rate of 35 cents (€0.35) on every euro of the chargeable income in so far as such income is to be computed in accordance with the provisions of the said article 23(1) and (2). Other income arising to a Contractor shall be charged at the appropriate rate or rates.""",
        'metadata': {
            'citation': 'Income Tax Act Cap. 123, Article 56',
            'article': '56',
            'doc_code': 'cap_123',
            'jurisdiction': 'Malta'
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
            'jurisdiction': 'Malta'
        }
    },
    {
        'id': 'doc_4',
        'content': """45. Every merchant shall be obliged to keep orderly accounting books in which a record of all his commercial transactions, his active and passive assets and liabilities shall be entered.

The books referred to in this article must be kept for ten years from the date of the last entry therein.

The books of merchants duly kept in accordance with the provisions of this article shall constitute evidence in commercial matters.""",
        'metadata': {
            'citation': 'Commercial Code Cap. 13, Article 45',
            'article': '45',
            'doc_code': 'cap_13',
            'jurisdiction': 'Malta'
        }
    }
]


@st.cache_resource
def initialize_system():
    """Initialize CRAG system and vector database."""
    try:
        crag = LegalCRAG(
            llm_provider="openrouter",
            openrouter_api_key=os.getenv('OPENROUTER_API_KEY')
        )

        vector_db = VoyageVectorDB(voyage_api_key=os.getenv('VOYAGE_API_KEY'))
        vector_db.add_documents(TEST_DOCUMENTS)

        return crag, vector_db, None
    except Exception as e:
        return None, None, str(e)


def main():
    # Header
    st.title("⚖️ Malta Legal CRAG System")
    st.markdown("**Corrective RAG with Voyage Law Embeddings + OpenRouter LLM**")
    st.markdown("---")

    # Initialize system
    with st.spinner("Initializing CRAG system..."):
        crag, vector_db, error = initialize_system()

    if error:
        st.error(f"❌ Failed to initialize: {error}")
        st.info("Make sure API keys are configured correctly.")
        return

    st.success("✅ System initialized with Voyage Law embeddings and OpenRouter LLM")

    # Sidebar - System Info
    with st.sidebar:
        st.header("📊 System Configuration")
        st.markdown(f"""
        **Embeddings**: Voyage Law 2
        **LLM**: OpenRouter (Claude 3.5 Sonnet)
        **Documents**: {len(TEST_DOCUMENTS)} verified Malta laws
        **Confidence Threshold**: {crag.CONFIDENCE_THRESHOLD}
        """)

        st.markdown("---")
        st.header("📚 Available Documents")
        for doc in TEST_DOCUMENTS:
            with st.expander(doc['metadata']['citation']):
                st.code(doc['content'][:200] + "...", language="text")

        st.markdown("---")
        st.header("ℹ️ About CRAG")
        st.markdown("""
        **Corrective RAG** improves traditional RAG by:

        1. **Grading**: Filter irrelevant docs BEFORE generation
        2. **Validation**: Verify answer against sources AFTER generation
        3. **Citations**: Enforce exact article references
        4. **Confidence**: Block low-confidence answers

        This prevents hallucinations!
        """)

    # Main area - Question input
    st.header("💬 Ask a Legal Question")

    # Example questions
    example_questions = [
        "What is the definition of ownership in Malta?",
        "What is the tax rate for contractors in Malta?",
        "When does property transfer in a sale contract?",
        "How long must merchants keep accounting books?",
    ]

    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_input(
            "Your question about Malta law:",
            placeholder="e.g., What is the definition of ownership according to Malta law?"
        )
    with col2:
        selected_example = st.selectbox("Or try an example:", [""] + example_questions)

    if selected_example:
        question = selected_example

    # Process question
    if st.button("🔍 Search & Analyze", type="primary", use_container_width=True):
        if not question:
            st.warning("Please enter a question")
            return

        with st.spinner("Running CRAG pipeline..."):
            # Retrieve documents
            retrieved_docs = vector_db.search(question, top_k=4)

            # Run CRAG pipeline
            response = crag.answer_legal_question(
                question=question,
                retrieved_docs=retrieved_docs,
                verbose=False
            )

        # Display results in tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Answer",
            "🔬 Pipeline Stages",
            "✅ Validation",
            "📊 Metrics"
        ])

        with tab1:
            st.header("Final Answer")

            # Confidence badge
            conf_color = "green" if response.confidence >= crag.CONFIDENCE_THRESHOLD else "red"
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 5px; background-color: {'#d4edda' if conf_color == 'green' else '#f8d7da'}; border: 1px solid {'#c3e6cb' if conf_color == 'green' else '#f5c6cb'};">
                <strong>Confidence:</strong> {response.confidence:.2%}
                {'✅ ACCEPTED' if response.confidence >= crag.CONFIDENCE_THRESHOLD else '⚠️ LOW CONFIDENCE'}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(f"**Q:** {question}")
            st.markdown(f"**A:** {response.answer}")

            if response.confidence < crag.CONFIDENCE_THRESHOLD:
                st.warning(f"⚠️ This answer has low confidence ({response.confidence:.2%}). Use with caution.")

        with tab2:
            st.header("CRAG Pipeline Stages")

            # Stage 1: Retrieval
            st.subheader("1️⃣ Document Retrieval")
            st.info(f"Retrieved {len(retrieved_docs)} documents using Voyage Law embeddings")

            for i, doc in enumerate(retrieved_docs, 1):
                with st.expander(f"Doc {i}: {doc['metadata']['citation']} (Score: {doc.get('score', 0):.3f})"):
                    st.code(doc['content'][:300] + "...", language="text")

            # Stage 2: Grading
            st.subheader("2️⃣ Document Grading")

            grade_counts = {
                'RELEVANT': sum(1 for g in response.grade_details if g.grade.value == 'RELEVANT'),
                'PARTIAL': sum(1 for g in response.grade_details if g.grade.value == 'PARTIAL'),
                'IRRELEVANT': sum(1 for g in response.grade_details if g.grade.value == 'IRRELEVANT')
            }

            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Relevant", grade_counts['RELEVANT'])
            col2.metric("~ Partial", grade_counts['PARTIAL'])
            col3.metric("❌ Irrelevant", grade_counts['IRRELEVANT'])

            for grade in response.grade_details:
                emoji = "✅" if grade.grade.value == "RELEVANT" else "~" if grade.grade.value == "PARTIAL" else "❌"
                with st.expander(f"{emoji} {grade.document_id}: {grade.grade.value}"):
                    st.write(f"**Reasoning:** {grade.reasoning}")
                    st.write(f"**Confidence:** {grade.confidence:.2%}")

            # Stage 3: Generation
            st.subheader("3️⃣ Answer Generation")
            st.success(f"Generated answer using {len(response.relevant_docs)} relevant documents")
            st.code(response.answer, language="text")

            # Stage 4: Validation
            st.subheader("4️⃣ Answer Validation")
            st.info("Validated answer against source documents")

        with tab3:
            st.header("Validation Results")

            # Grounded status
            if response.validation_result.grounded:
                st.success("✅ Answer is GROUNDED in source documents")
            else:
                st.error("❌ Answer is NOT GROUNDED")

            # Citation accuracy
            st.metric(
                "Citation Accuracy",
                f"{response.validation_result.citation_accuracy:.1%}",
                help="Percentage of citations that exist in source documents"
            )

            # Issues
            if response.validation_result.issues:
                st.warning("⚠️ Validation Issues Found:")
                for issue in response.validation_result.issues:
                    st.markdown(f"- {issue}")
            else:
                st.success("✅ No validation issues found")

            # Source documents used
            st.subheader("Source Documents Used")
            for doc in response.relevant_docs:
                st.info(f"📄 {doc['metadata']['citation']}")

        with tab4:
            st.header("Performance Metrics")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Overall Confidence", f"{response.confidence:.2%}")
                st.metric("Citation Accuracy", f"{response.validation_result.citation_accuracy:.2%}")
                st.metric("Grounded Status", "✅ Yes" if response.grounded else "❌ No")

            with col2:
                st.metric("Relevant Documents", len(response.relevant_docs))
                st.metric("Total Retrieved", len(retrieved_docs))
                st.metric("Filtering Rate", f"{(1 - len(response.relevant_docs)/len(retrieved_docs))*100:.1f}%")

            # JSON export
            st.subheader("Export Results")
            if st.button("📥 Download JSON"):
                result_json = response.to_dict()
                st.download_button(
                    "Download",
                    data=json.dumps(result_json, indent=2),
                    file_name="crag_result.json",
                    mime="application/json"
                )


if __name__ == "__main__":
    main()
