# PeaBox PDF Studio Desktop v1.1.0

A local-first native PDF editor built with Python, PySide6 and PyMuPDF.

## v1.1 highlights

- 20-step undo and redo for document changes
- Zoom In, Zoom Out, Fit Page and 100% controls
- Keyboard shortcuts for open, save, undo, redo and zoom
- Labeled tools for existing-text correction, new text, image/signature, rotate, delete and merge
- New-text dialog with font-size control
- Image/signature dialog with position and size controls
- Existing text continues to preserve its extracted size and baseline
- Page thumbnails refresh after edits
- Unsaved-change protection

## Installation

1. Install Python 3.11 or newer.
2. Extract the release ZIP.
3. Double-click `run_windows.bat`.

Manual installation:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

## Basic use

1. Open a PDF with `Ctrl+O`.
2. Double-click existing text to correct it.
3. Use the labeled left-side tools for new text, images, rotation, deletion or merging.
4. Use `Ctrl+Z` and `Ctrl+Y` to undo or redo.
5. Save a new copy with `Ctrl+Shift+S`.

## Safe text editing

PeaBox preserves the detected font size. It does not shrink replacement text automatically. If replacement text cannot fit in the original area, the edit is rejected rather than damaging the layout.
