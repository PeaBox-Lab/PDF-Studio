import os,tempfile,pymupdf,pdf_engine as e
def make():
 p=tempfile.mktemp(suffix='.pdf');e.create_sample(p);return p
def test_document_tools():
 p=make();d=e.open_document(p);e.set_metadata(d,'T','A','S','K');e.add_watermark(d,'DRAFT');e.add_header_footer(d,'H','F');e.add_page_numbers(d);assert d.metadata['title']=='T';assert 'Page 1' in d[0].get_text();d.close();os.remove(p)
def test_security():
 p=make();d=e.open_document(p);out=p+'.secure.pdf';e.save_encrypted(d,out,'owner','open');d.close();x=pymupdf.open(out);assert x.needs_pass and x.authenticate('open')>0;x.close();os.remove(p);os.remove(out)
