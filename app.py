import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# File paths
STUDENTS_FILE = "students.json"
ATTENDANCE_FILE = "attendance.csv"

# Initialize files if they don't exist
if not os.path.exists(STUDENTS_FILE):
    with open(STUDENTS_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(ATTENDANCE_FILE):
    pd.DataFrame(columns=["Date", "Student ID", "Name", "Status"]).to_csv(ATTENDANCE_FILE, index=False)


# Load students data
def load_students():
    with open(STUDENTS_FILE, "r") as f:
        return json.load(f)


# Save students data
def save_students(students):
    with open(STUDENTS_FILE, "w") as f:
        json.dump(students, f)


# Load attendance data
def load_attendance():
    return pd.read_csv(ATTENDANCE_FILE)


# Save attendance data
def save_attendance(data):
    data.to_csv(ATTENDANCE_FILE, index=False)


# Streamlit UI
st.title("📌 Attendance Management System")

# Sidebar navigation
menu = st.sidebar.radio("Navigation", ["Register Students", "Mark Attendance", "View Attendance"])

# 📌 Register Students
if menu == "Register Students":
    st.subheader("📝 Register a New Student")

    student_id = st.text_input("Enter Student ID:")
    student_name = st.text_input("Enter Student Name:")

    if st.button("Register"):
        students = load_students()
        if any(s["id"] == student_id for s in students):
            st.error("⚠️ Student ID already exists!")
        else:
            students.append({"id": student_id, "name": student_name})
            save_students(students)
            st.success(f"✅ Student {student_name} registered successfully!")

    st.subheader("📋 Registered Students")
    students = load_students()
    st.table(pd.DataFrame(students))

# 📌 Mark Attendance
elif menu == "Mark Attendance":
    st.subheader("✅ Mark Attendance")

    students = load_students()
    if not students:
        st.warning("⚠️ No students registered yet!")
    else:
        present_students = st.multiselect("Select Present Students", [s["name"] for s in students])

        if st.button("Submit Attendance"):
            today = datetime.today().strftime("%Y-%m-%d")
            attendance_data = load_attendance()

            for student in students:
                status = "Present" if student["name"] in present_students else "Absent"
                new_entry = pd.DataFrame(
                    [{"Date": today, "Student ID": student["id"], "Name": student["name"], "Status": status}]
                )
                attendance_data = pd.concat([attendance_data, new_entry], ignore_index=True)

            save_attendance(attendance_data)
            st.success("✅ Attendance marked successfully!")

# 📌 View Attendance
elif menu == "View Attendance":
    st.subheader("📊 View Attendance Records")

    attendance_data = load_attendance()
    if attendance_data.empty:
        st.warning("⚠️ No attendance records found!")
    else:
        st.table(attendance_data)

    # Export CSV
    st.download_button(
        "Download Attendance CSV",
        attendance_data.to_csv(index=False).encode("utf-8"),
        "attendance.csv",
        "text/csv",
    )
