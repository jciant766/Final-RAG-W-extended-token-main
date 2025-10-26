import streamlit as st
import os
import json
from pathlib import Path
from vector_store import VectorStore
from search_engine import SearchEngine
from debug_logger import DebugLogger

# Page config
st.set_page_config(
    page_title="Malta Commercial Code Search",
    page_icon="⚖️",
    layout="centered"
)

# Initialize debug logger
debug = DebugLogger("main_app")

# Custom CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stTextInput > label {display: none;}
    
    .search-container {
        margin: 2rem 0;
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .article-ref {
        font-weight: bold;
        color: #1f77b4;
        font-size: 1.1rem;
    }
    
    .relevance {
        background: #e3f2fd;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.9rem;
        color: #1565c0;
    }
    
    .doc-badge {
        background: #fff3e0;
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        font-size: 0.85rem;
        color: #ef6c00;
        margin-left: 0.5rem;
        white-space: nowrap;
    }
    
    .debug-panel {
        background: #f5f5f5;
        padding: 1rem;
        border-radius: 5px;
        font-family: monospace;
        font-size: 0.85rem;
    }

    /* Ensure long legal texts wrap within expanders without horizontal scroll */
    .full-article {
        white-space: pre-wrap;
        word-wrap: break-word;
        overflow-x: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Initialize system
@st.cache_resource
def init_system():
    """Initialize search system with progress tracking"""
    debug.log("info", "Initializing system")

    # Check if vector database needs to be built
    if not os.path.exists("chroma_db") or not os.path.exists("processed_chunks.json"):
        st.warning("🔧 Vector database not found. Building from documents...")

        # Check for OPENAI_API_KEY before processing
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            try:
                api_key = st.secrets.get("OPENAI_API_KEY")
            except:
                pass

        if not api_key:
            st.error("❌ OPENAI_API_KEY not found!")
            st.info("""
            **For Streamlit Cloud deployment:**
            1. Go to your app settings
            2. Click on "Secrets"
            3. Add: `OPENAI_API_KEY = "your-api-key-here"`

            **For local development:**
            1. Create a file named `.env` or `env` in the project root
            2. Add: `OPENAI_API_KEY=your-api-key-here`
            """)
            st.stop()

        # Import here to avoid circular imports
        from doc_processor import DocumentProcessor

        processor = DocumentProcessor()
        ocr_output_dir = Path("ocr/output")

        if not ocr_output_dir.exists():
            st.error(f"❌ Source documents directory not found: {ocr_output_dir}")
            st.error("Please ensure the 'ocr/output' directory with legal text files is present in the repository.")
            st.stop()

        if ocr_output_dir.exists():
            text_files = sorted(ocr_output_dir.glob("*.txt"))
            total_files = len(text_files)

            st.info(f"📄 Found {total_files} legal document files to process")

            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            all_chunks = []
            documents_processed = []

            # Process each document
            for idx, text_file in enumerate(text_files, 1):
                try:
                    progress = idx / total_files
                    progress_bar.progress(progress)
                    status_text.text(f"Processing [{idx}/{total_files}]: {text_file.name}")

                    result = processor.process_document(str(text_file))

                    with open('processed_chunks.json', 'r', encoding='utf-8') as f:
                        chunks = json.load(f)

                    all_chunks.extend(chunks)
                    documents_processed.append({
                        'file': text_file.name,
                        'articles': result['total_articles'],
                        'chunks': result['total_chunks'],
                        'document': result['document']
                    })
                except Exception as e:
                    st.error(f"Error processing {text_file.name}: {e}")

            # Remove duplicates
            unique_chunks = {}
            for chunk in all_chunks:
                chunk_id = chunk['id']
                if chunk_id not in unique_chunks:
                    unique_chunks[chunk_id] = chunk

            all_chunks = list(unique_chunks.values())

            # Save all chunks
            with open('processed_chunks.json', 'w', encoding='utf-8') as f:
                json.dump(all_chunks, f, ensure_ascii=False, indent=2)

            # Save report
            total_articles = sum(doc['articles'] for doc in documents_processed)
            report = {
                "total_documents": len(documents_processed),
                "total_articles": total_articles,
                "total_chunks": len(all_chunks),
                "documents": documents_processed
            }

            with open('processing_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            progress_bar.progress(1.0)
            status_text.text("✅ Document processing complete!")

            st.success(f"✅ Processed {len(documents_processed)} documents with {total_articles} articles into {len(all_chunks)} chunks")

            # Now build embeddings
            st.info("🧠 Building vector database with embeddings...")
            embedding_progress = st.progress(0)
            embedding_status = st.empty()

            # This will trigger vector store initialization with embeddings
            def embedding_callback(batch_num, total_batches, chunks_done, total_chunks):
                progress = chunks_done / total_chunks
                embedding_progress.progress(progress)
                embedding_status.text(f"Generating embeddings: Batch {batch_num}/{total_batches} ({chunks_done}/{total_chunks} chunks)")

            # Initialize vector store (will load documents and create embeddings)
            vector_store = VectorStore()

            embedding_progress.progress(1.0)
            embedding_status.text("✅ Vector database ready!")

            st.success("🚀 System initialization complete!")
        else:
            st.error(f"❌ OCR output directory not found: {ocr_output_dir}")
            st.stop()
    else:
        # Vector database exists, just load it
        with st.spinner("Loading vector database..."):
            vector_store = VectorStore()

    search_engine = SearchEngine(vector_store, enable_ai_overview=True)

    debug.log("info", "System initialized successfully")
    return search_engine

# Header
st.title("⚖️ Malta Commercial Code Search")
st.markdown("*Smart legal search with automatic query understanding*")

# Debug mode toggle (hidden)
if st.session_state.get('debug_clicks', 0) >= 3:
    debug_mode = st.checkbox("🔧 Debug Mode", key="debug_mode")
else:
    debug_mode = False

# Click counter for debug mode
col1, col2, col3 = st.columns([1, 8, 1])
with col3:
    if st.button("⚙️", key="settings"):
        st.session_state['debug_clicks'] = st.session_state.get('debug_clicks', 0) + 1

# Initialize system
search_engine = init_system()

# Search interface
with st.container():
    query = st.text_input(
        "search",
        placeholder="Search articles or ask questions...",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        search_button = st.button("Search", type="primary", use_container_width=True)

# Search handling
if query and search_button:
    debug.log("query", query)
    
    with st.spinner("Searching..."):
        search_payload = search_engine.search(query)
    
    # Results display
    results = []
    ai_overview = None
    query_analysis = {}
    if isinstance(search_payload, dict):
        results = search_payload.get('results', []) or []
        ai_overview = search_payload.get('ai_overview')
        query_analysis = search_payload.get('query_analysis') or {}
    else:
        results = search_payload or []
    
    if results:
        st.markdown("---")
        st.markdown(f"**Found {len(results)} relevant results:**")

        # Detected intent
        if isinstance(query_analysis, dict):
            intent = query_analysis.get('intent')
            intent_map = {
                'definition': 'Definition',
                'procedural': 'Procedure',
                'penalty': 'Penalty / Offence',
                'requirement': 'Requirement / Obligation',
                'temporal': 'Timing / Deadline'
            }
            intent_text = intent_map.get(intent, 'General information')
            st.caption(f"Detected intent: {intent_text}")
        
        # Optional AI overview
        if ai_overview and isinstance(ai_overview, dict) and ai_overview.get('overview'):
            st.markdown("#### AI Overview")
            # Main overview text
            st.write(ai_overview['overview'])
            
            # Confidence badge (optional)
            conf = ai_overview.get('confidence')
            if isinstance(conf, (int, float)):
                st.caption(f"Confidence: {conf:.0%}")
            
            # Sources list
            citations = ai_overview.get('citations') or []
            if citations:
                st.markdown("**Sources**")
                for c in citations:
                    doc = c.get('document', '')
                    cit = c.get('citation', '')
                    page = c.get('page')
                    # Always show page number if it's a valid positive integer
                    page_str = ""
                    if page is not None:
                        try:
                            page_num = int(page)
                            if page_num >= 1:
                                page_str = f" (Page {page_num})"
                        except (ValueError, TypeError):
                            pass
                    st.markdown(f"- {doc} — {cit}{page_str}")
        
        for i, result in enumerate(results):
            # Result card
            st.markdown(f"""
            <div class="result-card">
                <div class="result-header">
                    <div>
                        <span class="article-ref">{result['citation'].split(',')[0]}</span>
                        <span class="doc-badge">{result.get('metadata', {}).get('document', '')}</span>
                    </div>
                    <span class="relevance">{result['score']:.0%} match</span>
                </div>
                <div>{result['content'][:400]}...</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Expandable full content - always show expander
            with st.expander(f"Read full article - {result['citation'].split(',')[0]}"):
                st.markdown(f"<div class='full-article'>{result['content']}</div>", unsafe_allow_html=True)
                
                # Debug info
                if debug_mode:
                    st.json({
                        'article': result['metadata']['article'],
                        'tokens': result['metadata'].get('tokens', 'N/A'),
                        'chunk': f"{result['metadata'].get('chunk_index', 0) + 1}/{result['metadata'].get('total_chunks', 1)}",
                        'page': result['metadata']['page']
                    })
    else:
        st.info("No results found. Try different keywords or check the debug log.")

# Debug panel
if debug_mode:
    st.markdown("---")
    st.markdown("### 🔍 Debug Information")
    
    tabs = st.tabs(["Recent Logs", "Query Analysis", "System Stats"])
    
    with tabs[0]:
        # Recent logs
        logs = DebugLogger.get_recent_logs(n=20)
        for log in logs:
            level_color = {
                'error': '#d32f2f',
                'info': '#1976d2',
                'debug': '#388e3c',
                'query': '#f57c00'
            }.get(log['level'], '#666')
            
            st.markdown(f"""
            <div class="debug-panel">
                <span style="color: {level_color};">[{log['level'].upper()}]</span>
                <span>{log['timestamp']}</span>
                <span>{log['module']}</span>: {log['message']}
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[1]:
        # Query analysis
        analysis = DebugLogger.analyze_queries()
        st.json(analysis)
    
    with tabs[2]:
        # System stats
        if os.path.exists('processing_report.json'):
            with open('processing_report.json', 'r') as f:
                stats = json.load(f)
            st.json(stats)

# Help section
with st.expander("📚 Search Tips"):
    st.markdown("""
    **Query Examples:**
    
    **General Commercial Law:**
    - `What is a trader?` - Definitions
    - `trade books requirements` - Accounting obligations
    - `acts of trade` - Commercial activities
    
    **Commercial Agents & Brokers:**
    - `commercial agent duties` - Agency relationships
    - `broker requirements` - Brokerage regulations
    - `agent commissions` - Payment structures
    
    **Bills of Exchange:**
    - `bills of exchange requirements` - Commercial instruments
    - `endorsement procedures` - Transfer mechanisms
    - `acceptance of bills` - Payment obligations
    
    **Maritime Trade:**
    - `maritime insurance` - Marine coverage
    - `bills of lading` - Shipping documents
    - `general average` - Maritime law concepts
    
    **Bankruptcy:**
    - `Article 477` - Bankruptcy declaration
    - `bankruptcy trustee duties` - Insolvency procedures
    - `debt agreements` - Restructuring options
    
    **Late Payments:**
    - `late payment penalties` - Commercial transactions
    - `interest rates` - Financial obligations
    
    **System Features:**
    - Automatic query type detection
    - Smart chunking for long articles
    - Token-aware processing
    - Debug mode for troubleshooting
    """)
