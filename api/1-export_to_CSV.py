#!/usr/bin/python3
import csv
import requests
import sys


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        user_id = int(sys.argv[1])
        url = "https://jsonplaceholder.typicode.com"
        response = requests.get(f"{url}/users/{user_id}")
        if response.ok:
            user = response.json()
            response = requests.get(f"{url}/todos?userId={user_id}")
            if response.ok:
                todos = response.json()
                with open(f"{user_id}.csv", mode="w") as csv_file:
                    fieldnames = ["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"]
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    for todo in todos:
                        writer.writerow({
                            "USER_ID": user["id"],
                            "USERNAME": user["username"],
                            "TASK_COMPLETED_STATUS": str(todo["completed"]),
                            "TASK_TITLE": todo["title"]
                        })
                    print(f"{len(todos)} tasks have been exported to {user_id}.csv")
            else:
                print(f"Error: could not retrieve todos for user {user_id}")
        else:
            print(f"Error: could not retrieve user with id {user_id}")
    else:
        print("Usage: python3 1-export_to_CSV.py <user_id>")
