from flask import Flask, request, jsonify
import datetime
import threading
import time
import webbrowser

app = Flask(__name__)

tasks = []  # Stores tasks in memory

def generate_task_id():
    """ Generates a task ID in the format mm-dd-yyyy-taskNumber """
    today = datetime.date.today().strftime("%m-%d-%Y")
    task_number = len(tasks) + 1
    return f"{today}-{task_number}"

def wait_and_open(task_time, task_url):
    """ Waits until the specified time, then opens the URL """
    while True:
        now = datetime.datetime.now()
        if now >= task_time:
            webbrowser.open(task_url)  # Opens URL in default browser
            break
        time.sleep(5)  # Check every 5 seconds

@app.route("/save-task", methods=["POST"])
def save_task():
    """ Saves a new task and schedules a URL push automatically """
    data = request.json
    task_id = generate_task_id()
    task_time = datetime.datetime.strptime(data["time"], "%Y-%m-%dT%H:%M")
    
    task = {
        "id": task_id,
        "title": data["title"],
        "category": data["category"],
        "time": data["time"],
        "url": data["url"]
    }
    tasks.append(task)

    # Start a background thread to handle the URL push
    threading.Thread(target=wait_and_open, args=(task_time, data["url"]), daemon=True).start()

    return jsonify({"message": "Task saved and scheduled!", "task_id": task_id})

@app.route("/get-tasks", methods=["GET"])
def get_tasks():
    """ Returns all stored tasks """
    return jsonify(tasks)

@app.route("/delete-task/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """ Deletes a task by its unique ID """
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted!"})

if __name__ == "__main__":
    app.run(port=5000)
