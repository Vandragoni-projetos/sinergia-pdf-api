# Para rodar online: uvicorn api.main:app --host 0.0.0.0 --port 10000
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, logging
from datetime import datetime
from .sinergia_core import gerar_pdf, gerar_capa, gerar_contracapa

# Criação de pastas necessárias
os.makedirs("logs", exist_ok=True)
os.makedirs("temp", exist_ok=True)

# Configuração do log
logging.basicConfig(
    filename=f'logs/api_{datetime.now().strftime("%Y-%m-%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

# Permitir apenas o frontend Base44 para segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app--sinerg-ia-gerador-de-pdf-para-livr-eadd1938.base44.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensagem": "API do SinergIA está online"}

@app.post("/gerar-pdf")
async def endpoint_gerar_pdf(
    files: list[UploadFile] = File(...),
    filename: str = Form(...),
    page_format: str = Form("A4"),
    header_text: str = Form(""),
    header_font: str = Form("Arial"),
    header_size: str = Form("12"),
    footer_text: str = Form(""),
    footer_font: str = Form("Arial"),
    footer_size: str = Form("10"),
    insert_page_marker: bool = Form(False),
    fill_full_page: bool = Form(False)
):
    image_paths = []
    for file in files:
        temp_path = f"temp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_paths.append(temp_path)

    pdf_path = gerar_pdf(
        image_paths=image_paths,
        filename=filename,
        page_format=page_format,
        header_text=header_text,
        header_font=header_font,
        header_size=int(header_size),
        footer_text=footer_text,
        footer_font=footer_font,
        footer_size=int(footer_size),
        insert_page_marker=insert_page_marker,
        fill_full_page=fill_full_page
    )

    logging.info(f"PDF gerado: {filename}.pdf com {len(files)} imagens.")
    return StreamingResponse(open(pdf_path, "rb"), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename}.pdf"})

@app.post("/gerar-capa")
async def endpoint_gerar_capa(file: UploadFile = File(...), filename: str = Form(...)):
    temp_path = f"temp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pdf_path = gerar_capa(temp_path, filename)
    logging.info(f"Capa gerada: capa_{filename}.pdf")
    return StreamingResponse(open(pdf_path, "rb"), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=capa_{filename}.pdf"})

@app.post("/gerar-contracapa")
async def endpoint_gerar_contracapa(link: str = Form(...), filename: str = Form(...)):
    pdf_path = gerar_contracapa(link, filename)
    logging.info(f"Contracapa gerada com QR: contracapa_{filename}.pdf")
    return StreamingResponse(open(pdf_path, "rb"), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=contracapa_{filename}.pdf"})
