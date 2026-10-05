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


def chatbot(messages: list[dict], health_context: dict | None = None) -> str:
    """
    messages:        [{"role": "user"|"assistant", "content": "..."}]
    health_context:  optional {"input": {...}, "result": {...}}
    Returns the assistant reply as a string.
    """
    system_prompt = (
        "You are BioLens AI, a friendly health & lifestyle assistant. "
        "Answer briefly and clearly. Never give a medical diagnosis. "
        "If the question is serious, advise the user to consult a doctor."
    )

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