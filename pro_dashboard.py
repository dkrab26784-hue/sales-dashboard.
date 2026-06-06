import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Sales Dashboard", layout="wide", page_icon="📊")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Sales Dashboard")
st.markdown("Upload your data to get instant insights!")

# Demo or Upload
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("⬆️ Upload CSV or Excel", type=["csv","xlsx"])
with col2:
    use_demo = st.button("🎮 Try Demo Data")

# Load data
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully!")
elif use_demo:
    df = pd.DataFrame({
        "Month": ["Jan","Feb","Mar","Apr","May","Jun"],
        "Phone": [120,135,150,160,145,170],
        "Earphone": [80,90,85,95,100,110],
        "Case": [200,210,195,220,230,250]
    })
    st.info("🎮 Using demo data")
else:
    st.warning("⬆️ Upload your file or try demo data to get started!")
    st.stop()

# Column Mapping
st.subheader("🗂️ Column Mapping")
all_cols = df.columns.tolist()
month_col = st.selectbox("Select Month/Date column", all_cols)
value_cols = st.multiselect("Select value columns", 
                             [c for c in all_cols if c != month_col],
                             default=[c for c in all_cols if c != month_col])

if not value_cols:
    st.warning("Please select at least one value column")
    st.stop()

# KPI
st.subheader("📈 Key Metrics")
kpi_cols = st.columns(len(value_cols))
for i, col in enumerate(value_cols):
    total = df[col].sum()
    avg = round(df[col].mean(), 1)
    kpi_cols[i].metric(f"Total {col}", f"{total:,}", f"Avg: {avg}")

# Chart
st.subheader("📊 Sales Trend")
products = st.multiselect("Filter products", value_cols, default=value_cols)
fig = px.line(df, x=month_col, y=products, markers=True,
              title="Performance Over Time",
              template="plotly_white")
fig.update_layout(hovermode="x unified", height=400)
st.plotly_chart(fig, use_container_width=True)

# Summary
st.subheader("💡 Quick Summary")
best_col = df[value_cols].sum().idxmax()
worst_col = df[value_cols].sum().idxmin()
best_month = df.loc[df[value_cols].sum(axis=1).idxmax(), month_col]
st.success(f"🏆 Best performing: {best_col}")
st.error(f"⚠️ Needs attention: {worst_col}")
st.info(f"📅 Best month overall: {best_month}")

# Raw Data
with st.expander("📋 View Raw Data"):
    st.dataframe(df)

# Export
st.subheader("💾 Export")
col1, col2 = st.columns(2)

with col1:
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    st.download_button("📥 Download Excel", 
                       excel_buffer.getvalue(),
                       "data.xlsx",
                       mime="application/vnd.ms-excel")

with col2:
    csv = df.to_csv(index=False)
    st.download_button("📥 Download CSV",
                       csv,
                       "data.csv",
                       mime="text/csv")