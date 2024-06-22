import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to smart-crm backend server"}

class Dialogue(BaseModel):
    speakerTag: int
    content: str

class Prompt(BaseModel):
    api_key: str
    transcript: str
    dialogues: list[Dialogue]

@app.post("/")
async def generate(prompt: Prompt):
    print(prompt)
    if prompt.api_key != os.getenv('BACKEND_API_KEY'):
        raise HTTPException(status_code=401, detail="Unauthorized: invalid API key.")
    return { "message": "Succesfully generated" }