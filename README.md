# PeaBox PDF Studio v0.4.0

A visual, local-first PDF editor with a FastAPI/PyMuPDF backend and a responsive browser workspace.

## What changed
v0.3 replaces form-driven coordinate entry with a direct-manipulation editor. Existing text blocks are detected automatically. Click a block to replace it, edit in place, move objects visually, and use a contextual property panel.

## Features
- Visual page canvas with zoom and navigation
- Click detected text to replace it
- In-place text editing with font size and colour
- Add draggable text boxes by double-clicking the page
- Add images and signature images visually
- Highlights and permanent black redactions
- Undo/redo before commit
- Commit edits and continue editing
- Download without committing
- Delete pages and reverse page order
- Merge PDFs
- Password-protected PDF opening
- Local temporary in-memory document handling

## Run on Windows
Double-click `run_windows.bat`, then open http://127.0.0.1:8000.

## Manual run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

## Important PDF reality
The editor replaces a selected text region by removing its PDF content and writing replacement text into the same rectangle. This is genuine region-level PDF editing, but PDF has no paragraph reflow model. Long replacement text must fit the original region or the user should enlarge the box.


## Windows launcher note
The v0.4.0 launcher deliberately starts Uvicorn with `python -m uvicorn` instead of relying on a `uvicorn.exe` command being present on Windows PATH. This supports locked-down/user-level Python installations where packages are installed under the user profile.

Alternative start command:
```bat
py -3 -m uvicorn app:app --host 127.0.0.1 --port 8000
```
