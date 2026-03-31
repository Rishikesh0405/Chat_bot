import streamlit as st
import requests
import time
import base64

BACKEND_URL = "http://127.0.0.1:8000"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="UNIBOT AI",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------- FORCE SIDEBAR VISIBLE ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: block !important;
}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR LOGIN TYPE ----------------
with st.sidebar:
    st.markdown("## 🔐 Login Type")
    login_type = st.radio(
    "Login Type",
    ["User", "Admin"],
    label_visibility="collapsed"
)
# ---------------- BACKGROUND IMAGE ----------------
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bot_image = ""
try:
    bot_image = get_base64("bot.png")
except:
    pass

# ---------------- CUSTOM CSS (UNCHANGED UI) ----------------
st.markdown(f"""
<style>
.stApp {{
    background-color: #0e1117;
    background-image: radial-gradient(circle at 80% 20%, #1a1c2c 0%, #0e1117 100%);
    overflow: hidden;
}}

.stApp::after {{
    content: "";
    position: fixed;
    right: 0;
    top: 80px;
    width: 600px;
    height: 600px;
    background-image: url("data:image/png;base64,{bot_image}");
    background-size: contain;
    background-repeat: no-repeat;
    opacity: 0.08;
    z-index: 0;
}}

.block-container {{
    position: relative;
    z-index: 1;
    padding-top: 4rem;
}}

.header-text {{
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
    text-shadow: 0 0 15px rgba(255,255,255,0.4);
    margin-bottom: 5px;
}}

div[data-baseweb="input"] {{
    background-color: #161922 !important;
    border: 1px solid #4d4dff !important;
    border-radius: 12px !important;
    box-shadow: 0 0 10px rgba(77, 77, 255, 0.2);
}}

div[data-baseweb="input"]:focus-within {{
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.7) !important;
    border: 1px solid #00d4ff !important;
}}

input {{
    color: white !important;
}}

.stButton>button {{
    width: 100%;
    background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
    color: white;
    border: none;
    padding: 14px;
    border-radius: 10px;
    font-weight: bold;
    text-transform: uppercase;
    box-shadow: 0 0 20px rgba(0, 198, 255, 0.4);
}}

.stButton>button:hover {{
    box-shadow: 0 0 35px rgba(0, 198, 255, 0.9);
}}

label {{
    color: #d1d1d1 !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- UI (UNCHANGED) ----------------
st.markdown("<h1 class='header-text'>🤖 UNIBOT</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #888; margin-top:-10px;'>Next-Gen AI Assistant</h4>", unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

with col1:
    login_type = st.radio(
        "",
        ["User", "Admin"],
        horizontal=True,
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)
login_input = st.text_input("👤 User name")

# 👇 ONLY USER MODE me extra fields
if login_type == "User":
    email = st.text_input("📧 Email (for new users only)")
    phone = st.text_input("📞 Phone (for new users only)")
else:
    email = ""
    phone = ""

password = st.text_input("🔑 Password", type="password")

# ---------------- LOGIN BUTTON ----------------
if st.button("SIGN IN TO UNIBOT"):

    if not login_input or not password:
        st.error("Login ID & Password required")
        st.stop()

    try:
        res = requests.post(
            f"{BACKEND_URL}/users/login",
            json={
                "login_id": login_input,
                "password": password
            },
            timeout=5
        )

        if res.status_code == 200:
            data = res.json()

            # 🔥 ADMIN VALIDATION
            if login_type == "Admin" and data["role"] != "admin":
                st.error("Not an admin account ❌")
                st.stop()

            st.session_state.logged_in = True
            st.session_state.role = data["role"]
            st.session_state.username = data.get("username", "admin")

            st.success("Login successful! Redirecting...")
            time.sleep(1)

            if data["role"] == "admin":
                st.switch_page("pages/admin.py")
            else:
                st.switch_page("pages/app.py")

            st.stop()

        # ---------------- SIGNUP ONLY FOR USER ----------------
        elif res.status_code == 404 and login_type == "User":

            if not email or not phone:
                st.warning("New user detected. Enter Email & Phone to register.")
                st.stop()

            signup_res = requests.post(
                f"{BACKEND_URL}/users/signup",
                json={
                    "email": email,
                    "username": login_input,
                    "phone": phone,
                    "password": password
                },
                timeout=5
            )

            if signup_res.status_code == 200:
                st.success("Account created! Click Sign In again.")
            else:
                st.error(signup_res.json().get("detail", "Signup failed"))

        elif res.status_code == 401:
            st.error("Incorrect password")

        else:
            st.error("User not found or invalid login type")

    except requests.exceptions.ConnectionError:
        st.error("Backend server not running")