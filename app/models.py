from pydantic import BaseModel


class Dialogue(BaseModel):
    speakerTag: int
    content: str

    def __str__(this):
        return f"Speaker {this.speakerTag}:\n{this.content}"

class Prompt(BaseModel):
    email: str
    transcript: str
    dialogues: list[Dialogue]