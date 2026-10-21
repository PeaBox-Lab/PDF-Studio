# PeaBox PDF Studio Desktop v1.0.0

A Windows-friendly local desktop PDF editor. This is a clean break from the earlier browser UI.

## Why desktop
- Native scrolling, dialogs, menus, keyboard shortcuts, and high-DPI handling
- No local web server or browser zoom complications
- Explicit labeled tools instead of unexplained icons
- PDF page remains central
- Safer existing-text correction workflow

## Safe text editing
Double-click an existing text span. PeaBox removes only that exact rectangle and inserts a replacement that must fit the same area. If the replacement is too long, the operation is rejected instead of reflowing or damaging surrounding layout.

## Working features
- Native PDF viewing with thumbnails
- Fit Page and 100% zoom
- Existing-text correction by double-click
- Add new text by double-click in Add Text mode
- Add an image/signature
- Rotate and delete pages
- Merge PDFs
- Save As, reload original, keyboard shortcuts
- Unsaved-changes warning

## Run on Windows
Extract the ZIP and double-click `run_windows.bat`.

## Notes
This release intentionally prioritizes predictable correction of short text, names, dates, labels, and amounts. PDF is fixed-layout. It is not safe to offer Word-like paragraph reflow without reconstructing the page.
