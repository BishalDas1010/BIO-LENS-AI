import streamlit as st
import requests
import plotly.graph_objects as go
from assistant_page import assistant_page
from medicine_page import medicine_page
from homepage import home_page

st.set_page_config(page_title="BioLens - Body Condition", layout="wide")

# API URLs
API_URL = "http://127.0.0.1:8000/predict"
AI_API_URL = "http://127.0.0.1:8000" 

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { background: #0B1220; border-right: 1px solid #e5e7eb; }
    [data-testid="stSidebar"] > div:first-child { padding: 1.5rem 1rem; }

    .biolens-logo { text-align: center; padding: 5px 0 18px 0; }
    .biolens-logo h2 { margin: 0; font-size: 25px; font-weight: 700; color: #2f6bff; }
    .biolens-logo p { margin: 5px 0 0 0; font-size: 12px; color: #64748b; }

    [data-testid="stSidebar"] hr {
        margin: 5px 0 18px 0; border: none; border-top: 1px solid #e2e8f0;
    }

    .menu-title {
        margin: 0 0 8px 5px; color: #94a3b8; font-size: 11px;
        font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] { width: 100%; }
    [data-testid="stSidebar"] [data-testid="stRadio"] > div { gap: 5px; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child { display: none; }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        display: flex; align-items: center; width: 100%;
        padding: 11px 13px; margin: 3px 0; border-radius: 10px;
        background: transparent; color: #475569; font-size: 14px;
        font-weight: 500; cursor: pointer;
        transition: background 0.2s ease, color 0.2s ease, transform 0.2s ease;
        box-sizing: border-box;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #edf3ff; color: #2f6bff; transform: translateX(3px);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: #2f6bff; color: white; font-weight: 600;
        box-shadow: 0 4px 12px rgba(47, 107, 255, 0.20);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label p {
        margin: 0; padding: 0; color: inherit;
    }

    .sidebar-user {
        margin-top: 25px; padding: 12px; border-radius: 12px;
        background: white; border: 1px solid #e2e8f0;
        display: flex; align-items: center; gap: 10px;
    }
    .sidebar-user-icon {
        width: 35px; height: 35px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        background: #eaf0ff; font-size: 18px;
    }
    .sidebar-user-name { font-size: 13px; font-weight: 600; color: #1e293b; }
    .sidebar-user-status { font-size: 11px; color: #64748b; margin-top: 3px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# SIDEBAR
with st.sidebar:
    st.markdown(
        """
        <div class="biolens-logo">
            <h2>🌿 BioLens-AI</h2>
            <p>Your Personal Health Assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown('<div class="menu-title">Menu</div>', unsafe_allow_html=True)
    
    selected_page = st.radio(
        "Menu",
        [
            "🏠 Home",
            "❤️ Body Condition",
            "🫀 Heart Disease",
            "🧠 Mental Health",
            "💊 Medicine Information",
            "💬 AI Assistant",
            "📈 History",
        ],
        index=1,
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="sidebar-user">
            <div class="sidebar-user-icon">👤</div>
            <div class="sidebar-user-text">
                <div class="sidebar-user-name">My Health Profile</div>
                <div class="sidebar-user-status">● Health tracking active</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# WEB PAGES
# ==========================================

def body_condition_page():
    st.title("🩺 Body Condition Assessment")
    st.caption("Enter your health details and let AI analyze your body condition.")

    left, right = st.columns([1, 2], gap="large")

    with left:
        with st.container(border=True):
            st.subheader("📋 Enter Your Health Information")
            st.caption("Fill in your latest health measurements")

            age = st.number_input("Age (years)", min_value=1.0, max_value=120.0, value=22.0)
            sleep_hours = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, value=8.0, step=0.5)
            work_hours = st.number_input("Work Hours", min_value=0.0, max_value=24.0, value=8.0, step=0.5)
            screen_time = st.number_input("Screen Time (hours)", min_value=0.0, max_value=24.0, value=6.0, step=0.5)
            water_intake = st.number_input("Water Intake (L/day)", min_value=0.0, max_value=10.0, value=2.5, step=0.1)
            exercise = st.number_input("Exercise (times/week)", min_value=0.0, max_value=10.0, value=2.0, step=1.0)
            meals_per_day = st.number_input("Meals Per Day", min_value=1.0, max_value=10.0, value=3.0, step=1.0)
            caffeine_intake = st.number_input("Caffeine Intake", min_value=0.0, max_value=10.0, value=2.0, step=1.0)
            social_interaction = st.number_input("Social Interaction", min_value=0.0, max_value=10.0, value=3.0, step=1.0)
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=30.0, max_value=220.0, value=78.0, step=1.0)
            spo2 = st.number_input("SpO2 - Oxygen (%)", min_value=70.0, max_value=100.0, value=98.0, step=0.1)
            temperature = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, value=36.8, step=0.1)
            blood_pressure = st.number_input("Blood Pressure (Systolic)", min_value=50.0, max_value=250.0, value=138.0, step=1.0)
            cholesterol = st.number_input("Cholesterol", min_value=50.0, max_value=500.0, value=210.0, step=1.0)
            glucose = st.number_input("Blood Glucose - Fasting (mg/dL)", min_value=30.0, max_value=500.0, value=112.0, step=1.0)
            insulin = st.number_input("Insulin", min_value=0.0, max_value=500.0, value=22.0, step=1.0)

            analyze_clicked = st.button("📊 Analyze My Health", use_container_width=True)

    with right:
        if "prediction_result" not in st.session_state:
            st.session_state.prediction_result = None

        if analyze_clicked:
            payload = {
                "age": age, "sleep_hours": sleep_hours, "work_hours": work_hours, "screen_time": screen_time,
                "water_intake": water_intake, "exercise": exercise, "meals_per_day": meals_per_day,
                "caffeine_intake": caffeine_intake, "social_interaction": social_interaction, "heart_rate": heart_rate,
                "spo2": spo2, "temperature": temperature, "blood_pressure": blood_pressure,
                "cholesterol": cholesterol, "glucose": glucose, "insulin": insulin,
            }
            try:
                with st.spinner("Analyzing..."):
                    response = requests.post(API_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    st.session_state.prediction_result = response.json()
                    st.session_state.health_context = {"input": payload, "result": response.json()}
                else:
                    st.session_state.prediction_result = {"error": f"API error {response.status_code}: {response.text}"}
            except requests.exceptions.ConnectionError:
                st.session_state.prediction_result = {"error": "Cannot reach API. Is FastAPI running on http://127.0.0.1:8000 ?"}
            except Exception as e:
                st.session_state.prediction_result = {"error": f"{e}"}

        result = st.session_state.prediction_result

        with st.container(border=True):
            st.subheader("Overall Body Condition")
            if result is None:
                st.info("Fill in your details and click **Analyze My Health** to see results.")
            elif "error" in result:
                st.error(result["error"])
            else:
                pred, label, conf = result["prediction"], result["label"], result["confidence"]
                p0, p1 = result["probability_class_0"], result["probability_class_1"]

                c1, c2 = st.columns([2, 1], gap="large")
                with c1:
                    if pred == 1:
                        st.markdown("## :red[⚠️ At Risk]")
                        st.write("Your health indicators suggest an elevated risk. Please consult a doctor.")
                    else:
                        st.markdown("## :green[✅ No Risk]")
                        st.write("Your health indicators look normal. Keep up the healthy lifestyle!")

                def gauge(percent: float, color: str = "#22c55e"):
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number", value=percent * 100,
                        number={"suffix": "%", "font": {"size": 28}},
                        gauge={"axis": {"range": [0, 100], "tickwidth": 1}, "bar": {"color": color, "thickness": 0.28},
                               "bgcolor": "white", "borderwidth": 0, "steps": [{"range": [0, 100], "color": "#e5e7eb"}]},
                    ))
                    fig.update_layout(height=180, margin=dict(t=10, b=10, l=10, r=10))
                    return fig

                with c2:
                    st.metric("Confidence", f"{conf*100:.1f}%")
                    st.plotly_chart(gauge(conf), use_container_width=True, config={"displayModeBar": False})

                st.markdown("**Probability breakdown**")
                st.markdown(f"🟢 Class 0 (No Risk): **{p0*100:.1f}%**")
                st.progress(p0)
                st.markdown(f"🔴 Class 1 (At Risk): **{p1*100:.1f}%**")
                st.progress(p1)

        with st.container(border=True):
            st.subheader("Key Health Parameters")
            row1 = st.columns(3)
            with row1[0].container(border=True):
                st.caption("❤️ Heart Rate")
                st.markdown(f"### {heart_rate:.0f} bpm")
                st.markdown(":green[**Normal**]" if 60 <= heart_rate <= 100 else ":orange[**Check**]")
            with row1[1].container(border=True):
                st.caption("🩸 Blood Pressure")
                st.markdown(f"### {blood_pressure:.0f}")
                st.markdown(":green[**Normal**]" if blood_pressure < 130 else ":orange[**Elevated**]")
            with row1[2].container(border=True):
                st.caption("🫁 SpO2")
                st.markdown(f"### {spo2:.1f}%")
                st.markdown(":green[**Normal**]" if spo2 >= 95 else ":red[**Low**]")

            row2 = st.columns(3)
            with row2[0].container(border=True):
                st.caption("🌡️ Temperature")
                st.markdown(f"### {temperature:.1f}°C")
                st.markdown(":green[**Normal**]" if 36.1 <= temperature <= 37.2 else ":orange[**Check**]")
            with row2[1].container(border=True):
                st.caption("🩹 Glucose")
                st.markdown(f"### {glucose:.0f} mg/dL")
                st.markdown(":green[**Normal**]" if glucose < 100 else ":orange[**High**]")
            with row2[2].container(border=True):
                st.caption("🧪 Cholesterol")
                st.markdown(f"### {cholesterol:.0f}")
                st.markdown(":green[**Normal**]" if cholesterol < 200 else ":orange[**High**]")

        with st.container(border=True):
            h1, h2 = st.columns([3, 1])
            with h1:
                st.subheader("📄 Your Health Report")
                st.caption("Summary of your latest analysis.")
            with h2:
                st.button("⬇ Download PDF", use_container_width=True)

            if result and "error" not in result:
                st.table([
                    {"Parameter": "Prediction", "Result": result["label"]},
                    {"Parameter": "Confidence", "Result": f"{result['confidence']*100:.1f}%"},
                    {"Parameter": "Age", "Result": f"{age:.0f}"},
                    {"Parameter": "Heart Rate", "Result": f"{heart_rate:.0f} bpm"},
                    {"Parameter": "Blood Pressure", "Result": f"{blood_pressure:.0f}"},
                    {"Parameter": "SpO2", "Result": f"{spo2:.1f}%"},
                    {"Parameter": "Temperature", "Result": f"{temperature:.1f}°C"},
                    {"Parameter": "Glucose", "Result": f"{glucose:.0f} mg/dL"},
                    {"Parameter": "Cholesterol", "Result": f"{cholesterol:.0f}"},
                ])
            st.caption("This is a screening tool, not a medical diagnosis. Please consult a qualified doctor for medical advice.")


def heart_disease_page():
    st.title("🫀 Heart Disease")
    st.write("Heart disease risk assessment.")


def Mentalhelth():
    st.title("🧠 Mental Health Assessment")
    st.caption("A safe space to assess and track your mental wellness using clinically validated tools.")

    if 'mh_phq9' not in st.session_state: st.session_state.mh_phq9 = None
    if 'mh_gad7' not in st.session_state: st.session_state.mh_gad7 = None
    if 'mh_wellness' not in st.session_state: st.session_state.mh_wellness = None
    if 'mh_mood_score' not in st.session_state: st.session_state.mh_mood_score = None
    if 'ai_absolution' not in st.session_state: st.session_state.ai_absolution = None

    PHQ9_QS = [
        "Little interest or pleasure in doing things", "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much", "Feeling tired or having little energy",
        "Poor appetite or overeating", "Feeling bad about yourself",
        "Trouble concentrating on things", "Moving or speaking so slowly that other people could have noticed",
        "Thoughts that you would be better off dead or of hurting yourself"
    ]
    GAD7_QS = [
        "Feeling nervous, anxious, or on edge", "Not being able to stop or control worrying",
        "Worrying too much about different things", "Trouble relaxing", "Being so restless that it is hard to sit still",
        "Becoming easily annoyed or irritable", "Feeling afraid, as if something awful might happen"
    ]
    OPTS = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
    WELLNESS_OPTS = {
        "sleep": {"<5 hrs": 1, "5-6 hrs": 2, "7-8 hrs": 4, ">8 hrs": 3},
        "mood": {"Very Low": 0, "Low": 1, "Neutral": 2, "Good": 3, "Excellent": 4},
        "energy": {"Very Low": 0, "Low": 1, "Moderate": 2, "High": 3, "Very High": 4},
        "concentration": {"Very Poor": 0, "Poor": 1, "Fair": 2, "Good": 3, "Excellent": 4},
        "stress": {"Extremely": 0, "Very": 1, "Moderately": 2, "Slightly": 3, "Not at all": 4},
        "social": {"Very Uncomfortable": 0, "Uncomfortable": 1, "Neutral": 2, "Comfortable": 3, "Very Comfortable": 4}
    }

    def get_severity(score, is_phq):
        if score <= 4: return "Minimal"
        elif score <= 9: return "Mild"
        elif score <= 14: return "Moderate"
        elif is_phq and score <= 19: return "Moderately Severe"
        else: return "Severe"

    tab1, tab2, tab3, tab4 = st.tabs(["📋 1. Depression (PHQ-9)", "📋 2. Anxiety (GAD-7)", "🌿 3. Mood & Wellness", "📊 4. Final Absolution"])

    with tab1:
        st.subheader("PHQ-9 Depression Assessment")
        st.write("Over the **last 2 weeks**, how often have you been bothered by the following problems?")
        with st.form("mh_phq9_form"):
            answers = []
            for i, q in enumerate(PHQ9_QS):
                st.markdown(f"**{i+1}. {q}**")
                ans = st.radio(f"phq_q{i}", list(OPTS.keys()), key=f"mh_p_{i}", label_visibility="collapsed")
                answers.append(OPTS[ans])
                st.markdown("---")
            
            if st.form_submit_button("Save PHQ-9"):
                st.session_state.mh_phq9 = answers
                st.success("✅ PHQ-9 Saved! Please click on the Anxiety tab.")

    with tab2:
        st.subheader("GAD-7 Anxiety Assessment")
        if st.session_state.mh_phq9 is None:
            st.warning("⚠️ Please complete the PHQ-9 assessment in the first tab before continuing.")
        else:
            st.write("Over the **last 2 weeks**, how often have you been bothered by the following problems?")
            with st.form("mh_gad7_form"):
                answers = []
                for i, q in enumerate(GAD7_QS):
                    st.markdown(f"**{i+1}. {q}**")
                    ans = st.radio(f"gad_q{i}", list(OPTS.keys()), key=f"mh_g_{i}", label_visibility="collapsed")
                    answers.append(OPTS[ans])
                    st.markdown("---")
                
                if st.form_submit_button("Save GAD-7"):
                    st.session_state.mh_gad7 = answers
                    st.success("✅ GAD-7 Saved! Please click on the Mood tab.")

    with tab3:
        st.subheader("🌿 Mood & Emotional Wellness")
        if st.session_state.mh_gad7 is None:
            st.warning("⚠️ Please complete the GAD-7 assessment in the second tab before continuing.")
        else:
            with st.form("mh_wellness_form"):
                c1, c2 = st.columns(2)
                with c1:
                    sleep = st.selectbox("1. Average sleep hours?", list(WELLNESS_OPTS["sleep"].keys()))
                    mood = st.selectbox("2. Current mood?", list(WELLNESS_OPTS["mood"].keys()))
                    energy = st.selectbox("3. Energy level?", list(WELLNESS_OPTS["energy"].keys()))
                with c2:
                    concentration = st.selectbox("4. Concentration?", list(WELLNESS_OPTS["concentration"].keys()))
                    stress = st.selectbox("5. Stress level?", list(WELLNESS_OPTS["stress"].keys()))
                    social = st.selectbox("6. Social interactions?", list(WELLNESS_OPTS["social"].keys()))
                
                if st.form_submit_button("Calculate Mood Score"):
                    mood_score = (
                        WELLNESS_OPTS["sleep"][sleep] + WELLNESS_OPTS["mood"][mood] + 
                        WELLNESS_OPTS["energy"][energy] + WELLNESS_OPTS["concentration"][concentration] + 
                        WELLNESS_OPTS["stress"][stress] + WELLNESS_OPTS["social"][social]
                    )
                    st.session_state.mh_wellness = True
                    st.session_state.mh_mood_score = mood_score
                    st.success("✅ Mood Score Calculated! Please click on the Final Absolution tab.")

    with tab4:
        if st.session_state.mh_mood_score is None:
            st.info("Please complete all three assessment tabs to generate your final report.")
        else:
            p_score = sum(st.session_state.mh_phq9)
            g_score = sum(st.session_state.mh_gad7)
            mood_score = st.session_state.mh_mood_score
            p_sev = get_severity(p_score, True)
            g_sev = get_severity(g_score, False)

            # 1. SAFETY CHECK (HARD GUARDRAIL)
            safety_alert = st.session_state.mh_phq9[8] > 0
            if safety_alert:
                st.error("### ⚠️ URGENT SAFETY SUPPORT")
                st.markdown("""
                You indicated thoughts of self-harm. **You are not alone, and help is available right now.**
                *   **Tele-MANAS (India):** 14416 (Toll-Free, 24/7)
                *   **Emergency Services:** 112
                *   **If you are in immediate danger, please go to the nearest emergency room.**
                """)
                st.session_state.mental_health_context = {
                    "phq9_score": p_score, "gad7_score": g_score, "mood_score": mood_score, "safety_alert": True
                }
                st.stop()

            # 2. METRICS DISPLAY
            st.subheader("📊 Your Clinical Scores")
            c1, c2, c3 = st.columns(3)
            c1.metric("Depression (PHQ-9)", f"{p_score} / 27", f"{p_sev}")
            c2.metric("Anxiety (GAD-7)", f"{g_score} / 21", f"{g_sev}")
            
            mood_percentage = (mood_score / 24) * 100
            if mood_score >= 18: mood_sev = "Excellent"
            elif mood_score >= 13: mood_sev = "Good"
            elif mood_score >= 8: mood_sev = "Fair"
            else: mood_sev = "Poor"
            c3.metric("Mood Score", f"{mood_score} / 24", f"{mood_sev}")

            # Save to session state for the Chatbot to use
            st.session_state.mental_health_context = {
                "phq9_score": p_score, "phq9_severity": p_sev,
                "gad7_score": g_score, "gad7_severity": g_sev,
                "mood_score": mood_score, "mood_severity": mood_sev,
                "safety_alert": False
            }

            st.markdown("---")
            st.subheader("⚖️ Final Absolution (Generated by AI)")
            
            # 3. AI GENERATION
            if st.button("🤖 Generate AI Verdict"):
                with st.spinner("AI is analyzing your scores..."):
                    try:
                        payload = {
                            "phq9_score": p_score,
                            "gad7_score": g_score,
                            "mood_score": mood_score,
                            "safety_alert": False
                        }
                        response = requests.post(f"{AI_API_URL}/mental-health-absolution", json=payload, timeout=30)
                        
                        if response.status_code == 200:
                            st.session_state.ai_absolution = response.json()["absolution"]
                        else:
                            st.error(f"Failed to generate verdict. Server says: {response.text}")
                    except Exception as e:
                        st.error(f"Error connecting to AI: {e}")

            if st.session_state.ai_absolution:
                st.info(st.session_state.ai_absolution)
            else:
                st.write("Click the button above to let the BioLens AI analyze your results and give you a personalized verdict.")

            st.markdown("---")
            st.subheader("📈 Wellness Breakdown")
            
            norm_phq = (p_score / 27) * 100
            norm_gad = (g_score / 21) * 100
            norm_mood = 100 - mood_percentage

            fig = go.Figure(data=[
                go.Bar(name='Depression', x=['Score'], y=[norm_phq], marker_color='#ef4444'),
                go.Bar(name='Anxiety', x=['Score'], y=[norm_gad], marker_color='#f59e0b'),
                go.Bar(name='Mood Deficit', x=['Score'], y=[norm_mood], marker_color='#3b82f6')
            ])
            fig.update_layout(barmode='group', yaxis_title="Percentage (%)", title="Symptom Severity (Lower is Better)", height=300, margin=dict(t=40, b=20, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)

            st.warning("**Medical Disclaimer:** This tool does not provide medical diagnoses. Please consult a qualified healthcare professional for advice.")


def history_page():
    st.title("📈 History")
    st.write("View your previous health assessments.")


# ==========================================
# PAGE ROUTING
# ==========================================
PAGES = {
    "🏠 Home": home_page,
    "❤️ Body Condition": body_condition_page,
    "🫀 Heart Disease": heart_disease_page,
    "🧠 Mental Health": Mentalhelth,
    "💊 Medicine Information": medicine_page,
    "💬 AI Assistant": assistant_page,
    "📈 History": history_page,
}

if selected_page in PAGES:
    PAGES[selected_page]()
else:
    st.error(f"Page '{selected_page}' not found. Please check your navigation.")