import fitz
import pdf_engine as e

def sample(pages=3):
    d=fitz.open()
    for i in range(pages):
        p=d.new_page();p.insert_text((72,72),f"Page {i+1}")
    b=d.tobytes();d.close();return b

def count(data,password=""):
    d=e.open_pdf(data,password);n=d.page_count;d.close();return n

def test_ranges(): assert e.parse_page_range("1-2,3",3)==[0,1,2]
def test_extract(): assert count(e.extract_pages(sample(),[0,2]))==2
def test_delete(): assert count(e.delete_pages(sample(),[1]))==2
def test_reorder(): assert count(e.reorder_pages(sample(),[2,0,1]))==3
def test_merge(): assert count(e.merge_pdfs([(sample(2),""),(sample(1),"")]))==3
def test_text(): assert count(e.add_text(sample(1),0,"OK",20,20,12,(0,0,0)))==1
def test_rotate():
    out=e.rotate_pages(sample(1),[0],90);d=e.open_pdf(out);assert d[0].rotation==90;d.close()
def test_encrypt():
    out=e.encrypt_pdf(sample(1),"owner","open");assert count(out,"open")==1
