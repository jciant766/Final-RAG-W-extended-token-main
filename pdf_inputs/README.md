# PDF/TXT Inputs Directory

## 📂 Place Your Files Here

Put any Malta law documents here (PDF or TXT format) to be auto-extracted.

## ✅ Supported Formats

- **PDF files** (.pdf) - Automatically extracts text
- **TXT files** (.txt) - Direct text processing

## 📋 How to Use

### Step 1: Place File Here
```bash
# Example: Place civil_code_articles.pdf in this directory
cp ~/Downloads/civil_code_articles.pdf ./pdf_inputs/
```

### Step 2: Run Auto-Extractor
```bash
# From main directory
cd ..
python auto_extract_malta_law.py -i pdf_inputs/civil_code_articles.pdf -a "Civil Code" -c "Cap. 16"
```

### Step 3: Preview First (Recommended)
```bash
# Preview without saving to check detection
python auto_extract_malta_law.py -i pdf_inputs/file.pdf -a "Act Name" -c "Cap. X" --preview
```

## 📖 Examples

### Extract from PDF
```bash
python auto_extract_malta_law.py \
  -i pdf_inputs/civil_code.pdf \
  -a "Civil Code" \
  -c "Cap. 16"
```

### Extract from TXT
```bash
python auto_extract_malta_law.py \
  -i pdf_inputs/tax_act.txt \
  -a "Income Tax Act" \
  -c "Cap. 123"
```

### Extract Specific Topic
```bash
python auto_extract_malta_law.py \
  -i pdf_inputs/property_law.pdf \
  -a "Civil Code" \
  -c "Cap. 16" \
  -t "Property Rights"
```

## 🎯 What the Tool Does

1. ✅ **Auto-detects articles** (15., 320., etc.)
2. ✅ **Detects sub-articles** ((1), (2), (a), (b), etc.)
3. ✅ **Groups related articles** (320-322 if same topic)
4. ✅ **NO token limits** (preserves complete articles)
5. ✅ **Generates metadata** (citation, topic, chapter)
6. ✅ **Adds to database** (malta_law_database.py)

## ⚙️ Requirements

Install PDF support:
```bash
pip install PyPDF2
```

Or use text files (no dependencies needed).

## 📊 File Naming Recommendations

Good file names:
- `civil_code_property_law_art_300-600.pdf`
- `income_tax_act_full.pdf`
- `criminal_code_part_1.txt`

This helps you remember what each file contains.

## 🚀 Quick Start

1. **Download law from legislation.mt** (PDF or copy text)
2. **Save to this directory**
3. **Run extractor**: `python auto_extract_malta_law.py -i pdf_inputs/[file] -a "[Act]" -c "[Chapter]"`
4. **Check output**: Review malta_law_database.py
5. **Test**: Run `python test_expanded_crag.py`

## 💡 Tips

- **Preview first** with `--preview` flag to check article detection
- **Start small** - extract 10-20 articles first, then add more
- **Check metadata** - verify act names and chapters are correct
- **Clean PDFs work best** - scanned/OCR PDFs may have issues

## ❓ Troubleshooting

**"No articles detected"**
- PDF might be scanned (use OCR first)
- Text format might be unusual
- Try converting PDF to TXT first

**Articles merged incorrectly**
- Use `--preview` to check detection
- May need manual adjustment in database file

**Missing sub-articles**
- Tool auto-detects (1), (2), etc.
- All sub-articles stay with parent article
- Check preview to verify

## 📁 Current Files

(Place your PDFs/TXT files here - they will be listed when you add them)
