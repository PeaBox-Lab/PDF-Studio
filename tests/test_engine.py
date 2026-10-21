import pymupdf,tempfile,os,pdf_engine as e
def make():
 p=tempfile.mktemp(suffix='.pdf');d=pymupdf.open();pg=d.new_page();pg.insert_text((72,72),'Hello world',fontsize=12);d.save(p);d.close();return p
def test_same_size():
 p=make();d=e.open_document(p);s=e.text_spans(d[0])[0];assert e.replace_span(d,0,s,'Hello')==s['size'];d.close();os.remove(p)
def test_long_rejected_without_shrink():
 p=make();d=e.open_document(p);s=e.text_spans(d[0])[0]
 try:e.replace_span(d,0,s,'This replacement is intentionally much too long');assert False
 except ValueError as x:assert 'will not shrink' in str(x)
 d.close();os.remove(p)
def test_snapshot_bytes_reopen():
 p=make();d=e.open_document(p);snap=d.tobytes(garbage=4,deflate=True);d.close();x=pymupdf.open(stream=snap,filetype='pdf');assert x.page_count==1;x.close();os.remove(p)
