@echo off
title Iniciando API SinergIA
cd /d %~dp0
uvicorn main:app --reload
