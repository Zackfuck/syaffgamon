from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil, os, requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

WEBHOOK_URL = "https://discord.com/api/webhooks/1380591302407753880/Gp6y-sFwhFsDAaqg88Fx-qqNFAMcCoReS-JsOyBzgGNexnnt5b1kJQr1Qo5opFqtFaz6"

@app.get("/", response_class=HTMLResponse)
async def get_store(request: Request):
    return templates.TemplateResponse("mika_store.html", {"request": request})

@app.post("/submit")
async def submit_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    bank: str = Form(...),
    product: str = Form(...),
    resit: UploadFile = File(...)
):
    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, resit.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resit.file, buffer)

    with open(file_path, "rb") as image_file:
        requests.post(
            WEBHOOK_URL,
            data={
                "content": f"📦 **Order Baru!**\\n👤 Nama: {name}\\n📧 Email: {email}\\n🏦 Bank: {bank}\\n🛒 Produk: {product}"
            },
            files={"file": (resit.filename, image_file)}
        )

    return templates.TemplateResponse("thank_you.html", {"request": request})
