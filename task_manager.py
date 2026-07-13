import json
import os

TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(tasks):
    title = input("Task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return
    next_id = max((task["id"] for task in tasks), default=0) + 1
    tasks.append({"id": next_id, "title": title, "done": False})
    save_tasks(tasks)
    print(f"Added task {next_id}: {title}")


def view_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return
    for task in tasks:
        status = "x" if task["done"] else " "
        print(f"[{status}] {task['id']}: {task['title']}")


def complete_task(tasks):
    try:
        task_id = int(input("Task id to complete: ").strip())
    except ValueError:
        print("Please enter a valid task id.")
        return
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"Marked task {task_id} as complete.")
            return
    print(f"No task found with id {task_id}.")


def delete_task(tasks):
    try:
        task_id = int(input("Task id to delete: ").strip())
    except ValueError:
        print("Please enter a valid task id.")
        return
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Deleted task {task_id}.")
            return
    print(f"No task found with id {task_id}.")


def main():
    tasks = load_tasks()
    menu = (
        "\n--- Task Manager ---\n"
        "1. Add task\n"
        "2. View tasks\n"
        "3. Mark task complete\n"
        "4. Delete task\n"
        "5. Exit\n"
    )
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid option, please choose 1-5.")


if __name__ == "__main__":
    main()
