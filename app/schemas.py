from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ImageUpdateRequest(BaseModel):
    title: str
    notes: str