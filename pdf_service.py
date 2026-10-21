import io, pymupdf as fitz
from PIL import Image

def open_pdf(data, password=""):
    d=fitz.open(stream=data,filetype="pdf")
    if d.needs_pass and not d.authenticate(password): d.close(); raise ValueError("Valid password required")
    return d

def info(data,password=""):
    d=open_pdf(data,password)
    try:return {"pages":d.page_count,"metadata":d.metadata or {},"sizes":[[p.rect.width,p.rect.height] for p in d]}
    finally:d.close()

def render(data,page,scale=1.5,password=""):
    d=open_pdf(data,password)
    try:return d[page].get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False).tobytes("png")
    finally:d.close()

def text_blocks(data,page,password=""):
    d=open_pdf(data,password)
    try:
        out=[]
        info=d[page].get_text("dict")
        bid=0
        for block in info.get("blocks",[]):
            if block.get("type") != 0: continue
            for line in block.get("lines",[]):
                for span in line.get("spans",[]):
                    text=span.get("text","").strip()
                    if not text: continue
                    x0,y0,x1,y1=span["bbox"]
                    out.append({"id":bid,"x":x0,"y":y0,"w":x1-x0,"h":y1-y0,"text":text,"fontSize":span.get("size",11),"color":"#%06x" % int(span.get("color",0))})
                    bid+=1
        return out
    finally:d.close()

def apply(data,ops,password=""):
    d=open_pdf(data,password)
    try:
        for op in ops:
            p=d[int(op.get("page",0))]; kind=op.get("type")
            if kind=="replace_text":
                r=fitz.Rect(op["x"],op["y"],op["x"]+op["w"],op["y"]+op["h"])
                p.add_redact_annot(r,fill=(1,1,1))
                p.apply_redactions(images=0, graphics=0)
                text=op.get("text","")
                size=max(5,float(op.get("fontSize",11)))
                result=-1
                while size >= 5 and result < 0:
                    result=p.insert_textbox(r,text,fontsize=size,fontname="helv",color=hexcolor(op.get("color","#111827")),align=0,overlay=True)
                    if result < 0: size-=0.5
                if result < 0: raise ValueError("Replacement text does not fit the selected area. Shorten it or enlarge the edit box.")
            elif kind=="text":
                p.insert_text((op["x"],op["y"]),op.get("text",""),fontsize=float(op.get("fontSize",16)),fontname="helv",color=hexcolor(op.get("color","#111827")),overlay=True)
            elif kind in ("image","signature"):
                raw=bytes.fromhex(op["hex"]); Image.open(io.BytesIO(raw)).verify()
                r=fitz.Rect(op["x"],op["y"],op["x"]+op["w"],op["y"]+op["h"]);p.insert_image(r,stream=raw,keep_proportion=True,overlay=True)
            elif kind=="highlight":
                p.add_highlight_annot(fitz.Rect(op["x"],op["y"],op["x"]+op["w"],op["y"]+op["h"]))
            elif kind=="redact":
                p.add_redact_annot(fitz.Rect(op["x"],op["y"],op["x"]+op["w"],op["y"]+op["h"]),fill=(0,0,0));p.apply_redactions()
        return d.tobytes(garbage=4,deflate=True,clean=True)
    finally:d.close()

def organize(data,action,pages,password=""):
    src=open_pdf(data,password)
    try:
        if action=="delete":
            for i in sorted(set(pages),reverse=True): src.delete_page(i)
            if src.page_count<1: raise ValueError("Keep at least one page")
            return src.tobytes(garbage=4,deflate=True)
        out=fitz.open()
        try:
            order=pages if action=="reorder" else list(range(src.page_count))
            for i in order:out.insert_pdf(src,from_page=i,to_page=i)
            return out.tobytes(garbage=4,deflate=True)
        finally:out.close()
    finally:src.close()

def merge(items):
    out=fitz.open()
    try:
        for data in items:
            d=open_pdf(data)
            try:out.insert_pdf(d)
            finally:d.close()
        return out.tobytes(garbage=4,deflate=True)
    finally:out.close()

def hexcolor(v):
    v=v.lstrip("#");return tuple(int(v[i:i+2],16)/255 for i in (0,2,4))
