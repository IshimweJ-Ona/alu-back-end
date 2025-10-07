#!/usr/bin/python3
"""
Module that fetches and displays TODO list progress for a given employee ID.
Uses the JSONPlaceholder REST API: https://jsonplaceholder.typicode.com
"""

import requests
import sys


def get_employee_todo_progress(employee_id):
    """Fetch and display the TODO list progress for the given employee ID."""
    base_url = "https://jsonplaceholder.typicode.com"

    try:
        user_response = requests.get("{}/users/{}".format(base_url, employee_id))
        user_response.raise_for_status()
        user_data = user_response.json()
    except Exception as e:
        print("Error fetching user:", e)
        return

    if not user_data or not user_data.get("name"):
        print("Employee not found.")
        return

    employee_name = user_data.get("name")

    todos_response = requests.get("{}/todos".format(base_url),
                                  params={"userId": employee_id})
    todos = todos_response.json()

    total_tasks = len(todos)
    done_tasks = [task for task in todos if task.get("completed")]

    print("Employee {} is done with tasks({}/{}):".format(
        employee_name, len(done_tasks), total_tasks))

    for task in done_tasks:
        print("\t {}".format(task.get("title")))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
    else:
        try:
            emp_id = int(sys.argv[1])
            get_employee_todo_progress(emp_id)
        except ValueError:
            print("Employee ID must be an integer.")
