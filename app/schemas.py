from pydantic import BaseModel


class Message(BaseModel):
    content: str



class MessageView(BaseModel):
    content: str
    counter: int

    class Config:
        orm_mode = True