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
