from pathlib import Path
from fastapi import FastAPI,UploadFile,File,Form,HTTPException
from fastapi.responses import FileResponse,Response
from fastapi.staticfiles import StaticFiles
import json,uuid
import pdf_service as svc
BASE=Path(__file__).parent; STORE={}
app=FastAPI(title="PeaBox PDF Studio")
app.mount("/static",StaticFiles(directory=BASE/"static"),name="static")
@app.get("/")
def home():return FileResponse(BASE/"static/index.html")
@app.post("/api/open")
async def open_pdf(file:UploadFile=File(...),password:str=Form("")):
    try:
        data=await file.read(); meta=svc.info(data,password); key=str(uuid.uuid4());STORE[key]={"data":data,"password":password,"name":file.filename};return {"id":key,"name":file.filename,**meta}
    except Exception as e:raise HTTPException(400,str(e))
@app.get("/api/{key}/page/{page}")
def page(key:str,page:int,scale:float=1.5):
    try:
        x=STORE[key];return Response(svc.render(x["data"],page,scale,x["password"]),media_type="image/png")
    except Exception as e:raise HTTPException(404,str(e))
@app.get("/api/{key}/text/{page}")
def text(key:str,page:int):
    try:x=STORE[key];return svc.text_blocks(x["data"],page,x["password"])
    except Exception as e:raise HTTPException(404,str(e))
@app.post("/api/{key}/export")
async def export(key:str,payload:dict):
    try:
        x=STORE[key];out=svc.apply(x["data"],payload.get("operations",[]),x["password"]);return Response(out,media_type="application/pdf",headers={"Content-Disposition":f'attachment; filename="edited-{x["name"]}"'})
    except Exception as e:raise HTTPException(400,str(e))
@app.post("/api/{key}/commit")
async def commit(key:str,payload:dict):
    try:
        x=STORE[key];x["data"]=svc.apply(x["data"],payload.get("operations",[]),x["password"]);x["password"]="";return {"ok":True,**svc.info(x["data"])}
    except Exception as e:raise HTTPException(400,str(e))
@app.post("/api/{key}/organize")
async def organize(key:str,payload:dict):
    try:
        x=STORE[key];x["data"]=svc.organize(x["data"],payload["action"],payload["pages"],x["password"]);x["password"]="";return {"ok":True,**svc.info(x["data"])}
    except Exception as e:raise HTTPException(400,str(e))
@app.post("/api/merge")
async def merge(files:list[UploadFile]=File(...)):
    try:return Response(svc.merge([await f.read() for f in files]),media_type="application/pdf",headers={"Content-Disposition":'attachment; filename="merged.pdf"'})
    except Exception as e:raise HTTPException(400,str(e))
