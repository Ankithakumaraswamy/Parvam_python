# 🌿 NutriLore — Food Calorie Counter

A nutrition tracking web app built with **Python & Flask**, featuring a dark alchemical UI and real-time calorie tracking.

---

## ✨ Features
- 🔐 User authentication (register / login / logout)
- 📊 Live SVG calorie ring with animated progress bar
- 🔍 Food autocomplete with calorie auto-fill
- 🟥 Red warning when daily calorie goal is exceeded
- 🍽️ Meal breakdown by Breakfast, Lunch, Dinner, Snack
- 📅 Full history log across past days
- 📚 Searchable food reference (30+ items)

---

## 🚀 Setup

```bash
git clone https://github.com/YOUR_USERNAME/food-calorie-counter.git
cd food-calorie-counter
pip install flask
python app.py
```
Then open `http://127.0.0.1:5000`

---

## 🧪 Selenium Tests

```bash
pip install selenium webdriver-manager
python test_selenium.py   # (Flask must be running)
```

---

## 🗂️ Structure

```
├── app.py
├── foods.json        ← food database
├── meals.json        ← daily logs
├── users.json        ← accounts
├── static/css & js
└── templates/
```

---

## 🛠️ Tech Stack
`Python` · `Flask` · `JSON` · `Vanilla JS` · `CSS Animations` · `Selenium`

---

<p align="center">Made with 🌿 and Python</p>