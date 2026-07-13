# Task Manager

A simple task manager with two interfaces sharing the same data:
- A **Python CLI** (`task_manager.py`)
- A **web UI** (`app.py` + `index.html`) with a "Task of the Day" health tip feature

Both read and write the same `tasks.json` file, so tasks stay in sync no matter which one you use.

## Features

- Add a task
- View all tasks
- Mark a task complete
- Delete a task
- Random "Task of the Day" health suggestion (web UI only)
- Mobile-friendly, responsive interface (web UI)

## Requirements

- Python 3.8+
- No external dependencies — everything uses the Python standard library

## Getting Started

Clone the repo and `cd` into it:

```bash
git clone <your-repo-url>
cd taskmanager
```

### Option 1: Command-line interface

```bash
python task_manager.py
```

You'll see a menu:

```
1. Add task
2. View tasks
3. Mark task complete
4. Delete task
5. Exit
```

Type a number and press Enter to choose an action.

### Option 2: Web interface

```bash
python app.py
```

Then open **http://127.0.0.1:8000/** in your browser.

- Add tasks from the input field at the top
- Check the box to mark a task complete
- Click **Delete** to remove a task
- Click **New suggestion** on the green card for another healthy task idea

Stop the server with `Ctrl+C`.

## Project Structure

```
taskmanager/
├── task_manager.py    # CLI app
├── app.py             # Web server + JSON API
├── index.html          # Web UI
├── tasks.json          # Task storage (created automatically)
├── health_tasks.json   # Pool of "Task of the Day" health suggestions
└── README.md
```

## Data Storage

Tasks are stored in `tasks.json` as a list of objects:

```json
[
  { "id": 1, "title": "Buy groceries", "done": false }
]
```

The file is created automatically the first time you add a task.

## Customizing the Health Suggestions

Edit `health_tasks.json` to change the pool of "Task of the Day" suggestions. It accepts either:

- A list of plain strings:
  ```json
  ["Drink a glass of water", "Take a 10 minute walk"]
  ```
- A list of objects with a `task`, `title`, `name`, or `description` field:
  ```json
  [{ "task": "Drink a glass of water" }]
  ```

## Web API Reference

| Method | Endpoint                  | Description                    |
|--------|----------------------------|---------------------------------|
| GET    | `/api/tasks`               | List all tasks                 |
| POST   | `/api/tasks`               | Add a task (`{"title": "..."}`) |
| POST   | `/api/tasks/<id>/complete` | Mark a task complete           |
| DELETE | `/api/tasks/<id>`          | Delete a task                  |
| GET    | `/api/health-task`         | Get a random health suggestion |

## License

No license file is included yet. Add a `LICENSE` file (e.g. MIT) if you want to make reuse terms explicit before sharing this publicly.
