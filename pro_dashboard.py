import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(
    page_title="Sales Dashboard", 
    layout="wide", 
    page_icon="📊"
)

st.markdown("""
<style>
[data-testid="stMetricValue"] { color: #1f77b4 !important; font-size: 2rem !important; }
[data-testid="stMetricLabel"] { font-weight: bold !important; }
[data-testid="stMetricDelta"] { font-size: 0.9rem !important; }
.stDownloadButton button { width: 100%; }
div[data-testid="stFileUploader"] { 
    border: 2px dashed #1f77b4; 
    border-radius: 10px; 
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Sales Dashboard")
st.markdown("##### วิเคราะห์ข้อมูลธุรกิจของคุณได้ทันที | Instant Business Data Analysis")
st.divider()

# Upload + Demo
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### ⬆️ อัพโหลดไฟล์ข้อมูล")
    uploaded_file = st.file_uploader(
        "รองรับไฟล์ CSV และ Excel (.xlsx)",
        type=["csv", "xlsx"],
        help="ไฟล์ต้องมีแถวแรกเป็นชื่อคอลัมน์"
    )
with col2:
    st.markdown("### 🎮 ทดลองใช้")
    st.markdown(" ")
    use_demo = st.button("▶️ ลองใช้ข้อมูลตัวอย่าง", use_container_width=True)

st.divider()

# Load Data
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success(f"✅ อัพโหลดสำเร็จ! พบข้อมูล {len(df)} แถว {len(df.columns)} คอลัมน์")
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")
        st.stop()
elif use_demo:
    df = pd.DataFrame({
        "เดือน": ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย."],
        "โทรศัพท์": [120, 135, 150, 160, 145, 170],
        "หูฟัง": [80, 90, 85, 95, 100, 110],
        "เคส": [200, 210, 195, 220, 230, 250]
    })
    st.info("🎮 กำลังใช้ข้อมูลตัวอย่าง ลองอัพโหลดไฟล์ของคุณเองได้เลย!")
else:
    st.markdown("""
    ### 👋 ยินดีต้อนรับสู่ Sales Dashboard!
    
    วิธีใช้งาน:
    - 📁 อัพโหลดไฟล์ Excel หรือ CSV ของคุณ
    - 📊 ระบบจะวิเคราะห์และแสดงผลทันที
    - 💾 ดาวน์โหลดรายงานได้
    
    หรือกด "ลองใช้ข้อมูลตัวอย่าง" เพื่อดูตัวอย่างก่อน!
    """)
    st.stop()

# Column Mapping
with st.expander("🗂️ ตั้งค่าคอลัมน์ (Column Mapping)", expanded=True):
    all_cols = df.columns.tolist()
    col1, col2 = st.columns(2)
    with col1:
        month_col = st.selectbox("📅 เลือกคอลัมน์เดือน/วันที่", all_cols)
    with col2:
        value_cols = st.multiselect(
            "📈 เลือกคอลัมน์ที่ต้องการวิเคราะห์",
            [c for c in all_cols if c != month_col],
            default=[c for c in all_cols if c != month_col]
        )

if not value_cols:
    st.warning("⚠️ กรุณาเลือกอย่างน้อย 1 คอลัมน์")
    st.stop()

st.divider()

# KPI
st.markdown("### 📈 ภาพรวม Key Metrics")
kpi_cols = st.columns(len(value_cols))
for i, col in enumerate(value_cols):
    total = int(df[col].sum())
    avg = round(df[col].mean(), 1)
    max_val = int(df[col].max())
    kpi_cols[i].metric(
        label=f"📦 {col}",
        value=f"{total:,}",
        delta=f"เฉลี่ย {avg} | สูงสุด {max_val}"
    )

st.divider()

# Chart
st.markdown("### 📊 กราฟแสดงแนวโน้ม")
products = st.multiselect(
    "เลือกสินค้า/หมวดหมู่ที่ต้องการดู",
    value_cols,
    default=value_cols
)

tab1, tab2 = st.tabs(["📈 Line Chart", "📊 Bar Chart"])

with tab1:
    fig_line = px.line(
        df, x=month_col, y=products,
        markers=True,
        title="แนวโน้มยอดขายรายเดือน",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_line.update_layout(
        hovermode="x unified",
        height=450,
        legend_title="สินค้า",
        xaxis_title="เดือน",
        yaxis_title="ยอดขาย"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    fig_bar = px.bar(
        df, x=month_col, y=products,
        barmode="group",
        title="เปรียบเทียบยอดขายรายเดือน",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar.update_layout(height=450)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# Summary
st.markdown("### 💡 สรุปผลการวิเคราะห์")
col1, col2, col3 = st.columns(3)

best_col = df[value_cols].sum().idxmax()
worst_col = df[value_cols].sum().idxmin()
best_month = df.loc[df[value_cols].sum(axis=1).idxmax(), month_col]
worst_month = df.loc[df[value_cols].sum(axis=1).idxmin(), month_col]

with col1:
    st.success(f"🏆 สินค้าขายดีสุด\n\n{best_col}")
with col2:
    st.error(f"⚠️ สินค้าที่ต้องปรับปรุง\n\n{worst_col}")
with col3:
    st.info(f"📅 เดือนที่ดีที่สุด\n\n{best_month}")

st.divider()

# Raw Data
with st.expander("📋 ดูข้อมูลดิบ (Raw Data)"):
    st.dataframe(df, use_container_width=True)

# Export
st.markdown("### 💾 ดาวน์โหลดรายงาน")
col1, col2 = st.columns(2)

with col1:
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sales Data')
    st.download_button(
        "📥 ดาวน์โหลด Excel",
        excel_buffer.getvalue(),
        "sales_report.xlsx",
        mime="application/vnd.ms-excel",
        use_container_width=True
    )

with col2:
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        "📥 ดาวน์โหลด CSV",
        csv,
        "sales_report.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()
st.markdown("*Made with ❤️ using Python & Streamlit*")
