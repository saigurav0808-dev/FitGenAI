from flask import Flask, request, render_template
from model import generate_plan
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "frontend"),
    static_folder=os.path.join(BASE_DIR, "frontend")
)

@app.route("/")
def landing():
    return render_template("landingPage.html")

@app.route("/user-details")
def user_details():
    return render_template("user-details.html")

@app.route("/processing", methods=["POST"])
def processing():
    form_data = request.form.to_dict()
    return render_template("processing.html", data=form_data)

@app.route("/result", methods=["POST"])
def result():
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

    return render_template("result.html", data=plan)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
