# PeaBox PDF Studio Desktop v1.2.0

A local-first native PDF editor built with Python, PySide6 and PyMuPDF.

## Highlights

### Editing
- Correct existing text without automatic font shrinking
- Add new text
- Add images and signature images
- 20-step undo/redo
- Fit Page, 100%, zoom in/out

### Page workspace
- Page thumbnails
- Drag thumbnails to reorder pages
- Multi-select thumbnails with Ctrl/Shift
- Duplicate the current page
- Extract selected pages to a new PDF
- Insert a blank page after the current page
- Insert another PDF after the current page
- Rotate or delete pages
- Merge PDF files

## Installation

On Windows, extract the ZIP and double-click `run_windows.bat`.

Manual installation:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

## Page management guide

- **Reorder:** drag a page thumbnail to a new position.
- **Select several pages:** hold Ctrl while selecting thumbnails, or Shift for a range.
- **Extract:** select pages and choose `Extract selected pages`.
- **Duplicate:** navigate to a page and choose `Duplicate current page`.
- **Blank page:** inserts a same-size blank page directly after the current page.
- **Insert PDF:** appends every page of the selected PDF directly after the current page.

## Safe text editing

Existing-text replacement keeps the detected original font size. PeaBox rejects replacement text that cannot fit the original area rather than silently shrinking it or changing nearby layout.
