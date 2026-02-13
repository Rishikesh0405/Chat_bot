# UNIBOT – AI Chatbot

UNIBOT is a Python-based AI chatbot that can answer user questions in real time.  
It integrates a frontend, backend API, database, and an AI model to simulate a real-world application.

---

## Features

- User Login and Signup system  
- Real-time chatbot responses  
- AI-powered answers using Gemini API  
- Stores user queries in MySQL database  
- Clean and interactive UI using Streamlit  

---

## Tech Stack

- Python  
- FastAPI (Backend)  
- Streamlit (Frontend)  
- MySQL (Database)  
- Google Gemini API  

---

## Project Structure

Chat_bot/

Backend/  
  routers/  
  main.py  
  database.py  
  models.py  

Frontend/  
  login.py  
  pages/  
    app.py  

requirements.txt  
README.md  

---

## Installation

1. Clone the repository

git clone https://github.com/Rishikesh0405/Chat_bot.git  
cd Chat_bot  

2. Install dependencies

pip install -r requirements.txt  

3. Setup Environment Variables

Create a `.env` file and add:

GOOGLE_API_KEY=your_api_key  
MYSQL_HOST=localhost  
MYSQL_USER=root  
MYSQL_PASSWORD=your_password  
MYSQL_DB=unibot_db  

4. Run Backend

uvicorn Backend.main:app --reload  

5. Run Frontend

streamlit run Frontend/login.py  

---

## Future Improvements

- Chat history per user  
- FAQ matching improvement  
- Deployment on cloud  

---

## Author

Rishikesh Chandeliya  
GitHub: https://github.com/Rishikesh0405
