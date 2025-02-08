import webbrowser
from AppKit import NSDate, NSTimer, NSRunLoop, NSDefaultRunLoopMode
from Foundation import NSCalendar, NSCalendarUnitHour, NSCalendarUnitMinute, NSCalendarUnitSecond
from flask import Flask, request, jsonify
from threading import Thread



app = Flask(__name__)

class MultiScheduler:
    def __init__(self):
        self.schedules = []
        self.timer = None

    def add_schedule(self, hour, minute, second, callback_function, *args, **kwargs):
        self.schedules.append({
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
            NSCalendarUnitHour | NSCalendarUnitMinute | NSCalendarUnitSecond,
            now
        )
        return components.hour(), components.minute(), components.second()

    def check_schedules_(self, timer):
        current_hour, current_minute, current_second = self.get_current_time()
        
        for schedule in self.schedules:
            if (current_hour == schedule['hour'] and 
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
            print(f"- {schedule['hour']:02d}:{schedule['minute']:02d}:{schedule['second']:02d}")

# Example usage:
def function1(message):
    print(f"Function 1: {message}")

def function2(count):
    print(f"Function 2 executed {count} times")
    times = {}
    urls = {1: "https://www.boredbutton.com", 2: "https://docs.google.com/document/d/11IFMyuTilvXgB97vi6-c4OsUZJ674OsfPjzN1fRT4Xg/edit?tab=t.0"}
    url = urls[2]
    open_url(url)
    
def open_url(url): #uses the default browser set by user
    webbrowser.open_new(url)


def run_scheduler(sched):
    sched.start()


## flask

@app.route('/add_schedule', methods=['POST'])
def add_schedule():
    data = request.json
    hour = data['hour']
    minute = data['minute']
    second = data['second']
    message = data['message']
    
    def callback(message):
        print(f"Function triggered: {message}")
    
    scheduler.add_schedule(hour, minute, second, callback, message)
    return jsonify({"message": "Schedule added successfully"}), 200

@app.route('/start', methods=['POST'])
def start_scheduler():
    def run_scheduler():
        scheduler.start()
    
    # Run scheduler in a separate thread to avoid blocking the Flask server
    Thread(target=run_scheduler).start()
    return jsonify({"message": "Scheduler started"}), 200

@app.route('/stop', methods=['POST'])
def stop_scheduler():
    scheduler.stop()
    return jsonify({"message": "Scheduler stopped"}), 200

@app.route('/get_schedules', methods=['GET'])
def get_schedules():
    schedules = []
    for schedule in scheduler.schedules:
        schedules.append({
            "hour": schedule["hour"],
            "minute": schedule["minute"],
            "second": schedule["second"],
            "message": schedule["args"][0]
        })
    return jsonify(schedules), 200
##

scheduler = MultiScheduler()

if __name__ == '__main__':

    app.run(debug=True)
    
    # scheduler = MultiScheduler()
    
    # # Add multiple schedules
    # scheduler.add_schedule(14, 0, 0, function1, "It's 2 PM!")
    # scheduler.add_schedule(14, 23, 0, function2, 3)
    
    # run_schedule(scheduler)
    
    # # Keep the application running
    # from AppKit import NSApplication
    # NSApplication.sharedApplication().run()