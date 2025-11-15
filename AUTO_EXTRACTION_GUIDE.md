# Auto-Extraction Tool - Complete Guide

## 🎯 What This Tool Does

**Fully automates article extraction** - no manual formatting needed!

The tool:
1. ✅ **Reads PDFs or TXT files**
2. ✅ **Auto-detects articles** (15., 320., 1234., etc.)
3. ✅ **Auto-detects sub-articles** ((1), (2), (a), (b), etc.)
4. ✅ **Chunks properly** (one article per chunk or related articles grouped)
5. ✅ **NO token limits** (preserves complete articles, 50-5000+ tokens)
6. ✅ **Generates metadata** (citation, chapter, topic, etc.)
7. ✅ **Adds to database** (malta_law_database.py)

**You just provide the PDF/TXT, the tool does the rest!**

---

## 📋 What You Need

### Option 1: From Me (Nothing!)
I can run the extraction for you. Just tell me:
- What legal area to extract (e.g., "Civil Code property law articles 300-600")
- How many articles you want (e.g., "50 articles")

### Option 2: Do It Yourself
You need:
1. **PDF or TXT file** of Malta law (from legislation.mt)
2. **Know the Act name** (e.g., "Civil Code")
3. **Know the Chapter** (e.g., "Cap. 16")

That's it!

---

## 🚀 Quick Start (3 Steps)

### Step 1: Place File in pdf_inputs/
```bash
# Download law from legislation.mt
# Save as PDF or copy text to .txt file
# Put in pdf_inputs/ directory

cp ~/Downloads/civil_code.pdf ./pdf_inputs/
```

### Step 2: Preview (Check Detection)
```bash
python auto_extract_malta_law.py \
  -i pdf_inputs/civil_code.pdf \
  -a "Civil Code" \
  -c "Cap. 16" \
  --preview
```

**You'll see:**
```
✓ Detected 50 articles

Detected articles:
  • Article 300 [has sub-articles]
  • Article 301
  • Article 302 [has sub-articles]
  ...

Created 15 chunks
```

### Step 3: Extract & Add to Database
```bash
# Remove --preview flag to actually save
python auto_extract_malta_law.py \
  -i pdf_inputs/civil_code.pdf \
  -a "Civil Code" \
  -c "Cap. 16"
```

**Done! Articles added to database.**

---

## 📖 Detailed Examples

### Example 1: Extract from PDF

```bash
# 1. Place PDF in pdf_inputs/
cp ~/Downloads/property_law.pdf ./pdf_inputs/

# 2. Preview first
python auto_extract_malta_law.py \
  -i pdf_inputs/property_law.pdf \
  -a "Civil Code" \
  -c "Cap. 16" \
  --preview

# 3. Check output looks good, then extract
python auto_extract_malta_law.py \
  -i pdf_inputs/property_law.pdf \
  -a "Civil Code" \
  -c "Cap. 16"

# 4. Test the system
python test_expanded_crag.py
```

### Example 2: Extract from TXT (Simpler)

```bash
# 1. Copy text from legislation.mt and save as .txt
# 2. Extract directly (no PDF parsing needed)

python auto_extract_malta_law.py \
  -i pdf_inputs/tax_articles.txt \
  -a "Income Tax Act" \
  -c "Cap. 123"
```

### Example 3: Extract to Separate File (Review First)

```bash
# Save to separate file instead of adding to database
python auto_extract_malta_law.py \
  -i pdf_inputs/new_law.pdf \
  -a "Some Act" \
  -c "Cap. 999" \
  -o extracted_temp.py

# Review extracted_temp.py
# If good, manually merge into malta_law_database.py
```

---

## 🎨 How Article Detection Works

### What the Tool Recognizes

**Articles:**
```
15. This is an article...
320. Another article...
1234. Yet another article...
```
Pattern: **Number + period + space**

**Sub-articles:**
```
15.(1) First sub-article...
(2) Second sub-article...
(3) Third sub-article...
    (a) Nested sub-article...
    (b) Another nested one...
```
Pattern: **Number in parentheses**

**What It Ignores:**
```
CAP.540.]  ← Not an article (chapter header)
[320]      ← Not an article (brackets)
Section 5  ← Not an article (text, not number)
```

### Chunking Logic

**Single Article:**
```
Input:
  15.(1) First...
  (2) Second...

Output:
  Chunk 1: "15.(1) First...(2) Second..." [ONE chunk]
```

**Related Articles (Grouped):**
```
Input:
  320. Ownership is...
  321. No person can...
  322. (1) Save as...

Output:
  Chunk 1: "320. Ownership... 321. No person... 322. (1) Save..." [ONE chunk with 3 articles]
```

**Unrelated Articles (Separated):**
```
Input:
  100. About property...
  200. About marriage...

Output:
  Chunk 1: "100. About property..."
  Chunk 2: "200. About marriage..."
```

---

## 🔧 Command Options

```bash
python auto_extract_malta_law.py [OPTIONS]

Required:
  -i, --input FILE      PDF or TXT file to process
  -a, --act NAME        Act name (e.g., "Civil Code")
  -c, --chapter NUM     Chapter (e.g., "Cap. 16")

Optional:
  -t, --topic TOPIC     Override auto-detected topic
  -o, --output FILE     Save to new file instead of database
  -p, --preview         Preview only, don't save
  -h, --help            Show help
```

---

## 📊 What Gets Auto-Generated

For each chunk, the tool creates:

```python
{
    'id': 'doc_Cap_16_art_320_322',  # Auto-generated ID
    'content': '''320. Ownership is...
321. No person can...
322. (1) Save as...''',  # Complete article(s)
    'metadata': {
        'citation': 'Civil Code Cap. 16, Article 320-322',  # Auto
        'article': '320-322',  # Auto-detected range
        'chapter': 'Cap. 16',  # From your input
        'act_name': 'Civil Code',  # From your input
        'topic': 'Ownership',  # Auto-detected from content
        'jurisdiction': 'Malta',  # Auto-added
        'verified_source': 'legislation.mt',  # Auto-added
        'auto_extracted': True  # Marks as auto-extracted
    }
}
```

**Topic auto-detection** looks for keywords:
- "ownership" → "Ownership"
- "sale" → "Sale Contracts"
- "tax" → "Taxation"
- "insurance" → "Insurance Requirements"
- etc.

---

## 🎯 Workflow Comparison

### Old Way (Manual):
1. Copy text from legislation.mt
2. Open LLM prompt
3. Paste text
4. Wait for LLM to format
5. Copy formatted output
6. Paste to me
7. I add to database

**Time: 10-15 minutes per file**

### New Way (Automated):
1. Download PDF or save TXT
2. Run: `python auto_extract_malta_law.py -i file.pdf -a "Act" -c "Cap. X"`

**Time: 30 seconds**

---

## 💡 Best Practices

### 1. Preview First
```bash
# Always preview before saving
python auto_extract_malta_law.py -i file.pdf -a "Act" -c "Cap" --preview
```
This shows you what will be detected without saving.

### 2. Start Small
- Extract 10-20 articles first
- Test with `python test_expanded_crag.py`
- If good, extract more

### 3. Use Clean Sources
- PDFs from legislation.mt work best
- Avoid scanned/OCR PDFs (use text extraction first)
- TXT files are most reliable

### 4. Check Metadata
After extraction, open `malta_law_database.py` and verify:
- Article numbers are correct
- Citations are formatted properly
- Topics make sense

---

## 🔍 Troubleshooting

### Problem: "No articles detected"

**Cause**: PDF is scanned or has unusual formatting

**Solution**:
1. Try converting PDF to text first:
```bash
# If you have pdftotext installed
pdftotext file.pdf file.txt
python auto_extract_malta_law.py -i file.txt -a "Act" -c "Cap"
```

2. Or copy-paste text from PDF viewer to TXT file

### Problem: Articles are grouped wrong

**Cause**: Auto-grouping may not be perfect

**Solution**:
1. Use `--preview` to check grouping
2. If needed, manually adjust in `malta_law_database.py` after extraction
3. Or extract to separate file first with `-o` flag

### Problem: "PyPDF2 not installed"

**Solution**:
```bash
pip install PyPDF2
```

Or use TXT files (no dependencies needed).

### Problem: Topic detection is wrong

**Solution**: Use `-t` flag to override:
```bash
python auto_extract_malta_law.py \
  -i file.pdf \
  -a "Act" \
  -c "Cap" \
  -t "Custom Topic Name"
```

---

## 📁 File Organization

```
Final-RAG-W-extended-token-main/
├── auto_extract_malta_law.py      # The extraction tool
├── malta_law_database.py           # Database (articles added here)
├── test_expanded_crag.py           # Test suite
├── pdf_inputs/                     # PUT YOUR PDFs/TXT HERE
│   ├── README.md
│   ├── civil_code.pdf             # Your files
│   ├── tax_act.txt                # Your files
│   └── ...
└── ...
```

**Workflow:**
1. Put files in `pdf_inputs/`
2. Run `auto_extract_malta_law.py`
3. Articles go to `malta_law_database.py`
4. Test with `test_expanded_crag.py`

---

## 🚀 Common Use Cases

### Use Case 1: Add 50 Property Law Articles

```bash
# 1. Get Civil Code articles 300-600 from legislation.mt
# 2. Save as PDF or TXT in pdf_inputs/
# 3. Extract

python auto_extract_malta_law.py \
  -i pdf_inputs/civil_code_property.pdf \
  -a "Civil Code" \
  -c "Cap. 16"

# Result: ~50 articles added to database
```

### Use Case 2: Add Entire Tax Act

```bash
python auto_extract_malta_law.py \
  -i pdf_inputs/income_tax_act_full.pdf \
  -a "Income Tax Act" \
  -c "Cap. 123"

# Result: 100+ articles added
```

### Use Case 3: Test Before Adding

```bash
# Preview first
python auto_extract_malta_law.py \
  -i pdf_inputs/new_law.pdf \
  -a "Some Act" \
  -c "Cap. 999" \
  --preview

# If good, extract to temp file
python auto_extract_malta_law.py \
  -i pdf_inputs/new_law.pdf \
  -a "Some Act" \
  -c "Cap. 999" \
  -o temp_extracted.py

# Review temp_extracted.py
# If satisfied, add to database:
python auto_extract_malta_law.py \
  -i pdf_inputs/new_law.pdf \
  -a "Some Act" \
  -c "Cap. 999"
```

---

## ✅ What You Need to Provide

### Minimum Requirements:

1. **File** (PDF or TXT)
   - From legislation.mt or any official source
   - Clean formatting works best

2. **Act Name** (string)
   - Example: "Civil Code"
   - Example: "Income Tax Act"
   - Example: "Criminal Code"

3. **Chapter** (string)
   - Example: "Cap. 16"
   - Example: "Cap. 123"
   - Format: "Cap. [number]"

### Optional:

4. **Topic** (if you want to override auto-detection)
   - Example: "Property Rights"
   - Example: "Taxation"

**That's it! The tool handles everything else.**

---

## 🎯 Next Steps

### Option 1: I Do It For You
Tell me:
```
"Extract Civil Code articles 300-600 (property law)"
"Extract Income Tax Act in full"
"Extract 50 most common articles across all acts"
```

I'll use the tool and add to database.

### Option 2: You Do It
1. Download PDF/TXT from legislation.mt
2. Place in `pdf_inputs/`
3. Run tool with act name and chapter
4. Done!

### Option 3: Hybrid
- You download files and place in `pdf_inputs/`
- Tell me: "I put civil_code.pdf in pdf_inputs, can you extract it?"
- I run the tool for you

---

## 📊 Tool Capabilities

**Can handle:**
- ✅ Single articles (Article 15)
- ✅ Articles with many sub-articles (Article 56.(1)-(50))
- ✅ Nested sub-articles ((1)(a)(i))
- ✅ Very long articles (5000+ tokens - no limits!)
- ✅ Short articles (50 tokens)
- ✅ Sequential articles (320, 321, 322)
- ✅ Non-sequential articles (100, 200, 300)

**Cannot handle (yet):**
- ❌ Scanned PDFs without OCR
- ❌ Images of text
- ❌ Heavily formatted tables (may need cleanup)

---

## 🎉 Summary

**The tool is ready to use NOW!**

**To add 100 articles:**
1. Get PDF from legislation.mt
2. Put in `pdf_inputs/`
3. Run: `python auto_extract_malta_law.py -i pdf_inputs/file.pdf -a "Act" -c "Cap. X"`
4. Done!

**No manual formatting, no LLM prompt, no copy-pasting needed.**

---

**What do you want to extract?** Tell me and I'll help you get it done!
