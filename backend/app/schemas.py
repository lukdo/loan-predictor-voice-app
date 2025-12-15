from pydantic import BaseModel

class PredictionRequest(BaseModel):
    id: int
    annual_income: float
    debt_to_income_ratio: float
    credit_score: float
    loan_amount: float
    interest_rate: float
    gender: str
    marital_status: str
    education_level: str
    employment_status: str
    loan_purpose: str
    grade_subgrade: str
