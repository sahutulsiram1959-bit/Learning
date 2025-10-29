import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# 🎯 Page Setup
# ======================
st.set_page_config(page_title="Event Management Dashboard", layout="wide")
st.title("🎉 Event Management Dashboard")

# ======================
# 📥 Load Excel File (same folder)
# ======================
FILE_PATH = "event_dashboard_data.xlsx"

try:
    df = pd.read_excel(FILE_PATH)
except FileNotFoundError:
    st.error("❌ 'event_dashboard_data.xlsx' not found. Please place it in the same folder as this file.")
    st.stop()

# ======================
# 🧹 Data Preparation
# ======================
df["Profit (USD)"] = df["Revenue (USD)"] - df["Budget (USD)"]

# ======================
# 📄 Data Preview
# ======================
with st.expander("📘 View Data Preview", expanded=False):
    st.dataframe(df.head())

# ======================
# 📊 KPI SECTION
# ======================
total_revenue = df["Revenue (USD)"].sum()
total_budget = df["Budget (USD)"].sum()
total_profit = df["Profit (USD)"].sum()
avg_attendance = round(df["Attendees"].mean(), 1)

st.markdown("## 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Budget", f"${total_budget:,.0f}")
col3.metric("Total Profit", f"${total_profit:,.0f}")
col4.metric("Average Attendance", f"{avg_attendance}")

st.divider()

# ======================
# 📉 Charts Section
# ======================
st.markdown("## 📊 Visual Insights")

# 1️⃣ Revenue Trend Over Time
fig1 = px.line(
    df.sort_values("Date"),
    x="Date",
    y="Revenue (USD)",
    title="Revenue Trend Over Time",
    markers=True,
)
st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Top 10 Events by Revenue
top_events = df.sort_values("Revenue (USD)", ascending=False).head(10)
fig2 = px.bar(
    top_events,
    x="Event Name",
    y="Revenue (USD)",
    title="Top 10 Events by Revenue",
    color="Revenue (USD)",
)
st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Budget vs Revenue (Bubble chart)
fig3 = px.scatter(
    df,
    x="Budget (USD)",
    y="Revenue (USD)",
    size="Attendees",
    color="Profit (USD)",
    hover_name="Event Name",
    title="Budget vs Revenue (Bubble Size = Attendees)",
)
st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Profit Distribution
fig4 = px.histogram(df, x="Profit (USD)", nbins=20, title="Profit Distribution Across Events")
st.plotly_chart(fig4, use_container_width=True)

st.success("✅ Dashboard loaded successfully!")
