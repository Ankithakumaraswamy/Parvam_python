import json
import os
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key_for_calorie_app"
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "foods": [], "meals": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    
    data = load_data()
    username = session["username"]
    user_info = data["users"].get(username, {})
    goal = user_info.get("goal", 2000)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Get user's meals for today
    meals_today = [m for m in data["meals"] if m.get("username") == username and m.get("date") == today]
    
    total_calories = sum(int(m["calories"]) * int(m["qty"]) for m in meals_today)
    remaining_calories = max(0, goal - total_calories)
    
    # Meal-wise breakdown
    breakdown = {"Breakfast": 0, "Lunch": 0, "Dinner": 0, "Snack": 0}
    for m in meals_today:
        meal_type = m.get("meal", "Snack")
        if meal_type in breakdown:
            breakdown[meal_type] += int(m["calories"]) * int(m["qty"])
            
    foods = data["foods"]
    
    return render_template("index.html", 
                           username=username, 
                           goal=goal, 
                           total_calories=total_calories, 
                           remaining_calories=remaining_calories,
                           breakdown=breakdown,
                           meals=meals_today,
                           foods=foods,
                           today=today)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        age = request.form.get("age", type=int)
        weight = request.form.get("weight", type=float)
        occupation = request.form.get("occupation")
        workout_frequency = request.form.get("workout_frequency")
        goal = request.form.get("goal", 2000, type=int)
        
        data = load_data()
        if username in data["users"]:
            flash("Username already exists", "error")
            return redirect(url_for("register"))
            
        data["users"][username] = {
            "password": generate_password_hash(password),
            "age": age,
            "weight": weight,
            "occupation": occupation,
            "workout_frequency": workout_frequency,
            "goal": goal
        }
        save_data(data)
        
        # Auto-login after registration
        session["username"] = username
        flash("Welcome! Your account has been created.", "success")
        return redirect(url_for("index"))
        
    return render_template("login.html", action="register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        data = load_data()
        user_info = data["users"].get(username)
        
        if user_info and check_password_hash(user_info["password"], password):
            session["username"] = username
            return redirect(url_for("index"))
            
        flash("Invalid username or password", "error")
        return redirect(url_for("login"))
        
    return render_template("login.html", action="login")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/add_food", methods=["POST"])
def add_food():
    if "username" not in session:
        return redirect(url_for("login"))
        
    food_name = request.form.get("food")
    meal_type = request.form.get("meal")
    calories = request.form.get("calories", type=int)
    qty = request.form.get("qty", 1, type=int)
    
    if not all([food_name, meal_type, calories]):
        flash("Please fill all fields", "error")
        return redirect(url_for("index"))
        
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Save food to DB if it doesn't exist
    if not any(f.get("name", "").lower() == food_name.lower() for f in data["foods"]):
        data["foods"].append({"name": food_name, "calories": calories})
        
    data["meals"].append({
        "id": str(uuid.uuid4()),
        "username": session["username"],
        "date": today,
        "food": food_name,
        "meal": meal_type,
        "calories": calories,
        "qty": qty
    })
    save_data(data)
    
    return redirect(url_for("index"))

@app.route("/delete_log/<log_id>", methods=["POST"])
def delete_log(log_id):
    if "username" not in session:
        return redirect(url_for("login"))
        
    data = load_data()
    username = session["username"]
    
    original_len = len(data["meals"])
    data["meals"] = [m for m in data["meals"] if not (m.get("id") == log_id and m.get("username") == username)]
    
    if len(data["meals"]) < original_len:
        save_data(data)
        flash("Log deleted.", "success")
    else:
        flash("Log not found or access denied.", "error")
        
    return redirect(url_for("index"))

@app.route("/edit_log/<log_id>", methods=["POST"])
def edit_log(log_id):
    if "username" not in session:
        return redirect(url_for("login"))
        
    data = load_data()
    username = session["username"]
    
    for m in data["meals"]:
        if m.get("id") == log_id and m.get("username") == username:
            m["food"] = request.form.get("food")
            m["meal"] = request.form.get("meal")
            m["calories"] = request.form.get("calories", type=int)
            m["qty"] = request.form.get("qty", type=int)
            save_data(data)
            flash("Log updated.", "success")
            return redirect(url_for("index"))
            
    flash("Log not found or access denied.", "error")
    return redirect(url_for("index"))

@app.route("/reports")
def reports():
    if "username" not in session:
        return redirect(url_for("login"))
        
    data = load_data()
    username = session["username"]
    
    # Get last 7 days
    today = datetime.now()
    last_7_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    
    weekly_data = {date: 0 for date in last_7_days}
    meal_distribution = {"Breakfast": 0, "Lunch": 0, "Dinner": 0, "Snack": 0}
    
    user_meals = [m for m in data["meals"] if m.get("username") == username]
    
    for m in user_meals:
        date = m.get("date")
        cal = int(m.get("calories", 0)) * int(m.get("qty", 1))
        
        if date in weekly_data:
            weekly_data[date] += cal
            
        meal_type = m.get("meal", "Snack")
        if meal_type in meal_distribution:
            meal_distribution[meal_type] += cal
            
    return render_template("reports.html", 
                           weekly_labels=list(weekly_data.keys()),
                           weekly_values=list(weekly_data.values()),
                           meal_labels=list(meal_distribution.keys()),
                           meal_values=list(meal_distribution.values()))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
