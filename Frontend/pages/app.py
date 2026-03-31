import streamlit as st
import requests
import os

BACKEND_URL = "http://127.0.0.1:8000"

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="College Helpdesk Chatbot",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- HIDE SIDEBAR + CUSTOM CSS ----------
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
footer {visibility:hidden;}
header {visibility:hidden;}

body {
    background: linear-gradient(135deg, #e0f7fa, #fff3e0);
    color: #222;
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    background: transparent;
}

.title {
    text-align: center;
    color: #004d40;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.chat-bubble-user {
    background-color: #1976d2;
    color: white;
    padding: 10px 14px;
    border-radius: 20px 20px 0px 20px;
    margin: 5px 0;
    max-width: 70%;
    margin-left: auto;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.2);
}

.chat-bubble-bot {
    background-color: #f1f8e9;
    color: #333;
    padding: 10px 14px;
    border-radius: 20px 20px 20px 0px;
    margin: 5px 0;
    max-width: 70%;
    margin-right: auto;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.2);
}

.stChatInput {
    background-color: #f9f9f9 !important;
    border-radius: 10px !important;
}

/* Thinking animation */
.dots span {
    animation: blink 1.4s infinite both;
    font-weight: bold;
    font-size: 18px;
}

.dots span:nth-child(1) { animation-delay: 0s; }
.dots span:nth-child(2) { animation-delay: 0.2s; }
.dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
    0% { opacity: 0.2; }
    20% { opacity: 1; }
    100% { opacity: 0.2; }
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN + ROLE PROTECTION ----------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first")
    st.stop()

if st.session_state.get("role") != "user":
    st.error("Access Denied 🚫 User Only")
    st.stop()

# ---------- HEADER WITH LOGOUT ----------
col1, col2 = st.columns([9,1])

with col1:
    st.markdown("<div class='title'>Welcome to Unibot 🤖</div>", unsafe_allow_html=True)

with col2:
    if st.button("⎋", help="Logout"):
        st.session_state.clear()
        st.switch_page("login.py")
# ---------- CHAT SESSION ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- DISPLAY OLD MESSAGES ----------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='chat-bubble-user'>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-bubble-bot'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

# ---------- INPUT ----------
prompt = st.chat_input("Ask something about college, courses, or admission...")

if prompt:

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    st.markdown(
        f"<div class='chat-bubble-user'>{prompt}</div>",
        unsafe_allow_html=True
    )

    # Thinking animation
    thinking_placeholder = st.empty()

    thinking_placeholder.markdown("""
    <div class='chat-bubble-bot'>
        Unibot is typing
        <span class="dots">
            <span>.</span><span>.</span><span>.</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ---------- API CALL ----------
    try:
        res = requests.post(
            f"{BACKEND_URL}/bot/chat",
            json={
                "message": prompt,
                "username": st.session_state.username
            },
            timeout=10
        )

        if res.status_code == 200:
            bot_reply = res.json().get("reply", "No response")
        else:
            bot_reply = "Server error"

    except:
        bot_reply = "Backend not reachable"

    # Remove typing animation
    thinking_placeholder.empty()

    # Save bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    st.markdown(
        f"<div class='chat-bubble-bot'>{bot_reply}</div>",
        unsafe_allow_html=True
    )