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

from datetime import datetime, date, time
from dataclasses import dataclass

@dataclass
class Task:
    description: str
    time: time
    date: date
    status: str

task = {}
 
def create_task():
	task_name = input('What is the task name? ')
	description = input('Description: ')

	time_str = input('Time (HH:MM): ')
	date_str = input('Date (YYYY-MM-DD): ')

	status = input('Status: ')

	task_time = datetime.strptime(time_str, "%H:%M").time()
	task_date = datetime.strptime(date_str, "%Y-%m-%d").date()

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


			



	


