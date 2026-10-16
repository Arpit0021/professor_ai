import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

VALID_STYLES = ("standard", "short", "deep")
VALID_LEVELS = ("beginner", "intermediate", "advanced")


@lru_cache(maxsize=1)
def get_settings() -> dict:
    return {
        "api_key": os.getenv("GROQ_API_KEY", "").strip(),
        "model": os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip(),
        "temperature": float(os.getenv("LLM_TEMPERATURE", "0.4")),
        "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "2048")),
        "request_timeout": int(os.getenv("LLM_TIMEOUT", "60")),
    }


def validate() -> list[str]:
    """Return a list of configuration problems (empty list = ready to run)."""
    problems = []
    if not get_settings()["api_key"]:
        problems.append(
            "GROQ_API_KEY is missing. Copy `.env.example` to `.env` and add your key "
            "from https://console.groq.com/keys"
        )
    return problems
