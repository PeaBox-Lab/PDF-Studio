# PeaBox PDF Studio v0.2.0

A functional local-first web PDF editor built with Python, Streamlit, and PyMuPDF.

## Working features
- Open normal and password-protected PDFs
- Full-page preview and navigation
- Cumulative editing with 20-step undo/redo
- Add text with position, size, and colour
- Upload and place images or signature files
- Draw a signature in the browser and place it on a page
- Rotate, delete, extract, and reorder pages
- Append PDFs to the active document
- Standalone multi-file merge
- Add watermarks to selected pages
- Edit title, author, subject, and keywords
- Create AES-256 password-protected copies
- Download the current edited PDF

## Windows quick start
1. Install Python 3.11 or 3.12.
2. Extract this ZIP.
3. Double-click `run_windows.bat`.

## Manual start
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Tests
```bash
pytest -q
```

## Editing scope
PDF is a fixed-layout format. This release provides reliable overlays and page-level editing. It does not reconstruct and reflow existing paragraphs like Microsoft Word. OCR, redaction, annotations, page thumbnails, and direct selection tools are planned next.
