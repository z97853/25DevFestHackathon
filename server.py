from flask import Flask, request, jsonify
import datetime
import threading
import time
import webbrowser
import json
import os
import platform

app = Flask(__name__)

tasks = []  # Stores tasks in memory
URL_LOG_FILE = "opened_urls.json"

# Load opened URLs from file
def load_opened_urls():
    try:
        with open(URL_LOG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save opened URLs to file
def save_opened_urls(opened_urls):
    with open(URL_LOG_FILE, "w") as file:
        json.dump(opened_urls, file)

def generate_task_id():
    """ Generates a task ID in the format mm-dd-yyyy-taskNumber """
    today = datetime.date.today().strftime("%m-%d-%Y")
    task_number = len(tasks) + 1
    return f"{today}-{task_number}"

@app.route("/save-task", methods=["POST"])
def save_task():
    """ Saves a new task and schedules focus lock automatically """
    data = request.json
    task_id = generate_task_id()
    task = {
        "id": task_id,
        "title": data["title"],
        "category": data["category"],
        "time": data["time"],
        "url": data["url"]
    }
    tasks.append(task)

    # Start a background thread to open and lock the task
    task_time = datetime.datetime.strptime(data["time"], "%Y-%m-%dT%H:%M")
    threading.Thread(target=wait_and_open, args=(task_time, data["url"]), daemon=True).start()

    return jsonify({"message": "Task saved & focus lock scheduled!", "task_id": task_id})

@app.route("/get-tasks", methods=["GET"])
def get_tasks():
    """ Returns all stored tasks (To-Do List) """
    return jsonify(tasks)

@app.route("/focus-lock", methods=["POST"])
def focus_lock():
    """ Starts the 5-minute focus lock """
    data = request.json
    url = data["url"]
    threading.Thread(target=lock_for_5_minutes, args=(url,), daemon=True).start()
    return jsonify({"message": "Focus mode started for 5 minutes!"})

def lock_for_5_minutes(url):
    """ Opens URL and locks focus for 5 minutes """
    webbrowser.open(url)
    time.sleep(300)  # Lock for 5 minutes

def wait_and_open(task_time, task_url):
    """ Waits until the specified time, then opens the URL with focus lock """
    while True:
        now = datetime.datetime.now()
        if now >= task_time:
            webbrowser.open(task_url)
            threading.Thread(target=lock_for_5_minutes, args=(task_url,), daemon=True).start()
            break
        time.sleep(5)

if __name__ == "__main__":
    app.run(port=5000)
