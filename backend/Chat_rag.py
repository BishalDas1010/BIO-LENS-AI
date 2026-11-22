from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph import add_messages
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


#LLM + Graph 
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=API_KEY,
)


class ChatState(TypedDict):
    message: Annotated[list[BaseMessage], add_messages]


def node_one(state: ChatState):
    response = llm.invoke(state["message"])
    return {"message": [response]}


graph = StateGraph(ChatState)
graph.add_node("node_one", node_one)
graph.add_edge(START, "node_one")
graph.add_edge("node_one", END)
graph = graph.compile()

def chatbot(messages: list[dict], health_context: dict | None = None, mental_health_context: dict | None = None) -> str:
    """
    messages:        [{"role": "user"|"assistant", "content": "..."}]
    health_context:  optional body condition context
    mental_health_context: optional mental health scores
    Returns the assistant reply as a string.
    """
    system_prompt = (
        "You are BioLens AI, a friendly health & lifestyle assistant. "
        "Answer briefly and clearly. Never give a medical diagnosis. "
        "If the question is serious, advise the user to consult a doctor."
    )

    # 1. Add Body Condition Context
    if health_context:
        inp = health_context.get("input", {}) or {}
        res = health_context.get("result", {}) or {}
        system_prompt += f"""

The user has just completed a body-condition assessment in the BioLens app.
Use the data below when relevant. Do NOT invent numbers.

[Measurements]
- Age: {inp.get('age')}
- Sleep: {inp.get('sleep_hours')} h
- Work: {inp.get('work_hours')} h
- Screen: {inp.get('screen_time')} h
- Water: {inp.get('water_intake')} L
- Exercise: {inp.get('exercise')}/week
- Meals/day: {inp.get('meals_per_day')}
- Caffeine: {inp.get('caffeine_intake')}
- Social: {inp.get('social_interaction')}
- Heart rate: {inp.get('heart_rate')} bpm
- SpO2: {inp.get('spo2')} %
- Temp: {inp.get('temperature')} °C
- BP: {inp.get('blood_pressure')}
- Cholesterol: {inp.get('cholesterol')}
- Glucose: {inp.get('glucose')}
- Insulin: {inp.get('insulin')}

[Prediction]
- Result: {res.get('label')}
- Confidence: {res.get('confidence')}
- P(No risk): {res.get('probability_class_0')}
- P(At risk): {res.get('probability_class_1')}
"""

    # 2. Add Mental Health Context (FIXED)
    if mental_health_context:
        p_score = mental_health_context.get('phq9_score', 0)
        p_sev = mental_health_context.get('phq9_severity', 'Unknown')
        g_score = mental_health_context.get('gad7_score', 0)
        g_sev = mental_health_context.get('gad7_severity', 'Unknown')
        m_score = mental_health_context.get('mood_score', 0)
        
        system_prompt += f"""
        
[MENTAL HEALTH ASSESSMENT]
The user recently completed a mental health test. Use this to be highly empathetic.
- Depression (PHQ-9): {p_score}/27 (Severity: {p_sev})
- Anxiety (GAD-7): {g_score}/21 (Severity: {g_sev})
- Mood Score: {m_score}/24

Rule: If they ask about depression or their scores, provide supportive, non-medical advice (e.g., breathing exercises, routine, therapy). Do NOT prescribe medication.
"""
        
        # Safety override
        if mental_health_context.get('safety_alert'):
            system_prompt += """
            \n[CRITICAL SAFETY ALERT]
            The user indicated thoughts of self-harm on Question 9 of the PHQ-9.
            You MUST prioritize their safety. Tell them they are not alone.
            Immediately provide the Tele-MANAS (14416) and Emergency (112) numbers.
            """

    # Build LangChain message list
    lc_messages: list[BaseMessage] = [SystemMessage(content=system_prompt)]
    for m in messages:
        role = m.get("role")
        content = m.get("content", "")
        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))

    result = graph.invoke({"message": lc_messages})
    return result["message"][-1].content

def generate_absolution(phq9, gad7, mood, safety_alert):
    # Guardrail 1: Immediate safety crisis override
    if safety_alert or phq9 >= 20:
        return "⚠️ URGENT: Your scores indicate severe distress. Please reach out immediately to Tele-MANAS (14416) or Emergency Services (112)."

    prompt = f"""
    You are an empathetic mental health AI.
    User Scores:
    - PHQ-9 (Depression): {phq9}/27
    - GAD-7 (Anxiety): {gad7}/21
    - Mood Score: {mood}/24

    Provide a 3-sentence supportive summary. 
    Rule 1: Do NOT diagnose.
    Rule 2: Do NOT recommend medication.
    Rule 3: Suggest actionable lifestyle or professional support steps.
    """

    try:
        # FIX: Use the LangChain 'llm' object you initialized at the top, instead of 'client'
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        # Print the actual error to the backend terminal for debugging
        print(f"Error generating absolution: {e}")
        # Fallback response if the external AI API is rate-limited or offline
        return f"Based on your scores (Depression: {phq9}, Anxiety: {gad7}, Mood: {mood}), we recommend focusing on rest and structured routines. Consider speaking with a counselor if these feelings persist."