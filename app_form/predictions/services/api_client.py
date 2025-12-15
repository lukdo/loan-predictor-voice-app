import requests
import os


# to call local:
# def get_prediction_from_api(payload: dict) -> dict:
    # try:
    #     response = requests.post(
    #         "http://127.0.0.1:8001/predict",
    #         json=payload,
    #         timeout=3,
    #     )
    #     response.raise_for_status()
    #     return response.json()
    # except Exception as e:
    #     print("API error:", e)
    #     return {}

# to call docker container use its name.
def get_prediction_from_api(payload: dict) -> dict:
    try:
        # response = requests.post("http://fastapi-backend:8001/predict", json=payload)
        response = requests.post("https://loan-backend-849346508536.europe-west1.run.app", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("API error:", e)
        return {}


BACKEND_BASE_URL = os.getenv(
    "BACKEND_BASE_URL",
    "https://loan-backend-849346508536.europe-west1.run.app/",  # default: Cloud Run URL
)

def predict(payload: dict) -> dict:
    url = f"{BACKEND_BASE_URL}/predict"
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()
