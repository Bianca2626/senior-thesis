import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from supabase import create_client
from openai import OpenAI
app = FastAPI()
Supabase
supabase = create_client(
os.environ["SUPABASE_URL"],
os.environ["SUPABASE_SERVICE_KEY"]
)
Model API
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
response = client.responses.create(
model=MODEL_NAME,
input=request.message
)
return {
"reply": response.output_text
}

@app.post("/api/survey")
def submit_survey(request: SurveyRequest):
try:
supabase.table("survey_responses").insert({
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