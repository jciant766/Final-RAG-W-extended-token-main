"""
Streamlit Interface for Legal CRAG System
==========================================
With USER-VERIFIED exact quotes from legislation.mt
"""

import streamlit as st
import os
from legal_crag import LegalCRAG, VoyageVectorDB
import json

st.set_page_config(
    page_title="Malta Legal CRAG System",
    page_icon="⚖️",
    layout="wide"
)

# Set API keys
os.environ['VOYAGE_API_KEY'] = 'pa-1fb-bYoXcy9MYbKYkXhqSKGwJrcRX40hVVTLoa5FFA8'
os.environ['OPENROUTER_API_KEY'] = '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'

# USER-VERIFIED documents from legislation.mt
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
            'verified_source': 'legislation.mt - User verified'
        }
    },
    {
        'id': 'doc_2',
        'content': """(13) (a) The tax upon the chargeable income of any person referred to as a Contractor in article 23 shall be levied at the rate of 35 cents (€0.35) on every euro of the chargeable income in so far as such income is to be computed in accordance with the provisions of the said article 23(1) and (2). Other income arising to a Contractor shall be charged at the appropriate rate or rates.

(b) The rate at which tax shall be withheld by a Contractor from payments made to a sub-contractor in accordance with the provisions of article 23(5) shall be at 10 cents (€0.10) of every euro of the payments made as aforesaid.""",
        'metadata': {
            'citation': 'Income Tax Act Cap. 123, Article 56(13)',
            'article': '56',
            'verified_source': 'legislation.mt - User verified'
        }
    },
    {
        'id': 'doc_3',
        'content': """1346. A sale is a contract whereby one of the contracting parties binds himself to transfer to the other a thing for a price which the latter binds himself to pay to the former.

1347. A sale is complete between the parties, and, as regards the seller, the property of the thing is transferred to the buyer, as soon as the thing and the price have been agreed upon, although the thing has not yet been delivered nor the price paid; and from that moment the thing itself remains at the risk and for the benefit of the buyer.""",
        'metadata': {
            'citation': 'Civil Code Cap. 16, Article 1346-1347',
            'article': '1346',
            'verified_source': 'legislation.mt - User verified'
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
    st.markdown("**Corrective RAG with Voyage Law + OpenRouter**")
    st.markdown("*Using verified exact quotes from legislation.mt*")
    st.markdown("---")

    # Initialize
    with st.spinner("Initializing CRAG system..."):
        crag, vector_db, error = initialize_system()

    if error:
        st.error(f"❌ Failed to initialize: {error}")
        return

    st.success("✅ System initialized with user-verified Malta legislation quotes")

    # Sidebar
    with st.sidebar:
        st.header("📊 System Info")
        st.markdown(f"""
        **Embeddings**: Voyage Law 2
        **LLM**: OpenRouter (Claude 3.5 Sonnet)
        **Documents**: {len(TEST_DOCUMENTS)} verified quotes
        **Source**: legislation.mt
        **Confidence Threshold**: {crag.CONFIDENCE_THRESHOLD}
        """)

        st.markdown("---")
        st.header("📚 Verified Documents")
        for doc in TEST_DOCUMENTS:
            with st.expander(doc['metadata']['citation']):
                st.code(doc['content'][:300] + "...", language="text")
                st.caption(f"✓ {doc['metadata']['verified_source']}")

        st.markdown("---")
        st.header("ℹ️ CRAG vs Traditional RAG")
        st.markdown("""
        **CRAG adds:**
        1. 🔍 **Grading** - Filters bad docs
        2. ✅ **Validation** - Checks accuracy
        3. 📝 **Citations** - Verifies sources
        4. 🎯 **Confidence** - Blocks hallucinations
        """)

    # Main area
    st.header("💬 Ask a Legal Question")

    example_questions = [
        "What is the definition of ownership in Malta?",
        "What is the tax rate for contractors in Malta?",
        "When does property transfer in a sale contract?",
    ]

    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_input(
            "Your question about Malta law:",
            placeholder="e.g., What is ownership according to Malta law?"
        )
    with col2:
        selected_example = st.selectbox("Or try an example:", [""] + example_questions)

    if selected_example:
        question = selected_example

    if st.button("🔍 Search & Analyze", type="primary", use_container_width=True):
        if not question:
            st.warning("Please enter a question")
            return

        with st.spinner("Running CRAG pipeline..."):
            retrieved_docs = vector_db.search(question, top_k=3)
            response = crag.answer_legal_question(
                question=question,
                retrieved_docs=retrieved_docs,
                verbose=False
            )

        # Display results
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Answer",
            "🔬 Pipeline Stages",
            "✅ Validation",
            "📊 Metrics"
        ])

        with tab1:
            st.header("Final Answer")

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
                st.warning(f"⚠️ Low confidence ({response.confidence:.2%}). Use with caution.")

        with tab2:
            st.header("CRAG Pipeline Stages")

            st.subheader("1️⃣ Document Retrieval")
            st.info(f"Retrieved {len(retrieved_docs)} documents using Voyage Law embeddings")

            for i, doc in enumerate(retrieved_docs, 1):
                with st.expander(f"Doc {i}: {doc['metadata']['citation']} (Score: {doc.get('score', 0):.3f})"):
                    st.code(doc['content'][:300] + "...", language="text")

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

            st.subheader("3️⃣ Answer Generation")
            st.success(f"Generated answer using {len(response.relevant_docs)} relevant documents")
            st.code(response.answer, language="text")

            st.subheader("4️⃣ Answer Validation")
            st.info("Validated answer against source documents")

        with tab3:
            st.header("Validation Results")

            if response.validation_result.grounded:
                st.success("✅ Answer is GROUNDED in source documents")
            else:
                st.error("❌ Answer is NOT GROUNDED")

            st.metric(
                "Citation Accuracy",
                f"{response.validation_result.citation_accuracy:.1%}",
                help="Percentage of citations verified in sources"
            )

            if response.validation_result.issues:
                st.warning("⚠️ Validation Issues:")
                for issue in response.validation_result.issues:
                    st.markdown(f"- {issue}")
            else:
                st.success("✅ No validation issues")

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

            st.subheader("Export Results")
            result_json = response.to_dict()
            st.download_button(
                "📥 Download JSON",
                data=json.dumps(result_json, indent=2),
                file_name="crag_result.json",
                mime="application/json"
            )


if __name__ == "__main__":
    main()
