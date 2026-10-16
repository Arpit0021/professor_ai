# 🎓 Professor AI

A chatbot professor that answers **every** question in a fixed 3-step teaching format:

```
1. In Simple Words (Layman)  →  plain English + daily-life analogy
2. Diagram                   →  ASCII/text diagram of how it works
3. Example                   →  concrete, real-world worked example
4. Quick Recap               →  one-line summary
```

Built with **Streamlit + Groq LLM**.

---

## Project Structure

```
.
├── app.py                   # Streamlit chat UI (entry point)
├── professor_ai/            # Core application package
│   ├── __init__.py          # Package metadata / version
│   ├── config.py            # Env loading + settings + validation
│   ├── prompts.py           # Professor system prompt (3-step format)
│   ├── llm.py               # Groq API wrapper (chat + streaming)
│   └── service.py           # Orchestration: prompt → model → answer
├── tests/
│   └── test_service.py      # Unit tests (no API calls needed)
├── .streamlit/
│   └── config.toml          # Server + theme configuration
├── scripts/
│   ├── run.bat              # Windows launcher
│   └── run.sh               # macOS/Linux launcher
├── .env.example             # Template for secrets (copy to .env)
├── .gitignore
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container deployment
├── .dockerignore
└── README.md
```

---

## Local Setup

```bash
# 1. Create virtualenv & install
python -m venv venv
venv\Scripts\activate        # Windows:  source venv/bin/activate (macOS/Linux)
pip install -r requirements.txt

# 2. Configure secrets
copy .env.example .env       # macOS/Linux: cp .env.example .env
#    put your GROQ_API_KEY (from https://console.groq.com/keys) inside .env

# 3. Run
streamlit run app.py
#    or simply:  scripts\run.bat  (Windows) /  bash scripts/run.sh (Linux/Mac)
```

Open http://localhost:8501

---

## Run Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Deployment

### Docker (anywhere)

```bash
docker build -t professor-ai .
docker run -p 8501:8501 --env-file .env professor-ai
```

### Streamlit Community Cloud

1. Push this repo to GitHub (keep `.env` out — it is git-ignored).
2. Create an app at share.streamlit.io → select repo → main file `app.py`.
3. Add secret `GROQ_API_KEY` in **App settings → Secrets**.

### Render / Railway / Fly.io

Use the included `Dockerfile` (port **8501**) and set env var `GROQ_API_KEY`.

---

## Environment Variables

| Variable         | Required | Default                   | Description                  |
| ---------------- | -------- | ------------------------- | ---------------------------- |
| `GROQ_API_KEY`   | ✅       | —                         | Groq API key                 |
| `GROQ_MODEL`     | ❌       | `openai/gpt-oss-120b`     | Groq model id                |
| `LLM_TEMPERATURE`| ❌       | `0.4`                     | Creativity (0.0 – 1.0)       |
| `LLM_MAX_TOKENS` | ❌       | `2048`                    | Max answer length            |
| `LLM_TIMEOUT`    | ❌       | `60`                      | API timeout (seconds)        |
