import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# เชื่อม Firestore
if not firebase_admin._apps:
    key_dict = dict(st.secrets["firebase"])
    key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Admin password
ADMIN_PASSWORD = "admin1234"  # เปลี่ยนเป็นรหัสคุณ

def admin_page():
    st.title("🔧 Admin Panel")
    
    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False
    
    if not st.session_state["admin_logged_in"]:
        pwd = st.text_input("🔒 รหัสผ่าน Admin", type="password")
        if st.button("เข้าสู่ระบบ"):
            if pwd == ADMIN_PASSWORD:
                st.session_state["admin_logged_in"] = True
                st.rerun()
            else:
                st.error("❌ รหัสผ่านไม่ถูกต้อง")
        return
    
    st.success("✅ เข้าสู่ระบบ Admin แล้ว")
    st.divider()
    
    # ดู user ทั้งหมด
    st.markdown("### 👥 รายชื่อ Users")
    users = db.collection("users").get()
    for u in users:
        data = u.to_dict()
        col1, col2, col3 = st.columns([3,2,2])
        with col1:
            st.write(f"📧 {data.get('email')}")
        with col2:
            st.write(f"💎 {data.get('plan')} | {data.get('status')}")
        with col3:
            st.write(f"📅 หมด: {data.get('end_date')}")
    
    st.divider()
    
    # เพิ่ม/อัพเดท user
    st.markdown("### ➕ เพิ่ม/อัพเดท User")
    email = st.text_input("📧 Email ลูกค้า")
    duration = st.selectbox("⏱ ระยะเวลา", [
        "7 วัน (ทดลองใช้)",
        "30 วัน (1 เดือน)",
        "90 วัน (3 เดือน)",
        "365 วัน (1 ปี)"
    ])
    
    days_map = {
        "7 วัน (ทดลองใช้)": 7,
        "30 วัน (1 เดือน)": 30,
        "90 วัน (3 เดือน)": 90,
        "365 วัน (1 ปี)": 365
    }
    
    if st.button("✅ เปิดใช้งาน", type="primary"):
        if email:
            today = datetime.now()
            end = today + timedelta(days=days_map[duration])
            
            # เช็คว่ามี user อยู่แล้วไหม
            existing = db.collection("users").where("email","==",email).get()
            
            data = {
                "email": email,
                "plan": "premium",
                "status": "active",
                "start_date": today.strftime("%Y-%m-%d"),
                "end_date": end.strftime("%Y-%m-%d"),
                "price": 0 if days_map[duration] == 7 else 299,
                "currency": "THB"
            }
            
            if existing:
                existing[0].reference.update(data)
                st.success(f"✅ อัพเดท {email} แล้ว หมดอายุ {end.strftime('%Y-%m-%d')}")
            else:
                db.collection("users").add(data)
                st.success(f"✅ เพิ่ม {email} แล้ว หมดอายุ {end.strftime('%Y-%m-%d')}")
        else:
            st.warning("กรุณาใส่ email")

admin_page()