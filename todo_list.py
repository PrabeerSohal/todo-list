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

from datetime import date, time
from dataclasses import dataclass

@dataclass
class Task:

    description: str
    time: str
    date: int
    status: str

task = {}
 
def create_task():
	task_name = input('What is the task name?')
	description = input('Description:')
	time = input('Time:')
	date = input('Date:')
	status = input('Status:')
	task[task_name] = Task(description, time, date, status)


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
		print('Description:' + task[x].description + '\nTime:' + task[x].time + '\nDate:' + task[x].date + '\nStatus:' + task[x].status)
	except:
		print('Task not found')
		return
	print('What do you want to update? Press Enter if you do not want to update the particular information.')
	description = input('Description:')
	time = input('Time:')
	date = input('Date:')
	status = input('Status:')
	if description != '':
		task[x].description = description
	if time != '':
		task[x].time = time
	if date != '':
		task[x].date = date
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


			



	


