from typing import Optional
import requests
import json

from models import LarkMessage
from retrieve_lark_token import retrieve_lark_token

def send_message(email: str, message: str) -> Optional[LarkMessage]:
    url = "https://open.larksuite.com/open-apis/im/v1/messages/"
    params = {"receive_id_type":"email"}
    
    msgContent = {
        "text": message,
    }
    req = {
        "receive_id": email,
        "msg_type": "text",
        "content": json.dumps(msgContent)
    }
    payload = json.dumps(req)
    headers = {
        'Authorization': f"Bearer {retrieve_lark_token()}", # your access token
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, params=params, headers=headers, data=payload)
    try:
        result: dict = response.json()
        return result.get("data")
    except requests.exceptions.JSONDecodeError:
        return None

def reply_message(message_id: str, message: str) -> Optional[LarkMessage]:
    url = f"https://open.larksuite.com/open-apis/im/v1/messages/{message_id}/reply"
    
    msgContent = {
        "text": message,
    }
    req = {
        "msg_type": "text",
        "content": json.dumps(msgContent)
    }
    payload = json.dumps(req)
    headers = {
        'Authorization': f"Bearer {retrieve_lark_token()}", # your access token
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        result: dict = response.json()
        return result.get("data")
    except requests.exceptions.JSONDecodeError:
        return None