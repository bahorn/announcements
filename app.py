import datetime
import json
import threading
import time

import pusher
from flask import Flask, render_template
from flask_assets import Bundle, Environment
from flask_bootstrap import Bootstrap

from sheet import Sheets
from Announcement import Announcement

sheet: Sheets = Sheets('1wpSA1YsQguMT4tqulLR-1niqKHO8oM5qbGne3SWcOzE', 'A1:F')
sheet.credentials()
sheet.build_service()

posts: [Announcement] = sheet.get_past()

# run code in background
def background():
    global posts
    global sheet

    while True:
        announcements = sheet.get_current_active(datetime.timedelta(minutes=1))
        if len(announcements) > 0:
            announcement = announcements.pop(0)
            text = str(json.dumps(announcement.__dict__, default=str))
            send_announcement(text)
            sheet.set_active(announcement, False)

            posts = sheet.get_past()
        else:
            print("no announcements")
        time.sleep(3)

thread = threading.Thread(target=background)
thread.setDaemon(True)
thread.start()

# create app
app = Flask(__name__)

# setup app bootstrap
Bootstrap(app)
assets = Environment(app)

# setup app assets
assets.url = app.static_url_path
scss = Bundle('scss/main.scss', filters='pyscss', output='build/all.css')
assets.register('scss_all', scss)

@app.route('/')
def index():
    global posts
    return render_template('index.html', posts=posts)

@app.route('/announce')
def announce():
    global sheet

    data = sheet.get_first()
    text = str(json.dumps(data.__dict__, default=str))
    send_announcement(text)
    return text

def send_announcement(message):
    print('Announcing: ' + str(message))
    channels_client = pusher.Pusher(
        app_id='885408',
        key='e26d2d5c77e1ace54c55',
        secret='1e6aa8be2c8dcd2c52c0',
        cluster='eu',
        ssl=True
    )

    channels_client.trigger('announcements', 'new', message)

if __name__ == "__main__":
    app.run(app, host='0.0.0.0', port=5000)
    # setup()
    # announce(str(json.dumps(s.get_all()[10].__dict__, default=str)))
