"""Thin wrapper around the Groq chat-completions API."""

from groq import APIConnectionError, APIStatusError, Groq, RateLimitError

from .config import get_settings

RETRYABLE = (RateLimitError, APIConnectionError)


class LLMError(RuntimeError):
    """Raised when the model cannot produce an answer."""


def _client() -> Groq:
    settings = get_settings()
    return Groq(api_key=settings["api_key"], timeout=settings["request_timeout"])


def chat(messages: list[dict], *, retries: int = 2) -> str:
    """Send chat messages to Groq and return the assistant text."""
    settings = get_settings()
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            response = _client().chat.completions.create(
                model=settings["model"],
                messages=messages,
                temperature=settings["temperature"],
                max_tokens=settings["max_tokens"],
            )
            content = (response.choices[0].message.content or "").strip()
            if content:
                return content
            last_error = LLMError("Model returned an empty response.")
        except RETRYABLE as exc:
            last_error = exc
        except APIStatusError as exc:
            raise LLMError(f"Groq API error ({exc.status_code}): {exc.message}") from exc

    raise LLMError(f"Model failed after {retries + 1} attempts: {last_error}")


def chat_stream(messages: list[dict]):
    """Yield answer chunks as the model generates them."""
    settings = get_settings()
    try:
        stream = _client().chat.completions.create(
            model=settings["model"],
            messages=messages,
            temperature=settings["temperature"],
            max_tokens=settings["max_tokens"],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except RETRYABLE as exc:
        raise LLMError(f"Connection problem while streaming: {exc}") from exc
    except APIStatusError as exc:
        raise LLMError(f"Groq API error ({exc.status_code}): {exc.message}") from exc
