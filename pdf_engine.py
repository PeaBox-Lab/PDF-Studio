from __future__ import annotations
import io
from dataclasses import dataclass
from typing import Iterable
import fitz
from PIL import Image


def parse_page_range(spec: str, page_count: int) -> list[int]:
    """Return unique zero-based page indexes from a human range such as 1-3,5."""
    if page_count < 1:
        return []
    result: list[int] = []
    seen = set()
    for raw in (spec or "").replace(" ", "").split(","):
        if not raw:
            continue
        if "-" in raw:
            parts = raw.split("-")
            if len(parts) != 2 or not all(p.isdigit() for p in parts):
                raise ValueError(f"Invalid range: {raw}")
            start, end = map(int, parts)
            if start > end:
                raise ValueError(f"Range starts after it ends: {raw}")
            numbers = range(start, end + 1)
        else:
            if not raw.isdigit():
                raise ValueError(f"Invalid page: {raw}")
            numbers = [int(raw)]
        for number in numbers:
            if number < 1 or number > page_count:
                raise ValueError(f"Page {number} is outside 1-{page_count}")
            idx = number - 1
            if idx not in seen:
                seen.add(idx)
                result.append(idx)
    if not result:
        raise ValueError("Select at least one page")
    return result


def open_pdf(data: bytes, password: str = "") -> fitz.Document:
    doc = fitz.open(stream=data, filetype="pdf")
    if doc.needs_pass:
        if not password or not doc.authenticate(password):
            doc.close()
            raise ValueError("A valid PDF password is required")
    return doc


def save_pdf(doc: fitz.Document) -> bytes:
    return doc.tobytes(garbage=4, deflate=True, clean=True)


def render_page(data: bytes, page_index: int, zoom: float = 1.25, password: str = "") -> bytes:
    doc = open_pdf(data, password)
    try:
        if not 0 <= page_index < doc.page_count:
            raise ValueError("Page index is invalid")
        pix = doc[page_index].get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        return pix.tobytes("png")
    finally:
        doc.close()


def merge_pdfs(items: Iterable[tuple[bytes, str]]) -> bytes:
    out = fitz.open()
    try:
        for data, password in items:
            src = open_pdf(data, password)
            try:
                out.insert_pdf(src)
            finally:
                src.close()
        if out.page_count == 0:
            raise ValueError("No pages were available to merge")
        return save_pdf(out)
    finally:
        out.close()


def extract_pages(data: bytes, indexes: list[int], password: str = "") -> bytes:
    src = open_pdf(data, password)
    out = fitz.open()
    try:
        for idx in indexes:
            out.insert_pdf(src, from_page=idx, to_page=idx)
        return save_pdf(out)
    finally:
        src.close(); out.close()


def delete_pages(data: bytes, indexes: list[int], password: str = "") -> bytes:
    doc = open_pdf(data, password)
    try:
        if len(set(indexes)) >= doc.page_count:
            raise ValueError("A PDF must retain at least one page")
        for idx in sorted(set(indexes), reverse=True):
            doc.delete_page(idx)
        return save_pdf(doc)
    finally:
        doc.close()


def reorder_pages(data: bytes, order: list[int], password: str = "") -> bytes:
    src = open_pdf(data, password)
    out = fitz.open()
    try:
        if sorted(order) != list(range(src.page_count)):
            raise ValueError("Order must contain every page exactly once")
        for idx in order:
            out.insert_pdf(src, from_page=idx, to_page=idx)
        return save_pdf(out)
    finally:
        src.close(); out.close()


def rotate_pages(data: bytes, indexes: list[int], degrees: int, password: str = "") -> bytes:
    if degrees not in (90, 180, 270):
        raise ValueError("Rotation must be 90, 180, or 270 degrees")
    doc = open_pdf(data, password)
    try:
        for idx in indexes:
            page = doc[idx]
            page.set_rotation((page.rotation + degrees) % 360)
        return save_pdf(doc)
    finally:
        doc.close()


def add_text(data: bytes, page_idx: int, text: str, x: float, y: float, size: float,
             color: tuple[float, float, float], font: str = "helv", password: str = "") -> bytes:
    if not text.strip():
        raise ValueError("Text cannot be empty")
    doc = open_pdf(data, password)
    try:
        page = doc[page_idx]
        point = fitz.Point(float(x), float(y))
        if not page.rect.contains(point):
            raise ValueError("Text position is outside the page")
        page.insert_text(point, text, fontsize=float(size), fontname=font, color=color, overlay=True)
        return save_pdf(doc)
    finally:
        doc.close()


def add_image(data: bytes, page_idx: int, image: bytes, x: float, y: float,
              width: float, height: float, password: str = "") -> bytes:
    if width <= 0 or height <= 0:
        raise ValueError("Image dimensions must be positive")
    Image.open(io.BytesIO(image)).verify()
    doc = open_pdf(data, password)
    try:
        page = doc[page_idx]
        rect = fitz.Rect(x, y, x + width, y + height)
        if not page.rect.intersects(rect):
            raise ValueError("Image position is outside the page")
        page.insert_image(rect, stream=image, keep_proportion=True, overlay=True)
        return save_pdf(doc)
    finally:
        doc.close()


def add_watermark(data: bytes, text: str, indexes: list[int], opacity: float = .18,
                  angle: int = 45, password: str = "") -> bytes:
    if not text.strip():
        raise ValueError("Watermark cannot be empty")
    doc = open_pdf(data, password)
    try:
        for idx in indexes:
            page = doc[idx]
            rect = page.rect
            shape = page.new_shape()
            shape.insert_textbox(rect, text, fontsize=max(28, min(rect.width, rect.height) / 9),
                                 fontname="helv", color=(0.35, 0.35, 0.35),
                                 align=fitz.TEXT_ALIGN_CENTER, rotate=angle if angle in (0, 90, 180, 270) else 0)
            shape.finish(fill_opacity=opacity, stroke_opacity=opacity)
            shape.commit(overlay=True)
        return save_pdf(doc)
    finally:
        doc.close()


def set_metadata(data: bytes, title: str, author: str, subject: str, keywords: str,
                 password: str = "") -> bytes:
    doc = open_pdf(data, password)
    try:
        meta = doc.metadata or {}
        meta.update({"title": title, "author": author, "subject": subject, "keywords": keywords})
        doc.set_metadata(meta)
        return save_pdf(doc)
    finally:
        doc.close()


def encrypt_pdf(data: bytes, owner_password: str, user_password: str = "") -> bytes:
    if not owner_password:
        raise ValueError("Owner password is required")
    doc = open_pdf(data)
    try:
        return doc.tobytes(garbage=4, deflate=True,
            encryption=fitz.PDF_ENCRYPT_AES_256,
            owner_pw=owner_password, user_pw=user_password,
            permissions=fitz.PDF_PERM_ACCESSIBILITY | fitz.PDF_PERM_PRINT)
    finally:
        doc.close()
