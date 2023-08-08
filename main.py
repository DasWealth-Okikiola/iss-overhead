import time
import requests
import datetime as time_module
from twilio.rest import Client

My_lat = float("your latitude")
My_long = float("your longitude")

twilio_auth_token = "Your twilio auth token"
twilio_sid = "your twilio sid"
twilio_phone_number = "your twilio phone number"
to = "your receiver  phone"

def is_iss_nearby():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_position = (iss_longitude, iss_latitude)
    print(iss_position)
    # Your position is within +5 or -5 degrees
    if My_lat-5 <= iss_latitude <= My_lat+5 and My_long-5 <= iss_longitude <= My_long+5:
        return True


def is_it_nighttime():
    parameters = {
        "lat": My_lat,
        "lng": My_long,
        "formatted": 0}

    info = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    info.raise_for_status()
    info_data = info.json()
    sunrise_hour = int(info_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(info_data["results"]["sunset"].split("T")[1].split(":")[0])

    today = time_module.datetime.now()
    hour = today.hour
    if hour >= sunset_hour or hour <= sunrise_hour:
        return True


while True:
    time.sleep(60)
    if is_iss_nearby() and is_it_nighttime():
        msg="Look UP\n\n The ISS is above you in the skye!🌠"
        client = Client(twilio_sid, twilio_auth_token)
        message = client.messages.create(
            from_=twilio_phone_number,
            body=msg,
            to=to
        )
        print(message.status)
