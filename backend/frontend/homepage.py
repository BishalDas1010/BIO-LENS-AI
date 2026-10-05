import streamlit as st


def _go(page_name: str):
    st.session_state["page"] = page_name


def _hero():
    with st.container(border=True):
        left, right = st.columns([1.15, 1], gap="large", vertical_alignment="center")

        with left:
            st.markdown(":green-badge[:material/ecg_heart: AI-POWERED HEALTH ANALYSIS]")
            st.markdown("# See Your Health  \n# :green[More Clearly]")
            st.write(
                "BioLense analyzes your health parameters using advanced machine "
                "learning to estimate your current body condition, identify potential "
                "risks, and generate a personalized health report with actionable insights."
            )
            b1, b2 = st.columns(2)
            with b1:
                st.button(
                    "Start Health Assessment",
                    icon=":material/stethoscope:",
                    type="primary",
                    use_container_width=True,
                    on_click=_go,
                    args=("Assessment",),
                )
            with b2:
                st.button(
                    "View Dashboard",
                    icon=":material/bar_chart:",
                    use_container_width=True,
                    on_click=_go,
                    args=("Dashboard",),
                )

        with right:
            with st.container(border=True):
                st.caption("Sample preview")
                m1, m2, m3 = st.columns(3)
                m1.metric("Heart Rate", "78 BPM")
                m2.metric("Blood Pressure", "120/80")
                m3.metric("Temperature", "36.7 °C")

                s1, s2 = st.columns([1, 1])
                with s1:
                    st.metric("Health Score", "85 / 100")
                    st.progress(85)
                    st.markdown(":green-badge[Good]")
                with s2:
                    st.markdown("**Body Condition**")
                    st.markdown(":green[●] Normal")
                    st.markdown(":green[●] Low Risk")
                    st.markdown(":green[●] Stable")


def _features():
    st.header("What BioLense Offers", divider="green")
    st.caption("From data to insights — everything you need to understand your health.")

    features = [
        (":material/psychology:", "AI Health Analysis",
         "Analyzes your health parameters using machine learning to find patterns and anomalies."),
        (":material/monitoring:", "Health Score",
         "Get an easy-to-understand score based on your submitted data."),
        (":material/description:", "Personalized Report",
         "Detailed report with insights, risk indicators and lifestyle recommendations."),
        (":material/chat:", "Ask AI Assistant",
         "Ask health-related questions and get clear, evidence-based answers."),
    ]
    cols = st.columns(4)
    for col, (icon, title, text) in zip(cols, features):
        with col.container(border=True, height=210):
            st.markdown(f"### {icon}")
            st.markdown(f"**{title}**")
            st.caption(text)


def _trust_strip():
    items = [
        (":material/groups:", "AI Powered", "Health Analysis"),
        (":material/schedule:", "24/7", "Accessible"),
        (":material/verified_user:", "Secure", "Your Data is Safe"),
        (":material/favorite:", "All-in-One", "Health Intelligence Platform"),
    ]
    with st.container(border=True):
        cols = st.columns(4)
        for col, (icon, title, sub) in zip(cols, items):
            col.markdown(f"{icon} **{title}**")
            col.caption(sub)


def home_page():
    _hero()
    _features()
    _trust_strip()
    st.caption(
        "BioLense AI is a screening tool and does not replace professional medical advice."
    )