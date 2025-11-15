# Optimal Chunking Strategy for Malta Legal CRAG

## 🎯 Core Principle: NEVER SPLIT ARTICLES

**One Article = One Complete Chunk, Regardless of Token Count**

---

## ⚠️ Why NO Token Limits?

### The Problem with Token Limits

**BAD Approach (Token-limited chunking):**
```
Article 56 (700 tokens total)
↓
Chunk 1: Article 56.(1)-(5) [400 tokens] ✂️ SPLIT HERE
Chunk 2: Article 56.(6)-(10) [300 tokens]

Result: ❌ Article fragmented
        ❌ Context destroyed
        ❌ Legal meaning compromised
        ❌ CRAG validation fails
```

**GOOD Approach (Article-based chunking):**
```
Article 56 (700 tokens total)
↓
Chunk 1: Article 56.(1)-(10) [700 tokens complete] ✅

Result: ✅ Article intact
        ✅ Context preserved
        ✅ Legal meaning clear
        ✅ CRAG validation accurate
```

### Why Legal Documents Are Different

1. **Legal Integrity**: Articles are indivisible legal units
2. **Sub-article Dependencies**: Sub-article (5) may depend on context from (1)
3. **Citation Requirements**: Must cite [Act, Article X] - need complete article
4. **Validation Accuracy**: CRAG verifies claims against full article text
5. **Context Critical**: "Missing context can lead to costly errors" (Voyage AI)

---

## ✅ Revised Chunking Strategy

### Rule 1: One Article = One Chunk (ALWAYS)

**Never split an article, regardless of length.**

```python
# Article with ALL its sub-articles = ONE chunk
chunk = {
    'id': 'doc_1',
    'content': '''56.(1) First sub-article...
(2) Second sub-article...
(3) Third sub-article...
...
(15) Fifteenth sub-article...''',  # Could be 2000+ tokens - THAT'S FINE
    'metadata': {
        'citation': 'Income Tax Act Cap. 123, Article 56',
        'article': '56'
    }
}
```

### Rule 2: Group Related Articles (Optional)

**If articles are tightly related, you MAY group them:**

**Group Together IF:**
- Sequential numbers (320, 321, 322)
- Same specific topic (all define "ownership")
- They cross-reference each other
- They form a logical legal unit

**Example:**
```
Articles 320-322 (all about ownership) → ONE chunk
Articles 1346-1347 (both about sale contracts) → ONE chunk
```

**Keep Separate IF:**
- Different topics (even if sequential)
- Article is already substantial
- No logical connection

### Rule 3: Trust Voyage Law's 16K Context

**Technical Specs:**
- **voyage-law-2 context**: 16,000 tokens
- **Typical long article**: 500-2000 tokens
- **Very long article**: 3000-5000 tokens (rare)
- **Margin**: 3x-5x safety buffer

**Even the longest Malta law articles fit comfortably.**

---

## 📊 Real-World Token Analysis

### Your Current Documents (All Optimal)

```
Document 1: Civil Code Articles 320-322
├─ Article 320: ~60 tokens
├─ Article 321: ~40 tokens
└─ Article 322: ~150 tokens
Total: ~250 tokens ✅ PERFECT

Document 2: Income Tax Act Article 56(13)
├─ Article 56(13)(a): ~80 tokens
└─ Article 56(13)(b): ~40 tokens
Total: ~120 tokens ✅ PERFECT

Document 3: Civil Code Articles 1346-1347
├─ Article 1346: ~50 tokens
└─ Article 1347: ~80 tokens
Total: ~130 tokens ✅ PERFECT
```

### Example Long Articles (No Problem)

```
Hypothetical Complex Tax Article:
Article 156 with 20 sub-articles: ~1500 tokens
✅ Still only 9% of voyage-law-2's 16K capacity

Hypothetical Very Long Article:
Article 500 with 50 sub-articles: ~4000 tokens
✅ Still only 25% of voyage-law-2's 16K capacity
```

---

## 🏗️ Implementation

### Chunking Algorithm (Simplified)

```python
def chunk_malta_law(text: str, act_name: str) -> List[Dict]:
    """
    Split Malta law into chunks - ONE ARTICLE PER CHUNK.
    NO TOKEN LIMITS - preserve article integrity.
    """
    chunks = []

    # Split by article number (e.g., "15.", "320.")
    articles = re.split(r'\n(\d+)\.\s*', text)

    for i in range(1, len(articles), 2):
        article_num = articles[i]
        article_text = articles[i+1].strip()

        chunk = {
            'id': f'article_{article_num}',
            'content': f'{article_num}. {article_text}',
            'metadata': {
                'citation': f'{act_name}, Article {article_num}',
                'article': article_num,
                'act': act_name
            }
        }
        chunks.append(chunk)

    return chunks

# NO token counting, NO truncation, NO splitting
# Just pure article boundaries
```

### Grouping Algorithm (Optional Enhancement)

```python
def should_group_articles(article1: Dict, article2: Dict) -> bool:
    """
    Decide if two articles should be grouped.
    Based on semantic similarity, not token count.
    """
    # Check if sequential
    num1 = int(article1['metadata']['article'])
    num2 = int(article2['metadata']['article'])
    if num2 != num1 + 1:
        return False

    # Check if same topic (could use LLM or keywords)
    topic1 = classify_topic(article1['content'])
    topic2 = classify_topic(article2['content'])

    return topic1 == topic2

# Still NO token limits!
```

---

## 📏 No More Token Recommendations

### ❌ OLD (WRONG):
```
"Target: 150-400 tokens per chunk"
"Never exceed: 512 tokens"
"Optimal size: 256 tokens with 25-token overlap"
```

### ✅ NEW (CORRECT):
```
"One article = One chunk"
"No token limits"
"No truncation"
"Preserve complete legal units"
```

---

## 🔍 Why This Works

### 1. Voyage Law 2 Design
- **Built for long legal documents**
- "Trained on massive long-context legal documents"
- "Excels in long-context retrieval"
- 16K tokens is MASSIVE (16,000 tokens ≈ 12,000 words ≈ 24 pages)

### 2. Retrieval Precision
- With full articles, embeddings capture complete legal meaning
- No fragmented context
- Better semantic matching

### 3. CRAG Validation
- Validator sees complete article
- Can verify all sub-article references
- Citations are accurate
- No "claim is in sub-article (12) but we only have (1)-(6)" errors

### 4. Legal Accuracy
- Lawyers expect complete articles
- Sub-articles often modify/clarify earlier sub-articles
- Legal reasoning requires full context

---

## 🎯 Updated Submission Guidelines

### For Users Submitting Articles

**What to send:**
```
---
ACT: Civil Code
CITATION: Civil Code Cap. 16, Article 56
ARTICLES: 56
TOPIC: Property Rights
---

56.(1) First sub-article...
(2) Second sub-article...
(3) Third sub-article...
[... ALL sub-articles, even if there are 50 of them ...]
(50) Fiftieth sub-article...

---
```

**Don't worry about length. Just include the COMPLETE article.**

---

## 📊 Metadata to Track (Not Limit)

```python
{
    'id': 'doc_X',
    'content': '[FULL ARTICLE - NO TRUNCATION]',
    'metadata': {
        'citation': 'Act Name, Article X',
        'article': 'X',
        'act': 'Act Name',
        'topic': 'Topic Name',
        'token_count': 1543,  # Track for analytics, NOT for limiting
        'char_count': 8234,
        'sub_article_count': 12,
        'verified_source': 'legislation.mt'
    }
}
```

**Use token_count for ANALYTICS, not ENFORCEMENT.**

---

## ✅ Summary

### The New Rules

1. ✅ **One article = One chunk** (always)
2. ✅ **Include ALL sub-articles** with parent
3. ✅ **No token limits** (trust voyage-law-2's 16K context)
4. ✅ **Never truncate** article text
5. ✅ **Never split** articles mid-content
6. ✅ **Group related articles** (optional, based on topic not tokens)
7. ✅ **Preserve legal integrity** over arbitrary size limits

### Why This Is Right

- **Legal documents are not blog posts** - they have inherent structure
- **Articles are indivisible units** - like database transactions
- **Context is critical** - sub-article (20) may reference (1)
- **Voyage Law 2 can handle it** - 16K tokens is huge
- **CRAG needs complete articles** - for accurate validation
- **Better safe than sorry** - preserving too much context > fragmenting legal meaning

---

## 🚀 Going Forward

**All previous token limit recommendations are VOID.**

**New approach:**
- Submit complete articles
- Don't count tokens
- Trust the system
- Prioritize legal accuracy over chunk size optimization

**The system will:**
- Accept articles of any length
- Process them completely
- Embed full context
- Validate against complete text
- Return accurate, grounded answers

---

**Bottom line: Legal integrity > arbitrary token limits.**
