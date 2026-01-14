import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Absolute path setup taaki file kahin se bhi access ho sake
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_FILE = os.path.join(BASE_DIR, "users.json")

class User(BaseModel):
    username: str
    email: str
    phone: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except: return []

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

@router.post("/login")
def login(data: LoginData):
    users = load_users()
    for u in users:
        if u["email"] == data.email and u["password"] == data.password:
            return {"message": "Login success", "user": u}
    raise HTTPException(status_code=401, detail="Invalid email or password")

@router.post("/signup")
def signup(user: User):
    users = load_users()
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
    users.append(user.model_dump())
    save_users(users)
    return {"message": "Signup success"}