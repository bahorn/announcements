import argparse
import datetime
import json
import threading

from flask import Flask, render_template
from flask_assets import Bundle, Environment
from flask_socketio import SocketIO

from sheet import Sheets


def background():
    s = Sheets('1wpSA1YsQguMT4tqulLR-1niqKHO8oM5qbGne3SWcOzE', 'A1:F')
    s.credentials()
    s.build_service()
    announcements = s.get_current_active(datetime.timedelta(days=1))
    if len(announcements) > 0:
        announcement = announcements.pop(0)
        announce(json.dumps(announcement.__dict__, default=str))
        s.set_active(announcement, False)
    else:
        print("no announcements")


app = Flask(__name__)
socketio = SocketIO(app)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/main.scss', filters='pyscss', output='build/all.css')
assets.register('scss_all', scss)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/announce')
def hello():
    announce('hello there!')
    return 'done'


@app.route('/sheet')
def sheet():
    b = threading.Thread(name='background', target=background)
    b.start()
    return 'done'


def announce(message):
    print('Announcing: ' + str(message))
    socketio.emit('announcement', message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='run the flask server in debug mode')
    args = parser.parse_args()

    socketio.run(app, host='0.0.0.0', port=8000, debug=args.debug)
