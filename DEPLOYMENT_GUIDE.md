# Deployment Guide - Malta Legal RAG System

This guide explains how to deploy your RAG application to **GitHub** and **Streamlit Cloud**.

---

## Prerequisites

1. **GitHub Account** - [Sign up here](https://github.com/signup)
2. **Streamlit Cloud Account** - [Sign up here](https://streamlit.io/cloud) (free)
3. **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)
4. **Git installed locally** - [Download here](https://git-scm.com/downloads)

---

## Part 1: Push to GitHub

### Step 1: Initialize Git Repository (if not already done)

```bash
cd "Final-RAG-W-extended-token-main"
git init
```

### Step 2: Add All Files

**IMPORTANT:** Make sure these files are committed:
- All 44 `.txt` files in `ocr/output/` (including `13 - Commercial Code.txt`)
- All Python files (`.py`)
- `Requirements.txt`
- `.gitignore`

```bash
# Add all files
git add .

# Verify the text files are staged
git status | grep "ocr/output"
```

You should see all 44 text files listed, including:
- `ocr/output/13 - Commercial Code.txt`
- `ocr/output/16 - Civil Code.txt`
- `ocr/output/123 - Income Tax Act.txt`
- etc.

### Step 3: Create First Commit

```bash
git commit -m "Initial commit: Malta Legal RAG System with 44 legal documents"
```

### Step 4: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `malta-legal-rag` (or your preferred name)
3. Description: "RAG system for Malta legal documents search"
4. **Keep it Public** (or Private if preferred)
5. **Do NOT** initialize with README (we already have files)
6. Click "Create repository"

### Step 5: Push to GitHub

GitHub will show you commands like these (use them):

```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git branch -M main
git push -u origin main
```

**Replace** `YOUR-USERNAME` and `YOUR-REPO-NAME` with your actual values.

---

## Part 2: Deploy to Streamlit Cloud

### Step 1: Go to Streamlit Cloud

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Click "New app" button

### Step 2: Configure Deployment

Fill in the form:
- **Repository:** Select your GitHub repo (e.g., `your-username/malta-legal-rag`)
- **Branch:** `main` (or `master`)
- **Main file path:** `main.py`

### Step 3: Add OpenAI API Key (CRITICAL!)

Before clicking "Deploy", click **"Advanced settings"**:

1. In the "Secrets" section, add:

```toml
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
```

**⚠️ WARNING:** Without this, the app will fail to build the vector database!

### Step 4: Deploy!

Click **"Deploy"** and wait. The deployment process will:

1. ✅ Install dependencies from `Requirements.txt`
2. ✅ Load all 44 legal document files from `ocr/output/`
3. ✅ Show progress bars as it processes documents
4. ✅ Build the vector database (takes ~5-10 minutes on first run)
5. ✅ Generate embeddings using OpenAI API
6. ✅ Launch the application

---

## What Happens on First Launch

### On Streamlit Cloud (First Time):

1. **App starts** → No `chroma_db/` or `processed_chunks.json` found
2. **Automatic Build Triggered:**
   - Progress bar appears: "Processing [1/44]: 12 - Code of Organization..."
   - Each document is processed and chunked
   - Shows: "Processing [44/44]: EU Succession Regulation..."
   - Builds embeddings: "Generating embeddings: Batch 1/23..."
3. **Database Ready** → App loads and search becomes available

### Subsequent Launches:

- Vector database already exists in the container
- App loads instantly (no rebuild needed)
- Search is immediately available

---

## File Structure in Repository

Ensure your GitHub repo has this structure:

```
malta-legal-rag/
├── .gitignore                 ✅ Excludes chroma_db/, processed_chunks.json
├── main.py                    ✅ Streamlit app entry point
├── vector_store.py            ✅ Vector database management
├── doc_processor.py           ✅ Document processing with fixed inference
├── search_engine.py           ✅ Search functionality
├── ai_assistant.py            ✅ AI overview generation
├── debug_logger.py            ✅ Logging
├── build_vector_db.py         ✅ Manual rebuild script
├── process_all_documents.py   ✅ Process without embeddings
├── test_all_sources.py        ✅ Test script
├── Requirements.txt           ✅ Python dependencies
├── DEPLOYMENT_GUIDE.md        ✅ This file
└── ocr/
    └── output/                ✅ MUST BE IN REPO
        ├── 13 - Commercial Code.txt           ✅ 273 articles
        ├── 16 - Civil Code.txt                ✅ 547 articles
        ├── 123 - Income Tax Act.txt           ✅ 99 articles
        ├── 12 - Code of Organization...txt    ✅ 526 articles
        └── ... (40 more legal documents)      ✅ Total: 44 files
```

---

## Important Files for Deployment

### ✅ MUST Include in Git:

- **All 44 `.txt` files in `ocr/output/`** - Required for processing
- `main.py` - Entry point
- `*.py` - All Python files
- `Requirements.txt` - Dependencies

### ❌ DO NOT Include (in .gitignore):

- `chroma_db/` - Built automatically
- `processed_chunks.json` - Built automatically
- `processing_report.json` - Built automatically
- `.env` - Contains secrets
- `__pycache__/` - Python cache

---

## Verifying Deployment

### Check 1: Files are Committed

```bash
git ls-files ocr/output/ | wc -l
```

Should show: **44** (all text files)

### Check 2: Commercial Code is Present

```bash
git ls-files | grep "13 - Commercial Code"
```

Should show: `ocr/output/13 - Commercial Code.txt`

### Check 3: .gitignore is Correct

```bash
cat .gitignore | grep chroma_db
cat .gitignore | grep processed_chunks
```

Should show both are excluded.

---

## Troubleshooting

### Problem: "OPENAI_API_KEY not found"

**Solution:**
1. Go to Streamlit Cloud dashboard
2. Click on your app → ⋮ (menu) → "Settings"
3. Go to "Secrets" tab
4. Add: `OPENAI_API_KEY = "sk-..."`
5. Click "Save"
6. App will automatically restart

### Problem: "Source documents directory not found"

**Solution:**
- The `ocr/output/` folder wasn't committed to Git
- Run: `git add ocr/output/*.txt`
- Commit: `git commit -m "Add legal document text files"`
- Push: `git push`

### Problem: "All documents labeled as Commercial Code"

**Solution:**
- This is fixed in the latest `doc_processor.py`
- Make sure you committed the updated version
- Pull latest changes and redeploy

### Problem: App is slow on first load

**Expected behavior:**
- First launch takes 5-10 minutes to build the vector database
- Progress bars will show processing status
- Subsequent loads are instant

### Problem: OpenAI API quota exceeded

**Solution:**
1. Check your OpenAI account: [platform.openai.com/usage](https://platform.openai.com/usage)
2. Add credits to your account
3. Wait for quota to reset
4. Redeploy the app (it will rebuild the database)

---

## Testing Before Deployment

Run these tests locally before deploying:

### Test 1: Check Document Diversity

```bash
python test_all_sources.py
```

Should show:
- ✅ 19 unique documents
- ✅ 2,304+ total chunks
- ✅ Commercial Code is only ~11-12% of chunks

### Test 2: Verify All Files Exist

```bash
ls ocr/output/*.txt | wc -l
```

Should show: **44**

### Test 3: Test Streamlit Locally

```bash
streamlit run main.py
```

Should:
- ✅ Show progress bars for processing
- ✅ Build vector database
- ✅ Launch search interface

---

## Post-Deployment Checklist

After deploying to Streamlit Cloud:

- [ ] App URL is working
- [ ] Progress bars appear on first load
- [ ] All 44 documents are being processed
- [ ] Vector database builds successfully
- [ ] Search functionality works
- [ ] Results show diverse document sources (not just Commercial Code)
- [ ] AI Overview generates properly

---

## Updating the App

To update your deployed app:

```bash
# Make changes to files
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will automatically detect the push and redeploy.

**Note:** If you delete `chroma_db/` on Streamlit Cloud (via settings), it will rebuild on next launch.

---

## Cost Considerations

### OpenAI API Costs:

- **Vector Database Build** (first time only):
  - ~2,304 chunks × 3,072 dimensions
  - Cost: ~$0.50-$1.00 for embeddings
  - **Only charged once** (database is cached)

- **Per Search Query:**
  - 1 embedding call per search
  - Cost: ~$0.0001 per search
  - AI Overview: ~$0.002-$0.005 per generation

- **Estimated Monthly Cost:** $5-$20 depending on usage

### Streamlit Cloud:

- **Free tier:**
  - 1 app
  - Unlimited public viewers
  - Community support

---

## Support & Resources

- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **OpenAI API Docs:** [platform.openai.com/docs](https://platform.openai.com/docs)
- **GitHub Help:** [docs.github.com](https://docs.github.com)

---

## Summary

Your Malta Legal RAG system is now configured for cloud deployment!

✅ All 44 legal documents are ready
✅ Document inference correctly identifies 19 unique laws
✅ Progress bars show processing status
✅ Automatic database building on first run
✅ Production-ready for Streamlit Cloud

Just commit to GitHub, deploy to Streamlit Cloud, add your OpenAI API key, and you're live! 🚀
