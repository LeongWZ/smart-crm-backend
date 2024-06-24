from openai import OpenAI
import os
from dotenv import load_dotenv

from models import Dialogue

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate(transcript: str, dialogues: list[Dialogue]):
    dialogues_str = "\n".join(map(lambda dialogue: str(dialogue), dialogues))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are a Smart Sales Helper integrated within a Customer Relationship Management system\n" +
                    "Your task is to help a salesperson by generating narrative recommendations using based on the context and previous answers."
            },
            {
                "role": "user",
                "content": f"Transcript: {transcript}\n{dialogues_str}"
            }
        ]
    )

    return completion.choices[0].message.content