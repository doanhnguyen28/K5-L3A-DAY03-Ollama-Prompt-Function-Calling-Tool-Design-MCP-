from __future__ import annotations

import json
from datetime import datetime

import streamlit as st

from chat import (ARTIFACTS_DIR, ROOT, now_iso, run_model_tool_loop,
                  safe_slug, trim_history, write_transcript)
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="wide")

PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
SAMPLES = [
    "Tin tức AI hôm nay có gì nổi bật?",
    "Lấy 5 tweet mới nhất của Sam Altman",
    "Mọi người đang bàn gì về GPT-5 trên Twitter?",
    "Tóm tắt bài này: https://openai.com/blog/gpt-5",
    "Đăng bản tin này lên Telegram giúp mình",
]


@st.cache_resource
def get_provider(name: str):
    return make_provider(name)


def new_session(provider_name: str, model: str | None, version: str) -> None:
    av = build_artifact_version(version, PROMPT_PATH, TOOLS_PATH)
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    tid = "_".join([safe_slug(version), safe_slug(provider_name), "ui", stamp])
    st.session_state.history = []
    st.session_state.display = []
    st.session_state.transcript_path = ROOT / "transcripts" / f"{tid}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": tid,
        **artifact_version_dict(av),
        "provider": provider_name,
        "model": model or getattr(get_provider(provider_name), "default_model", None),
        "system_prompt": str(PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "source": "streamlit_ui",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    st.session_state.session_key = (provider_name, model, version)


def render_rounds(rounds: list[dict]) -> None:
    for r in rounds:
        for ev in r.get("tool_results", []):
            args = json.dumps(ev.get("args", {}), ensure_ascii=False)
            with st.expander(f"🔧 {ev.get('tool')}({args})"):
                st.json(ev.get("result", {}))


# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Cấu hình")
    provider_name = st.selectbox("Provider", ["openrouter", "openai", "anthropic", "gemini", "ollama"])
    model = st.text_input("Model (trống = mặc định)").strip() or None
    version = st.text_input("Version label", "v3")
    history_window = st.slider("History window", 1, 10, 5)
    max_rounds = st.slider("Max tool rounds", 1, 6, 4)

    if (st.button("🆕 Cuộc chat mới")
            or "transcript" not in st.session_state
            or st.session_state.session_key != (provider_name, model, version)):
        new_session(provider_name, model, version)

    st.caption(f"artifact: `{st.session_state.transcript['artifact_version']}`")
    st.caption(f"transcript: `{st.session_state.transcript_path.name}`")

    st.subheader("💡 Câu hỏi mẫu")
    for q in SAMPLES:
        st.code(q, language=None)

# ---------- Chat ----------
st.title("🔎 Research Agent")
st.caption("Tìm tin web, tweet theo tài khoản/chủ đề, đọc URL, tổng hợp digest, gửi Telegram (có xác nhận).")

for m in st.session_state.display:
    with st.chat_message(m["role"]):
        render_rounds(m.get("rounds", []))
        st.markdown(m["content"])

if user_text := st.chat_input("Hỏi agent..."):
    st.session_state.display.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
    tools = to_openai_tools(load_tool_declarations(TOOLS_PATH))
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": user_text},
    ]
    turn = {
        "turn_index": len(st.session_state.transcript["turns"]) + 1,
        "started_at": now_iso(), "user": user_text, "status": "started",
        "assistant_text": None, "rounds": [], "tool_events": [],
    }

    with st.chat_message("assistant"):
        with st.spinner("Agent đang xử lý..."):
            try:
                result = run_model_tool_loop(
                    provider=get_provider(provider_name), messages=messages,
                    tools=tools, model=model, max_tool_rounds=max_rounds,
                )
                turn.update(result)
                answer = result["assistant_text"] or "(không có nội dung)"
                st.session_state.history += [
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": answer},
                ]
            except Exception as exc:
                result = {"rounds": []}
                answer = f"⚠️ Lỗi: {type(exc).__name__}: {exc}"
                turn.update({"status": "provider_error", "error": answer})
        render_rounds(result.get("rounds", []))
        st.markdown(answer)

    st.session_state.display.append(
        {"role": "assistant", "content": answer, "rounds": result.get("rounds", [])})
    turn["ended_at"] = now_iso()
    st.session_state.transcript["turns"].append(turn)
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)
