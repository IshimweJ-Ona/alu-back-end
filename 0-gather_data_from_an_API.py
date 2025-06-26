#!/usr/bin/python3
"""Module to display TODO list progress of a given employee using REST API."""

import requests
import sys


def get_todo_list():
    """Fetch all TODO tasks from the API."""
    url = 'https://jsonplaceholder.typicode.com/todos/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code)
        return []


def get_user_name(employee_id):
    """Fetch the name of the employee using their ID."""
    url = 'https://jsonplaceholder.typicode.com/users/{}'.format(employee_id)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('name')
    else:
        print("Failed to retrieve employee information.")
        return None


def display_employee_progress(employee_id):
    """Display the completed TODO tasks for a given employee."""
    todos = get_todo_list()
    employee_name = get_user_name(employee_id)

    if not employee_name:
        return

    user_tasks = [task for task in todos if task.get('userId') == employee_id]
    done_tasks = [task for task in user_tasks if task.get('completed')]

    print("Employee {} is done with tasks({}/{}):".format(
        employee_name, len(done_tasks), len(user_tasks)))
    for task in done_tasks:
        print("\t {}".format(task.get('title')))


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: ./todo_progress.py <employee_id>")
    else:
        display_employee_progress(int(sys.argv[1]))
