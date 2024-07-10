from typing import List
from pydantic import BaseModel


class Transcript(BaseModel):
    speakerTag: int
    startTime: str
    endTime: str
    content: str

    def __str__(this):
        return f"[{this.startTime} - {this.endTime}] Speaker {this.speakerTag}: {this.content}"

class Prompt(BaseModel):
    email: str
    transcripts: list[Transcript]

class LarkUserId(BaseModel):
    union_id: str
    user_id: str
    open_id: str

class LarkMessage(BaseModel):
    class Sender(BaseModel):
        id: str
        id_type: str
        sender_type: str
        tenant_key: str

    class Body(BaseModel):
        content: str

    body: Body
    chat_id: str
    create_time: str
    deleted: bool
    message_id: str
    msg_type: str
    sender: Sender
    update_time: str
    updated: bool

    def __str__(self):
        if self.deleted:
            return f"Deleted message"
        
        return f"{self.sender.sender_type}: {self.body.content}"

class LarkRequest(BaseModel):
    class Header(BaseModel):
        event_id: str
        token: str
        create_time: str
        event_type: str
        tenant_key: str
        app_id: str

    class Event(BaseModel):
        class EventMessage(BaseModel):
            chat_id: str
            chat_type: str
            content: str
            create_time: str
            message_id: str
            message_type: str
            update_time: str

        class EventSender(BaseModel):
            class SenderID(BaseModel):
                open_id: str
                union_id: str
                user_id: str

            sender_id: SenderID
            sender_type: str
            tenant_key: str

        message: EventMessage
        sender: EventSender

    schema: str
    header: Header
    event: Event

class LarkChatHistory(BaseModel):
    class Data(BaseModel):
        has_more: bool
        items: List[LarkMessage]
        page_token: str

    code: int
    data: Data
    msg: str