from typing import TypedDict, Annotated, List
import os
import json
import re
import base64
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import (
    BaseMessage, HumanMessage, SystemMessage,
)
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

load_dotenv()
API_KEY = os.getenv("API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")



tavily_wrapper = TavilySearchAPIWrapper(
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)
tavily_tool = TavilySearchResults(max_results=5, api_wrapper=tavily_wrapper)


#  LLM 
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=API_KEY,
)
llm_with_tools = llm.bind_tools([tavily_tool])


#  State
class MedicineState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


#  Nodes 
def agent_node(state: MedicineState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def tool_node(state: MedicineState):
    return ToolNode([tavily_tool]).invoke(state)


def should_continue(state: MedicineState):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END


#  Graph 
graph = StateGraph(MedicineState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")
medicine_agent = graph.compile()


#  Prompt 
MEDICINE_SYSTEM_PROMPT = """You are the BioLens Medicine Information Assistant.
The user will ask about a specific medicine.

Use Tavily to search for:
- Uses / indications (Pros)
- Common side effects
- Serious risks / contraindications (Cons)
- Drug interactions

Reply with EXACTLY these headings:
**Uses (Pros)**
**Common Side Effects**
**Serious Risks (Cons)**
**Drug Interactions**
**Sources**

In Sources, list each entry as `[n] Title - URL`, one per line.
Never invent sources. If a source can't be found, say so.
End with: "This is not medical advice. Consult a doctor or pharmacist."
"""


# Public function 
def query_medicine(medicine_name: str, question: str = "") -> str:
    user_query = f"Medicine: {medicine_name}"
    if question:
        user_query += f"\nUser question: {question}"

    messages = [
        SystemMessage(content=MEDICINE_SYSTEM_PROMPT),
        HumanMessage(content=user_query),
    ]

    result = medicine_agent.invoke({"messages": messages})
    return result["messages"][-1].content



vision_llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",   # vision-capable
    temperature=0.0,
    api_key=API_KEY,
)


OCR_PROMPT = """You are a medical prescription reader.
Extract ONLY the names of the medicines written on this prescription.
Return a plain JSON array of strings, nothing else.
Example: ["Ibuprofen", "Metformin", "Amoxicillin"]
If you cannot read any medicines, return [].
"""


def extract_medicines(image_bytes: bytes) -> List[str]:
    """Read medicine names off a prescription image using Groq Vision."""
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    message = HumanMessage(
        content=[
            {"type": "text", "text": OCR_PROMPT},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
            },
        ]
    )

    try:
        response = vision_llm.invoke([message])
        text = response.content.strip()
    except Exception:
        return []

    # Pull the JSON array out of the LLM's reply
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        return []

    try:
        meds = json.loads(match.group(0))
        return [m.strip() for m in meds if isinstance(m, str) and m.strip()]
    except Exception:
        return []