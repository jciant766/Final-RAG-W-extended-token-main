# User Guide - Malta Legal RAG System

## What Happens When You Launch Streamlit

### First Time Launch (No Vector Database):

When you run `streamlit run main.py` for the **first time**:

```
1. App starts loading...
2. Checks for vector database → NOT FOUND ❌
3. Automatic build begins:

   🔧 Vector database not found. Building from documents...

   📄 Found 44 legal document files to process

   Progress Bar: ████████░░░░░░░░ 50%
   Processing [23/44]: 372 - Income Tax Management Act.txt

   [Wait 2-3 minutes for document processing]

   🧠 Building vector database with embeddings...

   Progress Bar: ████████████░░░░ 75%
   Generating embeddings: Batch 15/23 (1500/2304 chunks)

   [Wait 3-5 minutes for embeddings]

   ✅ System initialization complete!

4. Search interface appears
```

**Total time:** ~5-10 minutes (one-time only)

**Files created:**
- `chroma_db/` - Vector database directory (~50-100 MB)
- `processed_chunks.json` - Processed article chunks (~5-10 MB)
- `processing_report.json` - Statistics file (~10 KB)

---

### Subsequent Launches (Database Exists):

When you run `streamlit run main.py` **after the first time**:

```
1. App starts loading...
2. Checks for vector database → FOUND ✅
3. Loads existing database from chroma_db/
4. Search interface appears immediately

Total time: <5 seconds
```

**No rebuilding needed!** The vector database persists between sessions.

---

## How to Query the Vector Database

### The Search Interface

Once Streamlit loads, you'll see this interface:

```
⚖️ Malta Commercial Code Search
Smart legal search with automatic query understanding

┌────────────────────────────────────────────┐
│ Search articles or ask questions...       │
└────────────────────────────────────────────┘

           [ Search ]
```

### Simple Search Examples

#### 1. **Search by Article Number**

```
Query: "Article 477"
Query: "Art. 123"
Query: "article 26A"
```

**What happens:**
- System detects article lookup
- Finds exact article match
- Returns the complete article text
- Shows which legal code it's from

**Example Result:**
```
Found 1 relevant result:

Commercial Code (Cap. 13) Art. 477     [98% match]
─────────────────────────────────────────────────
A trader may be declared bankrupt in the following cases:
1. When he has absconded;
2. When he has fraudulently concealed...
[Content continues...]

▼ Read full article - Commercial Code (Cap. 13) Art. 477
```

---

#### 2. **Semantic Search (Concept-Based)**

```
Query: "bankruptcy requirements"
Query: "property transfer tax"
Query: "notary obligations"
Query: "money laundering prevention"
```

**What happens:**
- System understands the **concept** you're looking for
- Searches all 19 legal codes for relevant articles
- Returns most relevant matches ranked by similarity
- May include results from multiple legal codes

**Example Result:**
```
Found 5 relevant results:

Commercial Code (Cap. 13) Art. 477     [92% match]
─────────────────────────────────────────────────
A trader may be declared bankrupt in...

Income Tax Management Act (Cap. 372) Art. 45     [87% match]
─────────────────────────────────────────────────
When a person is declared bankrupt...

Prevention of Money Laundering Act (Cap. 373) Art. 12     [85% match]
─────────────────────────────────────────────────
Financial institutions must report...
```

Notice: Results come from **different legal codes** ✅

---

#### 3. **Question-Based Search**

```
Query: "What is a trader?"
Query: "How to register a property?"
Query: "When must notaries keep records?"
Query: "What are the penalties for money laundering?"
```

**What happens:**
- System detects query intent (definition, procedure, penalty, etc.)
- Searches for articles that answer your question
- Generates AI overview with citations
- Shows source articles

**Example Result:**
```
Found 3 relevant results:

Detected intent: Definition

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI Overview

A trader is defined as any person who carries out acts of
trade as their habitual profession. This includes merchants,
retailers, and businesses engaged in commercial activities
for profit.

Sources:
- Commercial Code (Cap. 13) — Art. 3 (Page 1)
- Commercial Code (Cap. 13) — Art. 4 (Page 1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commercial Code (Cap. 13) Art. 3     [95% match]
─────────────────────────────────────────────────
Acts of trade are those specified in this Code...

Commercial Code (Cap. 13) Art. 4     [91% match]
─────────────────────────────────────────────────
A trader is any person who habitually carries out...
```

---

### Advanced Search Examples

#### Search Multiple Legal Codes

```
Query: "income tax on property sales"
```

**Returns results from:**
- Income Tax Act (Cap. 123)
- Duty on Documents and Transfers Act (Cap. 364)
- Land Registration Act (Cap. 296)

---

#### Search for Procedures

```
Query: "How to transfer property ownership?"
```

**System detects:** Procedural query
**Returns:** Step-by-step procedures from relevant acts

---

#### Search for Requirements

```
Query: "What documents are needed for marriage?"
```

**System detects:** Requirement query
**Returns:** Required documents from Civil Code

---

#### Search for Penalties

```
Query: "penalties for late tax payment"
```

**System detects:** Penalty query
**Returns:** Articles describing penalties and fines

---

### Search Tips

#### ✅ Good Queries:

- `"Article 477"` - Specific article lookup
- `"bankruptcy procedures"` - Concept search
- `"What is a notary?"` - Question format
- `"property transfer tax rates"` - Topic search
- `"money laundering reporting requirements"` - Specific topic

#### ❌ Queries That May Not Work Well:

- `"law"` - Too vague
- `"stuff about tax"` - Unclear
- `"help"` - Not a legal query
- Very long queries (>100 words) - Be concise

---

## Understanding the Results

### Result Card Anatomy

```
┌─────────────────────────────────────────────────────────────┐
│ Civil Code (Cap. 16) Art. 1156          [94% match]         │
│ ─────────────────────────────────────────────────────────   │
│                                                              │
│ Marriage shall be contracted by the declaration of the      │
│ spouses that they take each other as husband and wife.      │
│ This declaration shall be made before the competent         │
│ authority...                                                │
│                                                              │
│ ▼ Read full article - Civil Code (Cap. 16) Art. 1156       │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
1. **Document Badge** - Which legal code (e.g., "Civil Code (Cap. 16)")
2. **Article Number** - Specific article reference
3. **Match Percentage** - How relevant this is to your query
4. **Preview Text** - First 400 characters
5. **Expand Button** - Click to read full article

---

### Match Percentage Meaning

- **90-100%** - Excellent match, highly relevant
- **80-89%** - Good match, relevant
- **70-79%** - Fair match, may be relevant
- **60-69%** - Weak match, possibly relevant
- **<60%** - Not shown (filtered out)

---

## Using the AI Overview Feature

### What is AI Overview?

When you search, an AI analyzes the top results and generates a summary with citations.

### Example:

**Your Query:** `"What are the requirements for a valid will?"`

**AI Overview Generated:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI Overview                           Confidence: 95%

A valid will in Malta must meet the following requirements:

1. The testator must be of sound mind and at least 18 years old
2. The will must be in writing
3. It must be signed by the testator in the presence of witnesses
4. Two witnesses must sign in the presence of the testator

There are different types of wills (public, secret, holographic)
with specific requirements for each type.

Sources:
- Civil Code (Cap. 16) — Art. 667 (Page 156)
- Civil Code (Cap. 16) — Art. 668 (Page 156)
- Civil Code (Cap. 16) — Art. 675 (Page 158)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Benefits:**
- ✅ Quick summary of complex topics
- ✅ Cites specific articles and page numbers
- ✅ Saves time reading multiple articles
- ✅ Shows confidence level

---

## Debug Mode (Advanced)

### Enabling Debug Mode

1. Click the **⚙️** icon (top right) **3 times**
2. A "🔧 Debug Mode" checkbox appears
3. Check the box

### What Debug Mode Shows

**Additional tabs appear:**

#### Tab 1: Recent Logs
```
[INFO] 2024-01-15 14:23:45 - vector_store: Search query: bankruptcy
[DEBUG] 2024-01-15 14:23:45 - search_engine: Found 12 results
[INFO] 2024-01-15 14:23:46 - ai_assistant: Generated overview
```

#### Tab 2: Query Analysis
```json
{
  "query_type": "semantic",
  "intent": "definition",
  "keywords": ["bankruptcy", "trader"],
  "document_hints": ["commercial_code"]
}
```

#### Tab 3: System Stats
```json
{
  "total_documents": 44,
  "total_articles": 2429,
  "total_chunks": 2304,
  "documents": [...]
}
```

**Use debug mode to:**
- Understand how queries are interpreted
- See system performance
- Troubleshoot search issues

---

## Example Search Session

Let's walk through a complete search session:

### Step 1: Launch App
```bash
streamlit run main.py
```

### Step 2: First Time Setup (Automatic)
```
🔧 Vector database not found. Building from documents...
📄 Found 44 legal document files to process

[Progress bars appear]
Processing [44/44]: EU Succession Regulation - 650.2012.txt... OK

🧠 Building vector database with embeddings...
[Progress bars appear]

✅ System initialization complete!
```

### Step 3: Search Interface Appears
```
⚖️ Malta Commercial Code Search
Smart legal search with automatic query understanding

[Search box ready]
```

### Step 4: Enter Your Query
```
Search: "property transfer tax"
[Click Search button]
```

### Step 5: View Results
```
Found 8 relevant results:

Detected intent: Requirement / Obligation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI Overview                           Confidence: 92%

Property transfer tax in Malta is governed by the Duty on
Documents and Transfers Act. The tax is levied at 5% on
the higher of the contract price or market value...

Sources:
- Duty on Documents and Transfers Act (Cap. 364) — Art. 14
- Duty on Documents and Transfers Act (Cap. 364) — Art. 15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[8 article results displayed]

Duty on Documents and Transfers Act (Cap. 364) Art. 14 [96% match]
─────────────────────────────────────────────────────────────────
[Article content...]

▼ Read full article - Duty on Documents and Transfers Act Art. 14
```

### Step 6: Expand Articles
Click "▼ Read full article" to see complete text with metadata.

### Step 7: Try Another Search
The vector database is now loaded and ready for instant searches!

---

## Programmatic Access (Optional)

If you want to query the vector database **programmatically** (not through Streamlit UI):

### Python Script Example:

```python
from vector_store import VectorStore
from search_engine import SearchEngine

# Initialize
vector_store = VectorStore()
search_engine = SearchEngine(vector_store)

# Query
results = search_engine.search("bankruptcy requirements")

# Print results
for result in results['results']:
    print(f"\n{result['citation']}")
    print(f"Score: {result['score']:.2%}")
    print(result['content'][:200])
```

### Direct Vector Store Query:

```python
from vector_store import VectorStore

# Initialize
vs = VectorStore()

# Article lookup
article = vs.get_article("477")
print(article)

# Semantic search
results = vs.search("property tax", n_results=5)
for r in results:
    print(r['metadata']['citation'])
```

---

## Files and Their Purpose

After running Streamlit, you'll see these files:

### Source Files (Committed to Git):
```
ocr/output/
├── 13 - Commercial Code.txt          ← Your source documents
├── 16 - Civil Code.txt
├── 123 - Income Tax Act.txt
└── ... (41 more files)
```

### Generated Files (Not in Git):
```
chroma_db/                             ← Vector database
├── chroma.sqlite3                     (SQLite database)
├── index/                             (Vector indices)
└── ...

processed_chunks.json                  ← All processed chunks (5-10 MB)
processing_report.json                 ← Statistics
```

**Important:**
- ✅ Source files (`ocr/output/*.txt`) are committed to Git
- ❌ Generated files are NOT committed (built automatically)

---

## Troubleshooting Queries

### Problem: "No results found"

**Possible causes:**
1. Query is too vague ("law", "help")
2. Query is not legal-related
3. Topic not covered in the 19 legal codes

**Solutions:**
- Be more specific: "bankruptcy trader" instead of "bankruptcy"
- Use legal terminology
- Try different phrasings

---

### Problem: Results are not relevant

**Possible causes:**
1. Query ambiguity
2. Term has multiple meanings

**Solutions:**
- Add context: "commercial bankruptcy" instead of just "bankruptcy"
- Use article numbers if you know them
- Rephrase as a question: "What are bankruptcy requirements?"

---

### Problem: Slow search

**Possible causes:**
1. First query after launch (loading database)
2. AI Overview generation

**Solutions:**
- Wait a few seconds for first query
- Subsequent queries are instant

---

## Summary: How to Use Your RAG System

### 1️⃣ **Launch Streamlit**
```bash
streamlit run main.py
```

### 2️⃣ **Wait for Setup** (first time only)
- ~5-10 minutes for automatic database build
- Progress bars show status

### 3️⃣ **Start Searching**
- Type query in search box
- Click "Search" button
- View results with AI overview

### 4️⃣ **Query Types You Can Use**
- Article numbers: `"Article 477"`
- Concepts: `"bankruptcy procedures"`
- Questions: `"What is a trader?"`
- Topics: `"property transfer tax"`

### 5️⃣ **Understand Results**
- Match percentage = relevance
- Document badge = which legal code
- AI Overview = quick summary
- Expand for full article text

### 6️⃣ **Subsequent Uses**
- Database persists
- Launch is instant (<5 seconds)
- Search immediately

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                  SEARCH QUICK REFERENCE                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Article Lookup:   "Article 477"                        │
│                    "Art. 123"                            │
│                                                          │
│  Semantic Search:  "bankruptcy requirements"            │
│                    "property transfer tax"               │
│                                                          │
│  Questions:        "What is a trader?"                  │
│                    "How to register property?"           │
│                                                          │
│  Topics:           "money laundering prevention"        │
│                    "notary obligations"                  │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  TIP: Be specific and use legal terminology            │
│  TIP: Results from all 19 legal codes                  │
│  TIP: Click ▼ to expand full article text             │
└─────────────────────────────────────────────────────────┘
```

---

**You're ready to search Malta's legal code! 🎉**
