#!/usr/bin/python3
"""
Module that fetches an employee's TODO list and exports it to JSON.
Uses the JSONPlaceholder REST API: https://jsonplaceholder.typicode.com
"""

import json
import requests
import sys


def export_employee_todo_to_json(employee_id):
    """Fetch and export all TODO tasks for a given employee ID to JSON."""
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch user information
    user_url = "{}/users/{}".format(base_url, employee_id)
    user_response = requests.get(user_url)
    user_data = user_response.json()

    if not user_data.get("username"):
        print("Employee not found.")
        return

    username = user_data.get("username")

    # Fetch employee's TODO tasks
    todos_url = "{}/todos".format(base_url)
    todos_response = requests.get(todos_url, params={"userId": employee_id})
    todos = todos_response.json()

    # Build JSON data structure
    tasks_list = []
    for task in todos:
        tasks_list.append({
            "task": task.get("title"),
            "completed": task.get("completed"),
            "username": username
        })

    data = {str(employee_id): tasks_list}

    # File name format: USER_ID.json
    filename = "{}.json".format(employee_id)

    # Write JSON file
    with open(filename, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file)

    print("Data exported to {}".format(filename))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
    else:
        try:
            emp_id = int(sys.argv[1])
            export_employee_todo_to_json(emp_id)
        except ValueError:
            print("Employee ID must be an integer.")
