from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routers import users, chat
from Backend.routers.faq_admin import router as faq_admin_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running"}

# IMPORTANT
app.include_router(users.router, prefix="/users")
app.include_router(chat.router, prefix="/bot")
app.include_router(faq_admin_router)