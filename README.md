# PeaBox PDF Studio

> **Edit, organize, annotate, protect, and manage PDFs locally.**

PeaBox PDF Studio is a local-first desktop PDF toolkit designed for everyday document editing and management without requiring users to upload documents to an online PDF service.

It combines PDF viewing, focused text correction, page management, annotations, OCR-assisted search, document metadata, watermarks, headers and footers, page numbering, and encrypted PDF export in a native desktop application.

**Current release:** `v1.5.0`

---

## Table of Contents

- [Why PeaBox PDF Studio?](#why-peabox-pdf-studio)
- [Core Principles](#core-principles)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [User Guide](#user-guide)
- [Editing Existing Text](#editing-existing-text)
- [Working with Pages](#working-with-pages)
- [Annotations and Redaction](#annotations-and-redaction)
- [OCR and Scanned PDFs](#ocr-and-scanned-pdfs)
- [Document Properties](#document-properties)
- [Watermarks](#watermarks)
- [Headers and Footers](#headers-and-footers)
- [Page Numbers](#page-numbers)
- [PDF Password Protection](#pdf-password-protection)
- [Saving Documents](#saving-documents)
- [Recommended Workflow](#recommended-workflow)
- [Privacy and Security](#privacy-and-security)
- [Known Limitations](#known-limitations)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Packaging and Deployment](#packaging-and-deployment)
- [Roadmap](#roadmap)
- [Version History](#version-history)
- [Contributing](#contributing)
- [License](#license)

---

# Why PeaBox PDF Studio?

PDF documents are everywhere.

Organizations use PDFs for:

- Contracts
- HR documents
- Employee records
- Policies
- Invoices
- Statements
- Approval forms
- Reports
- Certificates
- Application forms
- Financial documents
- Internal documentation

Making even a small correction can sometimes require an expensive commercial PDF editor or uploading the document to an online service.

You might only need to:

```text
Correct a name
Change a date
Fix an amount
Highlight a paragraph
Remove confidential information
Add a signature
Insert page numbers
Delete a page
Combine multiple PDFs
Password-protect a document
```

PeaBox PDF Studio is designed specifically around those practical workflows.

The goal is simple:

> **Open. Edit. Organize. Protect. Save. Done.**

---

# Core Principles

## Local First

Normal PDF processing happens on your computer.

PeaBox PDF Studio does not require a PeaBox cloud account or an external document-processing API for normal operation.

This makes local processing particularly useful for documents containing:

- Employee information
- Customer information
- Contracts
- Financial information
- Internal business documents
- Personal information
- Confidential records

---

## Understandable

Tools should explain what they do.

PeaBox prefers labels such as:

```text
Edit existing text
Add new text
Add image or signature
Highlight text
Permanently redact text
Rotate page
Delete page
Add watermark
Create protected copy
```

rather than relying entirely on unexplained icons.

---

## Conservative

PDF is a fixed-layout format.

PeaBox avoids making unpredictable changes simply to complete an edit.

For example, PeaBox does not automatically shrink replacement text until it fits an existing area.

If an edit cannot be completed safely, PeaBox should report the problem instead.

---

## Private

Documents should remain local whenever practical.

Cloud functionality, if introduced in future releases, should remain optional.

---

## Open

The codebase is intended to remain understandable and extensible.

Developers should be able to inspect, modify, test, package, and extend the application.

---

# Features

PeaBox PDF Studio v1.5.0 includes functionality across six major areas.

## PDF Editing

- Open PDF documents
- Correct existing PDF text
- Preserve detected text size
- Preserve text baseline
- Preserve text colour
- Add new text
- Add images
- Add signature images

## PDF Viewing

- Native desktop PDF viewer
- Page rendering
- Thumbnail navigation
- Fit Page
- 100% viewing
- Zoom controls
- Native scrolling
- Page navigation

## Page Management

- Drag-and-drop page reordering
- Duplicate pages
- Extract selected pages
- Insert blank pages
- Insert another PDF
- Rotate pages
- Delete pages
- Merge PDF documents

## Review and Annotation

- Highlight text
- Underline text
- Strike out text
- Add comments
- Permanent redaction
- Undo and redo

## OCR

- Detect pages likely to require OCR
- Run OCR on scanned pages
- Search OCR-recognized text
- Search regular PDF text
- Highlight search results

## Document Tools

- PDF metadata editor
- Watermarks
- Headers
- Footers
- Page numbering
- AES-256 protected copies
- Owner password
- Optional document-open password
- PDF printing/copying permission controls

---

# Technology Stack

PeaBox PDF Studio uses a native Python desktop architecture.

| Component | Technology |
|---|---|
| Programming language | Python |
| Desktop UI | PySide6 / Qt |
| PDF processing | PyMuPDF |
| OCR | Tesseract through PyMuPDF |
| Image processing | Pillow where required |
| Automated tests | pytest |
| Platform focus | Windows |

The desktop edition does not require a browser or local web server.

---

# System Requirements

## Recommended

```text
Operating System: Windows 10 or Windows 11
Architecture:     64-bit
Python:           3.11 or newer
RAM:              4 GB minimum
                  8 GB recommended
Disk:             Approximately 1 GB available
```

Large PDFs containing high-resolution scans may require more memory.

---

# Installation

## Option 1: Quick Windows Installation

This is the easiest installation method.

### Step 1: Download

Download:

```text
PeaBox_PDF_Studio_Desktop_v1.5.0.zip
```

### Step 2: Extract

Extract the ZIP into a normal directory.

For example:

```text
C:\PeaBox\PDFStudio\
```

Do not run the application directly from inside the ZIP archive.

### Step 3: Start

Double-click:

```text
run_windows.bat
```

The launcher installs the required Python packages and starts PeaBox PDF Studio.

The first launch may take longer because dependencies need to be installed.

---

# Manual Installation

For developers and advanced users, a Python virtual environment is recommended.

## Step 1: Open the project directory

```bat
cd C:\path\to\peabox-pdf-studio
```

## Step 2: Create a virtual environment

```bat
python -m venv .venv
```

## Step 3: Activate the environment

Command Prompt:

```bat
.venv\Scripts\activate
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Step 4: Upgrade pip

```bat
python -m pip install --upgrade pip
```

## Step 5: Install requirements

```bat
python -m pip install -r requirements.txt
```

## Step 6: Start PeaBox

```bat
python app.py
```

---

# Running the Application

After installation:

```bat
python app.py
```

or simply run:

```text
run_windows.bat
```

PeaBox opens as a native desktop window.

---

# User Guide

## Opening a PDF

Choose:

**Open PDF**

Select a `.pdf` file.

The document is loaded into the local PDF workspace.

Always keep a copy of important source documents before editing.

---

# Editing Existing Text

PDF text editing is fundamentally different from editing text in Microsoft Word.

PDF normally stores text at fixed coordinates.

A simplified PDF instruction could effectively mean:

```text
Draw "Business Owner"
at X = 240
at Y = 320
using font size 11
```

There may be no concept of a flowing paragraph.

PeaBox therefore uses a conservative editing strategy.

## Editing Workflow

1. Choose **Edit existing text**.
2. Navigate to the required page.
3. Move the pointer over the text.
4. PeaBox identifies editable text regions.
5. Double-click the required text.
6. Enter replacement text.
7. Confirm the edit.
8. Review the result.

---

## Good Existing-Text Edits

```text
2025 → 2026
```

```text
Draft → Final
```

```text
Pending → Approved
```

```text
John Smith → John Smyth
```

```text
$1,500 → $1,750
```

---

## Font Size Preservation

PeaBox does not automatically reduce existing text size simply to make a replacement fit.

If the original text is approximately:

```text
11 pt
```

PeaBox attempts to keep it:

```text
11 pt
```

If the replacement cannot fit safely, the application rejects the edit.

This prevents situations where one edited field suddenly appears much smaller than surrounding text.

---

## Long Replacement Text

Avoid replacing:

```text
Owner
```

with:

```text
Senior Global Business Application Operations Owner
```

inside the same small PDF text area.

Use shorter wording, move new content elsewhere, or modify the original source document.

---

# Adding New Text

Use **Add new text** when the information does not already exist in the PDF.

Typical examples:

```text
APPROVED
```

```text
Reviewed
```

```text
Reference: HR-2026-114
```

```text
31-Jan-2026
```

Adding new text and correcting existing text are intentionally separate workflows.

---

# Adding Images and Signatures

PeaBox supports adding images such as:

```text
PNG
JPG
JPEG
```

Use cases include:

- Signature
- Logo
- Stamp
- Photograph
- Screenshot
- QR code

## Signature Recommendation

Use:

```text
PNG
Transparent background
Minimal empty margins
```

for the cleanest result.

Adding a signature image is not the same as creating a certificate-backed digital signature.

---

# Working with Pages

## Reorder Pages

Drag page thumbnails into a new order.

Example:

```text
1
2
3
4
```

can become:

```text
1
3
2
4
```

---

## Duplicate a Page

Select the required page and choose:

**Duplicate current page**

A duplicate is inserted into the document.

---

## Extract Pages

Select one or more page thumbnails.

Use `Ctrl` to select individual pages.

Use `Shift` to select a range.

Choose:

**Extract selected pages**

Save the extracted pages as a separate PDF.

---

## Insert a Blank Page

Choose:

**Insert blank page**

A new blank page is inserted after the current page.

---

## Insert Another PDF

Choose:

**Insert PDF after page**

Select another PDF.

Its pages are inserted after the current page.

---

## Rotate

Select the page and choose:

**Rotate current page**

The page rotates in 90-degree increments.

---

## Delete

Select the page and choose:

**Delete current page**

PeaBox prevents deleting every page from the document.

---

# Merge PDFs

Choose:

**Merge PDF files**

Select the PDFs.

For example:

```text
Cover.pdf
Contract.pdf
Appendix.pdf
```

becomes:

```text
Complete-Contract.pdf
```

---

# Annotations and Redaction

## Highlight

Choose:

**Highlight text**

Double-click the required text.

A PDF highlight annotation is created.

---

## Underline

Choose:

**Underline text**

Double-click the text.

---

## Strikeout

Choose:

**Strike out text**

Double-click the text.

---

## Comments

Choose:

**Add comment to page**

Enter the comment.

PeaBox creates a PDF comment annotation.

---

# Permanent Redaction

Choose:

**Permanently redact text**

Select the required text.

PeaBox asks for confirmation.

After confirmation, the selected text is removed and a redaction area is applied.

## Important

Redaction should be treated as permanent after the document is saved.

Always retain an original document before performing redactions.

---

# Undo and Redo

PeaBox supports edit history for supported document modifications.

Keyboard shortcuts:

```text
Ctrl + Z    Undo
Ctrl + Y    Redo
```

The current architecture uses in-memory PDF snapshots for edit history.

---

# Zoom

Supported controls include:

```text
Zoom In
Zoom Out
Fit Page
100%
```

Common shortcuts:

```text
Ctrl + +
Ctrl + -
Ctrl + 0
Ctrl + 1
```

---

# OCR and Scanned PDFs

A scanned PDF may contain only images.

Conceptually:

```text
Paper
  ↓
Scanner
  ↓
Image
  ↓
PDF
```

The page looks like text to a human, but there may be no actual PDF text objects.

OCR is therefore required.

---

## OCR Current Page

Navigate to the page.

Choose:

**OCR current page**

or use:

```text
Ctrl + Shift + O
```

Enter the Tesseract language code.

English:

```text
eng
```

PeaBox runs OCR on the current page.

---

# Tesseract Requirement

OCR requires a separate Tesseract installation.

Tesseract language data must also be available.

Common language codes include:

```text
eng    English
deu    German
fra    French
spa    Spanish
```

Install the relevant language packages when additional languages are required.

---

# OCR Search

After running OCR:

```text
Ctrl + F
```

Enter the text.

PeaBox searches the OCR-generated text representation.

Matches are visually highlighted.

---

# OCR Editing Limitation

v1.5 intentionally does not treat OCR text like ordinary PDF text for replacement.

A scanned page still contains pixels representing the original words.

Simply inserting new text would leave the original scanned text underneath.

Safe scanned-text correction therefore requires image-region cleanup or reconstruction.

That workflow is planned for a later version.

---

# Find Text

Use:

```text
Ctrl + F
```

PeaBox can search:

- Native PDF text
- OCR-recognized page text after OCR processing

Search results are highlighted visually.

---

# Document Properties

v1.5 introduces PDF metadata editing.

Choose:

**Document properties**

You can edit:

```text
Title
Author
Subject
Keywords
```

The dialog also provides basic information about the document.

Metadata can be useful for:

- Search
- Document management
- Archiving
- Classification
- Knowledge management

---

# Watermarks

Choose:

**Add watermark**

Enter text such as:

```text
CONFIDENTIAL
```

```text
DRAFT
```

```text
INTERNAL USE ONLY
```

The watermark is placed across PDF pages using low-opacity text.

Watermarks modify document content.

Use Undo if a watermark was applied incorrectly before saving.

---

# Headers and Footers

Choose:

**Header and footer**

Enter content such as:

```text
PeaBox Labs
```

or:

```text
Confidential
```

PeaBox applies the header/footer consistently across the document.

---

# Page Numbers

Choose:

**Add page numbers**

Enter a prefix.

Example:

```text
Page 
```

Choose a starting number.

Example:

```text
1
```

The result becomes:

```text
Page 1
Page 2
Page 3
...
```

You can also use a custom prefix:

```text
Appendix -
```

to create:

```text
Appendix -1
Appendix -2
Appendix -3
```

---

# PDF Password Protection

v1.5 can create an AES-256 encrypted copy.

Choose:

**Create protected copy**

Enter:

### Owner Password

Required.

This controls document ownership/security settings.

### Open Password

Optional.

If specified, users must enter the password to open the PDF.

Example:

```text
Owner password:
StrongAdministrationPassword

Open password:
DocumentAccess2026
```

Then select the output PDF.

---

## PDF Permissions

Protected PDFs can also contain permission preferences such as:

- Allow printing
- Allow copying

Important:

> PDF permission flags depend on PDF reader software honoring them.

Password encryption should be considered the stronger security boundary.

---

# Saving Documents

Use **Save As** rather than overwriting important originals.

Recommended:

```text
Original:
Employment-Contract.pdf

Edited:
Employment-Contract-edited.pdf
```

---

# Recommended Workflow

For important documents:

```text
Open original PDF
        ↓
Make small edits
        ↓
Review affected pages
        ↓
Apply annotations if needed
        ↓
Apply document tools
        ↓
Save As a new file
        ↓
Close PeaBox
        ↓
Open saved PDF again
        ↓
Review entire document
        ↓
Distribute final copy
```

---

# Privacy and Security

PeaBox PDF Studio follows a local-first processing model.

Normal operations do not require:

```text
Cloud PDF processing
PeaBox account
Remote conversion API
Browser upload
External document storage
```

This can make the tool suitable for environments working with:

- Employee documents
- HR records
- Contracts
- Internal documentation
- Business reports
- Personal documents

Users remain responsible for:

- Windows security
- Disk encryption
- Endpoint protection
- File permissions
- Backups
- Secure distribution
- Document-retention policies

---

# Known Limitations

## Existing Text

- PDF paragraphs do not automatically reflow
- Replacement must fit the original area
- Exact embedded fonts cannot always be reused
- Text converted to outlines is not editable as normal text

## Scanned PDFs

- OCR supports reading/search
- OCR-text replacement is not yet supported
- Exact scan reconstruction is not yet supported

## Signatures

Current signatures are image-based.

Certificate-backed digital signatures are not yet implemented.

## Visual Editing

Advanced visual drag/resize controls for added images and text remain planned.

## Forms

Advanced PDF form creation/editing remains planned.

---

# Troubleshooting

## Application Does Not Start

Run:

```bat
py --version
```

Then:

```bat
py -3 -m pip install -r requirements.txt
```

Launch manually:

```bat
py -3 app.py
```

---

## PySide6 Missing

```text
ModuleNotFoundError: No module named 'PySide6'
```

Fix:

```bat
py -3 -m pip install PySide6
```

---

## PyMuPDF Missing

```text
ModuleNotFoundError: No module named 'pymupdf'
```

Fix:

```bat
py -3 -m pip install PyMuPDF
```

---

## Existing Text Cannot Be Selected

Possible causes:

- Scanned PDF
- Image-only PDF
- Text converted to vector paths
- Unsupported text encoding
- Unusual PDF structure

Try OCR if the page appears scanned.

---

## Text Replacement Is Rejected

The replacement is probably wider than the original region.

This is intentional.

Use shorter wording instead of forcing PeaBox to change the font size.

---

## OCR Fails

Verify Tesseract is installed.

Also ensure the required Tesseract language data exists.

---

# Project Structure

```text
peabox-pdf-studio/
│
├── app.py
├── pdf_engine.py
├── requirements.txt
├── run_windows.bat
│
├── README.md
├── CHANGELOG.md
├── ROADMAP.md
├── LICENSE
│
└── tests/
    └── test_engine.py
```

---

# Development Setup

Clone:

```bash
git clone https://github.com/PeaBox-Labs/peabox-pdf-studio.git
```

Enter directory:

```bash
cd peabox-pdf-studio
```

Create environment:

```bash
python -m venv .venv
```

Activate:

```bat
.venv\Scripts\activate
```

Install:

```bash
python -m pip install -r requirements.txt
```

Run:

```bash
python app.py
```

---

# Testing

Run:

```bash
pytest -q
```

Tests should be added whenever editing-engine behaviour changes.

Important regression areas include:

- Text size preservation
- Page operations
- Redaction
- Encryption
- Metadata
- Watermarks
- Page numbering
- OCR-related detection/search

---

# Packaging and Deployment

## Source Distribution

The simplest distribution mechanism is the release ZIP:

```text
PeaBox_PDF_Studio_Desktop_v1.5.0.zip
```

The user extracts it and runs:

```text
run_windows.bat
```

---

## Recommended Future Windows Packaging

For wider distribution, package PeaBox into a standalone Windows executable using PyInstaller.

Example development command:

```bat
python -m pip install pyinstaller
```

Then:

```bat
pyinstaller --noconsole --name "PeaBox PDF Studio" app.py
```

A future production build should additionally include:

- Application icon
- Version metadata
- Installer
- Start Menu shortcut
- File association
- Code signing
- Upgrade/uninstall support

An installer can subsequently be produced using tools such as Inno Setup or WiX.

---

# Roadmap

## v1.6 - Visual Editing

Planned:

- Drag images directly on the PDF
- Resize handles
- Move newly inserted text
- Move signatures
- Freehand drawing
- Lines
- Arrows
- Shapes

## v1.7 - Advanced OCR Editing

Planned:

- OCR-assisted scanned text correction
- Safe image-region cleanup
- Scan-aware reconstruction
- Better OCR language support

## v1.8 - PDF Management

Planned:

- PDF compression
- Optimization profiles
- Attachment management
- Bookmark management
- Table-of-contents editing

## v2.x

Potential longer-term areas:

- Advanced layout-aware editing
- Form creation
- Certificate-backed digital signatures
- PDF comparison
- Batch document processing
- Better embedded-font reconstruction

---

# Version History

## v1.5.0

- Document metadata editor
- Watermarks
- Headers and footers
- Page numbering
- AES-256 protected-copy export
- Password protection

## v1.4.0

- OCR-assisted reading
- OCR search
- Scanned-page detection
- Search-result highlighting

## v1.3.0

- Highlight
- Underline
- Strikeout
- Comments
- Permanent redaction

## v1.2.0

- Drag-and-drop page ordering
- Page extraction
- pull request
```

Example:

```bash
git checkout -b feature/visual-image-resize
```

---

# Reporting Bugs

Please include:

```text
PeaBox version
Windows version
Python version
PDF type
Operation performed
Expected result
Actual result
Error message
Steps to reproduce
```

Never publish confidential documents in a public issue.

Create a synthetic PDF reproducing the problem whenever possible.

---

# License

PeaBox PDF Studio is released under the MIT License.

See:

```text
LICENSE
```

for the complete license terms.

---

# PeaBox Labs

PeaBox PDF Studio is part of the PeaBox ecosystem of practical software and experimentation projects.

The project focuses on making everyday PDF operations understandable, private, and accessible without forcing users into a cloud-first workflow.

---

## Final Philosophy

PeaBox PDF Studio is not trying to win through the largest possible number of buttons.

It is trying to make common PDF tasks understandable:

> **Open. Edit. Organize. Review. Protect. Save. Done.**
