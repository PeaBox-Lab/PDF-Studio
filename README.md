# PeaBox PDF Studio v0.1.0

A local-first web PDF editor utility built with Python and Streamlit.

## Features
- Upload and preview PDF documents
- Merge multiple PDFs
- Split/extract page ranges such as `1-3,5,8`
- Add text to a selected page
- Add PNG/JPG images
- Add a drawn-looking signature image (PNG/JPG)
- Rotate selected pages
- Download the edited PDF

## Install
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown by Streamlit, normally http://localhost:8501.

## Notes
This MVP performs PDF page manipulation and overlays. It does not directly rewrite arbitrary existing paragraph text in a PDF. Scanned-document OCR and true content editing are future enhancements.
