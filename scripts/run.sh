#!/usr/bin/env bash
# Run Professor AI locally (macOS/Linux)
set -e
if [ ! -f .env ]; then
  echo "[setup] Creating .env from .env.example - add your GROQ_API_KEY first!"
  cp .env.example .env
fi
source venv/bin/activate 2>/dev/null || true
pip install -r requirements.txt
streamlit run app.py
