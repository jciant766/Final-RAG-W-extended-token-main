# Optimal Chunking Strategy for Malta Legal CRAG

## Research Summary from Voyage AI + Legal RAG Best Practices

### Key Findings

**From Voyage AI:**
- `voyage-law-2` has **16,000 token context length** (very large!)
- Trained on **1T legal tokens** including long-context legal documents
- Excels at **long-context retrieval**
- ⚠️ Warning: "Chunking can come at expense of broader context"
- 🔑 "Missing context can lead to **costly errors** in legal domains"

**From Legal RAG Research (2024-2025):**
- **Structure-aware chunking** performs best for legal documents
- Recommended chunk sizes:
  - **256 tokens** with 25-token overlap (empirically optimal)
  - OR **400-512 tokens** with 10-20% overlap
- **Page-level chunking** achieved highest accuracy (0.648) in NVIDIA benchmark
- 🎯 "Legal clauses or arguments should NOT be fragmented across chunks"
- ✅ "Leverage inherent organization (sections, articles, clauses)"

---

## Malta Law Structure Analysis

### From Your Sample

```
15.(1) All persons seeking psychosocial counselling...
15.(2) The pathologisation of any form of sexual orientation...

16.(1) The Minister, after consulting...
16.(2) The working group shall consist of...
16.(3) The Chairperson shall be a medical doctor...
16.(4) The members shall be three experts...
16.(5) The Minister shall appoint the working group...
16.(6) The members of the working group shall review...

17. The Minister may make regulations to give better effect...
```

**Structure:**
- **Article**: Number followed by period (e.g., `15.`, `16.`, `17.`)
- **Sub-article**: Number in parentheses (e.g., `(1)`, `(2)`, `(3)`)
- Articles are **semantically grouped** (15-17 all about gender identity treatment)

---

## Recommended Chunking Strategy

### ✅ OPTION 1: One Article Per Chunk (RECOMMENDED)

**Chunk = 1 Article + All Its Sub-articles**

**Example:**
```
Chunk 1:
15.(1) All persons seeking psychosocial counselling, support and
medical interventions relating to sex or gender should be given expert
sensitive and individually tailored support by psychologists and medical
practitioners or peer counselling. Such support should extend from the
date of diagnosis or self-referral for as long as necessary.
(2) The pathologisation of any form of sexual orientation, gender
identity and, or gender expression as may be classified under the
International Classification of Diseases or any other similar
internationally recognised classification, shall be null and void in
Malta. The nullity of such classification shall not impact negatively
the provision of any healthcare service related to sex and, or gender.

Chunk 2:
16.(1) The Minister, after consulting the Minister responsible
for health, shall appoint a working group.
(2) The working group shall consist of a Chairperson and nine members.
[... all sub-articles through (6)]
```

**Benefits:**
- ✅ Preserves **logical legal units** (article = complete legal concept)
- ✅ Keeps sub-articles with parent (sub-articles often clarify/qualify the main article)
- ✅ Natural legal structure respected
- ✅ Easy to cite: "According to [Act, Article 15(2)]..."
- ✅ Typical article size: 100-400 tokens (well within 256-512 recommendation)

**Drawbacks:**
- ~ Loses some cross-article context
- ~ Related articles (15-17) separated

---

### ⚠️ OPTION 2: Semantic Topic Groups (Alternative)

**Chunk = Multiple Related Articles**

**Example:**
```
Chunk 1 (Treatment Protocol - Articles 15-17):
15.(1) All persons seeking psychosocial counselling...
15.(2) The pathologisation of any form...
16.(1) The Minister, after consulting...
[... all of 15, 16, 17 together]
```

**Benefits:**
- ✅ Preserves **topic coherence** (all articles about same topic)
- ✅ Captures cross-references between articles
- ✅ More context for complex legal reasoning

**Drawbacks:**
- ❌ Chunks become **very large** (500-1000+ tokens)
- ❌ Harder to pinpoint specific article in retrieval
- ❌ May include irrelevant sub-articles
- ❌ Wastes voyage-law-2's precision

---

### ❌ OPTION 3: Sub-article Level (NOT RECOMMENDED)

**Chunk = Individual Sub-articles**

**Example:**
```
Chunk 1: Article 15(1)...
Chunk 2: Article 15(2)...
Chunk 3: Article 16(1)...
```

**Why Not:**
- ❌ **Fragments legal meaning** (sub-articles depend on parent)
- ❌ Loses critical context
- ❌ Legal error risk HIGH
- ❌ Citations become confusing

---

## Final Recommendation

### 🎯 Use **OPTION 1: One Article Per Chunk**

**Reasoning:**
1. **Legal precedent**: Articles are the fundamental legal unit in Malta law
2. **Size optimal**: Most articles = 100-400 tokens (within 256-512 best practice)
3. **Context preservation**: Sub-articles stay with parent
4. **Citation clarity**: Easy to cite [Act, Article X(Y)]
5. **Retrieval precision**: voyage-law-2 can find exact relevant article
6. **Validation accuracy**: CRAG can verify claims against specific articles

**Implementation:**
```python
def chunk_malta_law(text: str) -> List[Dict]:
    """
    Split Malta law text into chunks, one article per chunk.

    Article pattern: Bold number followed by period (e.g., "15.")
    Sub-article pattern: Number in parentheses (e.g., "(1)")
    """
    chunks = []

    # Regex: Match article number (e.g., "15.")
    articles = re.split(r'\n(\d+)\.\s*', text)

    for i in range(1, len(articles), 2):
        article_num = articles[i]
        article_text = articles[i+1].strip()

        chunks.append({
            'id': f'article_{article_num}',
            'content': f'{article_num}. {article_text}',
            'metadata': {
                'article': article_num,
                'type': 'article',
                # Add chapter, act name, etc.
            }
        })

    return chunks
```

---

## Token Count Analysis

### Your Current Documents

**Current (Multi-article chunks):**
- Doc 1: Articles 320-322 → ~250 tokens ✅
- Doc 2: Article 56(13) → ~120 tokens ✅
- Doc 3: Articles 1346-1347 → ~130 tokens ✅

**All within optimal range!**

**If Split to One Article Per Chunk:**
- Article 320 → ~60 tokens
- Article 321 → ~40 tokens
- Article 322(1)+(2) → ~150 tokens
- Article 56(13)(a)+(b) → ~120 tokens ✅
- Article 1346 → ~50 tokens
- Article 1347 → ~80 tokens

**Analysis:**
- Single articles often **too small** (40-80 tokens)
- Multi-article groups (2-3 related) are **optimal** (120-250 tokens)

---

## Revised Final Recommendation

### 🎯 **HYBRID APPROACH: Keep Related Articles Together**

**Rules:**
1. **Default**: One article per chunk
2. **Exception**: If articles are **tightly related** (sequential + same topic), group 2-4 together
3. **Target size**: 150-400 tokens per chunk
4. **Never exceed**: 512 tokens

**How to Identify "Related":**
- Sequential article numbers (320, 321, 322)
- Same legal topic (all about ownership)
- Cross-references between articles
- Sub-articles of a parent concept

**Example from Your Data:**
```
✅ GOOD: Articles 320-322 together (all about ownership, 250 tokens)
✅ GOOD: Article 56(13) alone (specific tax provision, 120 tokens)
✅ GOOD: Articles 1346-1347 together (both about sale contracts, 130 tokens)
```

**Example from Your Sample:**
```
✅ GOOD: Articles 15-17 together (all about treatment protocol, ~500 tokens)
   OR
✅ BETTER: Article 15 alone (psychosocial support, ~200 tokens)
          Article 16 alone (working group, ~250 tokens)
          Article 17 alone (regulations, ~80 tokens)
```

---

## Metadata to Include

For each chunk, add:
```python
{
    'id': 'doc_X',
    'content': '320. Ownership is...',
    'metadata': {
        'citation': 'Civil Code Cap. 16, Article 320-322',
        'article': '320',  # First article in chunk
        'article_range': '320-322',  # If multi-article
        'chapter': 'Cap. 16',
        'act_name': 'Civil Code',
        'topic': 'Ownership',  # Manual tag
        'jurisdiction': 'Malta',
        'verified_source': 'legislation.mt',
        'token_count': 250
    }
}
```

---

## Answer to Your Question

### "You think for every chunk we have one article?"

**My Answer: MOSTLY YES, with smart exceptions**

✅ **One article per chunk IF:**
- Article is substantial (150+ tokens)
- Article is self-contained topic
- Article doesn't heavily reference adjacent articles

✅ **Multiple articles per chunk IF:**
- Articles are tightly related (same topic)
- Combined size: 150-400 tokens
- They form a logical legal unit
- Sequential numbering (320, 321, 322)

❌ **Never:**
- Split sub-articles from parent
- Exceed 512 tokens per chunk
- Mix unrelated topics

---

## Current System Status

**Your 3 documents are ALREADY OPTIMAL:**
- Articles 320-322 together ✅ (related, 250 tokens)
- Article 56(13) alone ✅ (specific, 120 tokens)
- Articles 1346-1347 together ✅ (related, 130 tokens)

**Continue this pattern!**

---

## How Many Laws Do You Need?

### Current: 3 documents (covering 6 articles)

**For Production Legal RAG:**
- **Minimum viable**: 50-100 articles (10-20 chunks)
- **Good coverage**: 200-500 articles (50-100 chunks)
- **Comprehensive**: 1000+ articles (200-400 chunks)

**Priority Topics** (if you're expanding):
1. **Property Law** (Civil Code 320-500)
2. **Contract Law** (Civil Code 1100-1400)
3. **Tax Law** (Income Tax Act, Duty Act)
4. **Corporate Law** (Companies Act)
5. **Marriage/Family Law** (Civil Code 900-1100)
6. **Inheritance Law** (Civil Code 600-900)

**Quality > Quantity:**
- Better to have **100 verified articles** than 1000 unverified
- Focus on high-demand topics first

---

## Summary

✅ **Chunking Strategy**: One article per chunk (or 2-4 related articles)
✅ **Target Size**: 150-400 tokens per chunk
✅ **Current System**: Already optimal
✅ **Next Step**: Add more articles using same pattern
✅ **Recommendation**: Add 50-100 high-priority articles

**Want me to add more laws? Tell me:**
- What topics? (property, tax, contracts, etc.)
- How many articles? (10, 50, 100?)
- Specific acts? (Civil Code, Income Tax Act, etc.)

I'll extract them from legislation.mt with the optimal chunking strategy!
