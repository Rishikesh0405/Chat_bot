from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers import users, chat

app = FastAPI()

# root endpoint
@app.get("/")
def home():
    return {"message": "FastAPI backend running successfully!"}

# include routers
app.include_router(users.router, prefix="/users")
app.include_router(chat.router, prefix="/bot")
