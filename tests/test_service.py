"""Unit tests for Professor AI (no API calls required)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from professor_ai import service
from professor_ai.prompts import LEVEL_MODIFIERS, STYLE_MODIFIERS, build_system_prompt


def test_system_prompt_contains_three_step_format():
    prompt = build_system_prompt()
    assert "In Simple Words (Layman)" in prompt
    assert "Diagram" in prompt
    assert "Example" in prompt
    assert "Quick Recap" in prompt


def test_style_and_level_modifiers_applied():
    prompt = build_system_prompt("deep", "advanced")
    assert STYLE_MODIFIERS["deep"] in prompt
    assert LEVEL_MODIFIERS["advanced"] in prompt


def test_build_messages_orders_turns_correctly():
    history = [
        {"role": "user", "content": "old q"},
        {"role": "assistant", "content": "old a"},
    ]
    messages = service.build_messages("new q", history, style="short", level="beginner")
    assert messages[0]["role"] == "system"
    assert [m["role"] for m in messages[1:]] == ["user", "assistant", "user"]
    assert messages[-1]["content"] == "new q"
    assert STYLE_MODIFIERS["short"] in messages[0]["content"]
    assert LEVEL_MODIFIERS["beginner"] in messages[0]["content"]


def test_empty_question_is_handled():
    assert "type a question" in service.ask("").lower()


def test_ask_stream_yields_text_without_api(monkeypatch):
    from professor_ai import llm as llm_module

    def fake_stream(messages):
        yield "### 1. In Simple Words (Layman)\nhello"
        yield "\nworld"

    monkeypatch.setattr(llm_module, "chat_stream", fake_stream)
    chunks = list(service.ask_stream("what is 2+2?"))
    assert "".join(chunks) == "### 1. In Simple Words (Layman)\nhello\nworld"


def test_ask_stream_falls_back_on_error(monkeypatch):
    from professor_ai import llm as llm_module

    def broken_stream(messages):
        raise llm_module.LLMError("boom")
        yield  # pragma: no cover

    monkeypatch.setattr(llm_module, "chat_stream", broken_stream)
    output = "".join(service.ask_stream("q"))
    assert "### 2. Diagram" in output
    assert "boom" in output
