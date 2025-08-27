# main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class chatRequest(BaseModel):
    message: str = Field(description="The message to be processed")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def chat_endpoint(request: chatRequest):
    response_message = f"Received your message: {request.message}"
    return {"response": response_message}

