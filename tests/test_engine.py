import pymupdf, tempfile, os
import pdf_engine as e
def make():
 p=tempfile.mktemp(suffix='.pdf');d=pymupdf.open();x=d.new_page();x.insert_text((72,72),'Hello world');d.save(p);d.close();return p
def test_replace_keeps_page():
 p=make();d=e.open_document(p);s=e.text_spans(d[0])[0];e.replace_span(d,0,s,'Hi');out=p+'.out.pdf';e.save_copy(d,out);d.close();q=pymupdf.open(out);assert q.page_count==1 and 'Hi' in q[0].get_text();q.close();os.remove(p);os.remove(out)
def test_delete_and_rotate():
 p=make();d=e.open_document(p);e.rotate_pages(d,[0],90);assert d[0].rotation==90;d.close();os.remove(p)
