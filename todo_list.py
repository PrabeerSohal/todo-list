# To do list in python

# Stage 1 ( 1 day):
# Terminal based
# Options:

# Create a task

# Each task should have:
# Description, time, date, status

# Delete a task

# Update a task
# Update anything in the task

# Storage: 
# store tasks in a file 

import json
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


def delete_task():
	x = input('Which task do you want to delete:')
	try:
		del task[x]
		print('Task ' + x + ' deleted')
	except:
		print('Key not found')	

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

def task_to_dict(task: Task):
    return {
        "description": task.description,
        "time": task.time.strftime("%H:%M"),
        "date": task.date.strftime("%Y-%m-%d"),
        "status": task.status
    }

def save_tasks(filename="tasks.json"):
    data = {}
    for name, task_obj in task.items():
        data[name] = task_to_dict(task_obj)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_tasks(filename="tasks.json"):
    global task
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        for name, task_data in data.items():
            task[name] = Task(
                description=task_data["description"],
                time=datetime.strptime(task_data["time"], "%H:%M").time(),
                date=datetime.strptime(task_data["date"], "%Y-%m-%d").date(),
                status=task_data["status"]
            )
    except FileNotFoundError:
        task = {}



load_tasks()
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
		save_tasks()
		break
print('Program Ended')		


			



	


