import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "Indian_Food_Nutrition_Processed.csv")

GYM_WORKOUT = {
    "gain_muscle": {
        "Day 1": {
            "Chest": [
                "Bench Press – 4x8-10",
                "Incline Dumbbell Press – 3x10",
                "Chest Fly – 3x12",
                "Pushups – 2 sets till failure"
            ],
            "Triceps": [
                "Triceps Pushdown – 3x12",
                "Overhead Extension – 3x10",
                "Dips – 2 sets till failure"
            ]
        },
        "Day 2": {
            "Back": [
                "Lat Pulldown – 4x10",
                "Seated Row – 3x12",
                "Deadlift – 3x6"
            ],
            "Biceps": [
                "Barbell Curl – 3x10",
                "Hammer Curl – 3x12"
            ]
        },
        "Day 3": {
            "Legs": [
                "Squats – 4x8",
                "Leg Press – 3x10",
                "Leg Curl – 3x12",
                "Calf Raises – 4x15"
            ]
        },
        "Day 4": "Rest Day",
        "Day 5": {
            "Shoulders": [
                "Shoulder Press – 4x10",
                "Lateral Raises – 3x12",
                "Front Raises – 3x12",
                "Shrugs – 3x15"
            ]
        },
        "Day 6": {
            "Core": [
                "Plank – 3x45 sec",
                "Crunches – 3x20"
            ],
            "Cardio": [
                "Cycling / Treadmill – 20 min"
            ]
        },
        "Day 7": "Rest Day"
    }
}

HOME_WORKOUT = {
    "Day 1": {
        "Chest + Triceps": [
            "Push-ups – 4x12",
            "Incline Push-ups – 3x10",
            "Chair Dips – 3x12"
        ]
    },
    "Day 2": {
        "Back + Biceps": [
            "Door Rows – 4x10",
            "Biceps Curls (Water Bottles) – 3x15"
        ]
    },
    "Day 3": {
        "Legs": [
            "Bodyweight Squats – 4x15",
            "Lunges – 3x12",
            "Calf Raises – 4x20"
        ]
    },
    "Day 4": "Rest / Light Walking",
    "Day 5": {
        "Shoulders + Core": [
            "Pike Push-ups – 3x10",
            "Plank – 3x45 sec"
        ]
    },
    "Day 6": {
        "Cardio": [
            "Jumping Jacks – 3x40",
            "High Knees – 3x30 sec"
        ]
    },
    "Day 7": "Rest Day"
}

def generate_plan(age, gender, height_cm, weight_kg, goal, activity_level, workout_type):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        status = "Underweight"
    elif bmi < 25:
        status = "Normal"
    elif bmi < 30:
        status = "Overweight"
    else:
        status = "Obese"

    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    activity = {"low": 1.2, "moderate": 1.55, "high": 1.75}
    calories = int(bmr * activity[activity_level])

    df = pd.read_csv(CSV_PATH)
    df = df.rename(columns={
        "Dish Name": "Food",
        "Calories (kcal)": "Calories"
    })

    def pick_food(limit):
        return df[df["Calories"] <= limit].sample(1)["Food"].tolist()

    result = {
        "BMI": round(bmi, 2),
        "Status": status,
        "Calories": calories,
        "Breakfast": pick_food(calories * 0.3),
        "Lunch": pick_food(calories * 0.4),
        "Dinner": pick_food(calories * 0.3),
        "WorkoutType": workout_type
    }

    if workout_type == "home":
    result["WorkoutPlan"] = HOME_WORKOUT
else:
    result["WorkoutPlan"] = GYM_WORKOUT.get(goal, GYM_WORKOUT["gain_muscle"])


    return result



