import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Task Manager", layout="centered")
# st.title("Task Manager")

# def get_tasks():
#     try:
#         res = requests.get(f"{API_BASE_URL}/tasks")
#         if res.status_code == 200:
#             data = res.json()
#             return data if isinstance(data, dict) else {}
#         else:
#             st.error(f"Error fetching tasks: {res.status_code}")
#             return {}
#     except requests.exceptions.ConnectionError:
#         st.error("Could not connect to API. Is Flask running?")
#         return {}

# def create_task_api(name, description, time_str, date_str, status):
#     payload = {
#         "name": name,
#         "description": description,
#         "time": time_str,
#         "date": date_str,
#         "status": status,
#     }
#     return requests.post(f"{API_BASE_URL}/tasks", json=payload)

# def update_task_api(name, description=None, time_str=None, date_str=None, status=None):
#     payload = {}
#     if description: payload["description"] = description
#     if time_str: payload["time"] = time_str
#     if date_str: payload["date"] = date_str
#     if status: payload["status"] = status

#     if not payload:
#         return None

#     return requests.put(f"{API_BASE_URL}/tasks/{name}", json=payload)

# tasks = get_tasks()

# completed = {n:t for n,t in tasks.items() if t.get("status") == "done"}
# incomplete = {n:t for n,t in tasks.items() if t.get("status") != "done"}

# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("Incomplete Tasks")
#     if incomplete:
#         for name, t in incomplete.items():
#             st.markdown(
#                 f"**{name}**  \n"
#                 f"{t.get('description','')}  \n"
#                 f"Time: {t.get('time','')}  \n"
#                 f"Date: {t.get('date','')}"
#             )
#             st.divider()
#     else:
#         st.write("No incomplete tasks.")

# with col2:
#     st.subheader("Completed Tasks")
#     if completed:
#         for name, t in completed.items():
#             st.markdown(
#                 f"**{name}**  \n"
#                 f"{t.get('description','')}  \n"
#                 f"Time: {t.get('time','')}  \n"
#                 f"Date: {t.get('date','')}"
#             )
#             st.divider()
#     else:
#         st.write("No completed tasks.")

# st.divider()
# st.header("Create Task")

# with st.form("create_form"):
#     new_name = st.text_input("Task name")
#     new_desc = st.text_input("Description")
#     new_time = st.text_input("Time (HH:MM)")
#     new_date = st.text_input("Date (YYYY-MM-DD)")
#     new_status = st.radio("Status", ["not done", "done"], horizontal=True)

#     submitted = st.form_submit_button("Create Task")

#     if submitted:
#         if not new_name:
#             st.error("Task name required.")
#         else:
#             res = create_task_api(new_name, new_desc, new_time, new_date, new_status)
#             if res.status_code == 201:
#                 st.success(f"Task '{new_name}' created.")
#                 st.rerun()
#             else:
#                 st.error(res.json())

# st.divider()
# st.header("Update Task")

# if tasks:
#     selected = st.selectbox("Select task", list(tasks.keys()))
#     current = tasks[selected]

#     with st.form("update_form"):
#         upd_desc = st.text_input(
#             "New description (blank = keep same)",
#             placeholder=current.get("description","")
#         )
#         upd_time = st.text_input(
#             "New time HH:MM (blank = keep same)",
#             placeholder=current.get("time","")
#         )
#         upd_date = st.text_input(
#             "New date YYYY-MM-DD (blank = keep same)",
#             placeholder=current.get("date","")
#         )

#         upd_status = st.radio(
#             "Status",
#             ["keep current", "not done", "done"],
#             index=0,
#             horizontal=True
#         )

#         update_btn = st.form_submit_button("Update Task")

#         if update_btn:
#             status_value = None
#             if upd_status == "done":
#                 status_value = "done"
#             elif upd_status == "not done":
#                 status_value = "not done"

#             res = update_task_api(
#                 selected,
#                 upd_desc,
#                 upd_time,
#                 upd_date,
#                 status_value
#             )

#             if res is None:
#                 st.info("No changes made.")
#             elif res.status_code == 200:
#                 st.success("Task updated.")
#                 st.rerun()
#             else:
#                 st.error(res.json())
# else:
#     st.info("No tasks to update yet.")
