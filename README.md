# PDF Text Extraction Service Setup

## Overview

This service extracts text from PDF files. It's used as the **first method** for PDF text extraction (fastest and free), with OCR as a fallback.

## Environment Variable

Set `PDF_TEXT_EXTRACTION_SERVICE_URL` to point to your PDF text extraction service.

## Quick Deploy

The service files are already in this directory:
- `app.py` - Flask service
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration

### Option 1: Railway (Recommended - Free Tier Available)

1. **Push to GitHub** (or use Railway's GitHub integration)
2. **Create new Railway project**
3. **Connect your GitHub repo**
4. **Set root directory** to `supabase/functions/_shared/pdf-text-extraction-service`
5. **Railway will auto-detect the Dockerfile**
6. **Get the public URL** (e.g., `https://pdf-extract-production.up.railway.app/extract`)
7. **Set environment variable** in Supabase: `PDF_TEXT_EXTRACTION_SERVICE_URL=https://your-railway-url.com/extract`

### Option 2: Render (Free Tier Available)

1. **Create new Web Service** on Render
2. **Connect GitHub repo**
3. **Select Docker** as the environment
4. **Set root directory** to `supabase/functions/_shared/pdf-text-extraction-service`
5. **Deploy** and get public URL
6. **Set environment variable** in Supabase: `PDF_TEXT_EXTRACTION_SERVICE_URL=https://your-render-url.onrender.com/extract`

### Option 3: Fly.io (Free Tier Available)

1. **Install Fly CLI**: `curl -L https://fly.io/install.sh | sh`
2. **Navigate to service directory**:
   ```bash
   cd supabase/functions/_shared/pdf-text-extraction-service
   ```
3. **Launch and deploy**:
   ```bash
   fly launch
   fly deploy
   ```
4. **Get public URL** from `fly status`
5. **Set environment variable** in Supabase: `PDF_TEXT_EXTRACTION_SERVICE_URL=https://your-app.fly.dev/extract`

## Configuration

### Set in Supabase Dashboard

1. Go to: **Supabase Dashboard** → **Project Settings** → **Edge Functions** → **Secrets**
2. Click **Add new secret**
3. Enter:
   - **Name**: `PDF_TEXT_EXTRACTION_SERVICE_URL`
   - **Value**: `https://your-service-url.com/extract`
4. Click **Save**

### Set via CLI

```bash
supabase secrets set PDF_TEXT_EXTRACTION_SERVICE_URL=https://your-service-url.com/extract
```

### For Local Development

Add to your `.env` file:

```bash
PDF_TEXT_EXTRACTION_SERVICE_URL=https://your-service-url.com/extract
```

## Service API Format

The service accepts POST requests with JSON body:

```json
{
  "url": "https://example.com/file.pdf",
  "pdf_url": "https://example.com/file.pdf"  // Alternative field name
}
```

And returns JSON:

```json
{
  "text": "Extracted text content...",
  "pages": 5,
  "characters": 1234
}
```

## Extraction Flow

1. **First**: Try PDF text extraction service (fast, free)
2. **If fails**: Try OCR API (works for image-based PDFs)
3. **If fails**: Try PDF extractor (pdfjs-dist, for text-based PDFs)
4. **If all fail**: Return empty string (prevents raw PDF bytes)

## Benefits

- ✅ **Fast**: Direct text extraction, no OCR overhead
- ✅ **Free**: Self-hosted on Railway/Render/Fly.io free tiers
- ✅ **Reliable**: Works for text-based PDFs
- ✅ **Fallback**: OCR still available for image-based PDFs

## Testing

Test the service locally:

```bash
cd supabase/functions/_shared/pdf-text-extraction-service
pip install -r requirements.txt
python app.py
```

Then test with curl:

```bash
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/sample.pdf"}'
```

## Troubleshooting

- Verify service is running (check Railway/Render dashboard)
- Ensure URL is accessible from Supabase
- Check service logs for errors
- Verify environment variable name: `PDF_TEXT_EXTRACTION_SERVICE_URL`
- Test health endpoint: `GET /health`
