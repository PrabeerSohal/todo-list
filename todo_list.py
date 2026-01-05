import sqlite3
from datetime import datetime, date, time
from dataclasses import dataclass
from flask import Flask, jsonify, request

@dataclass
class Task:
    description: str
    time: time
    date: date
    status: str

task = {}

def get_valid_status():
    while True:
        status = input("Status (done / not done): ").strip().lower()
        if status in {"done", "not done"}:
            return status
        print("Status must be 'done' or 'not done'")

def get_valid_date():
    while True:
        date_str = input("Date (YYYY-MM-DD): ").strip()
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_valid_time():
    while True:
        time_str = input("Time (HH:MM): ").strip()
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            print("Invalid time format. Please use HH:MM (24-hour).")

def create_task():
    task_name = input('What is the task name? ')
    description = input('Description: ')
    task_time = get_valid_time()
    task_date = get_valid_date()
    status = get_valid_status()
    task[task_name] = Task(description, task_time, task_date, status)
    save_task_to_db(task_name, task[task_name])

def delete_task():
    x = input('Which task do you want to delete: ')
    if x in task:
        del task[x]
        delete_task_from_db(x)
        print(f'Task {x} deleted')
    else:
        print('Task not found')

def update_task():
    x = input('Which task do you want to update: ')
    try:
        print(
            f"Description: {task[x].description}"
            f"\nTime: {task[x].time}"
            f"\nDate: {task[x].date}"
            f"\nStatus: {task[x].status}"
        )
    except KeyError:
        print('Task not found')
        return

    print('What do you want to update? Press Enter if you do not want to update the particular information.')
    description = input('Description: ')
    time_input = input('Time (HH:MM): ')
    date_input = input('Date (YYYY-MM-DD): ')
    status = input('Status (done / not done): ').strip().lower()

    if description != '':
        task[x].description = description
    if time_input != '':
        task[x].time = datetime.strptime(time_input, "%H:%M").time()
    if date_input != '':
        task[x].date = datetime.strptime(date_input, "%Y-%m-%d").date()
    if status != '':
        if status in {"done", "not done"}:
            task[x].status = status
        else:
            print("Invalid status, keeping old value.")

    save_task_to_db(x, task[x])

def task_to_dict(task_obj: Task):
    return {
        "description": task_obj.description,
        "time": task_obj.time.strftime("%H:%M"),
        "date": task_obj.date.strftime("%Y-%m-%d"),
        "status": task_obj.status
    }

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    name TEXT PRIMARY KEY,
    description TEXT,
    time TEXT,
    date TEXT,
    status TEXT
)
""")
conn.commit()

def save_task_to_db(task_name, task_obj):
    cursor.execute("""
    INSERT OR REPLACE INTO tasks (name, description, time, date, status)
    VALUES (?, ?, ?, ?, ?)
    """, (
        task_name,
        task_obj.description,
        task_obj.time.strftime("%H:%M"),
        task_obj.date.strftime("%Y-%m-%d"),
        task_obj.status
    ))
    conn.commit()

def load_tasks_from_db():
    global task
    task = {}
    cursor.execute("SELECT name, description, time, date, status FROM tasks")
    rows = cursor.fetchall()
    for name, desc, t_str, d_str, status in rows:
        task[name] = Task(
            description=desc,
            time=datetime.strptime(t_str, "%H:%M").time(),
            date=datetime.strptime(d_str, "%Y-%m-%d").date(),
            status=status
        )

def delete_task_from_db(task_name):
    cursor.execute("DELETE FROM tasks WHERE name = ?", (task_name,))
    conn.commit()

app = Flask(__name__)

def validate_status_value(status: str) -> bool:
    return status in {"done", "not done"}

def parse_date_str(date_str: str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def parse_time_str(time_str: str):
    return datetime.strptime(time_str, "%H:%M").time()

@app.route("/tasks", methods=["GET"])
def api_get_tasks():
    load_tasks_from_db()
    all_tasks = {
        name: task_to_dict(t_obj) for name, t_obj in task.items()
    }
    return jsonify(all_tasks)

@app.route("/tasks/<name>", methods=["GET"])
def api_get_task(name):
    load_tasks_from_db()
    if name not in task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task_to_dict(task[name]))

@app.route("/tasks", methods=["POST"])
def api_create_task():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required = ["name", "description", "time", "date", "status"]
    if any(k not in data for k in required):
        return jsonify({"error": f"Missing one of required fields: {required}"}), 400

    try:
        task_time = parse_time_str(data["time"])
        task_date = parse_date_str(data["date"])
    except ValueError:
        return jsonify({"error": "Invalid date or time format. Use HH:MM and YYYY-MM-DD."}), 400

    status = data["status"].strip().lower()
    if not validate_status_value(status):
        return jsonify({"error": "Status must be 'done' or 'not done'"}), 400

    task_obj = Task(
        description=data["description"],
        time=task_time,
        date=task_date,
        status=status
    )

    save_task_to_db(data["name"], task_obj)
    return jsonify({"message": "Task created", "name": data["name"]}), 201

@app.route("/tasks/<name>", methods=["PUT"])
def api_update_task(name):
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    load_tasks_from_db()
    if name not in task:
        return jsonify({"error": "Task not found"}), 404

    current = task[name]

    description = data.get("description", current.description)
    time_str = data.get("time", current.time.strftime("%H:%M"))
    date_str = data.get("date", current.date.strftime("%Y-%m-%d"))
    status = data.get("status", current.status).strip().lower()

    try:
        task_time = parse_time_str(time_str)
        task_date = parse_date_str(date_str)
    except ValueError:
        return jsonify({"error": "Invalid date or time format. Use HH:MM and YYYY-MM-DD."}), 400

    if not validate_status_value(status):
        return jsonify({"error": "Status must be 'done' or 'not done'"}), 400

    updated = Task(
        description=description,
        time=task_time,
        date=task_date,
        status=status
    )

    save_task_to_db(name, updated)
    return jsonify({"message": "Task updated"})

@app.route("/tasks/<name>", methods=["DELETE"])
def api_delete_task(name):
    load_tasks_from_db()
    if name not in task:
        return jsonify({"error": "Task not found"}), 404

    delete_task_from_db(name)
    return jsonify({"message": f"Task '{name}' deleted"})

if __name__ == "__main__":
    load_tasks_from_db()
    while True:
        print('Press 1 to create a task')
        print('Press 2 to delete a task')
        print('Press 3 to update a task')
        print('Press 4 to end program')
        x = input()
        if x == '1':
            create_task()
        elif x == '2':
            delete_task()
        elif x == '3':
            update_task()
        elif x == '4':
            break
    print('Program Ended')
