"""Professor AI - Streamlit chat interface.

Run with:  streamlit run app.py
"""

import streamlit as st

from professor_ai import __version__
from professor_ai.config import get_settings, validate
from professor_ai.service import ask_stream

SUGGESTIONS = [
    "What is a neural network?",
    "How does HTTPS keep me safe?",
    "Explain compound interest like I'm 12",
    "What is the difference between RAM and storage?",
    "How do vaccines work?",
    "What is a REST API?",
]

st.set_page_config(
    page_title="Professor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { max-width: 900px; margin: 0 auto; }
    div[data-testid="stChatMessage"] { border-radius: 14px; padding: 6px 10px; }
    .prof-title { font-size: 2.1rem; font-weight: 700; margin: 0; }
    .prof-tag { color: #8b95a7; font-size: 0.95rem; margin-top: -8px; }
    .step-badge {
        display: inline-block; padding: 2px 10px; border-radius: 999px;
        background: #262730; color: #7dd3fc; font-size: 0.8rem; margin-left: 8px;
    }
    div[data-testid="stHorizontalBlock"] > div { gap: 0.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("style", "standard")
    st.session_state.setdefault("level", "intermediate")


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### 🎛️ Teaching Controls")
        st.session_state["style"] = st.radio(
            "Answer length",
            options=["short", "standard", "deep"],
            index=["short", "standard", "deep"].index(st.session_state["style"]),
            format_func=lambda s: {"short": "⚡ Short", "standard": "📘 Standard", "deep": "🔬 Deep"}[s],
            help="How much detail the professor should go into.",
        )
        st.session_state["level"] = st.radio(
            "Student level",
            options=["beginner", "intermediate", "advanced"],
            index=["beginner", "intermediate", "advanced"].index(st.session_state["level"]),
            format_func=lambda l: {
                "beginner": "🌱 Beginner",
                "intermediate": "🎒 Intermediate",
                "advanced": "🚀 Advanced",
            }[l],
        )
        st.divider()
        st.caption(f"Model: `{get_settings()['model']}`")
        st.caption(f"v{__version__} · answers follow **Layman → Diagram → Example**")

        if st.session_state["messages"] and st.button("🧹 Clear conversation", use_container_width=True):
            st.session_state["messages"] = []
            st.rerun()


def render_welcome() -> None:
    st.markdown('<p class="prof-title">🎓 Professor AI</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="prof-tag">Ask anything — every answer comes in 3 steps: '
        '<b>Simple Words → Diagram → Example</b></p>',
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown("**Try one of these:**")
    cols = st.columns(3)
    for i, question in enumerate(SUGGESTIONS):
        if cols[i % 3].button(question, use_container_width=True):
            st.session_state["pending"] = question
            st.rerun()


def render_history() -> None:
    for message in st.session_state["messages"]:
        avatar = "🧑‍🎓" if message["role"] == "user" else "🎓"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


def handle_question(question: str) -> None:
    st.session_state["messages"].append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🎓"):
        history = st.session_state["messages"][:-1]
        try:
            answer = st.write_stream(
                ask_stream(
                    question,
                    history,
                    style=st.session_state["style"],
                    level=st.session_state["level"],
                )
            )
        except Exception as exc:
            answer = f"⚠️ Something went wrong: `{exc}`"
            st.warning(answer)

    st.session_state["messages"].append({"role": "assistant", "content": answer or ""})


def main() -> None:
    init_state()
    render_sidebar()

    problems = validate()
    if problems:
        for problem in problems:
            st.error(problem)
        st.stop()

    render_welcome() if not st.session_state["messages"] else render_history()

    pending = st.session_state.pop("pending", None)
    if pending:
        handle_question(pending)

    if question := st.chat_input("Ask the professor anything…"):
        handle_question(question)


if __name__ == "__main__":
    main()
