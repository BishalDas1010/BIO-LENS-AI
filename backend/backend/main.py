from datetime import datetime
from typing import Optional

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="BioLens API")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
HISTORY: list = []
MAX_BYTES = 5 * 1024 * 1024


def detect_face(data: bytes) -> dict:
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(400, "Invalid image file")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
    if len(faces) == 0:
        return {"detected": False, "box": None}
    h, w = img.shape[:2]
    x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])
    return {
        "detected": True,
        "box": {"x": float(x / w), "y": float(y / h), "w": float(fw / w), "h": float(fh / h)},
    }


def indicator(name, value, status, note):
    return {"name": name, "value": value, "status": status, "note": note}


def screen(age, height, weight, hr, spo2, temp, symptoms):
    ind, recs = [], []

    bmi = round(weight / ((height / 100) ** 2), 1) if height and weight else None
    if bmi:
        if bmi < 18.5:
            ind.append(indicator("BMI", bmi, "watch", "Below the typical range"))
        elif bmi < 25:
            ind.append(indicator("BMI", bmi, "normal", "Within the typical range"))
        elif bmi < 30:
            ind.append(indicator("BMI", bmi, "watch", "Above the typical range"))
        else:
            ind.append(indicator("BMI", bmi, "attention", "Well above the typical range"))

    if hr is not None:
        if 60 <= hr <= 100:
            ind.append(indicator("Heart rate", f"{hr} bpm", "normal", "Typical resting range"))
        else:
            ind.append(indicator("Heart rate", f"{hr} bpm", "watch", "Outside 60-100 bpm resting range"))

    if spo2 is not None:
        if spo2 >= 95:
            ind.append(indicator("SpO2", f"{spo2}%", "normal", "Typical oxygen saturation"))
        elif spo2 >= 90:
            ind.append(indicator("SpO2", f"{spo2}%", "watch", "Slightly low"))
        else:
            ind.append(indicator("SpO2", f"{spo2}%", "attention", "Low - seek medical advice"))

    if temp is not None:
        if 36.1 <= temp <= 37.2:
            ind.append(indicator("Temperature", f"{temp} °C", "normal", "Typical body temperature"))
        elif temp <= 38.0:
            ind.append(indicator("Temperature", f"{temp} °C", "watch", "Slightly abnormal"))
        else:
            ind.append(indicator("Temperature", f"{temp} °C", "attention", "Fever range"))

    urgent = {"Chest Discomfort", "Shortness of Breath"}
    if urgent & set(symptoms):
        ind.append(indicator("Symptoms", ", ".join(symptoms), "attention",
                             "Chest discomfort or breathlessness can be serious"))
        recs.append("Seek medical attention promptly for chest discomfort or shortness of breath.")
    elif symptoms:
        ind.append(indicator("Symptoms", ", ".join(symptoms), "watch", "Reported symptoms"))

    if "Fatigue" in symptoms or "Poor Sleep" in symptoms:
        recs.append("Aim for regular sleep (7-9 hours), hydration and balanced meals.")
    if bmi and bmi >= 25:
        recs.append("Consider regular physical activity and a diet review with a professional.")
    if not recs:
        recs.append("Keep up healthy habits: activity, sleep, hydration, regular check-ups.")
    recs.append("If symptoms persist or worsen, consult a qualified doctor.")

    statuses = [i["status"] for i in ind]
    overall = "attention" if "attention" in statuses else "watch" if "watch" in statuses else "normal"
    return overall, ind, recs


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/detect-face")
async def detect(image: UploadFile = File(...)):
    data = await image.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "Image larger than 5MB")
    return detect_face(data)


@app.post("/api/analyze")
async def analyze(
    age: int = Form(...),
    gender: str = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    heart_rate: Optional[int] = Form(None),
    spo2: Optional[float] = Form(None),
    temperature: Optional[float] = Form(None),
    symptoms: str = Form(""),
    image: Optional[UploadFile] = File(None),
):
    face = None
    if image is not None:
        data = await image.read()
        if len(data) > MAX_BYTES:
            raise HTTPException(413, "Image larger than 5MB")
        face = detect_face(data)

    sym = [s.strip() for s in symptoms.split(",") if s.strip()]
    overall, indicators, recs = screen(age, height, weight, heart_rate, spo2, temperature, sym)
    result = {
        "id": len(HISTORY) + 1,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "overall": overall,
        "face_detected": face["detected"] if face else None,
        "indicators": indicators,
        "recommendations": recs,
        "disclaimer": "Screening indicators only. This is not a medical diagnosis.",
    }
    HISTORY.append(result)
    return result


@app.get("/api/history")
def history():
    return list(reversed(HISTORY))


class Chat(BaseModel):
    message: str


KB = {
    "spo2": "SpO2 is blood oxygen saturation. Around 95-100% is typical; below 90% needs medical attention.",
    "heart": "A typical resting heart rate for adults is about 60-100 bpm.",
    "bmi": "BMI = weight(kg) / height(m)^2. About 18.5-24.9 is the typical range.",
    "temperature": "Normal body temperature is about 36.1-37.2 °C. Above 38 °C is a fever.",
    "fatigue": "Fatigue has many causes, including sleep, stress and nutrition. See a doctor if it persists.",
}


@app.post("/api/chat")
def chat(body: Chat):
    text = body.message.lower()
    for key, answer in KB.items():
        if key in text:
            return {"reply": answer}
    return {"reply": "I can explain SpO2, heart rate, BMI, temperature or fatigue. I am not a substitute for a doctor."}
