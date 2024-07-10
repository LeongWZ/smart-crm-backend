import json
from typing import List
from pydantic import ValidationError
import requests

from retrieve_lark_token import retrieve_lark_token
from models import LarkChatHistory, LarkMessage

def get_chat_history(chat_id: str) -> List[LarkMessage]:
    url = f"https://open.larksuite.com/open-apis/im/v1/messages"
    params = {
        "container_id_type":"chat",
        "container_id": chat_id,
        "sort_type": "ByCreateTimeDesc",
        "page_size": 15
    }
    
    headers = {
        'Authorization': f"Bearer {retrieve_lark_token()}", # your access token
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, params=params, headers=headers)
    try:
        result = response.json()
        response_code = result.get("code")
        if response_code != 0:
            return []
        
        chat_history = LarkChatHistory.model_validate(result)

        return chat_history.data.items[::-1]
    except requests.exceptions.JSONDecodeError:
        return []
    except ValidationError as e:
        return []
    
def item_to_string(item: LarkMessage):
    if item.deleted:
        return f"Deleted message"
    content: dict = json.loads(item.body.content)
    return f"{item.sender.sender_type}: {content.get("text", "Empty message")}"
