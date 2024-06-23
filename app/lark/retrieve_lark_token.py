import requests
import os
from typing import Optional
import datetime as dt
from datetime import datetime, timedelta

class Token:
    def __init__(this, lark_token: str, expires_at: dt):
        this.lark_token = lark_token
        this.expires_at = expires_at

    def is_expired(this):
        return datetime.now(dt.UTC) >= this.expires_at

def obtain_lark_token()-> Optional[Token]:
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    r = requests.post(
        url,
        headers={
            "Content-Type": "application/json; charset=utf-8"
        },
        json={
            "app_id": os.getenv('LARK_APP_ID'),
            "app_secret": os.getenv('LARK_APP_SECRET')
        }
    )

    try:
        result = r.json()
        tenant_access_token = result.get("tenant_access_token", "")
        expires_at = datetime.now(dt.UTC) + timedelta(seconds=result.get("expire", 0) - 60)
        return Token(tenant_access_token, expires_at)
    except requests.exceptions.JSONDecodeError:
        return None

def retrieve_lark_token_callback():
    token: Optional[Token] = None    # cache token

    def helper() -> str:
        nonlocal token
        
        if token is None or token.is_expired():
            token = obtain_lark_token()
        
        return token.lark_token
    
    return helper
