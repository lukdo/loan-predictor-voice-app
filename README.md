# Loan Payback Predictor — Voice Autofill + ML Inference
**Django · FastAPI · Gemini · Docker · Cloud Run**

End-to-end prototype of a loan repayment prediction web application.

The application combines:
- a **Django frontend** for data entry and result display,
- a **FastAPI backend** for ML inference and voice processing,
- the **Gemini API** to extract structured loan data from a short voice recording.

The system was deployed and tested on Google Cloud Run.
To avoid ongoing cloud costs, the live demo is not permanently running, but the full setup is reproducible locally.

---

## What the application does

1. The user records a short voice note describing their loan situation
2. The audio is sent to the backend
3. Gemini converts the audio into structured JSON
4. The frontend form is automatically filled
5. The user submits the form
6. The backend returns a loan payback prediction

The focus of this project is **applied machine learning and system integration**.

---

## High-level architecture

```
Browser (HTML + JS)
        |
        |  POST /voice-form (audio)
        v
FastAPI backend
        |
        |  Gemini API (audio → structured JSON)
        v
Autofilled form (Django)
        |
        |  POST /predict (JSON payload)
        v
ML inference → prediction → UI
```

---

## Services

### Frontend — Django (`app_form/`)
- Renders the loan application form
- Displays prediction results
- Calls backend `/predict` server-side
- Calls backend `/voice-form` from browser JavaScript

### Backend — FastAPI (`backend/`)
- `POST /predict`: returns loan payback prediction
- `POST /voice-form`: accepts audio, returns structured fields extracted by Gemini

---

## Input fields

The system works with the following information:

**Financial**
- `annual_income`
- `debt_to_income_ratio`
- `credit_score`
- `loan_amount`
- `interest_rate`
- `grade_subgrade`

**Demographics**
- `gender`
- `marital_status`
- `education_level`
- `employment_status`

**Loan**
- `loan_purpose`

**UI-only**
- `name_surname` (also extracted from voice)

---

## Run locally (Docker)

You need to run **two services**.

### 1) Backend (FastAPI) — port `8001`

Create an environment file:

`backend/.env`
```env
GEMINI_API_KEY=your_key_here
```

Start the backend:

```bash
cd backend
docker compose up -d --build
docker compose logs -f
```

Test:
- http://localhost:8001/docs

---

### 2) Frontend (Django) — port `8000`

Start the frontend:

```bash
cd app_form
docker compose up -d --build
docker compose logs -f
```

Open in browser:
- http://localhost:8000/predict/

---

## Reliability notes

- The Gemini API can occasionally return `503 UNAVAILABLE` (model overload)
- The backend implements retries and graceful error handling
- The system is designed to fail safely and inform the user

---

## Project structure

```
app_form/     # Django frontend
backend/      # FastAPI backend (inference + voice processing)
models/       # model scripts / artifacts
notebooks/    # experimentation and exploration
raw_data/     # dataset samples
```

---

## Deployment

The application was deployed as two independent services on **Google Cloud Run**:
- Django frontend service
- FastAPI backend service

The deployment setup is documented in the repository and can be reproduced in a few commands.
The services are currently shut down to avoid unnecessary cloud costs.

---

## Why this project

This project demonstrates:
- Designing an end-to-end ML-powered web application
- Using LLMs for structured data extraction (voice → JSON)
- Separating frontend, inference, and orchestration concerns
- Deploying stateless services on a serverless platform
- Handling real-world issues (CORS, CSRF, API limits, retries)
- Making cost-aware engineering decisions
