import streamlit as st
import pandas as pd
import os
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="GOD MODE Dashboard", layout="wide")

# ---------- THEME TOGGLE ----------
theme = st.sidebar.toggle("🌌 Dark Mode", value=True)

# ---------- FLOATING SIDEBAR + GLASS UI ----------
st.markdown(f"""
<style>
.stApp {{
    background: {"#0d1117" if theme else "#f4f6f8"};
    color: {"white" if theme else "black"};
}}

section[data-testid="stSidebar"] {{
    background: rgba(13,17,23,0.75);
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(255,255,255,0.08);
}}

.glass {{
    background: rgba(13,17,23,0.65);
    border-radius: 18px;
    padding: 22px;
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.25s ease;
}}

.glass:hover {{
    transform: translateY(-6px);
    box-shadow: 0 20px 50px rgba(0,0,0,0.65);
}}

.stButton > button {{
    background: linear-gradient(90deg,#1f6feb,#2ea043);
    border-radius: 12px;
    color: white;
    font-weight: bold;
    box-shadow: 0 0 18px rgba(31,111,235,0.6);
}}
</style>
""", unsafe_allow_html=True)

# ---------- CSV ----------
FILE = "students.csv"
if not os.path.exists(FILE):
    pd.DataFrame(columns=["Name","Roll","Subject","Marks","Time"]).to_csv(FILE,index=False)

data = pd.read_csv(FILE)

# ---------- SIDEBAR ----------
st.sidebar.title("📊 Dashboard")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Reports", "AI Insights"]
)

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.title("📊 GOD MODE Dashboard")

    if data.empty:
        st.info("No data available")

    else:
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Records", len(data))
        c2.metric("Average", round(data["Marks"].mean(),2))
        c3.metric("Highest", data["Marks"].max())
        c4.metric("Lowest", data["Marks"].min())

        # INTERACTIVE CHART
        fig = px.bar(
            data.groupby("Subject")["Marks"].mean().reset_index(),
            x="Subject",
            y="Marks",
            color="Subject",
            title="Average Marks by Subject"
        )
        st.plotly_chart(fig, use_container_width=True)

# ================= REPORTS =================
elif menu == "Reports":

    st.title("📥 Export Reports")

    if data.empty:
        st.info("No data")

    else:
        st.download_button(
            "Download CSV Report",
            data.to_csv(index=False),
            "student_report.csv",
            "text/csv"
        )

# ================= AI INSIGHTS =================
elif menu == "AI Insights":

    st.title("🧠 AI Insights")

    if data.empty:
        st.info("No data")

    else:
        topper = data.loc[data["Marks"].idxmax()]
        weakest = data.loc[data["Marks"].idxmin()]

        st.success(f"🏆 Top Performer: {topper['Name']} ({topper['Marks']})")
        st.warning(f"⚠️ Needs Improvement: {weakest['Name']} ({weakest['Marks']})")

        avg = data["Marks"].mean()

        if avg > 75:
            st.info("Overall class performance is strong 📈")
        else:
            st.info("Class performance needs improvement 📉")
