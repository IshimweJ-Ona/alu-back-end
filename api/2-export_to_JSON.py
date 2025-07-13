#!/usr/bin/python3
"""
Exports employee's TODO list progress to a JSON file.
Records all tasks that are owned by this employee
Format of the json must be: { "USER_ID": [{"task": "TASK_TITLE", "completed": TASK_COMPLETED_STATUS, "username": "USERNAME"},
                                           {"task": "TASK_TITLE", "completed": TASK_COMPLETED_STATUS, "username": "USERNAME"}, 
                                           ... ]}
"""
import requests
import sys
import json

def main():
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        return

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer.")
        return

    # Fetch employee info
    user_response = requests.get(
        "https://jsonplaceholder.typicode.com/users/{}".format(employee_id)
    )
    user = user_response.json()
    username = user.get("username", "Unknown")

    # Fetch employee's todos
    todos_response = requests.get(
        "https://jsonplaceholder.typicode.com/todos",
        params={"userId": employee_id}
    )
    todos = todos_response.json()

    # Prepare data for JSON export
    tasks_data = [
        {
            "task": task.get("title"),
            "completed": task.get("completed"),
            "username": username
        } for task in todos
    ]

    # Write to JSON file
    filename = "{}.json".format(employee_id)
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump({employee_id: tasks_data}, jsonfile, indent=4)

if __name__ == "__main__":
    main()
