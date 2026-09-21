import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from supabase import create_client
from openai import OpenAI

load_dotenv()
app = FastAPI()

# Supabase
supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"]
)

# OpenAI
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

MODEL_NAME = os.environ["MODEL_NAME"]


class ChatRequest(BaseModel):
    message: str


class SurveyRequest(BaseModel):
    applicant_id: str | None = None
    answers: dict


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        response = client.responses.create(
            model=MODEL_NAME,
            instructions="""
            You are a supportive conversational assistant.
            Respond briefly and conversationally.
            Ask one thoughtful follow-up question at a time.
            """,
            input=request.message
        )

        return {
            "reply": response.output_text
        }

    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=500,
            detail="Could not generate response."
        )


@app.post("/api/survey")
def submit_survey(request: SurveyRequest):
    try:
        supabase.table("chatbot_responses").insert({
            "applicant_id": request.applicant_id,
            "answers": request.answers
        }).execute()

        return {"success": True}

    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=500,
            detail="Could not save survey."
        )