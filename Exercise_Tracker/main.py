import requests
from datetime import datetime
import os


APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
WEIGHT_KG = os.getenv("WEIGHT_KG")
HEIGHT_CM = os.getenv("HEIGHT_KG")
AGE = 23
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

exercise_endpoint = os.getenv("exercise_endpoint")
sheety_endpoint = os.getenv("sheety_endpoint")

exercise_text = input("What did you do today?\n")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

params = {
    "query": exercise_text,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(exercise_endpoint, json=params, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheety_header = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

for exercise in result["exercises"]:
    sheet_input = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": f"{exercise['duration_min']} min",
            "calories": exercise["nf_calories"]
        }
    }
    sheet_response = requests.post(
        sheety_endpoint,
        json=sheet_input,
        headers=sheety_header)

    print(sheet_response.text)
