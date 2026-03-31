from fastapi import APIRouter, HTTPException
from Backend.database import get_db

router = APIRouter(prefix="/admin", tags=["Admin FAQ"])


# ---------------- GET ALL FAQS ----------------
@router.get("/faqs")
def get_all_faqs():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM faqs ORDER BY id DESC")
    faqs = cursor.fetchall()

    cursor.close()
    db.close()

    return faqs


# ---------------- CREATE FAQ ----------------
@router.post("/faqs")
def create_faq(data: dict):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO faqs (question, answer, category)
        VALUES (%s, %s, %s)
        """,
        (data["question"], data["answer"], data["category"])
    )

    db.commit()
    cursor.close()
    db.close()

    return {"message": "FAQ created successfully"}


# ---------------- UPDATE FAQ ----------------
@router.put("/faqs/{faq_id}")
def update_faq(faq_id: int, data: dict):

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE faqs
        SET question=%s, answer=%s, category=%s
        WHERE id=%s
        """,
        (data["question"], data["answer"], data["category"], faq_id)
    )

    db.commit()
    cursor.close()
    db.close()

    return {"message": "FAQ updated successfully"}


# ---------------- DELETE FAQ ----------------
@router.delete("/faqs/{faq_id}")
def delete_faq(faq_id: int):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM faqs WHERE id=%s", (faq_id,))
    db.commit()

    cursor.close()
    db.close()

    return {"message": "FAQ deleted successfully"}