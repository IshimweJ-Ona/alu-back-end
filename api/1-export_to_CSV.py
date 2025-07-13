#!usr/bin/python3
#  we are going to extract employee names and their completed tasks in CSV format 
# the format must use USER_ID, USERNAME, TASK_COMPLETED_STATUS, TASK_TITLE
# the file name must be USER_ID.csv
import requests
import sys
import csv

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
    user_response = requests.get("https://jsonplaceholder.typicode.com/users/{}".format(employee_id))
    user = user_response.json()
    username = user.get("username", "Unknown")
    # Fetch employee's todos
    todos_response = requests.get("https://jsonplaceholder.typicode.com/todos", params={"userId": employee_id})
    todos = todos_response.json()

    #write to csv file
    filename = "{}.csv".format(employee_id)
    with open(filename, mode="w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for task in todos:
            writer.writerow({
                employee_id,
                username,
                str(task.get("completed")),
                task.get("title")
            })

if __name__ == "__main__":
    main()
