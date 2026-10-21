# PeaBox PDF Studio Desktop v1.3.0

A local-first native PDF editor and annotation workspace built with Python, PySide6 and PyMuPDF.

## v1.3 highlights

### Review and annotation tools
- Highlight detected PDF text
- Underline detected PDF text
- Strike out detected PDF text
- Permanently redact selected text
- Add a sticky-note comment to the current page
- Every annotation or redaction participates in Undo/Redo

### How to annotate
1. Open a PDF.
2. Choose **Highlight text**, **Underline text**, **Strike out text**, or **Permanently redact text**.
3. Hover over the exact text span.
4. Double-click the text.
5. Save the edited PDF with `Ctrl+Shift+S`.

Redaction is permanent after saving. PeaBox asks for confirmation and removes the selected text content instead of merely drawing a black rectangle over it.

## Existing features
- Existing-text correction without automatic font shrinking
- Add new text, images and signature images
- 20-step Undo/Redo
- Fit Page, 100%, Zoom In and Zoom Out
- Page thumbnails and drag-and-drop reordering
- Duplicate, extract, delete, rotate and insert pages
- Insert blank pages and complete PDFs
- Merge PDF files

## Installation

Extract the ZIP and double-click `run_windows.bat`.

Manual installation:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```
