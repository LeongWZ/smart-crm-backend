import os
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

from models import Transcript

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 512,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

def generate(transcripts: list[Transcript]):
    transcripts_str = "\n".join(map(lambda transcript: str(transcript), transcripts))

    response = model.generate_content(
        "You are a Smart Sales Helper integrated within a Customer Relationship Management system\n" +
        "Your task is to help a salesperson by generating narrative recommendations using based on the context and previous answers.\n" +
        f"Transcript:\n{transcripts_str}\n" +
        "Your response should meet the following requirements : " +
        "1. No bolded words. " +
        "2. Headers to be numbered and limited to 3. " +
        "3. Sub-pointers should be in bullet form. " +
        "4. Sub-pointers should not be bolded." +
        "5. May only use up to 350 characters."
    )

    processed_text = response.text.replace("**", "").replace("*", "-")

    return processed_text

def generate_reply(user_input: str, chat_history: List[str] = []):
    response = model.generate_content(
        "You are a Smart Sales Helper integrated within a Customer Relationship Management system\n" +
        "Your task is to assist a salesperson based on his input and chat history\n" +
        f"Chat History:\n{"\n".join(chat_history)}\n" +
        f"Input:\n{user_input}\n" +
        "Your response should meet the following requirements : " +
        "1. May only use up to 500 characters."
    )

    processed_text = response.text.replace("**", "").replace("*", "-")

    return processed_text
