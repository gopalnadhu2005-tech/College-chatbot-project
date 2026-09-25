from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "college.db"


# Create database and add sample college information
def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS college_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            keyword TEXT,
            answer TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM college_info")
    count = cursor.fetchone()[0]

    if count == 0:

        data = [
            (
                "General",
                "college",
                "Welcome to ABC College of Engineering and Technology."
            ),
            (
                "General",
                "principal",
                "The Principal is Dr. R. Kumar."
            ),
            (
                "General",
                "timing",
                "College working hours are from 9:00 AM to 4:30 PM."
            ),
            (
                "Admission",
                "admission",
                "Admissions are available for B.E, B.Tech, M.E and MBA programmes."
            ),
            (
                "Admission",
                "courses",
                "The college offers CSE, ECE, EEE, Mechanical, Civil and AI & Data Science."
            ),
            (
                "Fees",
                "fees",
                "The fee structure depends on the course and admission category."
            ),
            (
                "Department",
                "cse",
                "The CSE department teaches programming, databases, networking, AI and software development."
            ),
            (
                "Department",
                "ece",
                "The ECE department teaches electronics, communication systems, embedded systems and IoT."
            ),
            (
                "Library",
                "library",
                "The college library is open from 9:00 AM to 5:00 PM."
            ),
            (
                "Hostel",
                "hostel",
                "Separate hostel facilities are available for boys and girls."
            ),
            (
                "Transport",
                "bus",
                "College bus transportation is available on selected routes."
            ),
            (
                "Exam",
                "exam",
                "Semester examinations are conducted according to the academic schedule."
            ),
            (
                "Attendance",
                "attendance",
                "Students must maintain the minimum attendance required by university regulations."
            ),
            (
                "Placement",
                "placement",
                "The placement cell provides aptitude training, technical training and campus recruitment."
            ),
            (
                "Scholarship",
                "scholarship",
                "Eligible students can apply for government and institutional scholarships."
            ),
            (
                "Contact",
                "contact",
                "College Office: 04500-123456. Email: office@abccollege.edu"
            ),
            (
                "Location",
                "location",
                "ABC College is located near the main town."
            ),
            (
                "Timetable",
                "timetable",
                "Students can get the timetable from their department office."
            ),
            (
                "Events",
                "events",
                "The college conducts technical events, cultural events, sports competitions and workshops."
            )
        ]

        cursor.executemany(
            """
            INSERT INTO college_info
            (category, keyword, answer)
            VALUES (?, ?, ?)
            """,
            data
        )

    connection.commit()
    connection.close()


# Find chatbot answer
def get_answer(message):

    message = message.lower().strip()

    if message == "":
        return "Please type a question."

    if "hello" in message or "hi" in message:
        return "Hello! Welcome to the College Chatbot. How can I help you?"

    if "thank" in message:
        return "You're welcome!"

    if "bye" in message:
        return "Goodbye! Have a great day."

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT keyword, answer FROM college_info"
    )

    records = cursor.fetchall()

    connection.close()

    for keyword, answer in records:

        if keyword.lower() in message:
            return answer

    return (
        "Sorry, I could not find that information. "
        "You can ask about courses, admission, fees, "
        "library, hostel, transport, exams, attendance, "
        "placements or scholarships."
    )


# Home page
@app.route("/")
def home():

    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message", "")

    answer = get_answer(message)

    return jsonify({
        "answer": answer
    })


# Start Flask
if __name__ == "__main__":

    create_database()

    app.run(debug=True)
if __name__ == "__main__":
    app.run()   