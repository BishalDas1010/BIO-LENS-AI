from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path
from pydantic import BaseModel
import pandas as pd
from typing import Optional, List
from Chat_rag import chatbot   


# Load model 
BACKEND_DIR = Path(__file__).resolve().parent
MODEL_DIR = BACKEND_DIR.parent / "models"
model = joblib.load(MODEL_DIR / "health_model.pkl")
columns = joblib.load(MODEL_DIR / "model_columns.pkl")

app = FastAPI(title="Health Risk Predictor")


class ChatMessage(BaseModel):
    role: str        # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    health_context: Optional[dict] = None   # {"input": {...}, "result": {...}}


class ChatResponse(BaseModel):
    reply: str

#  Input schema 
class HealthInput(BaseModel):
    age: float
    sleep_hours: float
    work_hours: float
    screen_time: float
    water_intake: float
    exercise: float
    meals_per_day: float
    caffeine_intake: float
    social_interaction: float
    heart_rate: float
    spo2: float
    temperature: float
    blood_pressure: float
    cholesterol: float
    glucose: float
    insulin: float




@app.post("/predict")
def predict(data: HealthInput):
    # Build DataFrame with correct column order
    df = pd.DataFrame([data.dict()])[columns]

    pred = int(model.predict(df)[0])
    prob = model.predict_proba(df)[0].tolist()
    confidence = float(max(prob))

    return {
        "prediction": pred,
        "label": "AT RISK" if pred == 1 else "✅ NO RISK",
        "probability_class_0": round(prob[0], 4),
        "probability_class_1": round(prob[1], 4),
        "confidence": round(confidence, 4),
    }

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    msgs = [m.dict() for m in req.messages]
    reply = chatbot(msgs, health_context=req.health_context)
    return {"reply": reply}
