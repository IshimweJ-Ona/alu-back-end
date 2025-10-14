#!/usr/bin/python3
"""
Script to fetch users todos list progress of certain employee by giving the employee id
"""

import requests
import sys


def fetch_todos_employee(employee_id):
    #Urls
    USER_URL = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    TODO_URL = f"https://jsonplaceholder.typicode.com/todos?userId={employee_id}"

     # Fetch employee info
    user_resp = requests.get(USER_URL)
    if user_resp.status_code != 200:
        return {"error": "Failed to fetch employee info"}

    user_data = user_resp.json()
    employee_name = user_data.get("name")
    if not employee_name:
        return {"error": "Employee not found"}

    # Fetch TODO list
    todo_resp = requests.get(TODO_URL)
    if todo_resp.status_code != 200:
        return {"error": "Failed to fetch TODO list"}

    todo_data = todo_resp.json()
    done_tasks = [task.get("title") for task in todo_data if task.get("completed")]

    # Return dictionary
    return {
        "employee_name": employee_name,
        "total_tasks": len(todo_data),
        "completed_tasks": len(done_tasks),
        "tasks_done_titles": done_tasks
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} EMPLOYEE_ID")
        sys.exit(1)

    try:
        emp_id = int(sys.argv[1])
    except ValueError:
        print("EMPLOYEE_ID must be an interger")
        sys.exit(1)

    result = fetch_todos_employee(emp_id)

    if "error" in result:
        print(result["error"])
    else:
        print(f"Employee {result['employee_name']} is done with taks({result['completed_tasks']}/{result['total_tasks']}):")
        for title in result["tasks_done_titles"]:
            print(f"\t {title}")
            
