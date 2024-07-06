from typing import List
from pydantic import ValidationError
import requests

from retrieve_lark_token import retrieve_lark_token
from models import LarkChatHistory

def get_chat_history(chat_id: int) -> List[str]:
    url = f"https://open.larksuite.com/open-apis/im/v1/messages"
    params = {
        "container_id_type":"chat",
        "container_id": chat_id,
        "sort_type": "ByCreateTimeDesc",
        "page_size": 20
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

        return list(map(lambda item: item.body.content, chat_history.data.items))
    except requests.exceptions.JSONDecodeError:
        return []
    except ValidationError as e:
        return []