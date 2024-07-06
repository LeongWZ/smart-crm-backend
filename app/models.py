from typing import List, Optional
from pydantic import BaseModel


class Transcript(BaseModel):
    speakerTag: int
    startTime: str
    endTime: str
    content: str

    def __str__(this):
        return f"[{this.startTime} - {this.endTime}] Speaker {this.speakerTag}:\n{this.content}"

class Prompt(BaseModel):
    email: str
    transcripts: list[Transcript]

class LarkUserId(BaseModel):
    union_id: str
    user_id: str
    open_id: str

class LarkRequest(BaseModel):
    class Header(BaseModel):
        event_id: str
        token: str
        create_time: str
        event_type: str
        tenant_key: str
        app_id: str

    class Event(BaseModel):
        class Message(BaseModel):
            chat_id: str
            chat_type: str
            content: str
            create_time: str
            message_id: str
            message_type: str
            update_time: str

        class Sender(BaseModel):
            class SenderID(BaseModel):
                open_id: str
                union_id: str
                user_id: str

            sender_id: SenderID
            sender_type: str
            tenant_key: str

        message: Message
        sender: Sender

    schema: str
    header: Header
    event: Event