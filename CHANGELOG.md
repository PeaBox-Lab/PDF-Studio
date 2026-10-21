# Changelog
## v0.3.1
- Fixed Organize Pages modal appearing permanently on startup
- Added X, backdrop-click, and Escape-key modal closing
- Prevented page organizer from opening before a PDF is loaded
- Migrated legacy `fitz` imports to current `pymupdf` imports
- Added cache-busting for corrected frontend assets

## v0.3.0
- Replaced Streamlit UI with a purpose-built visual editor
- Added automatic text-block detection and click-to-edit
- Added in-place text objects, drag positioning, contextual properties, zoom, and visual overlays
- Added images, signatures, highlighting, redaction, page organization, merge, undo/redo, commit, and export
- Added FastAPI API and automated engine tests
## v0.2.0
- Functional PyMuPDF/Streamlit editor and page utilities
## v0.1.0
- Initial prototype
