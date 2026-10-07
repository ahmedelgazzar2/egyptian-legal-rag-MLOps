#extract.py
from langchain_community.document_loaders import PyPDFLoader
from Egyptian_legal_rag.config.settings import settings 

import re
import json
import logging
from Egyptian_legal_rag.utils.logging_config import setup_logging


# logger

logger = logging.getLogger(__name__)

print("Logger level:", logger.level)
print("Effective level:", logger.getEffectiveLevel())

# Extract text from a PDF file

from pathlib import Path

def load_pdf(file_path):
    """Load a PDF file and return its pages."""

    try:
        file_path = Path(file_path)

        logger.info("🔄 Loading PDF: %s", file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"❌ PDF not found: {file_path}")

        loader = PyPDFLoader(str(file_path))
        pages = loader.load()

        if not pages:
            logger.warning("⚠️ PDF contains no pages: %s", file_path)
            return []

        logger.info("✅ PDF loaded successfully | pages=%d", len(pages))

        return pages

    except Exception:
        logger.exception("❌ Failed to load PDF: %s", file_path)
        raise



# Extract Articles from pages

## Extract English Articles

def extract_english_articles(full_text):
    """"Extract English articles from the full text of the PDF."""

    try:
        # search on english pattern
        en_pattern = r'Article\s+(\d+)\s*\n(.*?)(?=Article\s+\d+|$)'
        en_matches = re.findall(en_pattern, full_text, re.DOTALL)

        english_dict = {}

        for num, text in en_matches:
            article_num = int(num)
            if article_num not in english_dict:
                lines = text.split('\n')
                en_lines = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    # break if you get an arabic content
                    if re.search(r'[\u0600-\u06FF]', line):
                        break
                    en_lines.append(line)
                
                english_text = ' '.join(en_lines).strip()
                if english_text:
                    english_dict[article_num] = english_text
        if english_dict:
            logger.info("english articles extracted ✅ ")
            return english_dict
        logger.warning("can't extract english articles ⚠️")
    except Exception:
        logger.exception("failed extract English articles ❌")
        raise


## Extract Arabic Articles

def extract_arabic_articles(full_text) -> dict:
    """"Extract Arabic articles from the full text of the PDF."""

    try:
        ar_pattern = r'مادة\s*[\(（]?\s*([\d٠-٩]+)[\)）]?\s*[\(（]?\s*\n?(.*?)(?=مادة\s*[\(（]?[\d٠-٩]+|Article\s+\d+|$)'
        ar_matches = re.findall(ar_pattern, full_text, re.DOTALL)
        
        arabic_to_english = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
        
        arabic_dict = {}
        for num, text in ar_matches:
            article_num = int(num.translate(arabic_to_english))
            
            if article_num not in arabic_dict:
                lines = text.split('\n')
                ar_lines = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    # break if you get an english content
                    if not re.search(r'[\u0600-\u06FF]', line):
                        break
                    ar_lines.append(line)
                
                arabic_text = ' '.join(ar_lines).strip()
                if arabic_text:
                    arabic_dict[article_num] = arabic_text    

        if arabic_dict:
            logger.info("arabic articles extracted ✅ ")
            return arabic_dict
        logger.warning(" can't extract arabic articles ⚠️")
    except Exception:
        logger.exception("failed extract arabic articles ❌")
        raise


# addong metadatafor every article ( arabic & english )

def merge_articles(dict) -> list[dict]:
    
    try:
        articles = []


        for num in sorted(dict.keys()):
            text = dict.get(num, '')
            
            is_repealed = any(
                w in text 
                for w in ['ملغاة', 'ألغيت', 'Repealed', 'repealed']
            )
            
            articles.append({
                'article_number': num,
                'text':   text,
                'is_repealed':    is_repealed
            })

        if articles:
            logger.info("extract articles with metadata ✅")
            return articles
        logger.warning("can't articles with metadata ⚠️")
    except Exception:
       logger.exception("failed extract articles with metadata ❌")
       raise


    # Save Json file

def save_json(articles, output_path):
    """Save the articles to a JSON file."""
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ Saved {len(articles)} articles to {output_path}")
    except Exception:
        logger.exception("failed save json ❌")
        raise
    


if __name__ == "__main__":

    setup_logging()
    try:
        pages = load_pdf(settings.PDF_DIR)

        full_text = ''
        for page in pages:
            full_text += page.page_content + '\n'

        english_dict = extract_english_articles(full_text)
        arabic_dict = extract_arabic_articles(full_text)

        english_articles = merge_articles(english_dict)
        arabic_articles = merge_articles(arabic_dict)

        save_json(arabic_articles, settings.JSON_AR)
        save_json(english_articles, settings.JSON_EN)

    except:
        logger.error("❌ error, can't extract articles")