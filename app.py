import argparse
import datetime
import json
import logging
import threading
import time

from flask import Flask, render_template
from flask_assets import Bundle, Environment
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask_cors import CORS
from sheet import Sheets

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
socketio = SocketIO(app)
Bootstrap(app)
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/main.scss', filters='pyscss', output='build/all.css')
assets.register('scss_all', scss)
cors = CORS(app, resources={r"/*": {"origins": "live.hackthemidlands.com"}})

# suppress http requests in output

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

@app.route('/')
def index():
    global s
    setup()

    posts = s.get_past()
    return render_template('index.html', posts=posts)

@app.route('/setup')
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
@socketio.on('reconnect',namespace='/test')
def test_reconnect():
    print('Client reconnected')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global is_setup
    print('Client connected')

    # Start the random number generator thread only if the thread has not been started before.
    if not is_setup:
        print("Starting backend")
        setup()
        start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

def announce(message):
    print('Announcing: ' + str(message))
    socketio.emit('announcement', str(message), namespace='/test')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='run the flask server in debug mode')
    args = parser.parse_args()

    socketio.run(app, host='0.0.0.0', port=5000, debug=args.debug)
