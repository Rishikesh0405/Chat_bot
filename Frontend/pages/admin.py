import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Unibot Admin Panel",
    page_icon="⚙️",
    layout="wide"
)

# ---------------- HIDE SIDEBAR + PREMIUM CSS ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp {
    background-color: #0e1117;
    background-image: radial-gradient(circle at 20% 20%, #1a1c2c 0%, #0e1117 100%);
    color: white;
}

.admin-header {
    font-size: 2.2rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.5rem;
}

.admin-sub {
    color: #8f9bb3;
    margin-bottom: 2rem;
}

.card {
    background-color: #161922;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.08);
    margin-bottom: 25px;
}

.section-title {
    font-size: 1.3rem;
    margin-bottom: 15px;
    font-weight: 600;
}

div[data-baseweb="input"],
textarea {
    background-color: #1e2230 !important;
    border-radius: 12px !important;
    border: 1px solid #2e3445 !important;
    color: white !important;
}

.stButton>button {
    background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
}

.stButton>button:hover {
    box-shadow: 0 0 20px rgba(0, 198, 255, 0.6);
}

.expander-header {
    font-weight: 600;
    color: #00d4ff;
}

.badge {
    background-color: #00d4ff33;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    margin-left: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN + ROLE PROTECTION ----------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("Access Denied 🚫 Admin Only")
    st.stop()

# ---------------- HEADER WITH LOGOUT ----------------
col1, col2 = st.columns([9,1])

with col1:
    st.markdown("<div class='admin-header'>⚙️ Admin FAQ Dashboard</div>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='admin-sub'>Logged in as: <b>{st.session_state.username}</b></div>",
        unsafe_allow_html=True
    )

with col2:
    if st.button("⎋", help="Logout"):
        st.session_state.clear()
        st.switch_page("login.py")

# ---------------- CREATE FAQ CARD ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>➕ Create FAQ</div>", unsafe_allow_html=True)

question = st.text_input("Question")
answer = st.text_area("Answer")
category = st.text_input("Category")

if st.button("Create FAQ"):
    res = requests.post(
        f"{BACKEND_URL}/admin/faqs",
        json={
            "question": question,
            "answer": answer,
            "category": category
        }
    )
    if res.status_code == 200:
        st.success("FAQ Created Successfully")
        st.rerun()
    else:
        st.error("Error creating FAQ")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MANAGE FAQ CARD ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📋 Manage FAQs</div>", unsafe_allow_html=True)

try:
    res = requests.get(f"{BACKEND_URL}/admin/faqs")

    if res.status_code == 200:
        faqs = res.json()
    else:
        st.error("Failed to load FAQs")
        faqs = []

except:
    st.error("Backend not reachable")
    faqs = []

for faq in faqs:
    with st.expander(f"📌 {faq['question']}"):
        st.markdown(
            f"<span class='badge'>{faq['category']}</span>",
            unsafe_allow_html=True
        )

        new_q = st.text_input("Edit Question", faq["question"], key=f"q{faq['id']}")
        new_a = st.text_area("Edit Answer", faq["answer"], key=f"a{faq['id']}")
        new_c = st.text_input("Edit Category", faq["category"], key=f"c{faq['id']}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Update", key=f"u{faq['id']}"):
                requests.put(
                    f"{BACKEND_URL}/admin/faqs/{faq['id']}",
                    json={
                        "question": new_q,
                        "answer": new_a,
                        "category": new_c
                    }
                )
                st.success("Updated Successfully")
                st.rerun()

        with col2:
            if st.button("Delete", key=f"d{faq['id']}"):
                requests.delete(f"{BACKEND_URL}/admin/faqs/{faq['id']}")
                st.warning("Deleted Successfully")
                st.rerun()

st.markdown("</div>", unsafe_allow_html=True)