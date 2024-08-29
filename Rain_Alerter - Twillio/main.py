import requests
from twilio.rest import Client
import os

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")

API_KEY = os.getenv("API_KEY")
LAT = 57.233190
LONG = 29.829330

parameters = {
    "lat": LAT,
    "lon": LONG,
    "appid": API_KEY,
    "cnt": 4,
}

response = requests.get("https://api.openweathermap.org/data/2.5/forecast",params=parameters)
response.raise_for_status()

weather_data = response.json()

will_rain = False

for data in weather_data["list"]:
    weather_codes = data["weather"][0]["id"]
    if int(weather_codes) < 700:
        will_rain = True
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today, remember to bring an umbrella! ☔",
        from_='+14054447869',
        to='+389071270713'
    )

    print(message.status)
