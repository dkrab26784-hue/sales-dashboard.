import streamlit as st
import requests
from dotenv import load_dotenv
import os
load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
FIREBASE_API_KEY = st.secrets["FIREBASE_API_KEY"]
def sign_up(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    data = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=data)
    return r.json()

def sign_in(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    data = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=data)
    return r.json()

def reset_password(email):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"
    data = {"requestType": "PASSWORD_RESET", "email": email}
    r = requests.post(url, json=data)
    return r.json()

def login_page():
    st.title("🔐 Sales Dashboard")
    st.markdown("##### วิเคราะห์ข้อมูลธุรกิจของคุณ")
    st.divider()

    tab1, tab2 = st.tabs(["🔑 เข้าสู่ระบบ", "📝 สมัครสมาชิก"])

    with tab1:
        email = st.text_input("📧 อีเมล", key="li_email")
        password = st.text_input("🔒 รหัสผ่าน", type="password", key="li_pass")
        st.checkbox("จดจำการเข้าสู่ระบบ")
        
        if st.button("เข้าสู่ระบบ", use_container_width=True, type="primary"):
            if email and password:
                result = sign_in(email, password)
                if "idToken" in result:
                    st.session_state["logged_in"] = True
                    st.session_state["email"] = email
                    st.session_state["token"] = result["idToken"]
                    st.success("✅ เข้าสู่ระบบสำเร็จ!")
                    st.rerun()
                else:
                    st.error("❌ อีเมลหรือรหัสผ่านไม่ถูกต้อง")
            else:
                st.warning("⚠️ กรุณากรอกอีเมลและรหัสผ่าน")

        st.markdown("---")
        if st.button("🔑 ลืมรหัสผ่าน?", use_container_width=True):
            if email:
                reset_password(email)
                st.success("📧 ส่ง email reset แล้ว กรุณาเช็ค gmail")
            else:
                st.warning("⚠️ กรุณาใส่ email ก่อน")

    with tab2:
        new_email = st.text_input("📧 อีเมล", key="su_email")
        new_pass = st.text_input("🔒 รหัสผ่าน", type="password", key="su_pass")
        confirm = st.text_input("🔒 ยืนยันรหัสผ่าน", type="password", key="su_confirm")
        if st.button("สมัครสมาชิก", use_container_width=True, type="primary"):
            if new_pass != confirm:
                st.error("❌ รหัสผ่านไม่ตรงกัน")
            elif len(new_pass) < 6:
                st.error("❌ รหัสผ่านต้องมีอย่างน้อย 6 ตัว")
            elif new_email and new_pass:
                result = sign_up(new_email, new_pass)
                if "idToken" in result:
                    st.success("✅ สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ")
                else:
                    error_msg = result.get("error", {}).get("message", "")
                    if error_msg == "EMAIL_EXISTS":
                        st.error("❌ อีเมลนี้ถูกใช้แล้ว")
                    else:
                        st.error(f"❌ {error_msg}")
