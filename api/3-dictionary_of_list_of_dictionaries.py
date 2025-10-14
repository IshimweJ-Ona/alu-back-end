#!/usr/bin/python3
"""
Module that fetches all employees' TODO lists and exports them to JSON.

Uses the JSONPlaceholder REST API:
https://jsonplaceholder.typicode.com
"""

import json
import requests


def export_all_employees_to_json():
    """
    Fetch and export all employees' TODO tasks to a single JSON file.
    """
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch all users
    users_response = requests.get("{}/users".format(base_url))
    users = users_response.json()

    # Fetch all todos
    todos_response = requests.get("{}/todos".format(base_url))
    todos = todos_response.json()

    # Dictionary to store all users' data
    all_data = {}

    for user in users:
        user_id = user.get("id")
        username = user.get("username")

        # Filter tasks for this user
        user_tasks = [task for task in todos if task.get("userId") == user_id]

        # Store tasks in the required format
        all_data[str(user_id)] = [
            {
                "username": username,
                "task": task.get("title"),
                "completed": task.get("completed")
            }
            for task in user_tasks
        ]

    # Write all data to a single JSON file
    filename = "todo_all_employees.json"
    with open(filename, mode="w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file)


if __name__ == "__main__":
    export_all_employees_to_json()
