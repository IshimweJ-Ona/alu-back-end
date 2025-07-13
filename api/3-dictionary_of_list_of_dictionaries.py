#!/usr/bin/python3
"""
we are to extract data from an rest api and display the data in a json dictionary format
Records all tasks from all employees
format musrt be:{ "USER_ID": [ {"username": "USERNAME", "task": "TASK_TITLE", "completed": TASK_COMPLETED_STATUS},
                             {"username": "USERNAME", "task": "TASK_TITLE", "completed": TASK_COMPLETED_STATUS}, 
                             ... ], 
                   "USER_ID": [ {"username": "USERNAME", "task": "TASK_TITLE", "completed": TASK_COMPLETED_STATUS}, 
                                {"username": "USERNAME", "task": "TASK_TITLE", "completed": TASK_COMPLETED_STATUS}, 
                ... ]}
File name must be: todo_all_employees.json
"""
import json
import requests
import sys

def main():
    if len(sys.argv) != 1:
        print("Usage: {} <no arguments required>".format(sys.argv[0]))
        return
    # Fetch all users
    users_response = requests.get("https://jsonplaceholder.typicode.com/users")
    users = users_response.json()
    # Fetch all todos
    todos_response = requests.get("https://jsonplaceholder.typicode.com/todos")
    todos = todos_response.json()
    # Prepare data for JSON export
    all_tasks_data = {}
    for user in users:
        user_id = user.get("id")
        username = user.get("username", "Unknown")
        tasks_data = [
            {
                "username": username,
                "task": task.get("title"),
                "completed": task.get("completed")
            } for task in todos if task.get("userId") == user_id
        ]
        all_tasks_data[user_id] = tasks_data
    # Write to JSON file
    filename = "todo_all_employees.json"
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(all_tasks_data, jsonfile, indent=4)

if __name__ == "__main__":
    main()
