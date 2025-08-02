from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List
import os
from .sinergia_core import gerar_pdf

app = FastAPI()

# Garante que a pasta 'temp' exista
if not os.path.exists("temp"):
    os.makedirs("temp")

# Libera CORS para frontend local e Base44
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://app--sinerg-ia-gerador-de-pdf-para-livr-eadd1938.base44.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/gerar-pdf")
async def criar_pdf(
    files: List[UploadFile] = File(...),
    filename: str = Form(...),
    page_format: str = Form(...),
    header_text: str = Form(""),
    header_font: str = Form("Arial"),
    header_size: int = Form(12),
    footer_text: str = Form(""),
    footer_font: str = Form("Arial"),
    footer_size: int = Form(12),
    insert_page_marker: bool = Form(False),
    fill_full_page: bool = Form(False),
):
    try:
        caminhos = []
        for file in files:
            caminho_temp = os.path.join("temp", file.filename)
            with open(caminho_temp, "wb") as buffer:
                buffer.write(await file.read())
            caminhos.append(caminho_temp)

        caminho_pdf = gerar_pdf(
            image_paths=caminhos,
            filename=filename,
            page_format=page_format,
            header_text=header_text,
            header_font=header_font,
            header_size=header_size,
            footer_text=footer_text,
            footer_font=footer_font,
            footer_size=footer_size,
            insert_page_marker=insert_page_marker,
            fill_full_page=fill_full_page
        )

        return FileResponse(
            path=caminho_pdf,
            filename=os.path.basename(caminho_pdf),
            media_type="application/pdf"
        )
    except Exception as e:
        print(f"[ERRO AO GERAR PDF]: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao gerar PDF")
