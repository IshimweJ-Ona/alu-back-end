#!/usr/bin/python3
"""
Fetches and displays an employee's TODO list progress
using the JSONPlaceholder REST API.
"""

import requests
import sys

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
    employee_name = user.get("name", "Unknown")

    # Fetch employee's todos
    todos_response = requests.get(
        "https://jsonplaceholder.typicode.com/todos",
        params={"userId": employee_id}
    )
    todos = todos_response.json()

    # Filter completed tasks
    completed_tasks = [task for task in todos if task.get("completed") is True]

    # Print summary
    print(
        "Employee {} is done with tasks({}/{}):".format(
            employee_name,
            len(completed_tasks),
            len(todos)
        )
    )

    # Print completed task titles
    for task in completed_tasks:
        print("\t {}".format(task.get("title")))

if __name__ == "__main__":
    main()
