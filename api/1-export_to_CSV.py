#!/usr/bin/python3
"""
Module that fetches an employee's TODO list and exports it to CSV.
Uses the JSONPlaceholder REST API: https://jsonplaceholder.typicode.com
"""

import csv
import requests
import sys

def export_employee_todo_to_csv(employee_id):
    """Fetch and export all TODO tasks for given employee id to csv."""
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

    #Fetch all todo tasks for the emloyee
    todos_response = requests.get("{}/todos".format(base_url),
                                  params={"userId": employee_id})
    todos = todos_response.json()

    # File name: USER_ID.csv
    filename = "{}.csv".format(employee_id)

    # Write csv with requested format only
    with open(filename, mode='w', newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for task in todos:
            writer.writerow([
                employee_id,
                username,
                task.get("completed"),
                task.get("title")
            ])

        print("Data exported to {}".format(filename))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <employee_id>".format(sys.argv[0]))
    else:
        try:
            emp_id = int(sys.argv[1])
            export_employee_todo_to_csv(emp_id)
        except ValueError:
            print("Employee ID must be an interger.")
