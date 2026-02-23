import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Student Analytics Dashboard", layout="wide")

# ---------- THEME TOGGLE ----------
theme = st.sidebar.toggle("🌌 Dark Mode", value=True)

# ---------- GLASS UI ----------
st.markdown(f"""
<style>
.stApp {{
    background: {"#0d1117" if theme else "#f4f6f8"};
    color: {"white" if theme else "black"};
}}

section[data-testid="stSidebar"] {{
    background: rgba(13,17,23,0.75);
    backdrop-filter: blur(14px);
}}

.stButton > button {{
    background: linear-gradient(90deg,#1f6feb,#2ea043);
    border-radius: 12px;
    color: white;
    font-weight: bold;
}}

[data-testid="metric-container"] {{
    background: rgba(13,17,23,0.7);
    border-radius: 12px;
    padding: 15px;
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
    ["Dashboard", "Add Record", "Reports", "AI Insights"]
)

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.title("📊 Student Performance Dashboard")

    if data.empty:
        st.info("No data available")

    else:
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Records", len(data))
        c2.metric("Average", round(data["Marks"].mean(),2))
        c3.metric("Highest", data["Marks"].max())
        c4.metric("Lowest", data["Marks"].min())

        st.subheader("📈 Subject Performance")
        st.bar_chart(data.groupby("Subject")["Marks"].mean())

# ================= ADD RECORD =================
elif menu == "Add Record":

    st.title("✍️ Add Student Record")

    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")

    subject = st.selectbox(
        "Subject",
        ["Math","Science","English","Computer"],
        index=None,
        placeholder="Select Subject"
    )

    marks = st.number_input("Marks",0,100)

    if st.button("Add Record"):

        name = name.strip()
        roll = roll.strip()

        if not name or not roll or not subject:
            st.warning("Fill all fields")

        else:
            duplicate = ((data["Roll"] == roll) & (data["Subject"] == subject)).any()

            if duplicate:
                st.error("Duplicate entry")

            else:
                new = pd.DataFrame([{
                    "Name": name,
                    "Roll": roll,
                    "Subject": subject,
                    "Marks": marks,
                    "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])

                data = pd.concat([data,new],ignore_index=True)
                data.to_csv(FILE,index=False)

                st.success("Record added successfully")
                st.rerun()

# ================= REPORTS =================
elif menu == "Reports":

    st.title("📥 Reports & Export Center")

    if data.empty:
        st.info("No data available")

    else:

        report_type = st.selectbox(
            "Select Report",
            [
                "Full Report",
                "Topper Leaderboard",
                "Risk Students",
                "Time-based Report"
            ]
        )

        if report_type == "Full Report":

            st.dataframe(data, use_container_width=True)

            st.download_button(
                "Download Full Report",
                data.to_csv(index=False),
                "full_report.csv",
                "text/csv"
            )

        elif report_type == "Topper Leaderboard":

            leaderboard = data.sort_values("Marks", ascending=False).head(10)
            st.dataframe(leaderboard, use_container_width=True)

        elif report_type == "Risk Students":

            risk = data[data["Marks"] < 50]
            st.dataframe(risk, use_container_width=True)

        elif report_type == "Time-based Report":

            data["Time"] = pd.to_datetime(data["Time"])
            time_data = data.sort_values("Time")

            st.line_chart(time_data.set_index("Time")["Marks"])

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
