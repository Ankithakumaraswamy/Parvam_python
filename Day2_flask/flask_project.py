import os
from functools import wraps
from pathlib import Path

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, session, url_for
from mysql.connector import Error
from werkzeug.security import check_password_hash, generate_password_hash


def load_env_file():
    env_path = Path(__file__).with_name(".env")

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


load_env_file()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "127.0.0.1")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT", "3306"))
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "")
app.config["MYSQL_DATABASE"] = os.getenv("MYSQL_DATABASE", "flask_task_manager")


def get_db_connection():
    return mysql.connector.connect(
        host=app.config["MYSQL_HOST"],
        port=app.config["MYSQL_PORT"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"],
    )


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Email already registered. Please log in.", "warning")
                return redirect(url_for("login"))

            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                (name, email, password_hash),
            )
            connection.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
        except Error as exc:
            flash(f"Database error: {exc}", "danger")
        finally:
            if "cursor" in locals():
                cursor.close()
            if "connection" in locals() and connection.is_connected():
                connection.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("login.html")

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                flash("Login successful.", "success")
                return redirect(url_for("dashboard"))

            flash("Invalid email or password.", "danger")
        except Error as exc:
            flash(f"Database error: {exc}", "danger")
        finally:
            if "cursor" in locals():
                cursor.close()
            if "connection" in locals() and connection.is_connected():
                connection.close()

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, title, description, status, created_at
            FROM tasks
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (session["user_id"],),
        )
        tasks = cursor.fetchall()
    except Error as exc:
        flash(f"Database error: {exc}", "danger")
        tasks = []
    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()

    return render_template("dashboard.html", tasks=tasks)


@app.route("/tasks/add", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Pending")

        if not title:
            flash("Task title is required.", "danger")
            return render_template("task_form.html", task=None, action="Add")

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (user_id, title, description, status)
                VALUES (%s, %s, %s, %s)
                """,
                (session["user_id"], title, description, status),
            )
            connection.commit()
            flash("Task added successfully.", "success")
            return redirect(url_for("dashboard"))
        except Error as exc:
            flash(f"Database error: {exc}", "danger")
        finally:
            if "cursor" in locals():
                cursor.close()
            if "connection" in locals() and connection.is_connected():
                connection.close()

    return render_template("task_form.html", task=None, action="Add")


def get_task_for_user(task_id, user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s AND user_id = %s",
        (task_id, user_id),
    )
    task = cursor.fetchone()
    cursor.close()
    connection.close()
    return task


@app.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = get_task_for_user(task_id, session["user_id"])

    if not task:
        flash("Task not found.", "warning")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Pending")

        if not title:
            flash("Task title is required.", "danger")
            return render_template("task_form.html", task=task, action="Edit")

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE tasks
                SET title = %s, description = %s, status = %s
                WHERE id = %s AND user_id = %s
                """,
                (title, description, status, task_id, session["user_id"]),
            )
            connection.commit()
            flash("Task updated successfully.", "success")
            return redirect(url_for("dashboard"))
        except Error as exc:
            flash(f"Database error: {exc}", "danger")
        finally:
            if "cursor" in locals():
                cursor.close()
            if "connection" in locals() and connection.is_connected():
                connection.close()

        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "status": status,
        }

    return render_template("task_form.html", task=task, action="Edit")


@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s AND user_id = %s",
            (task_id, session["user_id"]),
        )
        connection.commit()
        flash("Task deleted successfully.", "info")
    except Error as exc:
        flash(f"Database error: {exc}", "danger")
    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)


