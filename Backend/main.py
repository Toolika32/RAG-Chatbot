from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatbot import get_answer


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message": "RAG chatbot is running!"
    }


@app.post("/ask")
def ask_question(data: Question):


    answer = get_answer(data.question)


    return {
        "question": data.question,
        "answer": answer
    }