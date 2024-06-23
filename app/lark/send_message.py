import requests
from .retrieve_lark_token import retrieve_lark_token_callback
import json

API_ENDPOINT = "https://open.larksuite.com/open-apis/im/v1/messages/?receive_id_type=email"

retrieve_lark_token = retrieve_lark_token_callback()

def send_message(email: str, message: str) -> bool:
    params = {"receive_id_type":"chat_id"}
    
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
    response = requests.request("POST", API_ENDPOINT, params=params, headers=headers, data=payload)
    try:
        result = response.json()
        response_code = result.get("code")
        return response_code == 0
    except requests.exceptions.JSONDecodeError:
        return False

def validate_email(email: str) -> bool:
    return send_message(email, "Successfully connected to smart-crm")