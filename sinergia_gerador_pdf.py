import os
import webbrowser
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, Radiobutton, IntVar, Frame, messagebox, Toplevel, OptionMenu, Checkbutton, PhotoImage, Canvas, Scrollbar
from fpdf import FPDF
from PIL import Image
from tkinter import ttk
from PyPDF2 import PdfMerger
import qrcode  # Certifique-se de instalar a biblioteca

class PDFGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SinergIA - Gerador de PDF para Livros de Colorir")
        self.root.configure(bg="#f5f5f5")

        # --- Adicionando Scrollbar Vertical ---
        canvas = Canvas(self.root, borderwidth=0, background="#f5f5f5")
        frame = Frame(canvas, background="#f5f5f5")
        vsb = Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)
        self.root.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        self.scroll_container = frame

        self.root.geometry("1100x900")
        self.root.minsize(800, 600)
        self.root.resizable(True, True)

        self.filename = StringVar()
        self.cabecalho = StringVar()
        self.rodape = StringVar()
        self.logo_path = "C:/Users/vandr/anaconda3/Gerador PDF/LogoSinergAI.png"
        self.arquivos = []
        self.destino = ""
        self.formato_var = IntVar(value=1)
        self.formato_pagina = StringVar(value="A4")
        self.imprimir_marcador = IntVar()
        self.site_url = StringVar(value="https://example.com")
        self.qr_link = StringVar(value="https://veedea.com/t?v=11d865")
        self.preencher_capa = IntVar(value=0)  # Pode ser personalizada

        self.fontes_disponiveis = [
             "Arial", "Courier", "Helvetica", "Times", "Symbol", "ZapfDingbats"]
        self.cabecalho_font = StringVar(value="Arial")
        self.cabecalho_size = IntVar(value=12)
        self.rodape_font = StringVar(value="Arial")
        self.rodape_size = IntVar(value=10)
        self.pdf = FPDF()
        self.setup_ui()

    def setup_ui(self):
        self.tab_control = ttk.Notebook(self.scroll_container)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Configurações do PDF')
        self.tab_control.pack(expand=1, fill="both")

        logo = Image.open(self.logo_path)
        logo.thumbnail((150, 150), Image.LANCZOS)
        logo.save("temp_logo.png")

        logo_label = Label(self.tab1, bg="#f5f5f5")
        logo_label.image = PhotoImage(file="temp_logo.png")
        logo_label.config(image=logo_label.image)
        logo_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        Label(self.tab1, text="Nome do arquivo PDF:", bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=(10, 5), sticky="w")
        Entry(self.tab1, textvariable=self.filename, width=40).grid(row=1, column=1, padx=10, pady=(10, 5))

        Button(self.tab1, text="Selecionar Imagens", command=self.selecionar_arquivos).grid(row=2, column=0, columnspan=2, pady=(5, 20))

        Label(self.tab1, text="Formatos:", bg="#f5f5f5").grid(row=3, column=0, padx=10, pady=(10, 5), sticky="w")
        formatos = [("Todos", 1), ("*.jpg", 2), ("*.jpeg", 3), ("*.png", 4), ("Unificar Arquivos *.pdf", 5)]
        for i, (texto, val) in enumerate(formatos):
            Radiobutton(self.tab1, text=texto, variable=self.formato_var, value=val, bg="#f5f5f5").grid(row=3, column=i + 1, padx=5, sticky="w")

        Button(self.tab1, text="Selecionar Pasta Destino", command=self.selecionar_pasta_destino).grid(row=4, column=0, columnspan=2, pady=(5, 20))

        Label(self.tab1, text="Formato do Livro:", bg="#f5f5f5").grid(row=5, column=0, padx=10, pady=(10, 5), sticky="w")
        formatos_pagina = [("A4 (210x297mm)", "A4"),
                           ("Carta (216x279mm)", "LETTER"),
                           ("Amazon (215,9x279,4mm)", "AMAZON"),
                           ("Quadrado (210x210mm)", "SQUARE"),
                           ("A5 (148x210mm)", "A5-V"),
                           ("A5 (210X148mm)", "A5-H"),
                           ("A4 - 2xA5H (2x 210x148mm)", "A4-2A5H")]  # NOVO FORMATO
                            
        for i, (texto, val) in enumerate(formatos_pagina):
            Radiobutton(self.tab1, text=texto, variable=self.formato_pagina, value=val, bg="#f5f5f5").grid(row=5, column=i + 1, padx=5, sticky="w")

        Label(self.tab1, text="Cabeçalho (opcional):", bg="#f5f5f5").grid(row=6, column=0, padx=10, pady=(10, 5), sticky="w")
        Entry(self.tab1, textvariable=self.cabecalho, width=40).grid(row=6, column=1, padx=10)

        Label(self.tab1, text="Fonte Cabeçalho:", bg="#f5f5f5").grid(row=7, column=0, padx=10, pady=(10, 5), sticky="w")
        OptionMenu(self.tab1, self.cabecalho_font, *self.fontes_disponiveis).grid(row=7, column=1, padx=10)

        Label(self.tab1, text="Tamanho Cabeçalho:", bg="#f5f5f5").grid(row=8, column=0, padx=10, pady=(10, 5), sticky="w")
        Entry(self.tab1, textvariable=self.cabecalho_size, width=5).grid(row=8, column=1, padx=10)

        Label(self.tab1, text="Rodapé (opcional):", bg="#f5f5f5").grid(row=9, column=0, padx=10, pady=(10, 5), sticky="w")
        Entry(self.tab1, textvariable=self.rodape, width=40).grid(row=9, column=1, padx=10)

        Label(self.tab1, text="Fonte Rodapé:", bg="#f5f5f5").grid(row=10, column=0, padx=10, pady=(10, 5), sticky="w")
        OptionMenu(self.tab1, self.rodape_font, *self.fontes_disponiveis).grid(row=10, column=1, padx=10)

        Label(self.tab1, text="Tamanho Rodapé:", bg="#f5f5f5").grid(row=11, column=0, padx=10, pady=(10, 5), sticky="w")
        Entry(self.tab1, textvariable=self.rodape_size, width=5).grid(row=11, column=1, padx=10)

        Checkbutton(self.tab1, text="Imprimir Marcador de Página", variable=self.imprimir_marcador).grid(row=12, column=0, columnspan=2, pady=(10, 20))

        Button(self.tab1, text="Selecionar logomarca (opcional)", command=self.selecionar_logo).grid(row=13, column=0, columnspan=2, pady=(5, 10))
        Label(self.tab1, text="Link para Contracapa (QR Code):", bg="#f5f5f5").grid(row=14, column=0, padx=10, sticky="w")
        Entry(self.tab1, textvariable=self.qr_link, width=40).grid(row=14, column=1, padx=10)
        Checkbutton(self.tab1, text="Preencher totalmente a capa (sem margens)", variable=self.preencher_capa, bg="#f5f5f5").grid(row=15, column=0, columnspan=2, pady=(0, 10), sticky="w")

        # locos abaixos permite que fique responsivel
        button_frame = Frame(self.tab1, bg="#f5f5f5")
        button_frame.grid(row=16, column=0, columnspan=5, pady=20)        

        Button(button_frame, text="GERAR PDF", command=self.gerar_pdf, bg="#4A07B6", fg="white", width=20).grid(row=0, column=0, padx=5)
        Button(button_frame, text="GERAR PDF Capa", command=self.gerar_pdf_capa, bg="#08E20F", fg="white", width=20).grid(row=0, column=1, padx=5)
        Button(button_frame, text="LIMPAR CAMPOS", command=self.limpar_campos, bg="#f4ab0d", fg="black", width=20).grid(row=0, column=2, padx=5)
        Button(button_frame, text="GERAR CONTRACAPA", command=self.gerar_pdf_contracapa, bg="#f72206", fg="white", width=20).grid(row=0, column=3, padx=5)
        Button(button_frame, text="AJUDA", command=self.mostrar_ajuda, bg="#4C77AF", fg="white", width=20).grid(row=0, column=4, padx=5)

        self.progress = ttk.Progressbar(self.scroll_container, orient='horizontal', length=500, mode='determinate')
        self.progress.pack(pady=10)

    def selecionar_arquivos(self):
        formatos = {
            1: [("All Files", "*.*")],
            2: [("JPG Files", "*.jpg")],
            3: [("JPEG Files", "*.jpeg")],
            4: [("PNG Files", "*.png")],
            5: [("PDF Files", "Unificar Arquivos *.pdf")]
        }
        self.arquivos = filedialog.askopenfilenames(filetypes=formatos[self.formato_var.get()])

    def selecionar_pasta_destino(self):
        self.destino = filedialog.askdirectory()

    def selecionar_logo(self):
        self.logo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    def limpar_campos(self):
        self.filename.set("")
        self.cabecalho.set("")
        self.rodape.set("")
        self.logo_path = ""
        self.arquivos = []
        self.destino = ""
        self.formato_var.set(1)
        self.formato_pagina.set("A4")
        self.cabecalho_font.set("Arial")
        self.cabecalho_size.set(12)
        self.rodape_font.set("Arial")
        self.rodape_size.set(10)
        self.imprimir_marcador.set(0)

    def mostrar_ajuda(self):
        # Importes locais (garante que constantes estejam disponíveis mesmo sem import global)
        from tkinter import Text, WORD, END, BOTH, LEFT, RIGHT, Y

        help_window = Toplevel(self.root)
        help_window.title("Ajuda")
        help_window.geometry("700x600")

        # Frame principal (área rolável)
        frame = Frame(help_window, bg="white")
        frame.pack(fill=BOTH, expand=True, padx=10, pady=(10, 0))  # margem superior

        # Scrollbar vertical
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Widget de texto
        text = Text(
            frame,
            wrap=WORD,
            yscrollcommand=scrollbar.set,
            padx=10,
            pady=10,
            font=("Courier", 10),
            bg="white"
        )
        text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=text.yview)

        # Instruções completas (atualize livremente o texto)
        instructions = """INSTRUÇÕES DE USO – SINERG.IA

O Sinerg.IA – Gerador de PDF para Livros de Colorir faz parte de um ecossistema de ferramentas e agentes GPT que ajudam você a criar produtos digitais completos com poucos cliques.

----------------------------------------------------------------
1. NOME DO ARQUIVO PDF
----------------------------------------------------------------
Campo obrigatório. Define o nome do arquivo final (.pdf) salvo na pasta de destino.

----------------------------------------------------------------
2. SELECIONAR IMAGENS
----------------------------------------------------------------
Escolha uma ou várias imagens. A ordem de impressão segue a ordem alfabética/numérica dos nomes dos arquivos.
Dica: renomeie arquivos (001, 002, 003...) para controlar a sequência das páginas.

----------------------------------------------------------------
3. FORMATOS DE ARQUIVO
----------------------------------------------------------------
Use os botões de seleção:
- Todos
- *.jpg
- *.jpeg
- *.png
- Unificar arquivos *.pdf  (para juntar vários PDFs em um único)

⚠ Importante: Se for unificar PDFs, selecione essa opção ANTES de clicar em [GERAR PDF].

----------------------------------------------------------------
4. SELECIONAR PASTA DESTINO
----------------------------------------------------------------
Escolha onde os PDFs gerados serão salvos.

----------------------------------------------------------------
5. FORMATO DO LIVRO
----------------------------------------------------------------
Escolha o tamanho da página:
- A4 (210x297mm)
- Carta (216x279mm)
- Quadrado (210x210mm)
- A5-V (148x210mm – Vertical)
- A5-H (210x148mm – Horizontal)

----------------------------------------------------------------
6. CABEÇALHO (opcional)
----------------------------------------------------------------
Texto impresso no TOPO de cada página.
• Se vazio, nenhuma área é reservada (mais espaço para a imagem).
• Fonte e tamanho personalizáveis.

----------------------------------------------------------------
7. RODAPÉ (opcional)
----------------------------------------------------------------
Texto impresso na BASE de cada página (ex: créditos, marca).
• Pode ser combinado com marcador de página.
• Fonte e tamanho personalizáveis.

----------------------------------------------------------------
8. IMPRIMIR MARCADOR DE PÁGINA
----------------------------------------------------------------
Quando marcado, adiciona “Página X de Y” no rodapé (após o texto do rodapé, se houver).

----------------------------------------------------------------
9. SELECIONAR LOGOMARCA (opcional)
----------------------------------------------------------------
Inclui uma imagem (por ex. PNG com fundo transparente) no canto inferior direito das páginas do miolo.

----------------------------------------------------------------
10. PREENCHER TOTALMENTE A CAPA (SEM MARGENS)
----------------------------------------------------------------
Afeta *GERAR PDF CAPA* e também o miolo (GERAR PDF) se nenhuma área obrigatória for reservada.
• Marcado: a imagem ocupa toda a página (pode cortar/distorcer dependendo do formato).
• Desmarcado: a imagem é centralizada com margens de respiro proporcionais ao formato escolhido.

----------------------------------------------------------------
11. GERAR PDF
----------------------------------------------------------------
Gera o miolo completo:
• Usa cabeçalho, rodapé, logomarca e marcador (se configurados).
• Se você só selecionar imagens + destino + formato (sem cabeçalho/rodapé/logo), o app aplica margens padrão de respiro.
• Se “Preencher totalmente a capa” estiver marcado e não houver cabeçalho/rodapé/logo/marcador, as páginas podem usar área total (modo fullscreen).

----------------------------------------------------------------
12. GERAR PDF CAPA
----------------------------------------------------------------
Gera um PDF com apenas a primeira imagem como capa.
• Centralizado com margens por padrão.
• Se “Preencher totalmente a capa” estiver marcado: ocupa toda a página.

----------------------------------------------------------------
13. GERAR CONTRACAPA
----------------------------------------------------------------
Cria um PDF de contracapa com mensagem + QR Code apontando para o link informado (site, loja, WhatsApp, etc.).

----------------------------------------------------------------
14. LINK PARA CONTRACAPA (QR CODE)
----------------------------------------------------------------
Digite o link que será codificado. Se vazio, usa valor padrão do sistema.

----------------------------------------------------------------
15. LIMPAR CAMPOS
----------------------------------------------------------------
Reseta todos os campos e volta às configurações padrão.

----------------------------------------------------------------
DICAS
----------------------------------------------------------------
• Use imagens em boa resolução (ideal 300 DPI) para impressão.
• Para miolos de livros de colorir: imagens em preto e branco funcionam melhor quando salvas como PNG.
• Para formatos muito diferentes (ex: quadrado vs retangular), teste com margens antes de imprimir em lote.
• Este app substitui fluxos manuais (ex: ajustes no Canva) ao automatizar redimensionamento e montagem em PDF.

----------------------------------------------------------------
OBRIGADO POR USAR O SINERG.IA!
Para novidades, atualizações e outras ferramentas, clique abaixo:
"""
        # Inserir e bloquear edição
        text.insert(END, instructions)
        text.config(state="disabled")

        # Botão fora da área rolável (fica fixo no rodapé da janela)
        Button(help_window, text="Visite meu site", command=self.abrir_site, bg="#4CAF50", fg="white").pack(pady=10)

    def abrir_site(self):
        url = "https://vitrinedgtlead.com.br/costrutor-prompt"  # Substitua pelo seu URL desejado
        webbrowser.open(url)        

    def gerar_pdf(self):
        self.progress['value'] = 0  # Reset progress bar

        if not self.arquivos:
            messagebox.showinfo("Debug", f"Arquivos carregados: {self.arquivos}")
            messagebox.showwarning("Aviso", "Nenhuma imagem selecionada.")
            return
            
        if not self.destino or not self.filename.get():
            messagebox.showerror("Erro", "Preencha o nome do arquivo PDF e selecione a pasta de destino.")
            return

        formato_selecionado = self.formato_pagina.get()
        pdf_merger = PdfMerger()

        # FORMATO ESPECIAL: A4-2A5H (duas imagens por página)
        if formato_selecionado == "A4-2A5H":
            formato_pdf = (210, 297)
            pdf = FPDF(orientation="P", unit="mm", format=formato_pdf)
            imagens = self.arquivos
            total_paginas = (len(imagens) + 1) // 2

            for k, i in enumerate(range(0, len(imagens), 2)):
                pdf.add_page()

                # --- SUPERIOR ---
                img_path1 = imagens[i]
                img1 = Image.open(img_path1).convert("RGBA")
                img1_w, img1_h = img1.size
                aspect1 = img1_w / img1_h
                target_w = 210
                target_h = 148

                # Redimensionamento proporcional
                if aspect1 > (target_w / target_h):
                    new_w = target_w * 0.92
                    new_h = new_w / aspect1
                else:
                    new_h = target_h * 0.92
                    new_w = new_h * aspect1
                x1 = (210 - new_w) / 2 + 10  # Centraliza e recua 10mm à direita
                y1 = (148 - new_h) / 2 

                temp_img1 = f"_temp_{os.path.basename(img_path1)}_a5h1.jpg"
                img1.convert("RGB").save(temp_img1, "JPEG")
                pdf.image(temp_img1, x=x1, y=y1, w=new_w, h=new_h)
                os.remove(temp_img1)

                # --- INFERIOR (se houver) ---
                if i+1 < len(imagens):
                    img_path2 = imagens[i+1]
                    img2 = Image.open(img_path2).convert("RGBA")
                    img2_w, img2_h = img2.size
                    aspect2 = img2_w / img2_h
                    if aspect2 > (target_w / target_h):
                        new_w2 = target_w * 0.92
                        new_h2 = new_w2 / aspect2
                    else:
                        new_h2 = target_h * 0.92
                        new_w2 = new_h2 * aspect2
                    x2 = (210 - new_w2) / 2 + 10  # Centraliza e recua 10mm à direita
                    y2 = 148 + (148 - new_h2) / 2  # metade inferior

                    temp_img2 = f"_temp_{os.path.basename(img_path2)}_a5h2.jpg"
                    img2.convert("RGB").save(temp_img2, "JPEG")
                    pdf.image(temp_img2, x=x2, y=y2, w=new_w2, h=new_h2)
                    os.remove(temp_img2)

                self.progress['value'] = ((k + 1) / total_paginas) * 100

            nome_pdf = os.path.join(self.destino, self.filename.get() + ".pdf")
            pdf.output(nome_pdf)
            messagebox.showinfo("Concluído", f"PDF gerado com sucesso em: {nome_pdf}")
            return

        # --- FORMATOS NORMAIS ---
        # Verifica se o formato é PDF puro
        if self.formato_var.get() == 5:
            # Adiciona a capa se houver
            capa_path = os.path.join(self.destino, self.filename.get() + "_capa.pdf")
            if os.path.exists(capa_path):
                pdf_merger.append(capa_path)

            for img_path in self.arquivos:
                if img_path.endswith('.pdf'):
                    pdf_merger.append(img_path)
                else:
                    temp_pdf_path = self.pdf_from_image(img_path)
                    pdf_merger.append(temp_pdf_path)

            nome_pdf = os.path.join(self.destino, self.filename.get() + ".pdf")
            pdf_merger.write(nome_pdf)
            pdf_merger.close()
            messagebox.showinfo("Concluído", f"PDF unificado gerado com sucesso em: {nome_pdf}")
            return

        # --- OUTROS FORMATOS DE LIVRO ---
        # Definição dos formatos
        if formato_selecionado == "A4":
            formato_pdf = "A4"
            largura_max, altura_max = 210, 297
        elif formato_selecionado == "LETTER":
            formato_pdf = (216, 279)
            largura_max, altura_max = 216, 279
        elif formato_selecionado == "AMAZON":
            formato_pdf = (215.9, 279.4)
            largura_max, altura_max = 215.9, 279.4
        elif formato_selecionado == "SQUARE":
            formato_pdf = (210, 210)
            largura_max, altura_max = 210, 210
        elif formato_selecionado == "A5-V":
            formato_pdf = (148, 210)
            largura_max, altura_max = 148, 210
        elif formato_selecionado == "A5-H":
            formato_pdf = (210, 148)
            largura_max, altura_max = 210, 148
        else:
            formato_pdf = "A4"
            largura_max, altura_max = 210, 297

        pdf = FPDF(orientation="P", unit="mm", format=formato_pdf)
        total_paginas = len(self.arquivos)

        for i, img_path in enumerate(self.arquivos):
            pdf.add_page()

            # Cabeçalho
            usar_cabecalho = bool(self.cabecalho.get().strip())
            usar_rodape = bool(self.rodape.get().strip())
            usar_logo = os.path.exists(self.logo_path)
            preencher_total = self.preencher_capa.get() == 1

            if usar_cabecalho:
                try:
                    pdf.set_font(self.cabecalho_font.get(), size=self.cabecalho_size.get())
                except:
                    pdf.set_font("Arial", size=self.cabecalho_size.get())
                    pdf.set_y(10)
                    pdf.set_x(10)  # Margem lateral
                    pdf.multi_cell(0, 8, self.cabecalho.get(), align="C")

            img = Image.open(img_path).convert("RGBA")
            img_width, img_height = img.size
            background = Image.new("RGBA", img.size, (255, 255, 255, 255))
            background.paste(img, (0, 0), img)
            temp_img_path = f"_temp_{os.path.basename(img_path)}"
            background.convert("RGB").save(temp_img_path)

            # Definição de margens e áreas úteis
            if preencher_total:
                margem_topo = margem_base = margem_laterais = 0
            else:
                margem_topo = 20 if usar_cabecalho else 5
                margem_base = 48 if usar_rodape or self.imprimir_marcador.get() else 5
                margem_laterais = 10 if usar_logo else 5

            largura_util = largura_max - 2 * margem_laterais
            altura_util = altura_max - margem_topo - margem_base

            # Redimensionamento proporcional
            aspect_ratio = img_width / img_height
            new_width = largura_util
            new_height = new_width / aspect_ratio
            if new_height > altura_util:
                new_height = altura_util
                new_width = new_height * aspect_ratio

            x = (largura_max - new_width) / 2
            y = margem_topo + ((altura_util - new_height) / 2)
            if y < margem_topo:
                y = margem_topo

            pdf.image(temp_img_path, x=x, y=y, w=new_width, h=new_height)
            os.remove(temp_img_path)

            # Rodapé
            if usar_rodape or self.imprimir_marcador.get():
                try:
                    pdf.set_font(self.rodape_font.get(), size=self.rodape_size.get())
                except:
                    pdf.set_font("Arial", size=self.rodape_size.get())
                    pdf.set_y(altura_max - 48)
                    pdf.set_x(10)  # Margem lateral
                    rodape_txt = self.rodape.get()
                    texto_final = f"{rodape_txt}" if rodape_txt else ""
                    if self.imprimir_marcador.get():
                        texto_final += f" | Página {i + 1} de {total_paginas}"
                    pdf.multi_cell(0, 8, texto_final.strip(), align="C")

            # Logomarca
            if self.logo_path and os.path.exists(self.logo_path):
                logo_w = 25
                logo = Image.open(self.logo_path)
                logo_ratio = logo.width / logo.height
                logo_h = logo_w / logo_ratio
                logo_x = largura_max - logo_w - 10
                logo_y = altura_max - logo_h - 10
                pdf.image(self.logo_path, x=logo_x, y=logo_y, w=logo_w, h=logo_h)

            self.progress['value'] = (i + 1) / total_paginas * 100

        nome_pdf = os.path.join(self.destino, self.filename.get() + ".pdf")
        pdf.output(nome_pdf)
        messagebox.showinfo("Concluído", f"PDF gerado com sucesso em: {nome_pdf}")
        
    def gerar_pdf_capa(self):
        if not self.arquivos or not self.destino or not self.filename.get():
            messagebox.showerror("Erro", "Preencha os campos obrigatórios e selecione a imagem da capa.")
            return

        formato_selecionado = self.formato_pagina.get()
        if formato_selecionado == "A4":
            formato_pdf = "A4"
            largura_max, altura_max = 210, 297
        elif formato_selecionado == "LETTER":
            formato_pdf = (216, 279)
            largura_max, altura_max = 216, 279
        elif formato_selecionado == "AMAZON":
            formato_pdf = (215.9, 279.4)
            largura_max, altura_max = 215.9, 279.4
        elif formato_selecionado == "SQUARE":
            formato_pdf = (210, 210)
            largura_max, altura_max = 210, 210
        elif formato_selecionado == "A5-V":
            formato_pdf = (148, 210)
            largura_max, altura_max = 148, 210
        elif formato_selecionado == "A5-H":
            formato_pdf = (210, 148)
            largura_max, altura_max = 210, 148
        elif formato_selecionado == "A4-2A5H":   # NOVO
            formato_pdf = (210, 297)
            largura_max, altura_max = 210, 297

        pdf = FPDF(orientation="P", unit="mm", format=formato_pdf)
        pdf.add_page()

        img_path = self.arquivos[0]
        img = Image.open(img_path).convert("RGBA")
        img_width, img_height = img.size

        background = Image.new("RGBA", img.size, (255, 255, 255, 255))
        background.paste(img, (0, 0), img)
        background_rgb = background.convert("RGB")

        temp_img_path = f"_temp_capa_{os.path.basename(img_path)}"
        background_rgb.save(temp_img_path, "JPEG")

        preencher_total = self.preencher_capa.get() == 1

        if preencher_total:
            x = 0
            y = 0
            w = largura_max
            h = altura_max
        else:
            aspect_ratio = img_width / img_height
            page_ratio = largura_max / altura_max

            if aspect_ratio > page_ratio:
                w = largura_max * 0.92
                h = w / aspect_ratio
            else:
                h = altura_max * 0.92
                w = h * aspect_ratio

            x = (largura_max - w) / 2
            y = (altura_max - h) / 2

        pdf.image(temp_img_path, x=x, y=y, w=w, h=h)
        os.remove(temp_img_path)

        nome_pdf = os.path.join(self.destino, self.filename.get() + "_capa.pdf")
        pdf.output(nome_pdf)

        messagebox.showinfo("Concluído", f"Capa gerada com sucesso em: {nome_pdf}")

    def gerar_pdf_contracapa(self):
        if not self.destino or not self.filename.get():
            messagebox.showerror("Erro", "Informe o nome do arquivo e a pasta de destino.")
            return

        formato_selecionado = self.formato_pagina.get()
        if formato_selecionado == "A4":
            formato_pdf = "A4"
            largura_max, altura_max = 210, 297
        elif formato_selecionado == "LETTER":
            formato_pdf = (216, 279)
            largura_max, altura_max = 216, 279
        elif formato_selecionado == "AMAZON":
            formato_pdf = (215.9, 279.4)
            largura_max, altura_max = 215.9, 279.4
        elif formato_selecionado == "SQUARE":
            formato_pdf = (210, 210)
            largura_max, altura_max = 210, 210
        elif formato_selecionado == "A5-V":
            formato_pdf = (148, 210)
            largura_max, altura_max = 148, 210
        elif formato_selecionado == "A5-H":
            formato_pdf = (210, 148)
            largura_max, altura_max = 210, 148
        elif formato_selecionado == "A4-2A5H":   # NOVO
            formato_pdf = (210, 297)
            largura_max, altura_max = 210, 297

        pdf = FPDF(orientation="P", unit="mm", format=formato_pdf)
        pdf.add_page()

        # Texto de agradecimento
        pdf.set_font("Arial", size=14)
        pdf.set_text_color(60, 60, 60)
        pdf.set_xy(10, altura_max / 2 - 20)
        pdf.multi_cell(0, 10, "Obrigado por utilizar este material! Acesse mais conteúdos escaneando o QR Code abaixo:", align="C")

        # QR Code com link personalizado
        link = self.qr_link.get().strip() or "https://veedea.com"
        qr = qrcode.make(link)
        qr_path = "_temp_qrcode.png"
        qr.save(qr_path)

        qr_w = 40
        qr_h = 40
        x_qr = (largura_max - qr_w) / 2
        y_qr = altura_max / 2 + 10
        pdf.image(qr_path, x=x_qr, y=y_qr, w=qr_w, h=qr_h)
        os.remove(qr_path)

        nome_pdf = os.path.join(self.destino, self.filename.get() + "_contracapa.pdf")
        pdf.output(nome_pdf)

        messagebox.showinfo("Concluído", f"Contracapa gerada com sucesso em: {nome_pdf}")

    # def gerar_pdf_from_image(self, img_path):(self, img_path):
    def gerar_pdf_from_image(self, img_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.image(img_path)
        pdf_output_path = f"_temp_{os.path.basename(img_path)}.pdf"
        pdf.output(pdf_output_path)
        return pdf_output_path

if __name__ == "__main__":
    root = Tk()
    PDFGeneratorApp(root)
    root.mainloop()