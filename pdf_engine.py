from __future__ import annotations
import io, pymupdf
from PIL import Image

def open_document(path, password=""):
    doc=pymupdf.open(path)
    if doc.needs_pass and not doc.authenticate(password): doc.close(); raise ValueError("A valid PDF password is required")
    return doc

def render_page(doc,index,zoom=1.35):
    pix=doc[index].get_pixmap(matrix=pymupdf.Matrix(zoom,zoom),alpha=False)
    return pix.tobytes("png"), pix.width, pix.height

def text_spans(page):
    result=[]
    for block in page.get_text("dict").get("blocks",[]):
        if block.get("type")!=0: continue
        for line in block.get("lines",[]):
            for span in line.get("spans",[]):
                text=span.get("text","")
                if not text.strip(): continue
                x0,y0,x1,y1=span["bbox"]
                result.append({"text":text,"rect":(x0,y0,x1,y1),"size":float(span.get("size",11)),"color":int(span.get("color",0)),"font":span.get("font","Helvetica")})
    return result

def rgb(value): return ((value>>16&255)/255,(value>>8&255)/255,(value&255)/255)

def replace_span(doc,page_index,span,new_text):
    page=doc[page_index]; x0,y0,x1,y1=span["rect"]
    rect=pymupdf.Rect(x0-0.8,y0-0.8,x1+0.8,y1+0.8)
    page.add_redact_annot(rect,fill=(1,1,1))
    page.apply_redactions(images=0,graphics=0)
    size=max(5.0,float(span.get("size",11)))
    placed=-1
    while size>=5 and placed<0:
        placed=page.insert_textbox(rect,new_text,fontsize=size,fontname="helv",color=rgb(span.get("color",0)),overlay=True)
        if placed<0:size-=0.25
    if placed<0: raise ValueError("Replacement does not fit the original text area. Use shorter text.")

def add_text(doc,page_index,point,text,size=14,color=(0,0,0)):
    doc[page_index].insert_text(pymupdf.Point(*point),text,fontsize=size,fontname="helv",color=color,overlay=True)

def add_image(doc,page_index,path,rect):
    Image.open(path).verify();doc[page_index].insert_image(pymupdf.Rect(*rect),filename=path,keep_proportion=True,overlay=True)

def save_copy(doc,path): doc.save(path,garbage=4,deflate=True,clean=True)

def delete_pages(doc,indexes):
    if len(set(indexes))>=doc.page_count: raise ValueError("A document must retain at least one page")
    for i in sorted(set(indexes),reverse=True):doc.delete_page(i)

def rotate_pages(doc,indexes,degrees):
    for i in indexes:doc[i].set_rotation((doc[i].rotation+degrees)%360)

def merge_paths(paths,out_path):
    out=pymupdf.open()
    try:
        for path in paths:
            src=pymupdf.open(path);out.insert_pdf(src);src.close()
        out.save(out_path,garbage=4,deflate=True)
    finally:out.close()
