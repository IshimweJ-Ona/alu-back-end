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

    # Fetch user info
    user_url = "{}/users/{}".format(base_url, employee_id)
    user_response = requests.get(user_url)
    user_data = user_response.json()

    # If user doesn't exist
    if not user_data.get("name"):
        print("Employee not found.")
        return

    employee_name = user_data.get("name")

    # Fetch TODO list for the employee
    todos_url = "{}/todos".format(base_url)
    todos_response = requests.get(todos_url, params={"userId": employee_id})
    todos = todos_response.json()

    # Calculate task progress
    total_tasks = len(todos)
    done_tasks = [task for task in todos if task.get("completed")]
    number_of_done_tasks = len(done_tasks)

    # Display progress
    print("Employee {} is done with tasks({}/{}):".format(
        employee_name, number_of_done_tasks, total_tasks))

    # Display completed task titles
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
