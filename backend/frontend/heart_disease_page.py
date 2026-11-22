import streamlit as st 


import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. PAGE CONFIG & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="BIO-LENS Mental Health", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    div[data-testid="stMetric"] {
        background-color: #ffffff; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stMetric"] label { color: #64748b !important; font-weight: 600; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #0ea5e9 !important; font-weight: 700; }
    .stButton > button {
        background-color: #0ea5e9; color: white; border-radius: 8px; border: none; 
        padding: 0.5rem 1rem; font-weight: 600; transition: all 0.3s ease; width: 100%;
    }
    .stButton > button:hover { background-color: #0284c7; box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3); }
    h1 { color: #0f172a; font-weight: 700; }
    h2, h3 { color: #1e293b; font-weight: 600; }
    .stAlert { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE LOGIC (SQLite)
# ==========================================
DB_NAME = "mental_health.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, phq9_score INTEGER, gad7_score INTEGER,
        sleep TEXT, mood TEXT, energy TEXT, concentration TEXT, stress TEXT, social TEXT)''')
    conn.commit()
    conn.close()

def save_assessment(p_score, g_score, w_data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO assessments (date, phq9_score, gad7_score, sleep, mood, energy, concentration, stress, social) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (datetime.now().strftime("%Y-%m-%d %H:%M"), p_score, g_score, w_data['sleep'], w_data['mood'], 
               w_data['energy'], w_data['concentration'], w_data['stress'], w_data['social']))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM assessments ORDER BY date ASC", conn)
    conn.close()
    return df

init_db()

# ==========================================
# 3. DATA & SCORING LOGIC
# ==========================================
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

def get_severity(score, is_phq):
    if score <= 4: return "Minimal"
    elif score <= 9: return "Mild"
    elif score <= 14: return "Moderate"
    elif is_phq and score <= 19: return "Moderately Severe"
    else: return "Severe"

# ==========================================
# 4. SESSION STATE INIT
# ==========================================
if 'page' not in st.session_state: st.session_state.page = "Home"
if 'phq9' not in st.session_state: st.session_state.phq9 = None
if 'gad7' not in st.session_state: st.session_state.gad7 = None
if 'wellness' not in st.session_state: st.session_state.wellness = None

# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🧠 BIO-LENS")
st.sidebar.markdown("Mental Health Module")
st.sidebar.markdown("---")
nav = st.sidebar.radio("Navigation", ["Home", "1. PHQ-9 (Depression)", "2. GAD-7 (Anxiety)", "3. Wellness Check", "4. Results & Progress"])

# ==========================================
# 6. PAGE ROUTING & UI
# ==========================================

# --- HOME PAGE ---
if nav == "Home":
    st.title("🏠 Welcome to BIO-LENS Mental Health")
    st.markdown("This is a safe space to assess and track your mental wellness.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 📋 PHQ-9\nDepression Assessment")
        if st.button("Start PHQ-9"): st.session_state.page = "1. PHQ-9 (Depression)"; st.rerun()
    with col2:
        st.info("### 📋 GAD-7\nAnxiety Assessment")
        if st.button("Start GAD-7"): st.session_state.page = "2. GAD-7 (Anxiety)"; st.rerun()
    with col3:
        st.info("### 🌿 Wellness\nLifestyle Check")
        if st.button("Start Wellness"): st.session_state.page = "3. Wellness Check"; st.rerun()
    
    st.markdown("---")
    st.subheader("📊 Your Latest Summary")
    df = get_history()
    if not df.empty:
        last = df.iloc[-1]
        c1, c2, c3 = st.columns(3)
        c1.metric("Last PHQ-9 Score", f"{last['phq9_score']} / 27")
        c2.metric("Last GAD-7 Score", f"{last['gad7_score']} / 21")
        c3.metric("Date", str(last['date']).split()[0])
    else:
        st.info("No previous assessments found.")

# --- PHQ-9 PAGE ---
elif nav == "1. PHQ-9 (Depression)":
    st.title("📋 PHQ-9 Depression Assessment")
    st.markdown("Over the **last 2 weeks**, how often have you been bothered by the following?")
    
    with st.form("phq9_form"):
        answers = []
        for i, q in enumerate(PHQ9_QS):
            st.markdown(f"**{i+1}. {q}**")
            ans = st.radio(f"q{i}", list(OPTS.keys()), key=f"p_{i}", label_visibility="collapsed")
            answers.append(OPTS[ans])
            st.markdown("---")
        
        if st.form_submit_button("Save & Next"):
            st.session_state.phq9 = answers
            st.session_state.page = "2. GAD-7 (Anxiety)"
            st.rerun()

# --- GAD-7 PAGE ---
elif nav == "2. GAD-7 (Anxiety)":
    if st.session_state.phq9 is None:
        st.warning("Please complete the PHQ-9 first.")
        st.stop()
        
    st.title("📋 GAD-7 Anxiety Assessment")
    st.markdown("Over the **last 2 weeks**, how often have you been bothered by the following?")
    
    with st.form("gad7_form"):
        answers = []
        for i, q in enumerate(GAD7_QS):
            st.markdown(f"**{i+1}. {q}**")
            ans = st.radio(f"g{i}", list(OPTS.keys()), key=f"g_{i}", label_visibility="collapsed")
            answers.append(OPTS[ans])
            st.markdown("---")
            
        if st.form_submit_button("Save & Next"):
            st.session_state.gad7 = answers
            st.session_state.page = "3. Wellness Check"
            st.rerun()

# --- WELLNESS PAGE ---
elif nav == "3. Wellness Check":
    if st.session_state.gad7 is None:
        st.warning("Please complete the GAD-7 first.")
        st.stop()
        
    st.title("🌿 Emotional Wellness Check")
    with st.form("wellness_form"):
        sleep = st.selectbox("1. Average sleep hours?", ["<5 hrs", "5-6 hrs", "7-8 hrs", ">8 hrs"])
        mood = st.selectbox("2. Current mood?", ["Very Low", "Low", "Neutral", "Good", "Excellent"])
        energy = st.selectbox("3. Energy level?", ["Very Low", "Low", "Moderate", "High", "Very High"])
        concentration = st.selectbox("4. Concentration?", ["Very Poor", "Poor", "Fair", "Good", "Excellent"])
        stress = st.selectbox("5. Stress level?", ["Not at all", "Slightly", "Moderately", "Very", "Extremely"])
        social = st.selectbox("6. Social interactions?", ["Very Uncomfortable", "Uncomfortable", "Neutral", "Comfortable", "Very Comfortable"])
        
        if st.form_submit_button("Submit & View Results"):
            st.session_state.wellness = {"sleep": sleep, "mood": mood, "energy": energy, "concentration": concentration, "stress": stress, "social": social}
            
            # Save to Database
            save_assessment(sum(st.session_state.phq9), sum(st.session_state.gad7), st.session_state.wellness)
            st.session_state.page = "4. Results & Progress"
            st.rerun()

# --- RESULTS & PROGRESS PAGE ---
elif nav == "4. Results & Progress":
    if st.session_state.wellness is None:
        st.warning("Please complete the assessments first.")
        st.stop()
        
    st.title("📊 Assessment Results")
    
    p_score = sum(st.session_state.phq9)
    g_score = sum(st.session_state.gad7)
    p_sev = get_severity(p_score, True)
    g_sev = get_severity(g_score, False)
    
    # --- SAFETY SYSTEM (Q9 CHECK) ---
    if st.session_state.phq9[8] > 0:
        st.error("### ⚠️ URGENT SAFETY SUPPORT")
        st.markdown("""
        You indicated thoughts of self-harm. **You are not alone, and help is available right now.**
        *   **Tele-MANAS (India):** 14416 (Toll-Free, 24/7)
        *   **Emergency Services:** 112
        *   **If you are in immediate danger, please go to the nearest emergency room.**
        """)
        st.stop()
        
    # --- METRICS ---
    c1, c2 = st.columns(2)
    c1.metric("PHQ-9 Score (Depression)", f"{p_score} / 27", f"Severity: {p_sev}")
    c2.metric("GAD-7 Score (Anxiety)", f"{g_score} / 21", f"Severity: {g_sev}")
    
    st.markdown("---")
    
    # --- RECOMMENDATIONS ---
    st.subheader("💡 Personalized Recommendations")
    if p_sev in ["Minimal", "Mild"] and g_sev in ["Minimal", "Mild"]:
        st.info("**Depression/Anxiety:** Maintain healthy routines. Continue regular exercise and sleep.")
    elif p_sev in ["Moderate", "Moderately Severe"] or g_sev == "Moderate":
        st.warning("**Depression/Anxiety:** Consider professional mental health support. Maintain a structured daily routine.")
    else:
        st.error("**Depression/Anxiety:** Prompt professional assessment is highly encouraged. Please reach out to a healthcare provider.")
        
    st.markdown("---")
    st.subheader("📈 Historical Progress")
    
    df = get_history()
    if len(df) > 1:
        df_melted = df.melt(id_vars=['date'], value_vars=['phq9_score', 'gad7_score'], var_name='Type', value_name='Score')
        df_melted['Type'] = df_melted['Type'].map({'phq9_score': 'Depression (PHQ-9)', 'gad7_score': 'Anxiety (GAD-7)'})
        
        fig = px.line(df_melted, x='date', y='Score', color='Type', markers=True, 
                      title="Score Trends Over Time", color_discrete_sequence=["#0ea5e9", "#38bdf8"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Complete another assessment later to see progress trends.")
        
    st.warning("**Medical Disclaimer:** This tool does not provide medical diagnoses. Please consult a qualified healthcare professional for advice.")