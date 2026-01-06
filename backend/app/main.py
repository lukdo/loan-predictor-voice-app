from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.inference import predict_from_payload

import json
import time

from google.api_core.exceptions import ServiceUnavailable
from google import genai
from google.genai import types


# === Existing prediction schema ===
class PredictionRequest(BaseModel):
    annual_income: float | None = None
    debt_to_income_ratio: float | None = None
    credit_score: float | None = None
    loan_amount: float | None = None
    interest_rate: float | None = None
    gender: str | None = None
    marital_status: str | None = None
    education_level: str | None = None
    employment_status: str | None = None
    loan_purpose: str | None = None
    grade_subgrade: str | None = None


app = FastAPI()

# --- CORS so Django frontend can call this API ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can restrict if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Gemini client (uses GEMINI_API_KEY env var) ---
client = genai.Client()


# ========= EXISTING PREDICT ENDPOINT =========
@app.post("/predict")
def predict(request: PredictionRequest):
    payload = request.dict()
    result = predict_from_payload(payload)
    return result


# ========= NEW VOICE ENDPOINT =========
@app.post("/voice-form")
async def voice_form(audio: UploadFile = File(...)):
    """
    Receives an audio file, sends it to Gemini, gets structured JSON with:
    annual_income, debt_to_income_ratio, credit_score, loan_amount,
    interest_rate, gender, marital_status, education_level,
    employment_status, loan_purpose, grade_subgrade.
    """

    # --- read audio from upload ---
    try:
        audio_bytes = await audio.read()
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="No audio data received")
    except Exception as e:
        print("Error reading audio:", e)
        raise HTTPException(status_code=400, detail="Error reading uploaded audio")

    mime_type = audio.content_type or "audio/webm"

    # --- define JSON schema expected from Gemini ---
    schema = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "annual_income": types.Schema(
                type=types.Type.NUMBER,
                description="Yearly gross income in euros.",
                nullable=True,
            ),
            "debt_to_income_ratio": types.Schema(
                type=types.Type.NUMBER,
                description="Debt-to-income ratio as a number (e.g. 0.15 for 15%).",
                nullable=True,
            ),
            "credit_score": types.Schema(
                type=types.Type.NUMBER,
                description="Credit score as a number (e.g. 736).",
                nullable=True,
            ),
            "loan_amount": types.Schema(
                type=types.Type.NUMBER,
                description="Loan amount in euros.",
                nullable=True,
            ),
            "interest_rate": types.Schema(
                type=types.Type.NUMBER,
                description="Interest rate in percent (e.g. 13.67).",
                nullable=True,
            ),
            "name_surname": types.Schema(
                type=types.Type.STRING,
                description="Full name of the applicant, e.g. 'John Doe'.",
                nullable=True,
            ),
            "gender": types.Schema(
                type=types.Type.STRING,
                description='One of "Male", "Female", "Other", or null.',
                nullable=True,
            ),
            "marital_status": types.Schema(
                type=types.Type.STRING,
                description='One of "Single", "Married", "Divorced", "Separated", "Widowed", or null.',
                nullable=True,
            ),
            "education_level": types.Schema(
                type=types.Type.STRING,
                description='One of "High School", "Bachelor\'s", "Master\'s", "PhD", "Other", or null.',
                nullable=True,
            ),
            "employment_status": types.Schema(
                type=types.Type.STRING,
                description='One of "Employed", "Unemployed", "Self-employed", "Retired", "Student", "Other", or null.',
                nullable=True,
            ),
            "loan_purpose": types.Schema(
                type=types.Type.STRING,
                description='One of "Debt consolidation", "Car", "Home improvement", "Education", "Medical", "Vacation", "Other", or null.',
                nullable=True,
            ),
            "grade_subgrade": types.Schema(
                type=types.Type.STRING,
                description='Grade/subgrade label like "C3", "D3", "F1", etc.',
                nullable=True,
            ),
        },
    )

    prompt = """
You are an assistant that processes a short voice note about a credit application.

The user describes themselves and their loan request in English, saying things like:
- their income (per month or per year),
- their debt-to-income ratio (if any),
- their credit score,
- the loan amount,
- the interest rate,
- their name,
- gender,
- marital status,
- education level,
- employment status,
- the purpose of the loan,
- and possibly a grade/subgrade like C3, D3, F1, etc.

Your job:

1. Understand the audio.
2. Extract the information into this JSON structure:
   - annual_income: yearly gross income in euros (if the user gives monthly income, multiply by 12).
   - debt_to_income_ratio: as a number (e.g. 0.15 for 15%).
   - credit_score: numeric credit score (e.g. 736).
   - loan_amount: loan amount in euros.
   - interest_rate: interest rate in percent (e.g. 13.67).
   - name_surname: full name of the applicant if explicitly mentioned (e.g. "John Doe").
   - gender: "Male", "Female", "Other", or null.
   - marital_status: "Single", "Married", "Divorced", "Separated", "Widowed", or null.
   - education_level: "High School", "Bachelor's", "Master's", "PhD", "Other", or null.
   - employment_status: "Employed", "Unemployed", "Self-employed", "Retired", "Student", "Other", or null.
   - loan_purpose: "Debt consolidation", "Car", "Home improvement", "Education", "Medical", "Vacation", "Other", or null.
   - grade_subgrade: grade/subgrade string like "C3", "D3", "F1", etc.

If a field is not mentioned, set it to null.
If the user gives a percentage like "16.1%", set interest_rate = 16.1.
If they say "I make 3,000 per month", set annual_income = 3000 * 12.

Return ONLY valid JSON matching the schema.
"""

    # --- retry logic around Gemini call (handles 503 / overload) ---
    max_retries = 3
    backoff_seconds = 2
    response = None

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",  # lighter / more stable
                contents=[
                    types.Content(
                        parts=[
                            types.Part(text=prompt),
                            types.Part.from_bytes(
                                data=audio_bytes,
                                mime_type=mime_type,
                            ),
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                ),
            )
            # success → break out of loop
            break
        except ServiceUnavailable as e:
            # 503 UNAVAILABLE: model overloaded
            print(f"Gemini ServiceUnavailable on attempt {attempt}: {e}")
            if attempt == max_retries:
                raise HTTPException(
                    status_code=503,
                    detail="Voice model is temporarily overloaded. Please try again in a moment.",
                )
            # simple backoff: 2s, 4s, 6s
            time.sleep(backoff_seconds * attempt)
        except Exception as e:
            # other error: no retry
            print("Error calling Gemini:", e)
            raise HTTPException(
                status_code=500,
                detail=f"Error calling Gemini API: {e}",
            )

    if response is None:
        # should not happen, but just in case
        raise HTTPException(
            status_code=500,
            detail="No response from Gemini after retries.",
        )

    # --- parse JSON returned by Gemini ---
    try:
        json_str: str = response.text
        data = json.loads(json_str)
    except Exception as e:
        print("Error parsing Gemini response:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON from Gemini: {e}",
        )

    return data
