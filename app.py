from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev_fallback_temporary_key_123')

STUDENT_PROFILE = {
    "name": "Siddharth Goutham",
    "semester": "2nd Sem",
    "department": "Information Science & Engineering (ISE)",
    "section": "3",
    "college": "Bangalore Institute of Technology (BIT)",
    "cgpa": 9.35,
    "cgpa_change": "+0.3 this sem",
    "attendance": 93,
    "attendance_status": "Safe zone",
    "assignments_due": 3,
    "assignments_overdue": 1,
    "streak": 12,
}

# Added Individual Attendance metrics to each course node
SUBJECT_PERFORMANCE = [
    {"name": "Mathematics", "score": 58, "attendance": 84, "insight": "Need +20 marks to be safe", "status": "danger"},
    {"name": "Python", "score": 88, "attendance": 96, "insight": "Looking solid!", "status": "excellent"},
    {"name": "Chemistry", "score": 76, "attendance": 92, "insight": "Need +12 marks to be safe", "status": "warning"},
    {"name": "Introduction to Electrical Engineering (IEE)", "score": 70, "attendance": 90,
     "insight": "Need +15 marks to be safe", "status": "warning"},
    {"name": "Artificial Intelligence (AI)", "score": 82, "attendance": 95, "insight": "Need +8 marks to be safe",
     "status": "good"},
    {"name": "English", "score": 91, "attendance": 98, "insight": "Excellent command", "status": "excellent"}
]

LEADERBOARD = [
    {"rank": "🥇", "name": "Priya Sharma", "xp": "2,840 XP", "is_user": False},
    {"rank": "🥈", "name": "Rohan Mehta", "xp": "2,610 XP", "is_user": False},
    {"rank": "🥉", "name": "Kavya Nair", "xp": "2,190 XP", "is_user": False},
    {"rank": "4", "name": f"{STUDENT_PROFILE['name']} (you)", "xp": "1,340 XP", "is_user": True},
    {"rank": "5", "name": "Aditya Kumar", "xp": "1,280 XP", "is_user": False}
]

INSTANTS_FEED = [
    {
        "id": 1,
        "category": "Urgent",
        "author": "Alumni Veteran",
        "content": "Internal assessment pattern for Math is heavily repeating from the 2024 model papers. Do not skip the Fourier transform modules.",
        "verified": True,
        "boosts": 42,
        "expires_in": "12h left"
    },
    {
        "id": 2,
        "category": "Ghost class",
        "author": "Anonymous",
        "content": "Chem lab instructor is on leave today. Batch B text chains are saying session is pushed to next Tuesday.",
        "verified": False,
        "boosts": 8,
        "expires_in": "3h left"
    }
]

CLASS_TOOLS_STATE = {
    "prof_here_votes": {"yes": 3, "no": 12},
    "vibe_counts": {"lost": 5, "meh": 3, "got_it": 24, "great": 18, "too_much": 2}
}

WEEKLY_TIMETABLE = {
    "Monday": [
        {"time": "08:00", "subject": "Mathematics", "room": "Room 101", "prof": "Nikhitha S"},
        {"time": "09:00", "subject": "❌ Free Period (No Lecture)", "room": "Student Lounge", "prof": "None"},
        {"time": "10:00", "subject": "Short Break", "room": "Cafeteria", "prof": "-", "tag": "RELAX",
         "tag_class": "next"},
        {"time": "10:30", "subject": "Python", "room": "Room 204", "prof": "Prof. Deeksha C"},
        {"time": "01:30", "subject": "Lunch Break", "room": "Food Court", "prof": "-", "tag": "EAT",
         "tag_class": "next"},
        {"time": "02:00", "subject": "Chemistry", "room": "Room 302", "prof": "Dr. N Suresha"}
    ],
    "Tuesday": [
        {"time": "08:00", "subject": "⚡ Python Lab (2-Hour Block)", "room": "ISE Lab 2", "prof": "Prof. Shilpa T",
         "tag": "LAB", "tag_class": "live"},
        {"time": "09:00", "subject": "⚡ Python Lab (Contd.)", "room": "ISE Lab 2", "prof": "Prof. Shilpa T"},
        {"time": "10:00", "subject": "Short Break", "room": "Cafeteria", "prof": "-", "tag": "RELAX",
         "tag_class": "next"},
        {"time": "10:30", "subject": "Introduction to Electrical Engineering (IEE)", "room": "EE Block",
         "prof": "Avinash S"},
        {"time": "01:30", "subject": "Lunch Break", "room": "Food Court", "prof": "-", "tag": "EAT",
         "tag_class": "next"},
        {"time": "02:00", "subject": "Artificial Intelligence (AI)", "room": "AI Center", "prof": "Prof. Roopa B"}
    ],
    "Wednesday": [
        {"time": "08:00", "subject": "English", "room": "Humanities Wing", "prof": "Nisarga"},
        {"time": "10:00", "subject": "Short Break", "room": "Cafeteria", "prof": "-", "tag": "RELAX",
         "tag_class": "next"},
        {"time": "10:30", "subject": "Mathematics", "room": "Room 101", "prof": "Nikhitha S"},
        {"time": "01:30", "subject": "Lunch Break", "room": "Food Court", "prof": "-", "tag": "EAT",
         "tag_class": "next"},
        {"time": "02:00", "subject": "Python", "room": "Room 204", "prof": "Prof. Deeksha C"}
    ],
    "Thursday": [
        {"time": "08:00", "subject": "Chemistry", "room": "Room 302", "prof": "Dr. N Suresha"},
        {"time": "10:00", "subject": "Short Break", "room": "Cafeteria", "prof": "-", "tag": "RELAX",
         "tag_class": "next"},
        {"time": "10:30", "subject": "⚡ Chem Lab (2-Hour Block)", "room": "Chemistry Main Lab", "prof": "Dr. N Suresha",
         "tag": "LAB", "tag_class": "live"},
        {"time": "11:30", "subject": "⚡ Chem Lab (Contd.)", "room": "Chemistry Main Lab", "prof": "Dr. N Suresha"},
        {"time": "01:30", "subject": "Lunch Break", "room": "Food Court", "prof": "-", "tag": "EAT",
         "tag_class": "next"},
        {"time": "02:00", "subject": "Introduction to Electrical Engineering (IEE)", "room": "EE Block",
         "prof": "Avinash S"}
    ],
    "Friday": [
        {"time": "08:00", "subject": "Artificial Intelligence (AI)", "room": "AI Center", "prof": "Prof. Roopa B"},
        {"time": "10:00", "subject": "Short Break", "room": "Cafeteria", "prof": "-", "tag": "RELAX",
         "tag_class": "next"},
        {"time": "10:30", "subject": "English", "room": "Humanities Wing", "prof": "Nisarga"},
        {"time": "01:30", "subject": "Lunch Break", "room": "Food Court", "prof": "-", "tag": "EAT",
         "tag_class": "next"},
        {"time": "02:00", "subject": "Mathematics", "room": "Room 101", "prof": "Nikhitha S"}
    ]
}


def get_live_schedule(day_name):
    day_schedule = WEEKLY_TIMETABLE.get(day_name, [])
    if not day_schedule:
        return [{"time": "Weekend", "subject": "🎉 No Classes Scheduled", "room": "Home / Studio", "prof": "-",
                 "tag": "FREE", "tag_class": "next"}]

    processed_schedule = [dict(slot) for slot in day_schedule]
    now = datetime.now()
    current_absolute_mins = (now.hour * 60) + now.minute
    found_next = False

    for activity in processed_schedule:
        start_hours = int(activity["time"].split(":")[0])
        start_mins = int(activity["time"].split(":")[1]) if ":" in activity["time"] else 0
        start_absolute_mins = (start_hours * 60) + start_mins
        duration = 120 if "2-Hour Block" in activity.get("subject", "") or "Contd." in activity.get("subject",
                                                                                                    "") else (
            30 if "Break" in activity.get("subject", "") else 60)
        end_absolute_mins = start_absolute_mins + duration

        if start_absolute_mins <= current_absolute_mins < end_absolute_mins:
            activity["tag"] = "LIVE"
            activity["tag_class"] = "live"
        elif start_absolute_mins > current_absolute_mins and not found_next:
            activity["tag"] = "NEXT"
            activity["tag_class"] = "next"
            found_next = True

    return processed_schedule


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') == "admin" and request.form.get('password') == "password123":
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        error = "Invalid engineering keys. Try admin / password123"
    return render_template('login.html', error=error)


@app.route('/')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    current_day = datetime.now().strftime("%A")
    return render_template(
        'dashboard.html',
        profile=STUDENT_PROFILE,
        subjects=SUBJECT_PERFORMANCE,
        leaderboard=LEADERBOARD,
        instants=INSTANTS_FEED,
        class_tools=CLASS_TOOLS_STATE,
        schedule=get_live_schedule(current_day),
        current_day=current_day
    )


@app.route('/create_instant', methods=['POST'])
def create_instant():
    content = request.form.get('content')
    category = request.form.get('category', 'Social')
    anonymous = request.form.get('anonymous') == 'true'

    new_instant = {
        "id": len(INSTANTS_FEED) + 1,
        "category": category,
        "author": "Anonymous" if anonymous else STUDENT_PROFILE["name"],
        "content": content,
        "verified": False,
        "boosts": 0,
        "expires_in": "24h left"
    }
    INSTANTS_FEED.insert(0, new_instant)
    return redirect(url_for('dashboard'))


@app.route('/boost_instant/<int:post_id>', methods=['POST'])
def boost_instant(post_id):
    for post in INSTANTS_FEED:
        if post["id"] == post_id:
            post["boosts"] += 1
            if post["boosts"] >= 15:
                post["verified"] = True
            return jsonify({"status": "success", "new_boost_count": post["boosts"], "verified": post["verified"]})
    return jsonify({"status": "error"}), 404


@app.route('/vote_prof', methods=['POST'])
def vote_prof():
    data = request.json or {}
    vote = data.get('vote')
    if vote in CLASS_TOOLS_STATE["prof_here_votes"]:
        CLASS_TOOLS_STATE["prof_here_votes"][vote] += 1
    return jsonify({"status": "success", "votes": CLASS_TOOLS_STATE["prof_here_votes"]})


@app.route('/submit_vibe', methods=['POST'])
def submit_vibe():
    data = request.json or {}
    vibe = data.get('vibe')
    if vibe in CLASS_TOOLS_STATE["vibe_counts"]:
        CLASS_TOOLS_STATE["vibe_counts"][vibe] += 1
    return jsonify({"status": "success", "vibe_counts": CLASS_TOOLS_STATE["vibe_counts"]})


@app.route('/get_quiz/<subject>')
def get_quiz(subject):
    QUIZ_DATA = {
        "Mathematics": [{"q": "Evaluate ∫ x dx from 0 to 2.", "a": "2"}],
        "Python": [{"q": "What is output of print(type([]))?", "a": "<class 'list'>"}],
        "Artificial Intelligence (AI)": [{"q": "What does RAG stand for?", "a": "Retrieval-Augmented Generation"}]
    }
    quizzes = QUIZ_DATA.get(subject,
                            [{"q": "Review syllabus milestone metrics for this module block.", "a": "Check textbooks"}])
    return jsonify(quizzes)


@app.route('/book_proctor', methods=['POST'])
def book_proctor():
    data = request.json or {}
    return jsonify({"status": "success",
                    "message": f"1-on-1 Mentor session successfully locked for {data.get('subject', 'Core module')}!"})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
