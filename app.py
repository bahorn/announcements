import datetime
import json
import sys
import threading
import time
import traceback

import pusher
from flask import Flask, render_template
from flask_assets import Bundle, Environment
from flask_bootstrap import Bootstrap

from Config import Settings

print(Settings)

from sheet import Sheets
from Announcement import Announcement

sheet: Sheets = Sheets(Settings.SHEET, Settings.SHEET_RANGE)
sheet.credentials()
sheet.build_service()

print(sheet)

posts: [Announcement] = sheet.get_past()
print('Preloaded posts:', posts, file=sys.stderr)

# run code in background
def background():
    global posts
    global sheet
    while True:
        print('loading announcements... ', end='')
        try:
            print(sheet.values())
            announcements = sheet.get_current_active(datetime.timedelta(minutes=1))
            if len(announcements) > 0:
                announcement = announcements.pop(0)
                text = str(json.dumps(announcement.__dict__, default=str))
                send_announcement(text)
                sheet.set_active(announcement, False)

                posts = sheet.get_past()
                print()
                print('Updated posts:', posts, file=sys.stderr)
            else:
                print("no announcements")

            time.sleep(3)
        except:
            traceback.print_last(file=sys.stderr)
            time.sleep(5)

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

# @app.route('/announce')
def announce():
    global sheet

    data = sheet.get_first()
    text = str(json.dumps(data.__dict__, default=str))
    send_announcement(text)
    return text

def send_announcement(message):
    print('Announcing: ' + str(message))
    channels_client = pusher.Pusher(
        app_id=Settings.PUSHER_APP_ID,
        key=Settings.PUSHER_KEY,
        secret=Settings.PUSHER_SECRET,
        cluster=Settings.PUSHER_CLUSTER,
        ssl=True
    )

    channels_client.trigger(Settings.PUSHER_CHANNEL, 'new', message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
