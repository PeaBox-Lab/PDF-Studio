# PeaBox PDF Studio Desktop v1.4.0

A local-first native PDF editor, page organizer, annotation workspace, and OCR-assisted PDF reader built with Python, PySide6 and PyMuPDF.

## New in v1.4

- Detects pages that appear to be image/scanned pages
- OCR Current Page command
- OCR word recognition through PyMuPDF's Tesseract integration
- Find text on native PDF pages
- Find text against OCR results on an OCR-processed page
- Visual orange search-result highlights
- OCR result caching per page during the current session
- `Ctrl+F` Find
- `Ctrl+Shift+O` OCR Current Page

## OCR requirement

PyMuPDF's integrated OCR uses Tesseract. Install Tesseract OCR separately on the computer. On Windows, make sure Tesseract's `tessdata` language-data directory is available to PyMuPDF. English uses the language code `eng`.

OCR is intentionally run page-by-page because OCR is substantially slower than native PDF text extraction. Once OCR has been completed for a page, PeaBox reuses that page's OCR context during the session.

## Using OCR

1. Open a scanned PDF.
2. Navigate to the scanned page.
3. Choose **OCR current page** or press `Ctrl+Shift+O`.
4. Enter the Tesseract language code, such as `eng`.
5. Wait for recognition to complete.
6. Press `Ctrl+F` and search the recognized text.

OCR recognition does not reconstruct the original fonts. It is primarily used for reading and search in v1.4. Direct OCR-text replacement remains a future workflow because blindly replacing text on an image scan would not remove the pixels of the original scanned text safely.

## Existing features

- Existing native-PDF text correction with preserved text size
- Highlight, underline and strikeout
- Permanent redaction
- Sticky-note comments
- Add new text, image and signature images
- 20-step Undo/Redo
- Zoom, Fit Page and 100%
- Drag-and-drop page reordering
- Extract, duplicate, insert, rotate and delete pages
- Merge PDFs
