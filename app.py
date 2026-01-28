"""
Simple PDF Text Extraction Service
Deploy this to Railway, Render, or Fly.io for free PDF text extraction
"""

from flask import Flask, request, jsonify
import pdfplumber
import requests
from io import BytesIO
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'pdf-text-extraction'})


@app.route('/extract', methods=['POST'])
def extract_text():
    """
    Extract text from PDF
    
    Request body:
    {
        "url": "https://example.com/file.pdf",
        "pdf_url": "https://example.com/file.pdf"  // Alternative field name
    }
    
    Response:
    {
        "text": "Extracted text content...",
        "pages": 5
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'Missing request body'}), 400
        
        # Support both 'url' and 'pdf_url' field names
        pdf_url = data.get('url') or data.get('pdf_url')
        
        if not pdf_url:
            return jsonify({'error': 'Missing url or pdf_url field'}), 400
        
        logger.info(f"Extracting text from PDF: {pdf_url}")
        
        # Download PDF
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()
        
        # Validate it's a PDF
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type and not pdf_url.lower().endswith('.pdf'):
            logger.warning(f"Content type is {content_type}, but proceeding anyway")
        
        # Check PDF header
        if not response.content[:4].startswith(b'%PDF'):
            return jsonify({'error': 'File does not appear to be a valid PDF'}), 400
        
        # Extract text using pdfplumber
        text = ""
        pages = 0
        
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            pages = len(pdf.pages)
            logger.info(f"Processing {pages} pages")
            
            for i, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
                except Exception as e:
                    logger.warning(f"Error extracting text from page {i}: {e}")
                    continue
        
        if not text.strip():
            return jsonify({
                'error': 'No text could be extracted from PDF (might be image-based)',
                'pages': pages
            }), 400
        
        logger.info(f"Successfully extracted {len(text)} characters from {pages} pages")
        
        return jsonify({
            'text': text.strip(),
            'pages': pages,
            'characters': len(text)
        })
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading PDF: {e}")
        return jsonify({'error': f'Failed to download PDF: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return jsonify({'error': f'Extraction failed: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
