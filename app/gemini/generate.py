import os
import google.generativeai as genai
from dotenv import load_dotenv

from models import Dialogue

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

def generate(transcript: str, dialogues: list[Dialogue]):
    dialogues_str = "\n".join(map(lambda dialogue: str(dialogue), dialogues))

    response = model.generate_content(
        "You are a Smart Sales Helper integrated within a Customer Relationship Management system\n" +
        "Your task is to help a salesperson by generating narrative recommendations using based on the context and previous answers.\n" +
        f"Transcript: {transcript}\n{dialogues_str}"
    )

    return response.text
