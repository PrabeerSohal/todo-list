# Stage 2:
# Move tasks from file to database. Use sqlite3

import sqlite3
from datetime import datetime, date, time
from dataclasses import dataclass

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
        del task[x]  # remove from memory
        delete_task_from_db(x)  # remove from database
        print(f'Task {x} deleted')
    else:
        print('Task not found')	


def update_task():
	x = input('Which task do you want to update:')
	try:
		print(f"Description: {task[x].description}"
		f"\nTime: {task[x].time}"
		f"\nDate: {task[x].date}"
		f"\nStatus: {task[x].status}")
	except:
		print('Task not found')
		return
	print('What do you want to update? Press Enter if you do not want to update the particular information.')
	description = input('Description:')
	time_input = input('Time (HH:MM): ')
	date_input = input('Date (YYYY-MM-DD): ')
	status = input('Status:')
	if description != '':
		task[x].description = description
	if time_input != '':
		task[x].time = datetime.strptime(time_input, "%H:%M").time()
	if date_input != '':
		task[x].date = datetime.strptime(date_input, "%Y-%m-%d").date()
	if status != '':
		task[x].status = status

	save_task_to_db(x, task[x])


def task_to_dict(task: Task):
    return {
        "description": task.description,
        "time": task.time.strftime("%H:%M"),
        "date": task.date.strftime("%Y-%m-%d"),
        "status": task.status
    }


conn = sqlite3.connect("tasks.db")
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


load_tasks_from_db()
while True:
	print('Press 1 to create a task\nPress 2 to delete a task\nPress 3 to update a task\nPress 4 to end program')
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


			



	


