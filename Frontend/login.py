import streamlit as st
import requests
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="UNIBOT | Login", page_icon="🎓", layout="centered")

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.8)), 
                url('https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&q=80');
    background-size: cover;
}
#MainMenu, footer, header {visibility: hidden;}

.login-card {
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(15px);
    padding: 50px;
    border-radius: 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    text-align: center;
}

.title-text {
    font-size: 3.2rem;
    font-weight: 850;
    background: linear-gradient(to right, #00d2ff, #3a7bd5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

input {
    background-color: rgba(0, 0, 0, 0.2) !important;
    color: white !important;
}

div.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
    border-radius: 12px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN CARD ----------------
st.markdown("<div class='login-card'>", unsafe_allow_html=True)
st.markdown("<h1 class='title-text'>UNIBOT</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#94a3b8;'>Next-Gen College Helpdesk</p>", unsafe_allow_html=True)

email = st.text_input("📧 Email")
username = st.text_input("👤 Username (for new users)")
phone = st.text_input("📞 Phone")
password = st.text_input("🔑 Password", type="password")

if st.button("SIGN IN TO UNIBOT"):

    if not (email and password):
        st.error("❌ Email & Password required")
        st.stop()

    try:
        # -------- LOGIN TRY --------
        res = requests.post(
            "http://127.0.0.1:8000/users/login",
            json={"email": email, "password": password},
            timeout=5
        )

        if res.status_code == 200:
            user = res.json()["user"]

            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.email = user["email"]
            st.session_state.phone = user["phone"]

            st.success("✅ Login successful! Redirecting...")
            time.sleep(1)
            st.switch_page("pages/app.py")

        elif res.status_code == 401:
            # -------- SIGNUP --------
            if not (username and phone):
                st.error("⚠️ Username & Phone required for signup")
                st.stop()

            signup = requests.post(
                "http://127.0.0.1:8000/users/signup",
                json={
                    "username": username,
                    "email": email,
                    "phone": phone,
                    "password": password
                },
                timeout=5
            )

            if signup.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.email = email
                st.session_state.phone = phone

                st.success("🎉 Account created! Redirecting...")
                time.sleep(1)
                st.switch_page("pages/app.py")
            else:
                st.error("❌ Email already exists")

    except Exception as e:
        st.error("❌ Backend server not running")

st.markdown("</div>", unsafe_allow_html=True)
