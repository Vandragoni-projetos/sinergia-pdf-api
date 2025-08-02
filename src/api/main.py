from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from .sinergia_core import gerar_pdf
import os
import tempfile

app = FastAPI()

# Habilita CORS para testes locais e origem Base44
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app--sinerg-ia-gerador-de-pdf-para-livr-eadd1938.base44.app",
        "http://localhost",
        "http://127.0.0.1",
        "null"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/gerar-pdf")
async def gerar_pdf_endpoint(
    files: List[UploadFile] = File(...),
    filename: str = Form("output"),
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
    # Salva arquivos recebidos em disco e pega os caminhos
    temp_image_paths = []
    try:
        for file in files:
            suffix = os.path.splitext(file.filename)[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir="temp") as tmp:
                tmp.write(await file.read())
                temp_image_paths.append(tmp.name)

        # Gera o PDF passando os caminhos das imagens
        pdf_path = gerar_pdf(
            temp_image_paths, filename, page_format, header_text,
            header_font, header_size, footer_text, footer_font,
            footer_size, insert_page_marker, fill_full_page
        )

        # Retorna o PDF gerado como streaming
        pdf_file = open(pdf_path, "rb")
        return StreamingResponse(pdf_file, media_type="application/pdf")

    finally:
        # Limpa arquivos temporários
        for path in temp_image_paths:
            if os.path.exists(path):
                os.remove(path)

# Endpoint de saúde/simples
@app.get("/health")
def health():
    return {"status": "ok"}