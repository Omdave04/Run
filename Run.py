import streamlit as st
from datetime import datetime
import pandas as pd
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Student Dashboard", layout="wide")

# ---------- GLASS CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(5,7,10,0.92), rgba(5,7,10,0.92)),
                url("https://images.unsplash.com/photo-1510070112810-d4e9a46d9e91?q=80&w=2069");
    background-size: cover;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(13,17,23,0.85);
    backdrop-filter: blur(10px);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg,#1f6feb,#2ea043);
    border-radius: 8px;
    color: white;
    font-weight: bold;
}

/* Metrics */
[data-testid="metric-container"] {
    background: rgba(13,17,23,0.7);
    border-radius: 12px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------- CSV ----------
FILE = "students.csv"

if not os.path.exists(FILE):
    pd.DataFrame(columns=["Name","Roll","Subject","Marks","Time"]).to_csv(FILE,index=False)

data = pd.read_csv(FILE)

# ---------- SIDEBAR NAV ----------
st.sidebar.title("Student Dashboard")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Record", "Records", "Analytics", "Manage Data"]
)

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.title("📊 Student Performance Dashboard")

    if data.empty:
        st.info("No data available")

    else:
        total = len(data)
        avg = round(data["Marks"].mean(),2)
        highest = data["Marks"].max()
        lowest = data["Marks"].min()

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Total Records", total)
        c2.metric("Average", avg)
        c3.metric("Highest", highest)
        c4.metric("Lowest", lowest)

        st.subheader("📈 Performance Chart")
        st.line_chart(data["Marks"])

# ================= ADD RECORD =================
elif menu == "Add Record":

    st.title("Add Student Record")

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

                st.success("Record added")

# ================= RECORDS =================
elif menu == "Records":

    st.title("Student Records")

    if data.empty:
        st.info("No records")
    else:
        st.dataframe(data, use_container_width=True)

# ================= ANALYTICS =================
elif menu == "Analytics":

    st.title("Analytics Dashboard")

    if data.empty:
        st.info("No data")
    else:
        st.bar_chart(data.groupby("Subject")["Marks"].mean())

# ================= MANAGE DATA =================
elif menu == "Manage Data":

    st.title("Manage Database")

    if st.button("Delete Last Record"):

        if not data.empty:
            data = data.iloc[:-1]
            data.to_csv(FILE,index=False)
            st.success("Last record deleted")
            st.rerun()

    if st.button("Reset Database"):
        pd.DataFrame(columns=["Name","Roll","Subject","Marks","Time"]).to_csv(FILE,index=False)
        st.success("Database reset")
        st.rerun()
