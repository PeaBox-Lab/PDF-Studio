import pymupdf

def create_sample(path):
 d=pymupdf.open();p=d.new_page();p.insert_text((72,72),'PeaBox PDF Studio');d.save(path);d.close()
def open_document(path,password=''):
 d=pymupdf.open(path)
 if d.needs_pass and not d.authenticate(password):d.close();raise ValueError('Valid PDF password required')
 return d
def set_metadata(doc,title='',author='',subject='',keywords=''):
 m=dict(doc.metadata or {});m.update({'title':title,'author':author,'subject':subject,'keywords':keywords});doc.set_metadata(m)
def add_watermark(doc,text,opacity=.16):
 if not text.strip():raise ValueError('Watermark text cannot be empty')
 for page in doc:
  r=page.rect;s=page.new_shape();s.insert_textbox(r,text,fontsize=max(24,min(r.width,r.height)/9),fontname='helv',color=(.45,.45,.45),align=pymupdf.TEXT_ALIGN_CENTER);s.finish(fill_opacity=opacity,stroke_opacity=opacity);s.commit(overlay=True)
def add_page_numbers(doc,prefix='Page ',start=1):
 for i,page in enumerate(doc):
  r=page.rect;page.insert_textbox(pymupdf.Rect(0,r.height-32,r.width,r.height-8),f'{prefix}{start+i}',fontsize=9,fontname='helv',color=(.3,.3,.3),align=pymupdf.TEXT_ALIGN_CENTER,overlay=True)
def add_header_footer(doc,header='',footer=''):
 for page in doc:
  r=page.rect
  if header:page.insert_textbox(pymupdf.Rect(24,8,r.width-24,30),header,fontsize=9,fontname='helv',color=(.3,.3,.3),align=pymupdf.TEXT_ALIGN_CENTER,overlay=True)
  if footer:page.insert_textbox(pymupdf.Rect(24,r.height-30,r.width-24,r.height-8),footer,fontsize=9,fontname='helv',color=(.3,.3,.3),align=pymupdf.TEXT_ALIGN_CENTER,overlay=True)
def save_encrypted(doc,path,owner,user='',allow_print=True,allow_copy=False):
 if not owner:raise ValueError('Owner password is required')
 perms=pymupdf.PDF_PERM_ACCESSIBILITY
 if allow_print:perms|=pymupdf.PDF_PERM_PRINT
 if allow_copy:perms|=pymupdf.PDF_PERM_COPY
 doc.save(path,encryption=pymupdf.PDF_ENCRYPT_AES_256,owner_pw=owner,user_pw=user,permissions=perms,garbage=4,deflate=True)
def save(doc,path):doc.save(path,garbage=4,deflate=True,clean=True)
