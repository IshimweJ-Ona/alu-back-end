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
import requests
import json
import sys

def export_all_employees_todo_to_json():
    base_url = "https://jsonplaceholder.typicode.com"

    #fetch all users
    try:
        users_response = requests.get("{}/users".format(base_url))
        users_response.raise_for_status()
        users = users_response.json()
    except Exception as e:
        print("Error fetching users:", e)
        return
    
    #fetch all todos
    try:
        todos_response = requests.get("{}/todos".format(base_url))
        todos_response.raise_for_status()
        todos = todos_response.json()
    except Exception as e:
        print("Error fetching todos:", e)
        return
    
    #dictionary 
    user_dict = {user.get("id"): user.get("username") for user in users}

    #json structure
    data = {}
    for task in todos:
        user_id = task.get("userId")
        if user_id not in data:
            data[user_id] = []

        data[user_id].append({
            "username": user_dict.get(user_id),
            "task": task.get("title"),
            "completed": task.get("completed")
        })

    # export to jsonfile
    filename = "todo_all_employees.json"
    try:
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file)
        print("Data exported to {}".format(filename))
    except Exception as e:
        print("Error writing JSON file:", e)


if __name__ == "__main__":
    export_all_employees_todo_to_json()
