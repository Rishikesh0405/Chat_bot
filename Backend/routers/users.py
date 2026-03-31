from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Backend.database import get_db
import bcrypt

router = APIRouter()

# ---------------- MODELS ----------------

class SignupData(BaseModel):
    username: str
    email: str
    phone: str
    password: str


class LoginData(BaseModel):
    login_id: str
    password: str


# ---------------- SIGNUP (ONLY NORMAL USERS) ----------------

@router.post("/signup")
def signup(data: SignupData):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE email=%s", (data.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = bcrypt.hashpw(
        data.password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        """
        INSERT INTO users (username, email, phone, password_hash, role)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (data.username, data.email, data.phone, hashed_password, "user")
    )

    db.commit()
    cursor.close()
    db.close()

    return {"message": "Account created successfully"}


# ---------------- LOGIN ----------------

@router.post("/login")
def login(data: LoginData):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # 🔥 Find user by email OR username OR phone
    cursor.execute(
        """
        SELECT * FROM users
        WHERE email=%s OR username=%s OR phone=%s
        """,
        (data.login_id, data.login_id, data.login_id)
    )

    user = cursor.fetchone()

    if not user:
        cursor.close()
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(
        data.password.encode(),
        user["password_hash"].encode()
    ):
        cursor.close()
        db.close()
        raise HTTPException(status_code=401, detail="Incorrect password")

    cursor.close()
    db.close()

    return {
        "message": "Login successful",
        "role": user["role"],
        "username": user["username"]
    }