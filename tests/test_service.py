import pymupdf as fitz,pdf_service as s
def sample():
 d=fitz.open();p=d.new_page();p.insert_text((72,72),"Hello editable world");b=d.tobytes();d.close();return b
def test_blocks():assert any("Hello" in x["text"] for x in s.text_blocks(sample(),0))
def test_replace():
 b=s.apply(sample(),[{"type":"replace_text","page":0,"x":65,"y":55,"w":180,"h":30,"text":"Changed","fontSize":12,"color":"#111827"}]);d=s.open_pdf(b);assert "Changed" in d[0].get_text();d.close()
def test_render():assert len(s.render(sample(),0))>100
def test_merge():
 d=s.open_pdf(s.merge([sample(),sample()]));assert d.page_count==2;d.close()
