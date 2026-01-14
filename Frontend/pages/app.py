import streamlit as st
import os
from dotenv import load_dotenv
from google.genai import Client

# ---------- LOAD ENV ----------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found")
    st.stop()

# ---------- SECURITY ----------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first")
    st.stop()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="UNIBOT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- HIDE SIDEBAR ----------
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
.chat-user {
    background:#0b93f6;
    color:white;
    padding:12px 16px;
    border-radius:18px;
    max-width:70%;
    margin-left:auto;
}
.chat-bot {
    background:#e5f0ff;
    color:#000;
    padding:12px 16px;
    border-radius:18px;
    max-width:70%;
    margin-right:auto;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<h1 style="text-align:center;">🤖 UNIBOT</h1>
<p style="text-align:center; color:gray;">College Helpdesk Assistant</p>
""", unsafe_allow_html=True)

# ---------- CHAT MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    css = "chat-user" if m["role"] == "user" else "chat-bot"
    st.markdown(f"<div class='{css}'>{m['content']}</div>", unsafe_allow_html=True)

# ---------- INPUT ----------
prompt = st.chat_input("Ask about admission, courses, fees...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='chat-user'>{prompt}</div>", unsafe_allow_html=True)

    try:
        client = Client(api_key=API_KEY)

        response = client.models.generate_content(
            model="gemini-flash-latest",   # ✅ FINAL FIX
            contents=prompt
        )

        reply = response.text

    except Exception as e:
        reply = f"❌ Gemini Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown(f"<div class='chat-bot'>{reply}</div>", unsafe_allow_html=True)
