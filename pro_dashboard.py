import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Sales Dashboard", layout="wide", page_icon="📊")

st.markdown("""
<style>
[data-testid="stMetricValue"] { color: #1f77b4 !important; font-size: 2rem !important; }
[data-testid="stMetricLabel"] { font-weight: bold !important; }
.stDownloadButton button { width: 100%; }
div[data-testid="stFileUploader"] { border: 2px dashed #1f77b4; border-radius: 10px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# Language
lang = st.selectbox("🌐", ["🇹🇭 ภาษาไทย", "🇬🇧 English"], label_visibility="collapsed")
thai = lang == "🇹🇭 ภาษาไทย"

# Text
T = {
    "title": "📊 แดชบอร์ดยอดขาย" if thai else "📊 Sales Dashboard",
    "subtitle": "วิเคราะห์ข้อมูลธุรกิจของคุณได้ทันที" if thai else "Instant Business Data Analysis",
    "upload": "⬆️ อัพโหลดไฟล์ข้อมูล" if thai else "⬆️ Upload Data",
    "upload_hint": "รองรับ CSV และ Excel" if thai else "Supports CSV and Excel",
    "demo": "▶️ ลองใช้ข้อมูลตัวอย่าง" if thai else "▶️ Try Demo Data",
    "try_label": "🎮 ทดลองใช้" if thai else "🎮 Try it",
    "success": "✅ อัพโหลดสำเร็จ!" if thai else "✅ Upload successful!",
    "error": "❌ เกิดข้อผิดพลาด" if thai else "❌ Error occurred",
    "demo_info": "🎮 กำลังใช้ข้อมูลตัวอย่าง" if thai else "🎮 Using demo data",
    "welcome": "### 👋 ยินดีต้อนรับ!" if thai else "### 👋 Welcome!",
    "welcome_text": "- 📁 อัพโหลดไฟล์ Excel หรือ CSV\n- 📊 ระบบวิเคราะห์ทันที\n- 💾 ดาวน์โหลดรายงานได้" if thai else "- 📁 Upload Excel or CSV\n- 📊 Instant analysis\n- 💾 Download reports",
    "col_map": "🗂️ ตั้งค่าคอลัมน์" if thai else "🗂️ Column Mapping",
    "month_col": "📅 เลือกคอลัมน์เดือน/วันที่" if thai else "📅 Select Month/Date column",
    "value_col": "📈 เลือกคอลัมน์วิเคราะห์" if thai else "📈 Select value columns",
    "metrics": "### 📈 ภาพรวม Key Metrics" if thai else "### 📈 Key Metrics",
    "avg": "เฉลี่ย" if thai else "Avg",
    "max": "สูงสุด" if thai else "Max",
    "chart": "### 📊 กราฟแนวโน้ม" if thai else "### 📊 Sales Trend",
    "filter": "เลือกสินค้าที่ต้องการดู" if thai else "Filter products",
    "line": "📈 Line Chart",
    "bar": "📊 Bar Chart",
    "line_title": "แนวโน้มยอดขายรายเดือน" if thai else "Sales Trend",
    "bar_title": "เปรียบเทียบยอดขาย" if thai else "Sales Comparison",
    "month_axis": "เดือน" if thai else "Month",
    "sales_axis": "ยอดขาย" if thai else "Sales",
    "summary": "### 💡 สรุปผลการวิเคราะห์" if thai else "### 💡 Quick Summary",
    "best_prod": "🏆 สินค้าขายดีสุด" if thai else "🏆 Best Product",
    "worst_prod": "⚠️ ต้องปรับปรุง" if thai else "⚠️ Needs Attention",
    "best_month": "📅 เดือนที่ดีที่สุด" if thai else "📅 Best Month",
    "raw": "📋 ดูข้อมูลดิบ" if thai else "📋 View Raw Data",
    "export": "### 💾 ดาวน์โหลดรายงาน" if thai else "### 💾 Export Report",
    "dl_excel": "📥 ดาวน์โหลด Excel" if thai else "📥 Download Excel",
    "dl_csv": "📥 ดาวน์โหลด CSV" if thai else "📥 Download CSV",
    "footer": "สร้างด้วย ❤️ Python & Streamlit" if thai else "Made with ❤️ Python & Streamlit",
    "warn_col": "⚠️ กรุณาเลือกอย่างน้อย 1 คอลัมน์" if thai else "⚠️ Please select at least 1 column",
}

st.title(T["title"])
st.markdown(f"##### {T['subtitle']}")
st.divider()

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"### {T['upload']}")
    uploaded_file = st.file_uploader(T["upload_hint"], type=["csv", "xlsx"])
with col2:
    st.markdown(f"### {T['try_label']}")
    st.markdown(" ")
    use_demo = st.button(T["demo"], use_container_width=True)

st.divider()

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success(f"{T['success']} {len(df)} {'แถว' if thai else 'rows'} {len(df.columns)} {'คอลัมน์' if thai else 'columns'}")
    except Exception as e:
        st.error(f"{T['error']}: {e}")
        st.stop()
elif use_demo:
    if thai:
        df = pd.DataFrame({
            "เดือน": ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย."],
            "โทรศัพท์": [120, 135, 150, 160, 145, 170],
            "หูฟัง": [80, 90, 85, 95, 100, 110],
            "เคส": [200, 210, 195, 220, 230, 250]
        })
    else:
        df = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Phone": [120, 135, 150, 160, 145, 170],
            "Earphone": [80, 90, 85, 95, 100, 110],
            "Case": [200, 210, 195, 220, 230, 250]
        })
    st.info(T["demo_info"])
else:
    st.markdown(T["welcome"])
    st.markdown(T["welcome_text"])
    st.stop()

with st.expander(T["col_map"], expanded=True):
    all_cols = df.columns.tolist()
    c1, c2 = st.columns(2)
    with c1:
        month_col = st.selectbox(T["month_col"], all_cols)
    with c2:
        value_cols = st.multiselect(
            T["value_col"],
            [c for c in all_cols if c != month_col],
            default=[c for c in all_cols if c != month_col]
        )

if not value_cols:
    st.warning(T["warn_col"])
    st.stop()

st.divider()
st.markdown(T["metrics"])
kpi_cols = st.columns(len(value_cols))
for i, col in enumerate(value_cols):
    total = int(df[col].sum())
    avg = round(df[col].mean(), 1)
    max_val = int(df[col].max())
    kpi_cols[i].metric(
        label=f"📦 {col}",
        value=f"{total:,}",
        delta=f"{T['avg']}: {avg} | {T['max']}: {max_val}"
    )

st.divider()
st.markdown(T["chart"])
products = st.multiselect(T["filter"], value_cols, default=value_cols)

tab1, tab2 = st.tabs([T["line"], T["bar"]])

with tab1:
    fig_line = px.line(
        df, x=month_col, y=products,
        markers=True,
        title=T["line_title"],
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_line.update_layout(
        hovermode="x unified", height=450,
        xaxis_title=T["month_axis"],
        yaxis_title=T["sales_axis"]
    )
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    fig_bar = px.bar(
        df, x=month_col, y=products,
        barmode="group",
        title=T["bar_title"],
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar.update_layout(height=450)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.markdown(T["summary"])
c1, c2, c3 = st.columns(3)
best_col = df[value_cols].sum().idxmax()
worst_col = df[value_cols].sum().idxmin()
best_month = df.loc[df[value_cols].sum(axis=1).idxmax(), month_col]

with c1:
    st.success(f"{T['best_prod']}\n\n{best_col}")
with c2:
    st.error(f"{T['worst_prod']}\n\n{worst_col}")
with c3:
    st.info(f"{T['best_month']}\n\n{best_month}")

st.divider()
with st.expander(T["raw"]):
    st.dataframe(df, use_container_width=True)

st.markdown(T["export"])
c1, c2 = st.columns(2)
with c1:
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    st.download_button(T["dl_excel"], excel_buffer.getvalue(), "report.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
with c2:
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(T["dl_csv"], csv, "report.csv", mime="text/csv", use_container_width=True)

st.divider()
st.markdown(f"*{T['footer']}*")
