from flask import Flask, render_template, request, redirect, url_for
import requests
from urllib.parse import quote

app = Flask(__name__)

# Directly set bot token and chat ID
telegram_bot_token = '7486018078:AAFqcuZ6J84YDmH1p3jWCMt0LugraQsNWBk'
telegram_chat_id = '5195784360'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    if request.method == 'POST':
        reservation_for = request.form['reservation_for']
        users = request.form ['users']
        purpose = request.form['purpose']
        user_name = request.form['fullname']
        user_index = request.form['user_index']
        user_phone = request.form['user_phone']
        user_email = request.form['user_email']
        unique_code = request.form['unique_code']

        message = (f"New reservation request:\n"
                   f"user : {users}\n"
                   f"Name: {user_name}\n"
                   f"Index Number: {user_index}\n"
                   f"Phone Number: {user_phone}\n"
                   f"Email: {user_email}\n"
                   f"Purpose: {purpose}\n"
                   f"unique_code: {unique_code}\n")
        

        if reservation_for == 'device' or reservation_for == 'both':
            device_types = request.form.getlist('device_type[]')
            booking_dates = request.form.getlist('booking_date[]')
            booking_times = request.form.getlist('booking_time[]')
            durations = request.form.getlist('duration[]')
            unique_code = request.form.getlist('unique_code')

            for device_type, booking_date, booking_time, duration,unique_code in zip(device_types, booking_dates, booking_times, durations, unique_code):
                message += (f"\nDevice Booking Details:\n"
                            f"Device Type: {device_type}\n"
                            f"Date: {booking_date}\n"
                            f"Time: {booking_time}\n"
                            f"Duration: {duration} hours\n"
                            f"unique_code: {unique_code}")

        if reservation_for == 'classroom' or reservation_for == 'both':
            classroom = request.form['classroom']
            unique_code = request.form['unique_code']

            message += (f"\nClassroom Booking Details:\n"
                        f"Classroom: {classroom}\n"
                        f"unique_code: {unique_code}\n")
            

        if send_telegram_message(message):
            return redirect(url_for('success'))
        else:
            return 'Failed to send message', 500

    return 'Method not allowed', 405

def send_telegram_message(message):
    try:
        encoded_message = quote(message)
        url = (f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
               f"?chat_id={telegram_chat_id}&text={encoded_message}")
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to send Telegram message: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Exception sending Telegram message: {e}")
        return False

@app.route('/success')
def success():
    return "Your booking has been submitted successfully! You will receive an Email message for approval. Come with your student ID and unique code."

if __name__ == '__main__':
    app.run(debug=True)
