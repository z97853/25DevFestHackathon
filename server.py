from flask import Flask, request, jsonify
import datetime
import threading
import time
import webbrowser
import sys
import signal
import logging
from AppKit import NSWorkspace, NSRunningApplication, NSApplicationActivateAllWindows, NSApplicationActivateIgnoringOtherApps

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

# Handle Ctrl+C gracefully
def signal_handler(signum, frame):
    print("\nShutting down...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def focus_browser():
    """Focus the browser window using AppKit."""
    try:
        # Get all running applications
        running_apps = NSWorkspace.sharedWorkspace().runningApplications()
        
        # Extended list of common browsers and their variants
        browsers = [
            'Safari', 'Google Chrome', 'Firefox', 'Chromium', 
            'Microsoft Edge', 'Opera', 'Brave Browser'
        ]
        
        for app in running_apps:
            app_name = app.localizedName()
            logging.debug(f"Checking application: {app_name}")
            
            if any(browser.lower() in app_name.lower() for browser in browsers):
                logging.info(f"Found browser: {app_name}")
                # Activate the browser window with proper options
                activation_options = NSApplicationActivateAllWindows | NSApplicationActivateIgnoringOtherApps
                success = app.activateWithOptions_(activation_options)
                
                if success:
                    logging.info(f"Successfully activated {app_name}")
                    return True
                else:
                    logging.warning(f"Failed to activate {app_name}")
            
        logging.warning("No supported browsers found running")
        return False
        
    except Exception as e:
        logging.error(f"Error focusing browser window: {str(e)}", exc_info=True)
        return False

def keep_tab_active(url, interval=30):
    """
    Keep a browser tab active by periodically bringing it to front.
    
    Args:
        url (str): The URL to keep active
        interval (int): Seconds between focus attempts
    """
    # Handle Ctrl+C gracefully
    def signal_handler(signum, frame):
        print("\nShutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        # Open the URL in the default browser
        logging.info(f"Opening URL: {url}")
        # webbrowser.open(url)
        time.sleep(2)  # Wait for browser to open

        print(f"Keeping tab active. Press Ctrl+C to stop.")
        while True:
            if focus_browser():
                logging.info("Successfully focused browser window")
            else:
                logging.warning("Failed to focus browser window - retrying in {interval} seconds")

            time.sleep(interval)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    keep_tab_active("https://chatgpt.com/", interval=2)


if __name__ == "__main__":
    app.run(port=5000)
