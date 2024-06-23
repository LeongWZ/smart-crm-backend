import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from gemini.generate import generate

from models import Prompt
from lark.send_message import send_message

load_dotenv()

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Welcome to smart-crm backend server"}


@app.post("/")
async def POST(prompt: Prompt, api_key: str = ""):
    if api_key != os.getenv('BACKEND_API_KEY'):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid API key.")
    
    generated_response = generate(prompt.transcript, prompt.dialogues)

    if not send_message(prompt.email, generated_response):
        raise HTTPException(status_code=404, detail="Failed to send message to lark. " + 
                            "Please provide the email you had registered with your Lark account")
    
    return { "message": "Succesfully generated" }