# main.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import List
import os
from .sinergia_core import gerar_pdf  # ajustado para import local

app = FastAPI()

@app.post("/gerar-pdf")
async def criar_pdf(
    titulo: str = Form(...),
    subtitulo: str = Form(...),
    incluir_logo: bool = Form(...),
    incluir_numeracao: bool = Form(...),
    tamanho_pagina: str = Form(...),
    margem: int = Form(...),
    imagem_capa: UploadFile = File(...),
    imagem_contracapa: UploadFile = File(...),
    imagens: List[UploadFile] = File(...)
):
    # Criação de diretório temporário
    pasta_temporaria = "temp_uploads"
    os.makedirs(pasta_temporaria, exist_ok=True)

    def salvar_arquivo(upload: UploadFile, nome: str) -> str:
        caminho = os.path.join(pasta_temporaria, nome)
        with open(caminho, "wb") as f:
            f.write(await upload.read())
        return caminho

    # Salvar arquivos
    path_capa = await salvar_arquivo(imagem_capa, "capa.png")
    path_contracapa = await salvar_arquivo(imagem_contracapa, "contracapa.png")
    paths_imagens = []
    for i, img in enumerate(imagens):
        path = await salvar_arquivo(img, f"img_{i}.png")
        paths_imagens.append(path)

    # Caminho final do PDF
    caminho_pdf_final = "saida_final.pdf"

    # Chamar função principal
    gerar_pdf(
        titulo=titulo,
        subtitulo=subtitulo,
        incluir_logo=incluir_logo,
        incluir_numeracao=incluir_numeracao,
        tamanho_pagina=tamanho_pagina,
        margem=margem,
        capa_path=path_capa,
        contracapa_path=path_contracapa,
        imagens=paths_imagens,
        caminho_saida=caminho_pdf_final
    )

    return FileResponse(caminho_pdf_final, filename="livro_colorir.pdf", media_type="application/pdf")
