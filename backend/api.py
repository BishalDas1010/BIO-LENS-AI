from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path
from typing import Optional, List

from Chat_rag import chatbot
from medicine_agent import query_medicine, extract_medicines


BACKEND_DIR = Path(__file__).resolve().parent
MODEL_DIR = BACKEND_DIR.parent / "models"
model = joblib.load(MODEL_DIR / "health_model.pkl")
columns = joblib.load(MODEL_DIR / "model_columns.pkl")

app = FastAPI(title="BioLens Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- Schemas ----------------
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


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    health_context: Optional[dict] = None


class ChatResponse(BaseModel):
    reply: str


class MedicineRequest(BaseModel):
    medicine_name: str
    question: Optional[str] = ""


class MedicineResponse(BaseModel):
    reply: str


# ---------------- Routes ----------------
@app.get("/")
def root():
    return {"status": "ok", "service": "BioLens backend"}


@app.post("/predict")
def predict(data: HealthInput):
    df = pd.DataFrame([data.model_dump()])[columns]
    pred = int(model.predict(df)[0])
    prob = model.predict_proba(df)[0].tolist()
    return {
        "prediction": pred,
        "label": "AT RISK" if pred == 1 else "✅ NO RISK",
        "probability_class_0": round(prob[0], 4),
        "probability_class_1": round(prob[1], 4),
        "confidence": round(max(prob), 4),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    msgs = [m.model_dump() for m in req.messages]
    reply = chatbot(msgs, health_context=req.health_context)
    return {"reply": reply}


@app.post("/medicine", response_model=MedicineResponse)
def medicine_info(req: MedicineRequest):
    reply = query_medicine(req.medicine_name, req.question or "")
    return {"reply": reply}


@app.post("/medicine/scan")
async def medicine_scan(file: UploadFile = File(...)):
    image_bytes = await file.read()
    meds = extract_medicines(image_bytes)
    return {"medicines": meds}