from flask import Flask, request, render_template, redirect, session, url_for
from model import generate_plan
import time
import sqlite3
from chatbot import ask_chatbot

app = Flask(__name__)
app.secret_key = "fitgenai_secret"

# Database connection
conn = sqlite3.connect("fitgenai.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
message TEXT,
submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# ---------------- LANDING PAGE ----------------
@app.route("/")
def landing():
    return render_template("landingPage.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Email already registered. Please login."

        cursor.execute(
        "INSERT INTO users(name,email,password) VALUES (?,?,?)",
        (name,email,password)
        )

        conn.commit()

        return redirect("/login")

    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
        )

        user = cursor.fetchone()

        if user:
            session["user"] = email
            return redirect("/profile")

        else:
            return "Invalid Login"

    return render_template("login.html")


# ---------------- USER DETAILS ----------------
@app.route("/user-details")
def user_details():

    if "user" not in session:
        return redirect("/login")

    return render_template("user-details.html")


# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    email = session["user"]
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    if not user:
        return redirect("/login")

    user_data = {
        "id": user[0],
        "name": user[1],
        "email": user[2]
    }

    return render_template("profile.html", user=user_data)


# ---------------- PROCESSING ----------------
@app.route("/processing", methods=["POST"])
def processing():

    form_data = request.form.to_dict()

    return render_template("processing.html", data=form_data)


# ---------------- RESULT ----------------
@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        time.sleep(2)

        plan = generate_plan(
            age=int(request.form["age"]),
            gender=request.form["gender"],
            height_cm=int(request.form["height"]),
            weight_kg=int(request.form["weight"]),
            goal=request.form["goal"],
            activity_level=request.form["activity"],
            workout_type=request.form["workout_type"]
        )

        session["plan"] = plan
        return render_template("result.html", data=plan)

    plan = session.get("plan")
    if not plan:
        return redirect(url_for("user_details"))

    return render_template("result.html", data=plan)


# ---------------- FEEDBACK ----------------
@app.route("/feedback", methods=["POST"])
def feedback():

    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not (name and email and message):
        return "All feedback fields are required.", 400

    cursor.execute(
        "INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )
    conn.commit()

    return redirect("/user-details")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    reply = ask_chatbot(user_message)

    return {"reply": reply}
    
@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    print("Server Starting...")
    app.run(debug=True)