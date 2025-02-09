import webbrowser
from AppKit import NSDate, NSTimer, NSRunLoop, NSDefaultRunLoopMode
from Foundation import NSCalendar, NSCalendarUnitMonth, NSCalendarUnitDay, NSCalendarUnitHour, NSCalendarUnitMinute, NSCalendarUnitSecond

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

class MultiScheduler:
    def __init__(self):
        self.schedules = []
        self.timer = None

    def add_schedule(self, month, day, hour, minute, second, callback_function, *args, **kwargs):
        self.schedules.append({
            'month': month,
            'day': day,
            'hour': hour,
            'minute': minute,
            'second': second,
            'callback': callback_function,
            'args': args,
            'kwargs': kwargs,
            'has_executed': False
        })

    def get_current_time(self):
        now = NSDate.date()
        calendar = NSCalendar.currentCalendar()
        components = calendar.components_fromDate_(
            NSCalendarUnitMonth | NSCalendarUnitDay | NSCalendarUnitHour | NSCalendarUnitMinute | NSCalendarUnitSecond,
            now
        )
        return components.month(), components.day(), components.hour(), components.minute(), components.second()

    def check_schedules_(self, timer):
        current_month, current_day, current_hour, current_minute, current_second = self.get_current_time()
        
        for schedule in self.schedules:
            if (current_month == schedule['month'] and
                current_day == schedule['day'] and
                current_hour == schedule['hour'] and 
                current_minute == schedule['minute'] and 
                current_second == schedule['second'] and 
                not schedule['has_executed']):
                schedule['callback'](*schedule['args'], **schedule['kwargs'])
                schedule['has_executed'] = True
                NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                    2.0,
                    self,
                    'reset_flag:',
                    schedule,
                    False
                )

    def reset_flag_(self, timer):
        schedule = timer.userInfo()
        schedule['has_executed'] = False

    def start(self):
        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0,
            self,
            'check_schedules:',
            None,
            True
        )
        
        NSRunLoop.currentRunLoop().addTimer_forMode_(
            self.timer,
            NSDefaultRunLoopMode
        )
        
        # Print all scheduled times
        self.print_schedules()

    def stop(self):
        if self.timer:
            self.timer.invalidate()
            self.timer = None

    def print_schedules(self):
        print("Scheduled functions:")
        for schedule in self.schedules:
            print(f"- {schedule['month']:02d}:{schedule['day']:02d}:{schedule['hour']:02d}:{schedule['minute']:02d}:{schedule['second']:02d}")

# Example usage:

def function2(url):
    print(f"function2 executed")
    open_url(url)
    
def open_url(url): #uses the default browser set by user
    webbrowser.open_new(url)

scheduler = MultiScheduler()

# Add multiple schedules, format: MDHMS
# FOR ZOE
for task in tasks:
    scheduler.add_schedule(unpack(task[time]), function2, task[url])

scheduler.start()

# Keep the application running
from AppKit import NSApplication
NSApplication.sharedApplication().run()



