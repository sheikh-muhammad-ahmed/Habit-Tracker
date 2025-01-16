from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

habits = []

def get_time_left(habit_time):
    now = datetime.now()
    habit_time = datetime.strptime(habit_time, "%H:%M")
    habit_time = habit_time.replace(year=now.year, month=now.month, day=now.day)
    
    if habit_time < now:
        habit_time += timedelta(days=1)  # if the time is in the past, set it for the next day
    
    time_left = habit_time - now
    return str(time_left).split(".")[0]  

@app.route('/')
def main_page():
    for habit in habits:
        habit['time_left'] = get_time_left(habit['time'])
    
    return render_template('mainPage.html', habits=habits)

@app.route('/add_habit', methods=['POST'])
def add_habit():
    habit_name = request.form['habit_name']
    habit_time = request.form['habit_time']
    
    if len(habits) < 4:
        habit_card = {'name': habit_name, 'time': habit_time}
        habits.append(habit_card)
    else:
        print("You cannot add more than 4 habits.")
    
    return redirect(url_for('main_page'))

@app.route('/delete_habit', methods=['POST'])
def delete_habit():
    habit_id = request.form['habit_id']
    global habits
    habits = [habit for habit in habits if habit['name'] != habit_id]  
    return redirect(url_for('main_page'))

@app.route('/get_dynamic_time', methods=['GET'])
def get_dynamic_time():
    # Send current time in the server's timezone
    now = datetime.now().strftime("%I:%M:%S %p")
    return {'current_time': now}

if __name__ == '__main__':
    app.run(debug=True, port=8000)
