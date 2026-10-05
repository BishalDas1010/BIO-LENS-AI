# BioLens AI

BioLens AI is a health screening and wellness assistant that combines machine learning, conversational AI, and medical information tools into one application. The project helps users assess their body condition, understand health risks, ask health questions, and look up medicine details.

## Features

- Body condition assessment using health metrics and an ML model
- Heart disease risk prediction with model-based scoring
- AI health assistant for lifestyle and wellness guidance
- Medicine lookup and prescription-based medicine extraction
- Diabetes and face-scan UI sections for future health analysis extensions

## Tech Stack

- Frontend: Streamlit
- Backend: FastAPI
- ML: scikit-learn, joblib, pandas, numpy
- AI: LangChain, LangGraph, Groq
- Computer vision: OpenCV, MediaPipe
- Visualization: Matplotlib, Plotly

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your Groq API key to a `.env` file:

```bash
API_KEY=your_groq_api_key_here
```

4. Start the backend:

```bash
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

5. Start the frontend in a second terminal:

```bash
streamlit run backend/frontend/streamlit_app.py
```

The Streamlit app is configured to call the backend at `http://127.0.0.1:8000`, so the FastAPI server must be running before opening the UI.

## Main API Endpoints

- `POST /predict` — health-risk prediction from lifestyle and biometrics
- `POST /chat` — health assistant conversation
- `POST /medicine` — medicine information lookup
- `POST /medicine/scan` — prescription image medicine extraction

## Notes

- This application is intended for screening, education, and health awareness support.
- It is not a substitute for professional medical diagnosis or treatment.
- Some AI features depend on valid environment credentials and external model access.

