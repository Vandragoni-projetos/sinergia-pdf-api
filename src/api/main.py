from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Optional
from io import BytesIO
import os
import tempfile

from .sinergia_core import gerar_pdf

app = FastAPI()

# Permite acesso da interface local ou do Base44
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
    filename: str = Form("meu_livro"),
    page_format: str = Form("A4"),
    header_text: Optional[str] = Form(None),
    header_font: Optional[str] = Form("Arial"),
    header_size: Optional[int] = Form(12),
    footer_text: Optional[str] = Form(None),
    footer_font: Optional[str] = Form("Arial"),
    footer_size: Optional[int] = Form(10),
    insert_page_marker: Optional[bool] = Form(False),
    fill_full_page: Optional[bool] = Form(False),
):
    # Cria diretório temporário para armazenar arquivos
    with tempfile.TemporaryDirectory() as temp_dir:
        filepaths = []

        for file in files:
            temp_path = os.path.join(temp_dir, file.filename)
            with open(temp_path, "wb") as f:
                f.write(await file.read())
            filepaths.append(temp_path)

        # Gera PDF
        pdf_path = os.path.join(temp_dir, f"{filename}.pdf")

        gerar_pdf(
            imagens=filepaths,
            saida=pdf_path,
            formato_pagina=page_format,
            cabecalho_texto=header_text,
            cabecalho_fonte=header_font,
            cabecalho_tamanho=header_size,
            rodape_texto=footer_text,
            rodape_fonte=footer_font,
            rodape_tamanho=footer_size,
            incluir_numeracao=insert_page_marker,
            preencher_total=fill_full_page
        )

        # Retorna o PDF gerado como streaming + download automático
        pdf_file = open(pdf_path, "rb")
        headers = {
            "Content-Disposition": f"attachment; filename={filename}.pdf"
        }
        return StreamingResponse(pdf_file, media_type="application/pdf", headers=headers)
