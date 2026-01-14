from fastapi import APIRouter
from pydantic import BaseModel

# 👇 YAHAN PASTE KARO
from dotenv import load_dotenv
import os
from google.genai import Client

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

router = APIRouter()

client = Client(api_key=GOOGLE_API_KEY)

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",   # ✅ WORKING MODEL
            contents=req.message
        )
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"❌ Gemini Error: {str(e)}"}
