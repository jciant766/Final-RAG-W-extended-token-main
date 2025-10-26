#!/usr/bin/env python3
"""
Process All Documents Script
Processes ALL legal documents and builds chunks for RAG system

Use this script when:
- Adding new documents
- Reprocessing existing documents  
- Rebuilding the chunk database
"""

import os
import json
from pathlib import Path
from doc_processor import DocumentProcessor
from debug_logger import DebugLogger

def main():
    """Process all legal documents"""
    debug = DebugLogger("process_all")
    processor = DocumentProcessor()
    
    print("=" * 70)
    print("PROCESSING ALL LEGAL DOCUMENTS")
    print("=" * 70)
    
    all_chunks = []
    documents_processed = []

    # Process ALL documents from OCR output directory
    print("\nProcessing all documents from ocr/output/")
    print("-" * 70)

    ocr_output_dir = Path("ocr/output")
    if not ocr_output_dir.exists():
        print(f"ERROR: Directory not found: {ocr_output_dir}")
        return

    text_files = sorted(ocr_output_dir.glob("*.txt"))
    total_files = len(text_files)
    print(f"Found {total_files} document files to process\n")

    for idx, text_file in enumerate(text_files, 1):
        try:
            print(f"[{idx}/{total_files}] Processing: {text_file.name}...", end=" ")
            result = processor.process_document(str(text_file))

            # Load chunks from the file that was just created
            with open('processed_chunks.json', 'r', encoding='utf-8') as f:
                chunks = json.load(f)

            all_chunks.extend(chunks)
            documents_processed.append({
                'file': text_file.name,
                'articles': result['total_articles'],
                'chunks': result['total_chunks'],
                'document': result['document']
            })
            print(f"OK - {result['total_articles']} articles, {result['total_chunks']} chunks")
        except Exception as e:
            print(f"ERROR: {e}")
            debug.log("error", f"Failed to process {text_file}: {e}")

    # Save all chunks to master file
    print("\n\nSaving All Chunks")
    print("-" * 70)
    
    # Remove duplicates by ID
    unique_chunks = {}
    for chunk in all_chunks:
        chunk_id = chunk['id']
        if chunk_id not in unique_chunks:
            unique_chunks[chunk_id] = chunk
    
    all_chunks = list(unique_chunks.values())
    
    with open('processed_chunks.json', 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Saved {len(all_chunks)} unique chunks to processed_chunks.json")
    
    # Step 4: Generate comprehensive report
    print("\n\nStep 4: Generating Processing Report")
    print("-" * 70)
    
    total_articles = sum(doc['articles'] for doc in documents_processed)
    total_chunks = len(all_chunks)
    
    report = {
        "total_documents": len(documents_processed),
        "total_articles": total_articles,
        "total_chunks": total_chunks,
        "documents": documents_processed
    }
    
    with open('processing_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Processing report saved to processing_report.json")
    
    # Final Summary
    print("\n\n" + "=" * 70)
    print("PROCESSING COMPLETE!")
    print("=" * 70)
    print(f"Documents Processed: {len(documents_processed)}")
    print(f"Total Articles: {total_articles}")
    print(f"Total Chunks: {total_chunks}")
    print("\nDocuments Breakdown:")
    
    for doc in documents_processed:
        print(f"  - {doc['document']}")
        print(f"    File: {doc['file']}")
        print(f"    Articles: {doc['articles']}, Chunks: {doc['chunks']}")
    
    print("\n[NEXT] Run 'streamlit run main.py' to rebuild vector database")
    print("=" * 70)
    
    return report

if __name__ == "__main__":
    main()


