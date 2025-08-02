import requests
import json

# URL local da sua API
url = "url = "https://sinergia-pdf-api.onrender.com/gerar-pdf"

# Substitua pelos caminhos reais das imagens que deseja incluir
files = [
    ('imagens', ('imagem1.png', open("C:\\Users\\vandr\\Downloads\\ChatGPT Image 27_07_2025, 15_34_08.png", 'rb'), 'image/png')),
    ('imagens', ('imagem2.png', open("C:\\Users\\vandr\\Downloads\\ChatGPT Image 27_07_2025, 15_34_30.png", 'rb'), 'image/png')),
]

# Dados com as opções de configuração do PDF
opcoes = {
    "titulo": "Meu Livro de Colorir",
    "subtitulo": "Animais Felizes",
    "rodape": "Criado com ❤️ por SinergIA",
    "logomarca": True,
    "formato_pagina": "A4"
}

# Envia a requisição POST com os arquivos e as opções
response = requests.post(
    url,
    files=files,
    data={"opcoes": json.dumps(opcoes)}
)

# Salva o PDF de retorno
if response.status_code == 200:
    with open("livro_colorir_gerado.pdf", "wb") as f:
        f.write(response.content)
    print("✅ PDF salvo com sucesso: livro_colorir_gerado.pdf")
else:
    print("❌ Erro ao gerar PDF:", response.status_code, response.text)
