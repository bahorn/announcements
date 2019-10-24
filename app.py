import datetime
import json
import threading
import time

import pusher
from flask import Flask, render_template
from flask_assets import Bundle, Environment
from flask_bootstrap import Bootstrap

from sheet import Sheets

# from flask_socketio import SocketIO

s: Sheets
is_setup: bool = False

def background():
    global is_setup
    while True:
        if is_setup:
            announcements = s.get_current_active(datetime.timedelta(minutes=1))
            if len(announcements) > 0:
                announcement = announcements.pop(0)
                text = str(json.dumps(announcement.__dict__, default=str))
                announce(text)
                s.set_active(announcement, False)
            else:
                print("no announcements")
        time.sleep(3)

t = threading.Thread(target=background)
t.setDaemon(True)

app = Flask(__name__)
# # socketio = SocketIO(app)
Bootstrap(app)
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/main.scss', filters='pyscss', output='build/all.css')
assets.register('scss_all', scss)

# cors = CORS(app, resources={r"/**/*": {"origins": "*", "send_wildcard": "true"}})

# suppress http requests in output

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

@app.route('/')
def index():
    global s
    setup()

    posts = s.get_past()
    return render_template('index.html', posts=posts)

# @app.route('/setup')
def setup():
    global s
    global is_setup
    if not is_setup:
        s = Sheets('1wpSA1YsQguMT4tqulLR-1niqKHO8oM5qbGne3SWcOzE', 'A1:F')
        s.credentials()
        s.build_service()
        is_setup = True
        print("setup done!")
    return 'done'

@app.route('/announce')
def hello():
    global s
    setup()
    data = s.get_first()
    text = str(json.dumps(data.__dict__, default=str))
    announce(text)
    return text

# @app.route('/start')
def start():
    global t
    t.start()
    return 'done'

# @app.route('/stop')
def stop():
    global t
    t.join()
    return 'done'

# @app.route('/reset')
def reset():
    s.reset_all()
    return 'done'

def announce(message):
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
