@echo off
title FH Campus Dashboard
cd /d "%~dp0"

if not exist ".venv" (
    python -m venv .venv
)

call .venv\Scripts\activate.bat

python -m pip install -r requirements.txt

python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true

pause
