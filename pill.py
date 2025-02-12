from flask import Flask, jsonify, request
import threading
import time
from datetime import datetime

app = Flask(__name__)

alarms = []  # Store alarm details

# Endpoint to set an alarm
@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    data = request.json
    time_str = data.get('time')  # Alarm time in "HH:MM" format
    date_str = data.get('date')  # Alarm date in "YYYY-MM-DD" format
    message = data.get('message', "Alarm!")

    if not time_str or not date_str:
        return jsonify({"status": "error", "message": "Invalid time or date!"}), 400

    alarm_time = f"{date_str} {time_str}"  # Combine date and time
    alarms.append({"time": alarm_time, "message": message})
    threading.Thread(target=trigger_alarm, args=(alarm_time, message)).start()

    return jsonify({"status": "success", "message": f"Alarm set for {alarm_time}"})


# Background task to trigger the alarm
def trigger_alarm(alarm_time, message):
    alarm_datetime = datetime.strptime(alarm_time, "%Y-%m-%d %H:%M")
    while True:
        if datetime.now() >= alarm_datetime:
            print(f"Alarm triggered: {message}")
            break
        time.sleep(1)  # Check every second


if __name__ == '__main__':
    app.run(debug=False)
