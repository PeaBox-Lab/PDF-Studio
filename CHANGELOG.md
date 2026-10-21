# Changelog
## v0.4.2
- Replaced the remaining flex-height layout with a fixed viewport/grid workspace
- Center editor is now pinned between the 48px header and bottom of browser viewport
- PDF canvas gets the remaining viewport height directly, eliminating the large blank area above the page
- Initial page fit now considers BOTH available width and height
- Forced center canvas overflow scrolling independent of body/document scrolling
- Added double-animation-frame layout measurement before PDF rendering
- Added responsive compact sidebars for narrow effective viewports

## v0.4.1
- Reworked layout around the actual browser viewport, including reduced-height/zoomed browser sessions
- Added persistent visible horizontal and vertical document scrollbars
- PDF now auto-fits to the available center workspace on load and browser resize
- Reduced left and right panels, top header, tool spacing, and upload empty-state footprint
- Document starts at the top of the canvas instead of below an oversized empty area
- Tightened existing-text replacement region and editor chrome
- Added responsive widths for narrower effective viewport sizes

## v0.4.0
- Fixed PDF workspace viewport: document now scrolls inside the editor instead of loading below an inaccessible viewport
- Text detection upgraded from coarse blocks to individual PDF text spans
- Existing-text editing now preserves detected size/color and marks replacement edits separately from new text overlays
- Replacement applies redaction first, then writes fitted replacement text into the cleared region
- Added automatic font-size reduction when replacement text needs to fit
- Added explicit Existing PDF text vs New overlay UX guidance

## v0.3.2
- Fixed Windows startup when Uvicorn is installed in user site-packages but its executable is not on PATH
- Launcher now uses `py -3 -m uvicorn` / `python -m uvicorn`
- Removed dependency on virtual-environment activation succeeding
- Added delayed browser launch so Firefox does not open before the local server is listening
- Added clearer launcher diagnostics and `start.py` fallback

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
