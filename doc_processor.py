import re
import tiktoken
import json
from typing import List, Dict, Any
from debug_logger import DebugLogger

class DocumentProcessor:
    def __init__(self):
        self.debug = DebugLogger("doc_processor")
        self.encoding = tiktoken.get_encoding("cl100k_base")
        # Increased to allow near-whole-article chunks and reduce splitting
        self.max_tokens = 3000
        # Maintain context continuity across chunks
        self.overlap_tokens = 200
        # Document-aware fields (set per processed file)
        self.citation_prefix = "Commercial Code (Cap. 13)"
        self.citation_label = "Art."
        self.id_label = "article"
        self.doc_code = "code_13"
        
        # Document overviews for context enrichment
        self.doc_overviews = {
            "code_13": "Commercial Code (Cap. 13): Malta's primary commercial law governing traders, acts of trade, bills of exchange, commercial transactions, bankruptcy, and commercial disputes.",
            "companies_act": "Companies Act (Cap. 386): Governs company formation, structure, governance, directors' duties, share capital, distributions, financial assistance, beneficial ownership, and company records in Malta.",
            "sl_386_02": "S.L. 386.02 (Companies Act - Private Companies Regulations): Rules for private limited liability companies including formation, registration, and operational requirements.",
            "sl_386_03": "S.L. 386.03 (Companies Act - Public Companies Regulations): Regulations governing public limited companies including listing, disclosure, and shareholder protections.",
            "sl_386_04": "S.L. 386.04 (Company Secretary Regulations): Requirements and duties of company secretaries, qualifications, and professional standards.",
            "sl_386_05": "S.L. 386.05 (Beneficial Ownership Regulations): Rules for maintaining and disclosing beneficial ownership registers for companies.",
            "sl_386_06": "S.L. 386.06 (Financial Assistance Regulations): Rules governing companies providing financial assistance for acquisition of their own shares.",
            "sl_386_07": "S.L. 386.07 (Distribution Rules): Regulations on dividend distributions, solvency tests, and capital maintenance requirements.",
            "sl_386_08": "S.L. 386.08 (Cell Companies Regulations): Rules for protected cell companies and incorporated cell companies structure and operations.",
            "sl_386_09": "S.L. 386.09 (Annual Return Regulations): Requirements for filing annual returns, financial statements, and related penalties.",
            "sl_386_10": "S.L. 386.10 (Accounting Records Regulations): Rules for maintaining proper accounting records, books, and financial documentation.",
            "sl_386_11": "S.L. 386.11 (Directors' Duties Regulations): Detailed rules on directors' fiduciary duties, conflicts of interest, and liability.",
            "sl_386_12": "S.L. 386.12 (Share Transfer Regulations): Procedures and requirements for transferring shares in companies.",
            "sl_386_13": "S.L. 386.13 (Debenture Regulations): Rules for issuing, registering, and managing debentures and company debt instruments.",
            "sl_386_14": "S.L. 386.14 (Company Name Regulations): Requirements and restrictions for company names, name changes, and registrations.",
            "sl_386_15": "S.L. 386.15 (Liquidation Regulations): Procedures for company winding up, liquidation, and creditor protections.",
            "sl_386_16": "S.L. 386.16 (Foreign Companies Regulations): Rules for foreign companies operating or establishing presence in Malta.",
            "sl_386_18": "S.L. 386.18 (European Company Regulations): Rules for Societas Europaea (SE) companies operating in Malta.",
            "sl_386_21": "S.L. 386.21 (Single Member Companies Regulations): Special rules for companies with single shareholders.",
            "sl_386_22": "S.L. 386.22 (Investment Services Companies Regulations): Specific regulations for companies providing investment services.",
            "sl_386_23": "S.L. 386.23 (Audit Requirements Regulations): Rules for company audits, auditor qualifications, and financial reporting.",
            "sl_386_24": "S.L. 386.24 (Insolvency Trading Regulations): Rules prohibiting and penalizing trading while insolvent.",
            "sl_595_27": "S.L. 595.27: Subsidiary legislation under Cap. 595 related to commercial or corporate matters."
        }
        self.doc_overview = ""
        
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process the Malta Commercial Code document"""
        self.debug.log("info", f"Processing document: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Infer document info from file path/name
            self._infer_document_info(file_path)
            
            # Pre-clean OCR artifacts before article extraction
            content = self._preclean_document_text(content)
            
            # Clean and extract articles
            articles = self._extract_articles(content)
            self.debug.log("info", f"Extracted {len(articles)} articles")
            
            # Process each article
            all_chunks = []
            for article in articles:
                chunks = self._create_chunks(article)
                all_chunks.extend(chunks)
            
            # Save processed chunks for indexing
            with open('processed_chunks.json', 'w', encoding='utf-8') as f:
                json.dump(all_chunks, f, ensure_ascii=False)

            # Save processing report
            report = {
                "total_articles": len(articles),
                "total_chunks": len(all_chunks),
                "articles_processed": [a['article'] for a in articles],
                "document": self.citation_prefix
            }
            
            with open('processing_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            self.debug.log("info", f"Document processing complete. Created {len(all_chunks)} chunks")
            return report
            
        except Exception as e:
            self.debug.log("error", f"Error processing document: {e}")
            raise
    
    def _preclean_document_text(self, content: str) -> str:
        """Heuristically remove OCR header/footers and stray page numbers.
        Targets patterns observed in Companies Act/Subsidiary Legislation OCR such as:
        - Page headers like "COMPANIES [CAP. 386] 11"
        - Standalone page numbers
        - Markdown heading artifacts (lines starting with '## ')
        - Isolated 'Cap. 386.' lines repeated between blocks
        - Hyphenation across line breaks
        
        IMPORTANT: Preserves page markers like "--- PAGE 1 ---" for proper page attribution.
        """
        text = content
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove markdown heading lines entirely
        text = re.sub(r"(?m)^\s*##\s+.*$", "", text)
        
        # Remove page headers like "COMPANIES [CAP. 386] 11" or similar
        # But be careful not to match our page markers "--- PAGE 1 ---"
        text = re.sub(r"(?m)^\s*[A-Z][A-Z\s\[\]\.\-]*CAP\.?\s*\d+\]?\s*\d+\s*$", "", text)
        
        # Remove isolated Cap. XXX. lines
        text = re.sub(r"(?m)^\s*Cap\.\s*\d+\.?\s*$", "", text)
        
        # Remove pure page number lines, but NOT our page markers
        # Only remove standalone digits, not "--- PAGE N ---" format
        text = re.sub(r"(?m)^\s*\d+\s*$", "", text)
        
        # De-hyphenate line-break splits: "exam-\nple" -> "example"
        # Only match word characters before the hyphen to avoid page markers
        text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
        
        # Collapse multiple blank lines
        text = re.sub(r"\n{2,}", "\n\n", text)
        
        return text

    def _extract_articles(self, content: str) -> List[Dict[str, Any]]:
        """Extract articles using regex over the whole document.
        Matches headings like "547." or "26A." and captures text until next heading or page marker.
        """
        # Precompute page positions from markers to estimate page per article
        page_marker_re = re.compile(r"---\s*PAGE\s*(\d+)\s*---", re.IGNORECASE)
        page_positions: List[Dict[str, int]] = []
        for pm in page_marker_re.finditer(content):
            try:
                page_no = int(pm.group(1))
            except Exception:
                continue
            page_positions.append({"start": pm.start(), "page": page_no})
        page_positions.sort(key=lambda x: x["start"])  # ascending by start index

        # Primary: heading at start of line. Allow dot followed by space OR newline.
        heading_block_re = re.compile(
            r"(?ms)^[\t \u00A0]*([0-9]{1,4}[A-Z]?)\s*\.(?:\s|$)(.*?)(?=^[\t \u00A0]*[0-9]{1,4}[A-Z]?\s*\.(?:\s|$)|^---\s*PAGE\s*\d+\s*---|\Z)"
        )
        # Fallback: anywhere in text, used if primary yields too few articles
        fallback_heading_re = re.compile(r"([0-9]{1,4}[A-Z]?)\s*\.")

        def page_for_index(idx: int) -> int:
            if not page_positions:
                return 1
            # Binary search for last page whose start <= idx
            lo, hi = 0, len(page_positions) - 1
            best = page_positions[0]["page"]
            while lo <= hi:
                mid = (lo + hi) // 2
                if page_positions[mid]["start"] <= idx:
                    best = page_positions[mid]["page"]
                    lo = mid + 1
                else:
                    hi = mid - 1
            return best

        def normalize_article_id(art: str) -> str:
            m = re.match(r"^(0*)(\d+)([A-Z]?)$", art)
            if not m:
                return art
            base = m.group(2)
            suffix = m.group(3)
            return f"{int(base)}{suffix}" if suffix else str(int(base))

        def article_numeric_value(art: str) -> float:
            # Convert like 26A -> 26.1, 26B -> 26.2 etc.
            norm = normalize_article_id(art)
            m = re.match(r"^(\d+)([A-Z]?)$", norm)
            if not m:
                return -1.0
            base = int(m.group(1))
            suffix = m.group(2)
            if not suffix:
                return float(base)
            offset = ord(suffix) - ord('A') + 1
            return float(base) + offset / 10.0

        MAX_ARTICLE = 550
        articles: List[Dict[str, Any]] = []
        prev_val = -1.0
        seen_ids = set()
        for m in heading_block_re.finditer(content):
            art_id = normalize_article_id(m.group(1))
            val = article_numeric_value(art_id)
            if val <= 0 or val > MAX_ARTICLE:
                continue
            if val <= prev_val + 1e-6:
                continue
            raw_text = m.group(2)
            cleaned_content = self._clean_content(raw_text)
            if not cleaned_content:
                continue
            if art_id in seen_ids:
                continue
            seen_ids.add(art_id)
            prev_val = val
            articles.append({
                'article': str(art_id),
                'content': cleaned_content,
                'page': page_for_index(m.start()),
                'position': len(articles) + 1
            })

        # Fallback segmentation if too few articles found
        if len(articles) < 500:
            candidates = list(fallback_heading_re.finditer(content))
            prev_val = prev_val
            for idx, m in enumerate(candidates):
                art_id = normalize_article_id(m.group(1))
                val = article_numeric_value(art_id)
                if val <= 0 or val > MAX_ARTICLE:
                    continue
                if val <= prev_val + 1e-6:
                    continue
                start_idx = m.end()
                # find end index at next valid candidate
                end_idx = len(content)
                for j in range(idx + 1, len(candidates)):
                    next_art = normalize_article_id(candidates[j].group(1))
                    next_val = article_numeric_value(next_art)
                    if next_val > val:
                        end_idx = candidates[j].start()
                        break
                raw_text = content[start_idx:end_idx]
                cleaned_content = self._clean_content(raw_text)
                if not cleaned_content:
                    continue
                if art_id in seen_ids:
                    continue
                seen_ids.add(art_id)
                prev_val = val
                articles.append({
                    'article': str(art_id),
                    'content': cleaned_content,
                    'page': page_for_index(m.start()),
                    'position': len(articles) + 1
                })

            # Sort by numeric article value to stabilize order
            articles.sort(key=lambda a: article_numeric_value(a['article']))

        return articles
    
    def _clean_content(self, content: str) -> str:
        """Clean article content"""
        # Remove page markers if any slipped through
        content = re.sub(r'---\s*PAGE\s*\d+\s*---', ' ', content, flags=re.IGNORECASE)
        # Collapse whitespace
        content = re.sub(r'\s+', ' ', content)
        return content.strip()
    
    def _create_chunks(self, article: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create token-aware chunks from article content"""
        content = article['content']
        tokens = self.encoding.encode(content)
        
        if len(tokens) <= self.max_tokens:
            # Article fits in one chunk
            chunk = self._create_chunk(article, content, 0, 1)
            return [chunk]
        
        # Split into multiple chunks
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(tokens):
            end = min(start + self.max_tokens, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            chunk = self._create_chunk(article, chunk_text, chunk_index, 
                                     (len(tokens) + self.max_tokens - 1) // self.max_tokens)
            chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.overlap_tokens
            chunk_index += 1
            
            # Prevent infinite loop
            if start >= len(tokens) - self.overlap_tokens:
                break
        
        return chunks
    
    def _create_chunk(self, article: Dict[str, Any], content: str, chunk_index: int, total_chunks: int) -> Dict[str, Any]:
        """Create a single chunk with metadata"""
        # Ensure globally unique and document-aware IDs
        chunk_id = (
            f"{self.doc_code}_{self.id_label}_{article['article']}"
            f"_p{article['page']}_pos{article['position']}_chunk_{chunk_index + 1}"
        )
        
        return {
            'id': chunk_id,
            'content': content,
            'metadata': {
                'article': str(article['article']),
                'page': article['page'],
                'position': article['position'],
                'chunk_index': chunk_index,
                'total_chunks': total_chunks,
                'tokens': len(self.encoding.encode(content)),
                'citation': f"{self.citation_prefix} {self.citation_label} {article['article']}",
                'document': self.citation_prefix,
                'id_label': self.id_label,
                'doc_code': self.doc_code,
                'doc_overview': self.doc_overview
            }
        }

    def _infer_document_info(self, file_path: str) -> None:
        """Infer document citation/title and id prefix from file name.
        Maps filenames to their correct Chapter numbers and document types.
        """
        try:
            import os
            import re as _re
            base = os.path.basename(file_path)
            stem = os.path.splitext(base)[0]
            stem_upper = stem.upper()

            # Extract chapter number pattern "XXX - " or "XXX." at start
            chapter_match = _re.match(r'^(\d+(?:\.\d+)?)\s*[-\.]?\s*(.+)', stem)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                doc_name = chapter_match.group(2).strip()

                # Map based on Chapter number
                doc_mapping = {
                    "12": ("Code of Organization and Civil Procedure (Cap. 12)", "code_12"),
                    "13": ("Commercial Code (Cap. 13)", "code_13"),
                    "16": ("Civil Code (Cap. 16)", "code_16"),
                    "55": ("Notarial Profession and Notarial Archives Act (Cap. 55)", "notarial_act"),
                    "56": ("Public Registry Act (Cap. 56)", "public_registry"),
                    "79": ("Commissioners for Oaths Ordinance (Cap. 79)", "commissioners_oaths"),
                    "123": ("Income Tax Act (Cap. 123)", "income_tax_act"),
                    "246": ("AIP Act (Cap. 246)", "aip_act"),
                    "296": ("Land Registration Act (Cap. 296)", "land_registration"),
                    "364": ("Duty on Documents and Transfers Act (Cap. 364)", "duty_act"),
                    "372": ("Income Tax Management Act (Cap. 372)", "income_tax_mgmt"),
                    "373": ("Prevention of Money Laundering Act (Cap. 373)", "money_laundering"),
                    "398": ("Condominium Act (Cap. 398)", "condominium_act"),
                    "540": ("Gender Identity, Gender Expression and Sex Characteristics Act (Cap. 540)", "gender_identity"),
                    "604": ("Private Residential Leases Act (Cap. 604)", "residential_leases"),
                    "614": ("Cohabitation Act (Cap. 614)", "cohabitation_act"),
                    "615": ("Real Estate Agents, Property Brokers and Property Consultants Act (Cap. 615)", "real_estate_agents"),
                    "623.01": ("EPC Regulations (S.L. 623.01)", "epc_regulations"),
                }

                # Check if chapter matches any known document (exact match or with sub-section)
                for chap, (title, code) in doc_mapping.items():
                    # Exact match or match with sub-section (e.g., "123.27" matches "123")
                    if chapter_num == chap or (chapter_num.startswith(chap + ".") and chap.isdigit()):
                        self.citation_prefix = title
                        self.citation_label = "Art." if "." not in chap or chapter_num.count(".") > 0 else "Art."
                        # Determine if it's a regulation (subsidiary legislation)
                        is_regulation = chapter_num.count(".") > 0
                        self.citation_label = "Reg." if is_regulation else "Art."
                        self.id_label = "regulation" if is_regulation else "article"
                        self.doc_code = code
                        self.doc_overview = self.doc_overviews.get(self.doc_code, "")
                        return

            # EU Regulation pattern
            if "EU" in stem_upper or "650.2012" in stem:
                self.citation_prefix = "EU Succession Regulation (650/2012)"
                self.citation_label = "Art."
                self.id_label = "article"
                self.doc_code = "eu_succession"
                self.doc_overview = self.doc_overviews.get(self.doc_code, "")
                return

            # Companies Act
            if "COMPANIES ACT" in stem_upper:
                self.citation_prefix = "Companies Act (Cap. 386)"
                self.citation_label = "Art."
                self.id_label = "article"
                self.doc_code = "companies_act"
                self.doc_overview = self.doc_overviews.get(self.doc_code, "")
                return

            # Subsidiary Legislation e.g. "SUBSIDIARY LEGISLATION 386 02"
            m = _re.search(r"SUBSIDIARY\s+LEGISLATION\s+(\d+)\s+(\d+)", stem_upper)
            if m:
                cap = int(m.group(1))
                sub = int(m.group(2))
                self.citation_prefix = f"S.L. {cap}.{sub:02d}"
                self.citation_label = "Reg."
                self.id_label = "regulation"
                self.doc_code = f"sl_{cap}_{sub:02d}"
                self.doc_overview = self.doc_overviews.get(self.doc_code, "")
                return

            # Fallback to Commercial Code
            self.citation_prefix = "Commercial Code (Cap. 13)"
            self.citation_label = "Art."
            self.id_label = "article"
            self.doc_code = "code_13"
            self.doc_overview = self.doc_overviews.get(self.doc_code, "")
        except Exception:
            # Keep existing defaults on failure
            pass