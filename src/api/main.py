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
    arquivos: List[UploadFile] = File(...),
    nome_arquivo: str = Form(...),
    formato_pagina: str = Form(...),
    header_texto: str = Form(""),
    header_fonte: str = Form("Arial"),
    header_tamanho: int = Form(12),
    footer_texto: str = Form(""),
    footer_fonte: str = Form("Arial"),
    footer_tamanho: int = Form(12),
    mostrar_paginador: bool = Form(False),
    preencher_tela: bool = Form(False),
):
    try:
        # Salva os arquivos enviados
        caminhos = []
        for arquivo in arquivos:
            caminho_temp = os.path.join("temp", arquivo.filename)
            with open(caminho_temp, "wb") as buffer:
                buffer.write(await arquivo.read())
            caminhos.append(caminho_temp)

        # Gera o PDF
        caminho_pdf = gerar_pdf(
            image_paths=caminhos,
            filename=nome_arquivo,
            page_format=formato_pagina,
            header_text=header_texto,
            header_font=header_fonte,
            header_size=header_tamanho,
            footer_text=footer_texto,
            footer_font=footer_fonte,
            footer_size=footer_tamanho,
            insert_page_marker=mostrar_paginador,
            fill_full_page=preencher_tela
        )

        return FileResponse(
            path=caminho_pdf,
            filename=os.path.basename(caminho_pdf),
            media_type="application/pdf"
        )
    except Exception as e:
        print(f"[ERRO AO GERAR PDF]: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao gerar PDF")
