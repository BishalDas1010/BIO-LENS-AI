import streamlit as st

st.set_page_config(page_title="BioLens - Body Condition", page_icon="🩺", layout="wide")

# sidebar 
with st.sidebar:
    st.title("🌿 BioLens AI")
    st.caption("Your Personal Health Assistant")
    st.divider()
    st.radio(
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

# - page header
st.title("🩺 Body Condition Assessment")
st.caption("Enter your health details and let AI analyze your body condition.")

left, right = st.columns([1, 2], gap="large")

#  input form ----------------
with left:
    with st.container(border=True):
        st.subheader("📋 Enter Your Health Information")
        st.caption("Fill in your latest health measurements")

        st.number_input("Age (years)", value=22)
        st.radio("Gender", ["Male", "Female"], horizontal=True)
        st.number_input("Height (cm)", value=170)
        st.number_input("Weight (kg)", value=72)

        st.markdown("**Blood Pressure (Systolic / Diastolic)** - mmHg")
        bp1, bp2 = st.columns(2)
        bp1.number_input("Systolic", value=138)
        bp2.number_input("Diastolic", value=88)

        st.number_input("Heart Rate (bpm)", value=78)
        st.number_input("SpO2 - Oxygen (%)", value=98)
        st.number_input("Body Temperature (°C)", value=36.8)
        st.number_input("Blood Glucose - Fasting (mg/dL)", value=112)

        st.button("📊 Analyze My Health", type="primary", use_container_width=True)

# ---------------- RIGHT: results ----------------
with right:

    # Section 1: Overall Body Condition
    with st.container(border=True):
        st.subheader("📶 Overall Body Condition")
        c1, c2 = st.columns([2, 1], gap="large")
        with c1:
            st.markdown("## :orange[Moderate]")
            st.write(
                "Some parameters require attention. "
                "Maintain a healthy lifestyle and monitor your key indicators."
            )
        with c2:
            st.metric("Health Score", "68 / 100")
            st.progress(0.68)

    # Section 2: Key Health Parameters
    with st.container(border=True):
        st.subheader("💚 Key Health Parameters")

        row1 = st.columns(3)
        with row1[0].container(border=True):
            st.caption("⚖️ BMI")
            st.markdown("### 24.8")
            st.markdown(":green[**Normal**]")
        with row1[1].container(border=True):
            st.caption("🩸 Blood Pressure")
            st.markdown("### 138/88")
            st.markdown(":orange[**Elevated**]")
        with row1[2].container(border=True):
            st.caption("💓 Heart Rate")
            st.markdown("### 78 bpm")
            st.markdown(":green[**Normal**]")

        row2 = st.columns(3)
        with row2[0].container(border=True):
            st.caption("🫁 SpO2")
            st.markdown("### 98%")
            st.markdown(":green[**Normal**]")
        with row2[1].container(border=True):
            st.caption("🌡️ Temperature")
            st.markdown("### 36.8°C")
            st.markdown(":green[**Normal**]")
        with row2[2].container(border=True):
            st.caption("🩹 Glucose")
            st.markdown("### 112 mg/dL")
            st.markdown(":orange[**Slightly High**]")

    # Section 3: Your Health Report
    with st.container(border=True):
        h1, h2 = st.columns([3, 1])
        with h1:
            st.subheader("📄 Your Health Report")
            st.caption("Download a detailed PDF report of your analysis.")
        with h2:
            st.button("⬇ Download PDF", use_container_width=True)

        st.markdown("**BioLens AI - Health Assessment Report** &nbsp;&nbsp; _7 Oct 2024_")

        t1, t2 = st.columns([3, 2], gap="medium")
        with t1:
            st.table(
                [
                    {"Parameter": "Overall Condition", "Result": "Moderate"},
                    {"Parameter": "Health Score", "Result": "68 / 100"},
                    {"Parameter": "Age / Gender", "Result": "22 / Male"},
                    {"Parameter": "BMI", "Result": "24.8 (Normal)"},
                    {"Parameter": "Blood Pressure", "Result": "138/88 (Elevated)"},
                    {"Parameter": "Heart Rate", "Result": "78 bpm (Normal)"},
                    {"Parameter": "SpO2", "Result": "98% (Normal)"},
                    {"Parameter": "Temperature", "Result": "36.8°C (Normal)"},
                    {"Parameter": "Glucose", "Result": "112 mg/dL (Slightly High)"},
                ]
            )
        with t2:
            with st.container(border=True):
                st.markdown("**👁 Key Observations**")
                st.markdown("- Blood pressure is slightly elevated.")
                st.markdown("- Glucose level is higher than normal.")
                st.markdown("- Other parameters are within normal range.")
            with st.container(border=True):
                st.markdown("**💡 Suggestions**")
                st.markdown("- Follow a low-salt, balanced diet.")
                st.markdown("- Do regular physical activity.")
                st.markdown("- Monitor your health parameters.")
                st.markdown("- Consult a doctor if values remain high.")

        st.caption(
            "This is a screening tool, not a medical diagnosis. "
            "Please consult a qualified doctor for medical advice."
        )