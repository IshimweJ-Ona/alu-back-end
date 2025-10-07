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
    try:
        user_response = requests.get("{}/users/{}".format(base_url, employee_id))
        user_response.raise_for_status()
        user_data = user_response.json()
    except Exception as e:
        print("Error fetching user:", e)
        return

    if not user_data or not user_data.get("username"):
        print("Employee not found.")
        return

    username = user_data.get("username")

    # Fetch all TODO tasks for the employee
    todos_response = requests.get("{}/todos".format(base_url),
                                  params={"userId": employee_id})
    todos = todos_response.json()

    #JSON sturcture
    tasks_list = []
    for task in todos:
        tasks_list.append({
            "task": task.get("title"),
            "completed": task.get("completed"),
            "username": username
        })

    data = {str(employee_id): tasks_list}

    #Write Json file
    filename = "{}.json".format(employee_id)
    try:
        with open(filename, mode='w', encoding="utf-8") as json_file:
            json.dump(data, json_file)
        print("Data exported to {}".format(filename))
    except Exception as e:
        print("Error writing JSON file:", e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USage: {} <employee_id>".format(sys.argv[0]))
    else:
        try:
            emp_id = int(sys.argv[1])
            export_employee_todo_to_json(emp_id)
        except ValueError:
            print("Employee Id must be an integer.")
            
