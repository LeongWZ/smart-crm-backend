import requests
from .retrieve_lark_token import retrieve_lark_token_callback
import json

retrieve_lark_token = retrieve_lark_token_callback()

def send_message(email: str, message: str) -> bool:
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
        result = response.json()
        response_code = result.get("code")
        return response_code == 0
    except requests.exceptions.JSONDecodeError:
        return False

def reply_message(message_id: int, message: str) -> bool:
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
        result = response.json()
        response_code = result.get("code")
        return response_code == 0
    except requests.exceptions.JSONDecodeError:
        return False