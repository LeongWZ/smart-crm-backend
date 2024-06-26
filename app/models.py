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