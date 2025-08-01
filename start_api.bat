@echo off
title Iniciando API SinergIA...
cd /d C:\Users\vandr\OneDrive\Documentos\GitHub\fastapi-sinergia-gerador-pdf
call venv\Scripts\activate
uvicorn main:app --reload
pause
