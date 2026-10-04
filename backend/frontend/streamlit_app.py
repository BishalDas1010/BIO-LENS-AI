import streamlit as st
import requests
import plotly.graph_objects as go
from assistant_page import assistant_page


st.set_page_config(
    page_title="BioLens - Body Condition",layout="wide")
#api url 
API_URL = "http://127.0.0.1:8000/predict"


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

#side bar
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
            "🩸 Diabetes & Face Scan",
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

# web pages
def home_page():
    st.title("🏠 Home")
    st.write("Welcome to BioLens- AI.")


def body_condition_page():
    st.title("🩺 Body Condition Assessment")
    st.caption("Enter your health details and let AI analyze your body condition.")

    left, right = st.columns([1, 2], gap="large")

    #  LEFT: INPUT FORM 
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

    # RIGHT: RESULTS
    with right:
        # Placeholder state for results
        if "prediction_result" not in st.session_state:
            st.session_state.prediction_result = None

        # Call the API when button is clicked
        if analyze_clicked:
            payload = {
                "age": age,
                "sleep_hours": sleep_hours,
                "work_hours": work_hours,
                "screen_time": screen_time,
                "water_intake": water_intake,
                "exercise": exercise,
                "meals_per_day": meals_per_day,
                "caffeine_intake": caffeine_intake,
                "social_interaction": social_interaction,
                "heart_rate": heart_rate,
                "spo2": spo2,
                "temperature": temperature,
                "blood_pressure": blood_pressure,
                "cholesterol": cholesterol,
                "glucose": glucose,
                "insulin": insulin,
            }
            try:
                with st.spinner("Analyzing..."):
                    response = requests.post(API_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    st.session_state.prediction_result = response.json()
                    st.session_state.health_context = {
                            "input": payload,
                            "result": response.json()}



                else:
                    st.session_state.prediction_result = {
                        "error": f"API error {response.status_code}: {response.text}"
                    }
            except requests.exceptions.ConnectionError:
                st.session_state.prediction_result = {
                    "error": " Cannot reach API. Is FastAPI running on http://127.0.0.1:8000 ?"
                }
            except Exception as e:
                st.session_state.prediction_result = {"error": f"{e}"}

        result = st.session_state.prediction_result

        # ---------- Section 1: Overall Body Condition ----------
        with st.container(border=True):
            st.subheader("Overall Body Condition")

            if result is None:
                st.info("Fill in your details and click **Analyze My Health** to see results.")
            elif "error" in result:
                st.error(result["error"])
            else:
                pred = result["prediction"]
                label = result["label"]
                conf = result["confidence"]
                p0 = result["probability_class_0"]
                p1 = result["probability_class_1"]

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
                        mode="gauge+number",
                        value=percent * 100,
                        number={"suffix": "%", "font": {"size": 28}},
                        gauge={
                            "axis": {"range": [0, 100], "tickwidth": 1},
                            "bar": {"color": color, "thickness": 0.28},
                            "bgcolor": "white",
                            "borderwidth": 0,
                            "steps": [{"range": [0, 100], "color": "#e5e7eb"}],
                        },
                    ))
                    fig.update_layout(height=180, margin=dict(t=10, b=10, l=10, r=10))
                    return fig

                with c2:
                    st.metric("Confidence", f"{conf*100:.1f}%")
                    st.plotly_chart(gauge(conf), use_container_width=True, config={"displayModeBar": False})

               

                # Probability bars
                st.markdown("**Probability breakdown**")
                st.markdown(f"🟢 Class 0 (No Risk): **{p0*100:.1f}%**")
                st.progress(p0)
                st.markdown(f"🔴 Class 1 (At Risk): **{p1*100:.1f}%**")
                st.progress(p1)

        # Key Health Parameters 
        with st.container(border=True):
            st.subheader("Key Health Parameters")

            row1 = st.columns(3)
            with row1[0].container(border=True):
                st.caption("❤️ Heart Rate")
                st.markdown(f"### {heart_rate:.0f} bpm")
                status = ":green[**Normal**]" if 60 <= heart_rate <= 100 else ":orange[**Check**]"
                st.markdown(status)
            with row1[1].container(border=True):
                st.caption("🩸 Blood Pressure")
                st.markdown(f"### {blood_pressure:.0f}")
                status = ":green[**Normal**]" if blood_pressure < 130 else ":orange[**Elevated**]"
                st.markdown(status)
            with row1[2].container(border=True):
                st.caption("🫁 SpO2")
                st.markdown(f"### {spo2:.1f}%")
                status = ":green[**Normal**]" if spo2 >= 95 else ":red[**Low**]"
                st.markdown(status)

            row2 = st.columns(3)
            with row2[0].container(border=True):
                st.caption("🌡️ Temperature")
                st.markdown(f"### {temperature:.1f}°C")
                status = ":green[**Normal**]" if 36.1 <= temperature <= 37.2 else ":orange[**Check**]"
                st.markdown(status)
            with row2[1].container(border=True):
                st.caption("🩹 Glucose")
                st.markdown(f"### {glucose:.0f} mg/dL")
                status = ":green[**Normal**]" if glucose < 100 else ":orange[**High**]"
                st.markdown(status)
            with row2[2].container(border=True):
                st.caption("🧪 Cholesterol")
                st.markdown(f"### {cholesterol:.0f}")
                status = ":green[**Normal**]" if cholesterol < 200 else ":orange[**High**]"
                st.markdown(status)

        #Section 3: Health Report
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

            st.caption(
                "This is a screening tool, not a medical diagnosis. "
                "Please consult a qualified doctor for medical advice."
            )


def heart_disease_page():
    st.title("Heart Disease")
    st.write("Heart disease risk assessment.")


def diabetes_page():
    st.title(" Diabetes & Face Scan")
    st.write("Diabetes assessment and facial analysis.")


def medicine_page():
    st.title(" Medicine Information")
    st.write("Get information about medicines.")



def history_page():
    st.title("History")
    st.write("View your previous health assessments.")


# PAGE ROUTING
PAGES = {
    "🏠 Home": home_page,
    "❤️ Body Condition": body_condition_page,
    "🫀 Heart Disease": heart_disease_page,
    "🩸 Diabetes & Face Scan": diabetes_page,
    "💊 Medicine Information": medicine_page,
    "💬 AI Assistant": assistant_page,
    "📈 History": history_page,
}

PAGES[selected_page]()