import streamlit as st
import pandas as pd
import plotly.express as px
import io
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    key_dict = dict(st.secrets["firebase"])
    key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()
from datetime import datetime

def check_user_plan(email):
    user = db.collection("users").where("email", "==", email).get()
    if user:
        data = user[0].to_dict()
        if data.get("status") == "active" and data.get("plan") == "premium":
            end_date = data.get("end_date", "")
            if end_date >= datetime.now().strftime("%Y-%m-%d"):
                return True
    return False


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from auth import login_page
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login_page()
    st.stop()

email = st.session_state.get("email", "")
if not check_user_plan(email):
    st.warning("⚠️ คุณยังไม่มีแผน Premium")
    st.markdown("## 💎 Premium Plan — 299 บาท/เดือน")
    st.markdown("""
    ✅ อัพโหลดไฟล์ CSV/Excel  
    ✅ กราฟวิเคราะห์ครบทุกฟีเจอร์  
    ✅ Export PDF  
    ✅ แจ้งเตือนยอดขาย  
    ✅ รองรับภาษาไทย/อังกฤษ  
    """)
    st.markdown("### 📱 สแกน QR Code ชำระเงิน")
col1, col2 = st.columns([1,2])
with col1:
    st.image("qr_promptpay.png", width=200)
with col2:
    st.markdown("""
    PromptPay: 095-453-8158  
    ราคา: 299 บาท/เดือน  
    
    หลังโอนเงินแล้วกดปุ่ม "แจ้งชำระเงิน" ด้านล่างได้เลยครับ
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.info("📱 ติดต่อสั่งซื้อ Line: jsufijwu ไม่มี ๑ หรือ เบอร์โทร: 081-132-0649")
        st.link_button(
        "📝 แจ้งชำระเงิน / สมัคร Premium",
        "https://docs.google.com/forms/d/e/1FAIpQLSeeuv1B8Q7nLuRGrAECf7UCKroEpYzXQgSDNOPLoCrSURfSgQ/viewform?usp=publish-editor"  # ใส่ลิงก์ฟอร์มจริงของคุณ
        )
    with col2:
        st.info("🎁 ทดลองใช้ได้ฟรี 7 วัน! กรอกแบบฟอร์มเพื่อรับสิทธิ์ทดลองใช้")
        st.link_button(
            "📝 สมัครทดลองใช้ฟรี", 
            "https://docs.google.com/forms/d/e/1FAIpQLSe2h18XFeErBlhZuL03p7v4fBO1STwT3FXOefkXjebPw8DZVA/viewform?usp=publish-editor"
        )
    st.stop()


with st.sidebar:
    st.write(f"👤 {st.session_state.get('email', '')}")
    if st.button("🔒 ออกจากระบบ"):
        st.session_state["logged_in"] = False
        st.rerun()
    st.markdown("---")
    st.link_button("💬 ติดต่อแอดมิน Line", 
                   "https://line.me/ti/p/~jsufijwu")

st.set_page_config(page_title="Sales Dashboard", layout="wide", page_icon="📊")

st.markdown("""
<style>
[data-testid="stMetricValue"] { font-size: 2.5rem !important; font-weight: bold !important; }
.alert-red { background: #ff4444; color: white; padding: 10px; border-radius: 8px; margin: 5px 0; }
.alert-yellow { background: #ffaa00; color: white; padding: 10px; border-radius: 8px; margin: 5px 0; }
.alert-green { background: #00cc66; color: white; padding: 10px; border-radius: 8px; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# Language
lang = st.selectbox("🌐", ["🇹🇭 ภาษาไทย", "🇬🇧 English"], label_visibility="collapsed")
thai = lang == "🇹🇭 ภาษาไทย"

st.title("📊 แดชบอร์ดยอดขาย" if thai else "📊 Sales Dashboard")
st.markdown("##### เปิดมาแล้วรู้ทันทีว่าวันนี้เป็นยังไง" if thai else "##### Know your business status instantly")
st.divider()

# Upload + Demo
col1, col2 = st.columns([3, 1])
with col1:
    uploaded_file = st.file_uploader(
        "⬆️ อัพโหลด CSV หรือ Excel" if thai else "⬆️ Upload CSV or Excel",
        type=["csv", "xlsx"]
    )
with col2:
    st.markdown(" ")
    st.markdown(" ")
    use_demo = st.button(
        "▶️ ทดลองใช้ข้อมูลตัวอย่าง" if thai else "▶️ Try Demo Data",
        use_container_width=True
    )

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        st.success("✅ อัพโหลดสำเร็จ!" if thai else "✅ Uploaded!")
    except Exception as e:
        st.error(f"❌ {e}")
        st.stop()
elif use_demo:
    df = pd.DataFrame({
        "เดือน" if thai else "Month": ["ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย."] if thai else ["Jan","Feb","Mar","Apr","May","Jun"],
        "โทรศัพท์" if thai else "Phone": [120,135,150,160,45,170],
        "หูฟัง" if thai else "Earphone": [80,90,85,95,100,110],
        "เคส" if thai else "Case": [200,210,195,220,230,250]
    })
    st.info("🎮 กำลังใช้ข้อมูลตัวอย่าง" if thai else "🎮 Using demo data")
else:
    st.markdown("### 👋 ยินดีต้อนรับ!" if thai else "### 👋 Welcome!")
    st.markdown("อัพโหลดไฟล์หรือกดทดลองใช้เพื่อเริ่มต้น" if thai else "Upload a file or try demo to get started")
    st.stop()

# Column setup
all_cols = df.columns.tolist()
month_col = all_cols[0]
value_cols = all_cols[1:]

st.divider()

# ===== 1. ALERT BAR =====
st.markdown("### 🚨 การแจ้งเตือน" if thai else "### 🚨 Alerts")

alerts = []
for col in value_cols:
    last = df[col].iloc[-1]
    prev = df[col].iloc[-2]
    change = ((last - prev) / prev) * 100
    avg = df[col].mean()

    if change <= -20:
        alerts.append(("red", f"🔴 {col}: {'ยอดตก' if thai else 'Drop'} {abs(change):.1f}% {'จากเดือนก่อน' if thai else 'from last period'}"))
    elif change <= -10:
        alerts.append(("yellow", f"🟡 {col}: {'ยอดลดลง' if thai else 'Declined'} {abs(change):.1f}%"))
    elif last < avg * 0.8:
        alerts.append(("yellow", f"🟡 {col}: {'ต่ำกว่าค่าเฉลี่ย' if thai else 'Below average'}"))
    else:
        alerts.append(("green", f"🟢 {col}: {'ปกติดี' if thai else 'Normal'} ✓"))

for level, msg in alerts:
    st.markdown(f'<div class="alert-{level}">{msg}</div>', unsafe_allow_html=True)

st.divider()

# ===== 2. KPI =====
st.markdown("### 📊 ภาพรวมสำคัญ" if thai else "### 📊 Key Metrics")

kpi_cols = st.columns(len(value_cols))
for i, col in enumerate(value_cols):
    total = int(df[col].sum())
    last_val = int(df[col].iloc[-1])
    prev_val = int(df[col].iloc[-2])
    delta = last_val - prev_val
    kpi_cols[i].metric(
        label=f"📦 {col}",
        value=f"{total:,}",
        delta=f"{'+' if delta > 0 else ''}{delta} {'จากเดือนก่อน' if thai else 'vs last period'}"
    )

st.divider()

# ===== 3. CHART =====
st.markdown("### 📈 กราฟแนวโน้ม" if thai else "### 📈 Sales Trend")
tab1, tab2 = st.tabs(["📈 Line", "📊 Bar"])
with tab1:
    fig = px.line(df, x=month_col, y=value_cols, markers=True,
                  template="plotly_dark",
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(hovermode="x unified", height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = px.bar(df, x=month_col, y=value_cols, barmode="group",
                  template="plotly_dark",
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ===== 4. TOP PRODUCTS =====
st.markdown("### 🏆 สินค้าขายดีสุด" if thai else "### 🏆 Top Products")

totals = df[value_cols].sum().sort_values(ascending=False)
top_cols = st.columns(len(value_cols))
for i, (name, val) in enumerate(totals.items()):
    rank = ["🥇","🥈","🥉","4️⃣","5️⃣"][i] if i < 5 else f"{i+1}."
    top_cols[i].metric(f"{rank} {name}", f"{int(val):,}")

st.divider()

# ===== 5. EXPORT =====
st.markdown("### 💾 ดาวน์โหลดรายงาน" if thai else "### 💾 Export Report")

col1, col2, col3 = st.columns(3)

with col1:
    excel_buf = io.BytesIO()
    with pd.ExcelWriter(excel_buf, engine='openpyxl') as w:
        df.to_excel(w, index=False)
    st.download_button(
        "📥 Excel",
        excel_buf.getvalue(),
        "report.xlsx",
        mime="application/vnd.ms-excel",
        use_container_width=True
    )

with col2:
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        "📥 CSV",
        csv, "report.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    pdf_buf = io.BytesIO()
    c = canvas.Canvas(pdf_buf, pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, h-50, "Sales Dashboard Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, h-80, f"Total Products: {len(value_cols)}")
    y = h - 120
    for col in value_cols:
        c.drawString(50, y, f"{col}: {int(df[col].sum()):,}")
        y -= 25
    c.save()
    st.download_button(
        "📥 PDF",
        pdf_buf.getvalue(),
        "report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

with st.expander("📋 ดูข้อมูลดิบ" if thai else "📋 Raw Data"):
    st.dataframe(df, use_container_width=True)

st.divider()
st.markdown("*Made with ❤️ Python & Streamlit*")
