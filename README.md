# PeaBox PDF Studio

> **Edit PDFs locally. Keep your documents private.**

PeaBox PDF Studio is a lightweight, local-first desktop PDF editor for viewing PDFs, correcting existing text, managing pages, adding content, and performing common PDF operations without uploading documents to an external service.

The project focuses on one principle:

> **PDF editing should be simple, predictable, private, and should not destroy the original document layout.**

PeaBox PDF Studio is built with Python, PySide6/Qt, PyMuPDF, and Pillow.

---

## Current Release

**Version:** `v1.0.1`

**Application type:** Desktop application

**Primary platform:** Windows

**License:** MIT

---

# Table of Contents

- [Why PeaBox PDF Studio](#why-peabox-pdf-studio)
- [Features](#features)
- [Text Editing](#text-editing)
- [How Text Replacement Works](#how-text-replacement-works)
- [Installation](#installation)
- [Windows Quick Start](#windows-quick-start)
- [Manual Installation](#manual-installation)
- [User Guide](#user-guide)
- [Opening a PDF](#opening-a-pdf)
- [Navigating Pages](#navigating-pages)
- [Editing Existing Text](#editing-existing-text)
- [Adding New Text](#adding-new-text)
- [Adding Images and Signatures](#adding-images-and-signatures)
- [Rotating Pages](#rotating-pages)
- [Deleting Pages](#deleting-pages)
- [Merging PDFs](#merging-pdfs)
- [Saving a PDF](#saving-a-pdf)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Privacy](#privacy)
- [Supported PDFs](#supported-pdfs)
- [Scanned PDFs](#scanned-pdfs)
- [Fonts](#fonts)
- [Known Limitations](#known-limitations)
- [Troubleshooting](#troubleshooting)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

# Why PeaBox PDF Studio?

Many online PDF tools require users to upload documents to a remote service.

That may not be appropriate for documents containing:

- HR information
- Employee data
- Contracts
- Financial information
- Internal business documents
- Customer information
- Personal records
- Confidential material

PeaBox PDF Studio follows a **local-first** model.

Your PDF is opened and processed on your computer.

No PeaBox account is required.

No browser-based PDF service is required.

No PeaBox cloud upload is required for normal editing operations.

---

# Features

## PDF Viewing

- Open local PDF files
- Native desktop application
- Page thumbnail navigation
- Scroll through large PDF pages
- Fit page to the application window
- View individual pages
- Current page indicator
- Total page count
- Native Windows controls

---

## Existing Text Correction

PeaBox PDF Studio can identify textual content already contained inside many digitally generated PDFs.

You can:

- Select existing text
- Double-click text to edit it
- Enter replacement text
- Preserve the detected font size
- Preserve the original text baseline
- Preserve the original text colour
- Approximate the original font characteristics
- Prevent automatic font shrinking

The editor is particularly useful for corrections such as:

```text
John Smith
