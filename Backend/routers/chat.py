from fastapi import APIRouter
from pydantic import BaseModel
from Backend.database import get_db
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="Backend/.env")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use working model
model = genai.GenerativeModel("gemini-2.5-flash")

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    username: str


# 🔥 Improved FAQ Matching
def search_faq_mysql(user_query: str):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT question, answer FROM faqs")
    rows = cursor.fetchall()

    cursor.close()
    db.close()

    user_query = user_query.lower()

    # 🔥 stop words remove
    stop_words = ["what", "is", "the", "of", "a", "an", "for", "to", "in"]
    query_words = [word for word in user_query.split() if word not in stop_words]

    # 🔥 important keywords (HIGH PRIORITY)
    important_keywords = [
        "fees", "fee", "cost",
        "location", "address",
        "principal",
        "hod",
        "it", "cs",
        "name"
    ]

    best_match = None
    max_score = 0

    for row in rows:
        question = row["question"].lower()
        question_words = question.split()

        score = 0

        for word in query_words:
            # 🔥 HIGH PRIORITY MATCH
            if word in important_keywords and word in question_words:
                score += 5

            # normal match
            elif word in question_words:
                score += 2

            # partial match
            elif word in question:
                score += 1

        if score > max_score:
            max_score = score
            best_match = row

    return best_match

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()

        return None

    except Exception as e:
        print("Gemini Error:", str(e))
        return None


@router.post("/chat")
def chat(req: ChatRequest):

    user_query = req.message
    username = req.username

    faq = search_faq_mysql(user_query)

    # ✅ CASE 1: FAQ FOUND → POLISH ANSWER
    if faq:

        polish_prompt = f"""
You are Unibot, a friendly college assistant.

Rewrite this information clearly and professionally:
{faq['answer']}

Do not change meaning. Keep short and natural.
"""

        reply = ask_gemini(polish_prompt)

        if not reply:
            reply = faq["answer"]

    # ✅ CASE 2: FAQ NOT FOUND → NORMAL CHAT WITH PERSONALITY
    else:

        normal_prompt = f"""
You are Unibot, a friendly and helpful college assistant.

Guidelines:
- Always introduce yourself as Unibot if greeting.
- Keep tone friendly.
- Answer clearly and shortly.

User message:
{user_query}
"""

        reply = ask_gemini(normal_prompt)

        if not reply:
            reply = "I'm not sure about that. Please contact the college office."

    # Save chat
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO user_queries (username, query_text, bot_response)
            VALUES (%s, %s, %s)
        """, (username, user_query, reply))

        db.commit()
        cursor.close()
        db.close()

    except Exception as e:
        print("DB Save Error:", e)

    return {"reply": reply}