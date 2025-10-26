# Malta Legal RAG System 🇲🇹⚖️

An intelligent legal document search system powered by Retrieval-Augmented Generation (RAG) for Malta's legal code.

## Features

✨ **Comprehensive Legal Coverage**
- 44 legal documents indexed
- 19 unique Malta legal codes and acts
- 2,304+ searchable chunks
- 2,429 legal articles

🔍 **Intelligent Search**
- Semantic search using OpenAI embeddings
- Automatic query intent detection
- AI-generated overviews with citations
- Multi-document context awareness

📊 **Document Diversity**
- Civil Code (Cap. 16) - 554 chunks
- Code of Organization and Civil Procedure (Cap. 12) - 526 chunks
- Commercial Code (Cap. 13) - 273 chunks
- Income Tax Act (Cap. 123) - 136 chunks
- And 15 more legal documents!

🚀 **Production Ready**
- Streamlit Cloud compatible
- Automatic database building on first run
- Progress tracking with visual feedback
- Optimized for cloud deployment

## Technology Stack

- **Vector Database:** ChromaDB with cosine similarity
- **Embeddings:** OpenAI `text-embedding-3-large` (3072 dimensions)
- **Chunking:** 3,000 tokens with 200-token overlap
- **Frontend:** Streamlit
- **Search:** Semantic search with query analysis

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/malta-legal-rag.git
cd malta-legal-rag
```

2. **Install dependencies**
```bash
pip install -r Requirements.txt
```

3. **Set up OpenAI API key**

Create a file named `env` or `.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

4. **Run the application**
```bash
streamlit run main.py
```

The app will automatically:
- Process all 44 legal documents
- Build the vector database (first run only)
- Show progress bars for tracking
- Launch the search interface

## Deployment to Streamlit Cloud

See the comprehensive [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions.

**Quick summary:**
1. Push code to GitHub (including all `.txt` files in `ocr/output/`)
2. Deploy on Streamlit Cloud
3. Add `OPENAI_API_KEY` to Streamlit secrets
4. Wait for automatic database build (5-10 minutes)
5. Start searching! 🎉

## Project Structure

```
malta-legal-rag/
├── main.py                   # Streamlit app entry point
├── vector_store.py           # Vector database (ChromaDB)
├── doc_processor.py          # Document processing & chunking
├── search_engine.py          # Semantic search logic
├── ai_assistant.py           # AI overview generation
├── build_vector_db.py        # Manual database builder
├── test_all_sources.py       # Document diversity test
├── Requirements.txt          # Python dependencies
├── DEPLOYMENT_GUIDE.md       # Deployment instructions
└── ocr/output/               # 44 legal document text files
    ├── 13 - Commercial Code.txt
    ├── 16 - Civil Code.txt
    ├── 123 - Income Tax Act.txt
    └── ... (41 more documents)
```

## Key Files

### Source Documents (`ocr/output/`)
All 44 Malta legal document text files must be committed to the repository for the application to work.

### Generated Files (Not in Git)
- `chroma_db/` - Vector database (built automatically)
- `processed_chunks.json` - Processed legal chunks
- `processing_report.json` - Processing statistics

## How It Works

### 1. Document Processing
- Extracts articles from 44 legal text files
- Identifies document types (Cap. 12, 13, 16, etc.)
- Cleans OCR artifacts and normalizes text
- Validates article numbering

### 2. Intelligent Chunking
- Splits long articles into 3,000-token chunks
- Maintains 200-token overlap for context
- Preserves metadata (article number, page, document)
- Uses GPT-4 tokenizer for accuracy

### 3. Embedding Generation
- Generates 3,072-dimensional vectors per chunk
- Uses OpenAI `text-embedding-3-large` model
- Processes in batches for efficiency
- Supports up to 8,192 tokens per input

### 4. Vector Storage
- Stores in ChromaDB with cosine similarity
- Indexes by article number and document code
- Enables fast semantic search
- Persists to disk for reuse

### 5. Search & Retrieval
- Analyzes query intent (definition, procedure, penalty, etc.)
- Performs semantic similarity search
- Ranks and deduplicates results
- Generates AI-powered overviews with citations

## Document Coverage

The system includes these Malta legal codes:

| Chapter | Document | Articles | Chunks |
|---------|----------|----------|--------|
| Cap. 12 | Code of Organization and Civil Procedure | 526 | 526 |
| Cap. 13 | Commercial Code | 273 | 273 |
| Cap. 16 | Civil Code | 547 | 554 |
| Cap. 55 | Notarial Profession and Notarial Archives Act | 153 | 183 |
| Cap. 56 | Public Registry Act | 38 | 47 |
| Cap. 79 | Commissioners for Oaths Ordinance | 11 | 11 |
| Cap. 123 | Income Tax Act | 99 | 136 |
| Cap. 246 | AIP Act | 20 | 22 |
| Cap. 296 | Land Registration Act | 57 | 107 |
| Cap. 364 | Duty on Documents and Transfers Act | 70 | 104 |
| Cap. 372 | Income Tax Management Act | 63 | 63 |
| Cap. 373 | Prevention of Money Laundering Act | 47 | 72 |
| Cap. 398 | Condominium Act | 32 | 42 |
| Cap. 540 | Gender Identity Act | 18 | 18 |
| Cap. 604 | Private Residential Leases Act | 33 | 39 |
| Cap. 614 | Cohabitation Act | 31 | 31 |
| Cap. 615 | Real Estate Agents Act | 16 | 16 |
| S.L. 623.01 | EPC Regulations | 43 | 44 |
| EU 650/2012 | EU Succession Regulation | 16 | 16 |

## Testing

Verify document diversity:
```bash
python test_all_sources.py
```

Expected output:
- ✅ 19 unique documents
- ✅ 2,304 total chunks
- ✅ Commercial Code is only ~11-12% (good diversity!)

## Troubleshooting

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed troubleshooting.

**Common issues:**
- Missing OpenAI API key → Add to `.env` or Streamlit secrets
- "No documents found" → Ensure `ocr/output/` has all 44 `.txt` files
- Slow first load → Expected (building database takes 5-10 minutes)

## Performance

- **First Run:** 5-10 minutes (builds vector database)
- **Subsequent Runs:** <5 seconds (loads cached database)
- **Search Speed:** <1 second per query
- **Cost:** ~$0.50-$1.00 one-time build + ~$0.0001 per search

## License

This project is for legal research and educational purposes.

## Support

For issues or questions:
1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Review Streamlit logs
3. Verify OpenAI API key and quota

---

**Built with ❤️ for Malta's legal community**



