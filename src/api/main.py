
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from .sinergia_core import gerar_pdf

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
    pdf_stream = await gerar_pdf(
        files, filename, page_format, header_text,
        header_font, header_size, footer_text, footer_font,
        footer_size, insert_page_marker, fill_full_page
    )

    return StreamingResponse(pdf_stream, media_type="application/pdf")
