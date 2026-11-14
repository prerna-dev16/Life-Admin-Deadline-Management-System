
import json
import os
from datetime import datetime, date

FILE_NAME = "deadlines.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task(tasks):
    print("\n--- ADD NEW TASK ---")

    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()

    while True:
        due_date = input("Enter deadline (YYYY-MM-DD): ")
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date! Please use YYYY-MM-DD.")

    task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": "Pending"
    }

    tasks.append(task)
    save_tasks(tasks)

    print("\nTask added successfully!")


def view_tasks(tasks):
    print("\n--- ALL TASKS ---")

    if not tasks:
        print("No tasks available.")
        return

    today = date.today()

    for task in tasks:
        deadline = datetime.strptime(
            task["due_date"], "%Y-%m-%d"
        ).date()

        if task["status"] == "Completed":
            status = "Completed"
        elif deadline < today:
            status = "Overdue"
        else:
            status = "Pending"

        print("\nTask ID:", task["id"])
        print("Title:", task["title"])
        print("Description:", task["description"])
        print("Deadline:", task["due_date"])
        print("Status:", status)
        print("-" * 30)


def view_by_status(tasks, status):
    filtered = [
        task for task in tasks
        if task["status"] == status
    ]

    if not filtered:
        print(f"\nNo {status.lower()} tasks found.")
        return

    print(f"\n--- {status.upper()} TASKS ---")

    for task in filtered:
        print(
            f"ID: {task['id']} | "
            f"Title: {task['title']} | "
            f"Deadline: {task['due_date']}"
        )


def view_overdue(tasks):
    today = date.today()
    overdue = []

    for task in tasks:
        deadline = datetime.strptime(
            task["due_date"], "%Y-%m-%d"
        ).date()

        if deadline < today and task["status"] == "Pending":
            overdue.append(task)

    print("\n--- OVERDUE TASKS ---")

    if not overdue:
        print("No overdue tasks!")
        return

    for task in overdue:
        print(
            f"ID: {task['id']} | "
            f"Title: {task['title']} | "
            f"Deadline: {task['due_date']}"
        )


def complete_task(tasks):
    try:
        task_id = int(input("Enter task ID to complete: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "Completed":
                print("Task is already completed.")
            else:
                task["status"] = "Completed"
                save_tasks(tasks)
                print("Task marked as completed!")
            return

    print("Task ID not found.")


def delete_task(tasks):
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print("Task deleted successfully!")
            return

    print("Task ID not found.")


def main():
    tasks = load_tasks()

    while True:
        print("\n================================")
        print("     DEADLINE MANAGEMENT SYSTEM")
        print("================================")
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. View Overdue Tasks")
        print("6. Mark Task as Completed")
        print("7. Delete Task")
        print("8. Exit")
        print("================================")

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            view_by_status(tasks, "Pending")
        elif choice == "4":
            view_by_status(tasks, "Completed")
        elif choice == "5":
            view_overdue(tasks)
        elif choice == "6":
            complete_task(tasks)
        elif choice == "7":
            delete_task(tasks)
        elif choice == "8":
            print("Thank you for using Deadline Manager!")
            break
        else:
            print("Invalid choice! Please select 1-8.")


if __name__ == "__main__":
    main()
