import os
from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
from pydantic import ValidationError
from gemini.generate import generate, generate_reply

from models import LarkRequest, Prompt
from lark.send_message import reply_message, send_message
from lark.get_chat_history import get_chat_history

# Uncomment the following lines to connect to ngrok for development purposes
#from connect_to_ngrok import connect_to_ngrok
#connect_to_ngrok()

load_dotenv()

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Welcome to smart-crm backend server"}


@app.post("/")
async def POST(prompt: Prompt, api_key: str = ""):
    if api_key != os.getenv('BACKEND_API_KEY'):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid API key.")
    
    generated_response = generate(prompt.transcripts)

    if not send_message(prompt.email, generated_response):
        raise HTTPException(status_code=404, detail="Failed to send message to lark. " + 
                            "Please provide the email you had registered with your Lark account")
    
    return { "message": "Succesfully generated" }

@app.post("/lark")
async def lark(request: Request):
    body: dict = await request.json()

    try:
        lark_request: LarkRequest = LarkRequest.model_validate(body)
        message = lark_request.event.message
        if (message.message_type == "text"):
            chat_history = get_chat_history(message.chat_id)
            generated_reply = generate_reply(message.content, chat_history)
            reply_message(
                lark_request.event.message.message_id,
                generated_reply
            )
    except ValidationError as e: 
        pass

    return { "challenge": body.get("challenge") }

@app.post("/validate")
async def validate(email: str = "", api_key: str = ""):
    if api_key != os.getenv('BACKEND_API_KEY'):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid API key.")

    if not send_message(email, "Succesfully connected to smart-crm"):
        raise HTTPException(status_code=404, detail="Failed to send message to lark. " + 
                            "Please provide the email you had registered with your Lark account")
    
    return { "message": "Succesfully connected to smart-crm" }