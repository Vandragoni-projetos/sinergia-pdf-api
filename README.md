# SinergIA - Gerador de PDF via FastAPI

API para gerar livros de colorir com capa, conteúdo e contracapa.

## Como rodar

1. Instale os requisitos:
   ```
   pip install -r requirements.txt
   ```

2. Inicie a API:
   ```
   uvicorn main:app --reload
   ```
   ou clique duas vezes em `iniciar_api.bat`

## Endpoints

| Método | Rota              | Descrição                  |
|--------|-------------------|----------------------------|
| GET    | `/`               | Teste da API               |
| POST   | `/gerar-pdf`      | Gera PDF com imagens       |
| POST   | `/gerar-capa`     | Gera PDF de capa (1 imagem)|
| POST   | `/gerar-contracapa` | Gera contracapa com QR   |

## Logs

- Salvos em `logs/api_YYYY-MM-DD.log`

## Limpeza Automática

- A pasta `temp/` é limpa automaticamente ao iniciar a API.
