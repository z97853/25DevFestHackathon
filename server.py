from flask import Flask, request, jsonify
import json
import webbrowser
import datetime
import time
import os
import platform

URL_LOG_FILE = "opened_urls.json"

app = Flask(__name__)

tasks = []  # Stores tasks in memory

def generate_task_id():
    """ Generates a task ID in the format mm-dd-yyyy-taskNumber """
    today = datetime.date.today().strftime("%m-%d-%Y")
    task_number = len(tasks) + 1
    return f"{today}-{task_number}"


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

# Function to bring browser tab to front and make it full screen
def bring_to_front(url):
    system = platform.system()

    if system == "Darwin":  # macOS (Google Chrome)
        os.system(f'osascript -e \'tell application "Google Chrome" to activate\'')
        os.system(f'osascript -e \'tell application "Google Chrome" to set bounds of front window to {{0, 0, 1920, 1080}}\'')  # Full-screen
    elif system == "Windows":  # Windows (Google Chrome)
        os.system(f'powershell (New-Object -ComObject WScript.Shell).AppActivate("Chrome")')
        os.system(f'powershell (New-Object -ComObject WScript.Shell).SendKeys("^{VK_F11}")')  # Full-screen mode

def wait_and_open(task_time, task_url):
    """ Waits until the specified time, then opens or retrieves the URL and makes it full screen. """
    opened_urls = load_opened_urls()
    
    while True:
        now = datetime.datetime.now()
        if now >= task_time:
            if task_url in opened_urls:
                print(f"URL already opened: {task_url}, bringing it to the front.")
                bring_to_front(task_url)  # Bring the tab to the front and full screen
            else:
                webbrowser.open(task_url)  # Opens URL in default browser
                opened_urls[task_url] = now.strftime("%Y-%m-%d %H:%M:%S")  # Store timestamp
                save_opened_urls(opened_urls)  # Save to file
                print(f"Opened URL: {task_url} at {now}")
                time.sleep(3)  # Give browser time to open
                bring_to_front(task_url)  # Bring to front & full screen
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
