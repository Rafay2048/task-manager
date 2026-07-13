import json
import os
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")
HEALTH_TASKS_FILE = os.path.join(BASE_DIR, "health_tasks.json")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")

DEFAULT_HEALTH_TASKS = [
    "Drink a glass of water right now",
    "Take a 10 minute walk outside",
    "Stretch for 5 minutes",
]


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


def load_health_tasks():
    if not os.path.exists(HEALTH_TASKS_FILE):
        return DEFAULT_HEALTH_TASKS
    try:
        with open(HEALTH_TASKS_FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, ValueError):
        return DEFAULT_HEALTH_TASKS
    if not isinstance(data, list) or not data:
        return DEFAULT_HEALTH_TASKS
    tasks = []
    for item in data:
        if isinstance(item, str):
            tasks.append(item)
        elif isinstance(item, dict):
            for key in ("task", "title", "name", "description"):
                if key in item:
                    tasks.append(str(item[key]))
                    break
    return tasks or DEFAULT_HEALTH_TASKS


class TaskHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    def _extract_id(self, path, suffix=""):
        segment = path[len("/api/tasks/"):]
        if suffix and segment.endswith(suffix):
            segment = segment[: -len(suffix)]
        try:
            return int(segment)
        except ValueError:
            return None

    def _serve_index(self):
        if not os.path.exists(INDEX_FILE):
            self.send_error(404, "index.html not found")
            return
        with open(INDEX_FILE, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._serve_index()
        elif path == "/api/tasks":
            self._send_json(load_tasks())
        elif path == "/api/health-task":
            tasks = load_health_tasks()
            self._send_json({"task": random.choice(tasks)})
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/tasks":
            body = self._read_json_body()
            title = (body.get("title") or "").strip()
            if not title:
                self._send_json({"error": "Title is required"}, status=400)
                return
            tasks = load_tasks()
            next_id = max((t["id"] for t in tasks), default=0) + 1
            task = {"id": next_id, "title": title, "done": False}
            tasks.append(task)
            save_tasks(tasks)
            self._send_json(task, status=201)
        elif path.startswith("/api/tasks/") and path.endswith("/complete"):
            task_id = self._extract_id(path, suffix="/complete")
            tasks = load_tasks()
            task = next((t for t in tasks if t["id"] == task_id), None)
            if task is None:
                self._send_json({"error": "Task not found"}, status=404)
                return
            task["done"] = True
            save_tasks(tasks)
            self._send_json(task)
        else:
            self.send_error(404, "Not found")

    def do_DELETE(self):
        path = urlparse(self.path).path
        if path.startswith("/api/tasks/"):
            task_id = self._extract_id(path)
            tasks = load_tasks()
            remaining = [t for t in tasks if t["id"] != task_id]
            if len(remaining) == len(tasks):
                self._send_json({"error": "Task not found"}, status=404)
                return
            save_tasks(remaining)
            self._send_json({"deleted": task_id})
        else:
            self.send_error(404, "Not found")

    def log_message(self, format, *args):
        pass


def main():
    port = 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), TaskHandler)
    print(f"Task Manager web UI running at http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
