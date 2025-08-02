# === sinergia_core.py ===
from fpdf import FPDF
from PIL import Image
import os
import qrcode

def gerar_pdf(
    imagens,
    filename,
    page_format,
    header_text,
    header_font,
    header_size,
    footer_text,
    footer_font,
    footer_size,
    insert_page_marker,
    fill_full_page
):
    pdf = FPDF(orientation='P', unit='mm', format=page_format)

    for i, img_path in enumerate(imagens):
        pdf.add_page()

        if header_text:
            try:
                pdf.set_font(header_font, size=header_size)
            except:
                pdf.set_font("Arial", size=header_size)
            pdf.cell(0, 10, header_text, ln=True, align="C")

        with open(img_path, 'rb') as f:
            img = Image.open(f)
            img = img.convert('RGB')
            img_w, img_h = img.size
            max_width = pdf.w - 20 if fill_full_page else pdf.w - 40
            scaled_height = max_width * img_h / img_w
            x = (pdf.w - max_width) / 2
            y = (pdf.h - scaled_height) / 2
            pdf.image(img_path, x=x, y=y, w=max_width)

        if footer_text:
            pdf.set_y(-15)
            try:
                pdf.set_font(footer_font, size=footer_size)
            except:
                pdf.set_font("Arial", size=footer_size)
            pdf.cell(0, 10, footer_text, 0, 0, "C")

        if insert_page_marker:
            pdf.set_y(-8)
            pdf.set_font("Arial", size=8)
            pdf.cell(0, 10, f"Página {i+1}", 0, 0, "R")

    output_path = f"temp/{filename.replace(' ', '_')}.pdf"
    pdf.output(output_path)
    return output_path

def gerar_capa(image_path, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.image(image_path, x=0, y=0, w=210, h=297)
    output_path = f"temp/capa_{filename.replace(' ', '_')}.pdf"
    pdf.output(output_path)
    return output_path

def gerar_contracapa(link, filename):
    qr = qrcode.make(link)
    qr_path = f"temp/qr_{filename.replace(' ', '_')}.png"
    qr.save(qr_path)
    pdf = FPDF()
    pdf.add_page()
    pdf.image(qr_path, x=75, y=100, w=60, h=60)
    output_path = f"temp/contracapa_{filename.replace(' ', '_')}.pdf"
    pdf.output(output_path)
    if os.path.exists(qr_path):
        os.remove(qr_path)
    return output_path


# === main.py ===
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import shutil
from .sinergia_core import gerar_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/gerar-pdf")
async def criar_pdf(
    arquivos: list[UploadFile] = File(...),
    filename: str = Form(...),
    page_format: str = Form(...),
    header_text: str = Form(...),
    header_font: str = Form(...),
    header_size: int = Form(...),
    footer_text: str = Form(...),
    footer_font: str = Form(...),
    footer_size: int = Form(...),
    insert_page_marker: bool = Form(...),
    fill_full_page: bool = Form(...)
):
    if not os.path.exists("temp"):
        os.makedirs("temp")

    imagens = []
    for file in arquivos:
        caminho = f"temp/{file.filename}"
        with open(caminho, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        imagens.append(caminho)

    caminho_pdf = gerar_pdf(
        imagens=imagens,
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

    return FileResponse(caminho_pdf, media_type='application/pdf', filename=os.path.basename(caminho_pdf))
