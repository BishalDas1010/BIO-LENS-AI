import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

WELCOME = (
    "Hi! 👋 I'm **BioLens AI**, your personal health assistant.\n\n"
    "Ask me anything about **health, lifestyle, nutrition, sleep, or fitness**. 💚"
)

SUGGESTIONS = [
    "💧 How much water should I drink daily?",
    "😴 Tips to improve my sleep quality",
    "🏃 Best exercises for heart health",
    "🥗 What should I eat for better energy?",
]


def _ask_backend(user_text: str) -> str:
    """Send the whole chat history + ALL health context to FastAPI."""
    # build payload from current history (including the just-added user msg)
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.assistant_messages
    ]
    
    # FIXED: Added mental_health_context to the network payload
    payload = {
        "messages": history,
        "health_context": st.session_state.get("health_context"),
        "mental_health_context": st.session_state.get("mental_health_context"), 
    }

    try:
        r = requests.post(f"{API_URL}/chat", json=payload, timeout=60)
        if r.status_code == 200:
            return r.json()["reply"]
        return f"⚠️ Backend error {r.status_code}: {r.text}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot reach backend. Is FastAPI running on port 8000?"
    except Exception as e:
        return f"⚠️ {e}"


def assistant_page():
    st.title("💬 BioLens AI Assistant")
    st.caption("Ask anything about your health, lifestyle, nutrition & fitness.")

    if "assistant_messages" not in st.session_state:
        st.session_state.assistant_messages = [
            {"role": "assistant", "content": WELCOME}
        ]

    # --- SHOW BADGES FOR SYNCED DATA ---
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.get("health_context"):
            r = st.session_state.health_context["result"]
            color = "🔴" if r["prediction"] == 1 else "🟢"
            st.info(
                f"{color} Body Condition synced (**{r['label']}**)"
            )
            
    with col2:
        if st.session_state.get("mental_health_context"):
            mh = st.session_state.mental_health_context
            # Check if safety alert was triggered
            if mh.get("safety_alert"):
                st.error("🧠 Mental Health synced (⚠️ Safety Alert)")
            else:
                st.success(f"🧠 Mental Health synced (PHQ-9: {mh.get('phq9_score')}/27)")
        else:
            st.warning("🧠 No Mental Health data. Complete the assessment to sync.")

    # --- CHAT CONTROLS ---
    if st.button("🧹 Clear chat"):
        st.session_state.assistant_messages = [
            {"role": "assistant", "content": WELCOME}
        ]
        st.rerun()

    # render history
    for msg in st.session_state.assistant_messages:
        avatar = "🌿" if msg["role"] == "assistant" else "🧑"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # generate reply if last msg is from user
    if st.session_state.assistant_messages[-1]["role"] == "user":
        with st.chat_message("assistant", avatar="🌿"):
            with st.spinner("Thinking..."):
                reply = _ask_backend(
                    st.session_state.assistant_messages[-1]["content"]
                )
            st.markdown(reply)
        st.session_state.assistant_messages.append(
            {"role": "assistant", "content": reply}
        )

    # suggestion chips on fresh chat
    if len(st.session_state.assistant_messages) == 1:
        st.markdown("**Suggested questions:**")
        cols = st.columns(2)
        for i, text in enumerate(SUGGESTIONS):
            with cols[i % 2]:
                if st.button(text, key=f"sugg_{i}", use_container_width=True):
                    st.session_state.assistant_messages.append(
                        {"role": "user", "content": text}
                    )
                    st.rerun()

    # input
    prompt = st.chat_input("Ask BioLens AI...")
    if prompt:
        st.session_state.assistant_messages.append(
            {"role": "user", "content": prompt}
        )
        st.rerun()