import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "models" / "loan_pipeline_model.pkl"

model = joblib.load(MODEL_PATH)

def predict_from_payload(payload: dict):
    df = pd.DataFrame([payload])

    pred_proba = model.predict_proba(df)[0, 1]   # probability loan IS paid back (1)
    pred_class = model.predict(df)[0]            # 0 or 1

    return {
        "approved": bool(pred_class),
        "probability": round(float(pred_proba) * 100, 2)
    }
