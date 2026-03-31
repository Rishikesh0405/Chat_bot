from Backend.database import get_db

def search_faq_mysql(user_query: str):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT question, answer
        FROM faqs
        WHERE question LIKE %s
        LIMIT 1
    """
    cursor.execute(query, (f"%{user_query}%",))
    row = cursor.fetchone()

    cursor.close()
    db.close()

    return row
