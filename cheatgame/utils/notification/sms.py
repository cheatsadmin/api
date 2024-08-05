import json

import requests
from config.django.base import  PANEL_SMS_URL , PANEL_SMS_PASS , PANEL_SMS_USER

def send_sms(*, to: str, otp: str, pattern: str):
    url = PANEL_SMS_URL
    data = {
        "username": PANEL_SMS_USER,
        "password": PANEL_SMS_PASS,
        "from": "+983000505",
        "to": to,
        "pattern_code": pattern,
        "input_data": json.dumps({"verfication-code": f"{otp}"})
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url = url , params=data , headers=headers)
    return response.content

