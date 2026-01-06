import os
import requests

# Inside docker, Django can reach FastAPI using the docker-compose service name.
BACKEND_BASE_URL = os.getenv(
    "BACKEND_BASE_URL",
    "http://fastapi-backend:8001"  # docker-to-docker
)

def predict(payload: dict) -> dict:
    url = f"{BACKEND_BASE_URL}/predict"
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("API error:", e)
        return {}



# Used for cloud:

# to call docker container use its name.
# def get_prediction_from_api(payload: dict) -> dict:
#     try:
#         # response = requests.post("http://fastapi-backend:8001/predict", json=payload)
#         response = requests.post("https://loan-backend-849346508536.europe-west1.run.app", json=payload)
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         print("API error:", e)
#         return {}
