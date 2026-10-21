import pymupdf
from PIL import Image

def open_document(path,password=""):
 d=pymupdf.open(path)
 if d.needs_pass and not d.authenticate(password): d.close(); raise ValueError("A valid PDF password is required")
 return d

def render_page(doc,index,zoom=1.35):
 pix=doc[index].get_pixmap(matrix=pymupdf.Matrix(zoom,zoom),alpha=False);return pix.tobytes("png"),pix.width,pix.height

def text_spans(page):
 out=[]
 for b in page.get_text("dict").get("blocks",[]):
  if b.get("type")!=0:continue
  for line in b.get("lines",[]):
   for s in line.get("spans",[]):
    if not s.get("text","").strip():continue
    out.append({"text":s["text"],"rect":tuple(s["bbox"]),"origin":tuple(s.get("origin",(s["bbox"][0],s["bbox"][3]))),"size":float(s.get("size",11)),"color":int(s.get("color",0)),"font":s.get("font","Helvetica"),"flags":int(s.get("flags",0))})
 return out

def rgb(v):return ((v>>16&255)/255,(v>>8&255)/255,(v&255)/255)
def base_font(s):
 n=(s.get("font") or "").lower();bold="bold" in n or bool(s.get("flags",0)&16);italic="italic" in n or "oblique" in n or bool(s.get("flags",0)&2);serif="times" in n or "serif" in n or bool(s.get("flags",0)&4)
 if "cour" in n or "mono" in n:return "cobi" if bold and italic else "cob" if bold else "coi" if italic else "cour"
 if serif:return "tibi" if bold and italic else "tibo" if bold else "tiit" if italic else "tiro"
 return "hebi" if bold and italic else "hebo" if bold else "heit" if italic else "helv"
def replace_span(doc,page_index,span,new_text):
 p=doc[page_index];x0,y0,x1,y1=span["rect"];size=span["size"];font=base_font(span);width=pymupdf.get_text_length(new_text,fontname=font,fontsize=size);available=(x1-x0)+1
 if width>available:raise ValueError(f"Replacement is {width:.1f} pt wide but only {available:.1f} pt is available. PeaBox will not shrink the original {size:.1f} pt text. Use shorter text.")
 r=pymupdf.Rect(x0-.35,y0-.25,x1+.35,y1+.25);p.add_redact_annot(r,fill=(1,1,1));p.apply_redactions(images=0,graphics=0)
 ox,oy=span["origin"];p.insert_text(pymupdf.Point(ox,oy),new_text,fontsize=size,fontname=font,color=rgb(span["color"]),overlay=True)
 return size

def add_text(doc,page,point,text,size=14):doc[page].insert_text(pymupdf.Point(*point),text,fontsize=size,fontname="helv",overlay=True)
def add_image(doc,page,path,rect):Image.open(path).verify();doc[page].insert_image(pymupdf.Rect(*rect),filename=path,keep_proportion=True,overlay=True)
def save_copy(doc,path):doc.save(path,garbage=4,deflate=True,clean=True)
def delete_pages(doc,indexes):
 if len(set(indexes))>=doc.page_count:raise ValueError("A document must retain at least one page")
 for i in sorted(set(indexes),reverse=True):doc.delete_page(i)
def rotate_pages(doc,indexes,degrees):
 for i in indexes:doc[i].set_rotation((doc[i].rotation+degrees)%360)
def merge_paths(paths,out):
 d=pymupdf.open()
 try:
  for path in paths:
   s=pymupdf.open(path);d.insert_pdf(s);s.close()
  d.save(out,garbage=4,deflate=True)
 finally:d.close()

def reorder_pages(doc, order):
 if sorted(order)!=list(range(doc.page_count)): raise ValueError('New order must include every page exactly once')
 doc.select(order)

def duplicate_page(doc,index):
 doc.fullcopy_page(index, to=index)

def extract_pages(doc,indexes,path):
 if not indexes: raise ValueError('Select at least one page')
 out=pymupdf.open()
 try:
  for i in indexes:out.insert_pdf(doc,from_page=i,to_page=i)
  out.save(path,garbage=4,deflate=True)
 finally:out.close()

def insert_blank_page(doc,after_index,width=None,height=None):
 ref=doc[after_index].rect
 doc.new_page(pno=after_index+1,width=width or ref.width,height=height or ref.height)

def insert_pdf_after(doc,after_index,path):
 other=pymupdf.open(path)
 try:doc.insert_pdf(other,start_at=after_index+1)
 finally:other.close()

def annotate_span(doc,page_index,span,kind):
 page=doc[page_index]
 rect=pymupdf.Rect(*span['rect'])
 if kind=='highlight':
  annot=page.add_highlight_annot(rect);annot.set_colors(stroke=(1,0.82,0));annot.set_opacity(0.42);annot.update()
 elif kind=='underline':
  annot=page.add_underline_annot(rect);annot.set_colors(stroke=(0.1,0.35,0.9));annot.update()
 elif kind=='strikeout':
  annot=page.add_strikeout_annot(rect);annot.set_colors(stroke=(0.85,0.12,0.12));annot.update()
 elif kind=='redact':
  page.add_redact_annot(rect,fill=(0,0,0));page.apply_redactions(images=0,graphics=0);annot=None
 else:raise ValueError('Unsupported annotation type')
 return annot

def add_comment(doc,page_index,point,text):
 if not text.strip():raise ValueError('Comment cannot be empty')
 annot=doc[page_index].add_text_annot(pymupdf.Point(*point),text)
 annot.set_info(title='PeaBox PDF Studio',subject='Comment')
 annot.update();return annot

def add_rectangle(doc,page_index,rect,color=(0.1,0.35,0.9),width=1.5):
 annot=doc[page_index].add_rect_annot(pymupdf.Rect(*rect));annot.set_colors(stroke=color);annot.set_border(width=width);annot.update();return annot

def page_needs_ocr(page):
 text=page.get_text('text').strip()
 images=page.get_images(full=True)
 return len(text)<8 and bool(images)

def ocr_words(page,language='eng',dpi=200):
 try:
  tp=page.get_textpage_ocr(language=language,dpi=dpi,full=True)
 except Exception as exc:
  raise RuntimeError('OCR is unavailable. Install Tesseract OCR and ensure its tessdata language files are discoverable. Details: '+str(exc)) from exc
 words=page.get_text('words',textpage=tp,sort=True)
 return [{'x0':w[0],'y0':w[1],'x1':w[2],'y1':w[3],'text':w[4]} for w in words if str(w[4]).strip()]

def ocr_text(page,language='eng',dpi=200):
 try:tp=page.get_textpage_ocr(language=language,dpi=dpi,full=True)
 except Exception as exc:raise RuntimeError('OCR is unavailable. Install Tesseract OCR and ensure its tessdata language files are discoverable. Details: '+str(exc)) from exc
 return page.get_text('text',textpage=tp,sort=True)

def search_page(page,query,ocr=False,language='eng',dpi=200):
 if not query.strip():return []
 if not ocr:return [tuple(r) for r in page.search_for(query)]
 try:tp=page.get_textpage_ocr(language=language,dpi=dpi,full=True)
 except Exception as exc:raise RuntimeError('OCR is unavailable. Install Tesseract OCR and ensure its tessdata language files are discoverable. Details: '+str(exc)) from exc
 return [tuple(r) for r in page.search_for(query,textpage=tp)]
