from __future__ import annotations
import io
from datetime import datetime
import streamlit as st
from PIL import Image, ImageDraw
import pdf_engine as engine

st.set_page_config(page_title="PeaBox PDF Studio 0.2", page_icon="📄", layout="wide")

st.markdown("""
<style>
.block-container{padding-top:1.2rem;max-width:1500px}.stButton>button{border-radius:10px}
[data-testid="stSidebar"]{min-width:270px}.small-note{color:#64748b;font-size:.86rem}
</style>
""", unsafe_allow_html=True)

DEFAULTS = {"pdf": None, "name": "document.pdf", "password": "", "undo": [], "redo": [], "page": 1}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k] = v

def reset_document(data: bytes, name: str, password: str = ""):
    doc = engine.open_pdf(data, password); count = doc.page_count; doc.close()
    st.session_state.update(pdf=data, name=name, password=password, undo=[], redo=[], page=1)
    st.toast(f"Loaded {count} pages", icon="✅")

def apply_change(data: bytes, label: str):
    st.session_state.undo.append((st.session_state.pdf, label))
    st.session_state.undo = st.session_state.undo[-20:]
    st.session_state.pdf = data
    st.session_state.redo = []
    doc = engine.open_pdf(data, st.session_state.password); pages = doc.page_count; doc.close()
    st.session_state.page = min(st.session_state.page, pages)
    st.toast(label, icon="✅")

def safe_run(fn, label):
    try: apply_change(fn(), label)
    except Exception as exc: st.error(str(exc))

with st.sidebar:
    st.title("📄 PeaBox PDF Studio")
    st.caption("v0.2.0 · Local-first PDF workspace")
    upload = st.file_uploader("Open PDF", type=["pdf"])
    password = st.text_input("Password, if protected", type="password")
    if upload and st.button("Load document", type="primary", use_container_width=True):
        try: reset_document(upload.getvalue(), upload.name, password)
        except Exception as exc: st.error(str(exc))
    st.divider()
    c1,c2 = st.columns(2)
    if c1.button("↶ Undo", disabled=not st.session_state.undo, use_container_width=True):
        old,label=st.session_state.undo.pop(); st.session_state.redo.append((st.session_state.pdf,label)); st.session_state.pdf=old; st.rerun()
    if c2.button("↷ Redo", disabled=not st.session_state.redo, use_container_width=True):
        newer,label=st.session_state.redo.pop(); st.session_state.undo.append((st.session_state.pdf,label)); st.session_state.pdf=newer; st.rerun()
    if st.session_state.pdf:
        st.download_button("⬇ Download current PDF", st.session_state.pdf,
            file_name=f"edited-{st.session_state.name}", mime="application/pdf", use_container_width=True)
        st.caption("Every operation updates the working document. Undo keeps the last 20 changes.")

st.title("PeaBox PDF Studio")
st.caption("Edit and organize PDFs without sending them to a third-party service.")

if not st.session_state.pdf:
    st.info("Upload a PDF from the left sidebar, enter its password if needed, and select **Load document**.")
    st.stop()

try:
    doc = engine.open_pdf(st.session_state.pdf, st.session_state.password)
    page_count = doc.page_count
    metadata = doc.metadata or {}
    doc.close()
except Exception as exc:
    st.error(str(exc)); st.stop()

preview, controls = st.columns([1.35,1], gap="large")
with preview:
    nav1,nav2,nav3 = st.columns([1,2,1])
    if nav1.button("← Previous", disabled=st.session_state.page<=1, use_container_width=True): st.session_state.page-=1; st.rerun()
    st.session_state.page = nav2.number_input("Page",1,page_count,st.session_state.page,label_visibility="collapsed")
    if nav3.button("Next →", disabled=st.session_state.page>=page_count, use_container_width=True): st.session_state.page+=1; st.rerun()
    try:
        png=engine.render_page(st.session_state.pdf,st.session_state.page-1,1.35,st.session_state.password)
        st.image(png,caption=f"Page {st.session_state.page} of {page_count}",use_container_width=True)
    except Exception as exc: st.error(str(exc))

with controls:
    tabs=st.tabs(["Text","Image & sign","Pages","Watermark","Properties"])
    with tabs[0]:
        text=st.text_area("Text to place",height=90)
        c1,c2,c3=st.columns(3); x=c1.number_input("X",0.0,value=50.0); y=c2.number_input("Y",0.0,value=80.0); size=c3.number_input("Size",6.0,96.0,18.0)
        color=st.color_picker("Colour","#172554")
        rgb=tuple(int(color[i:i+2],16)/255 for i in (1,3,5))
        if st.button("Add text to current page",type="primary",use_container_width=True):
            safe_run(lambda:engine.add_text(st.session_state.pdf,st.session_state.page-1,text,x,y,size,rgb,password=st.session_state.password),"Text added")
    with tabs[1]:
        mode=st.radio("Source",["Upload image/signature","Draw signature"],horizontal=True)
        image_bytes=None
        if mode=="Upload image/signature":
            img=st.file_uploader("PNG or JPG",type=["png","jpg","jpeg"],key="img")
            if img:image_bytes=img.getvalue();st.image(image_bytes,width=260)
        else:
            st.caption("Draw with the mouse in the box. On touch devices, use a finger or stylus.")
            try:
                from streamlit_drawable_canvas import st_canvas
                canvas=st_canvas(stroke_width=3,stroke_color="#172554",background_color="#FFFFFF",height=150,width=500,drawing_mode="freedraw",key="signature")
                if canvas.image_data is not None:
                    im=Image.fromarray(canvas.image_data.astype("uint8")).convert("RGBA")
                    alpha=Image.new("L",im.size,0); px=im.load(); ap=alpha.load()
                    for yy in range(im.height):
                        for xx in range(im.width):
                            r,g,b,a=px[xx,yy]; ap[xx,yy]=255 if (r+g+b)<700 else 0
                    im.putalpha(alpha); buf=io.BytesIO(); im.save(buf,"PNG"); image_bytes=buf.getvalue()
            except Exception:
                st.warning("Signature canvas component is unavailable. Use an uploaded signature image.")
        c1,c2=st.columns(2); ix=c1.number_input("Image X",0.0,value=50.0); iy=c2.number_input("Image Y",0.0,value=80.0)
        c3,c4=st.columns(2); iw=c3.number_input("Width",10.0,value=180.0); ih=c4.number_input("Height",10.0,value=70.0)
        if st.button("Place on current page",type="primary",use_container_width=True,disabled=image_bytes is None):
            safe_run(lambda:engine.add_image(st.session_state.pdf,st.session_state.page-1,image_bytes,ix,iy,iw,ih,st.session_state.password),"Image/signature added")
    with tabs[2]:
        action=st.selectbox("Page operation",["Rotate","Delete","Extract","Reorder","Merge another PDF"])
        if action in ["Rotate","Delete","Extract"]:
            spec=st.text_input("Pages","1",help="Examples: 1-3,5")
            if action=="Rotate": degrees=st.selectbox("Clockwise degrees",[90,180,270])
            if st.button(f"{action} pages",type="primary",use_container_width=True):
                try:
                    indexes=engine.parse_page_range(spec,page_count)
                    if action=="Rotate": safe_run(lambda:engine.rotate_pages(st.session_state.pdf,indexes,degrees,st.session_state.password),"Pages rotated")
                    elif action=="Delete": safe_run(lambda:engine.delete_pages(st.session_state.pdf,indexes,st.session_state.password),"Pages deleted")
                    else:
                        out=engine.extract_pages(st.session_state.pdf,indexes,st.session_state.password)
                        st.download_button("Download extracted PDF",out,"extracted-pages.pdf","application/pdf",use_container_width=True)
                except Exception as exc: st.error(str(exc))
        elif action=="Reorder":
            order=st.text_input("New order",",".join(map(str,range(1,page_count+1))),help="Include every page once, e.g. 3,1,2")
            if st.button("Apply new order",type="primary",use_container_width=True):
                try:
                    indexes=engine.parse_page_range(order,page_count)
                    safe_run(lambda:engine.reorder_pages(st.session_state.pdf,indexes,st.session_state.password),"Pages reordered")
                except Exception as exc: st.error(str(exc))
        else:
            extras=st.file_uploader("PDFs to append",type=["pdf"],accept_multiple_files=True,key="extras")
            if st.button("Append PDFs",type="primary",use_container_width=True,disabled=not extras):
                safe_run(lambda:engine.merge_pdfs([(st.session_state.pdf,st.session_state.password)]+[(f.getvalue(),"") for f in extras]),"PDFs merged")
    with tabs[3]:
        mark=st.text_input("Watermark text","CONFIDENTIAL")
        pages=st.text_input("Apply to pages",f"1-{page_count}",key="wm_pages")
        opacity=st.slider("Opacity",.05,.7,.18,.05)
        rotation=st.selectbox("Text rotation",[0,90,180,270])
        if st.button("Apply watermark",type="primary",use_container_width=True):
            try:
                idx=engine.parse_page_range(pages,page_count)
                safe_run(lambda:engine.add_watermark(st.session_state.pdf,mark,idx,opacity,rotation,st.session_state.password),"Watermark added")
            except Exception as exc:st.error(str(exc))
    with tabs[4]:
        title=st.text_input("Title",metadata.get("title") or "")
        author=st.text_input("Author",metadata.get("author") or "")
        subject=st.text_input("Subject",metadata.get("subject") or "")
        keywords=st.text_input("Keywords",metadata.get("keywords") or "")
        if st.button("Save metadata",use_container_width=True):
            safe_run(lambda:engine.set_metadata(st.session_state.pdf,title,author,subject,keywords,st.session_state.password),"Metadata saved")
        st.divider(); st.subheader("Password protection")
        owner=st.text_input("Owner password",type="password"); user=st.text_input("Open password (optional)",type="password")
        if st.button("Create encrypted copy",use_container_width=True):
            try:
                secured=engine.encrypt_pdf(st.session_state.pdf,owner,user)
                st.download_button("Download encrypted PDF",secured,"protected.pdf","application/pdf",use_container_width=True)
            except Exception as exc:st.error(str(exc))

st.divider()
with st.expander("Merge PDFs as a separate operation"):
    merge_files=st.file_uploader("Select two or more PDFs in order",type=["pdf"],accept_multiple_files=True,key="standalone_merge")
    if st.button("Build merged PDF",disabled=not merge_files or len(merge_files)<2):
        try:
            merged=engine.merge_pdfs([(f.getvalue(),"") for f in merge_files])
            st.download_button("Download merged PDF",merged,"merged.pdf","application/pdf")
        except Exception as exc:st.error(str(exc))
