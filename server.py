from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

tasks = []  # Stores tasks in memory (or use a database)

def generate_task_id():
    """ Generates a task ID in the format mm-dd-yyyy-taskNumber """
    today = datetime.date.today().strftime("%m-%d-%Y")
    task_number = len(tasks) + 1
    return f"{today}-{task_number}"

@app.route("/save-task", methods=["POST"])
def save_task():
    """ Saves a new task with title, category, time, and URL """
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
    return jsonify({"message": "Task saved!", "task_id": task_id})

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
