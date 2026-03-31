from pydantic import BaseModel
from typing import Optional
from datetime import datetime
# FAQ MODELS
class FAQCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "general"


class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None


class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str
    category: str
    created_at: datetime
    updated_at: datetime

# USER MODELS (Optional future safe)

class UserLogin(BaseModel):
    email: str
    password: str


class UserSignup(BaseModel):
    username: str
    email: str
    phone: str
    password: str