# Changelog

## v1.4.0
- Added scanned-page detection heuristic
- Added Tesseract-backed OCR for the current page through PyMuPDF
- Added per-page in-session OCR caching
- Added Find for native PDF text
- Added Find against OCR text on OCR-processed pages
- Added visual search highlights
- Added Ctrl+F and Ctrl+Shift+O shortcuts
- Kept OCR text read/search-only to avoid unsafe modification of scanned-image pixels

## v1.3.0
- Added highlight, underline, strikeout, comments and permanent redaction

## v1.2.0
- Added advanced page management

## v1.1.0
- Added Undo/Redo and zoom controls

## v1.0.1
- Preserved existing text size and rejected oversized replacements
