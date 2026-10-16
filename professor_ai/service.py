"""Orchestrates prompt building and model calls for Professor AI."""

from . import llm
from .prompts import build_system_prompt

FALLBACK_TEMPLATE = """\
### 1. In Simple Words (Layman)
I could not reach my teaching brain just now, so here is the simple version of what happened:
{reason}

### 2. Diagram
```
[ You ask ] -> [ Professor AI ] -> [ Groq LLM ]
                     |
                     v
              ( connection failed )
                     |
                     v
             [ This friendly message ]
```

### 3. Example
Try again in a few seconds. If it keeps failing, check that `GROQ_API_KEY` is valid
in your `.env` file and that you have quota left at console.groq.com.

### 4. Quick Recap
The answer failed, the message above explains why, and a retry usually fixes it.
"""


def build_messages(
    question: str,
    history: list[dict] | None = None,
    *,
    style: str = "standard",
    level: str = "intermediate",
) -> list[dict]:
    history_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in (history or [])[-6:]
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]
    return [
        {"role": "system", "content": build_system_prompt(style, level)},
        *history_messages,
        {"role": "user", "content": question.strip()},
    ]


def ask(
    question: str,
    history: list[dict] | None = None,
    *,
    style: str = "standard",
    level: str = "intermediate",
) -> str:
    """Answer one question in the Layman -> Diagram -> Example format."""
    if not question or not question.strip():
        return "Please type a question first."

    messages = build_messages(question, history, style=style, level=level)
    try:
        return llm.chat(messages)
    except llm.LLMError as exc:
        return FALLBACK_TEMPLATE.format(reason=str(exc)[:300])


def ask_stream(
    question: str,
    history: list[dict] | None = None,
    *,
    style: str = "standard",
    level: str = "intermediate",
):
    """Yield the answer chunk by chunk; falls back to a formatted error."""
    if not question or not question.strip():
        yield "Please type a question first."
        return

    messages = build_messages(question, history, style=style, level=level)
    try:
        for chunk in llm.chat_stream(messages):
            yield chunk
    except llm.LLMError as exc:
        yield FALLBACK_TEMPLATE.format(reason=str(exc)[:300])
