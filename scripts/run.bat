@echo off
REM Run Professor AI locally (Windows)
if not exist ".env" (
  echo [setup] Creating .env from .env.example - add your GROQ_API_KEY first!
  copy .env.example .env
)
call venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
