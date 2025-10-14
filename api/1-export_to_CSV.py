#!/usr/bin/python3
"""
Module that exports an employee's TODO list to a CSV file.
Uses the JSONPlaceholder REST API: https://jsonplaceholder.typicode.com
"""

import csv
import requests
import sys


def export_to_csv(employee_id):
    """Fetch and export TODO list data for a given employee ID to CSV."""
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

    # File name format: USER_ID.csv
    filename = "{}.csv".format(employee_id)

    # Write data to CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
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
            export_to_csv(emp_id)
        except ValueError:
            print("Employee ID must be an integer.")
