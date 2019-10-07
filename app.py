import argparse
import json
import threading

from flask import Flask, render_template
from flask_assets import Bundle, Environment
from flask_socketio import SocketIO

from sheet import Sheets


def background():
    s = Sheets('1KfJJVpKwtQ4SMnCmvFRnWNZ4uIchqjknptZ4orqSlLs', 'A1:C')
    s.credentials()
    s.build_service()
    announcement = s.get_first()
    announce(json.dumps(announcement.__dict__, default=str))
    announce([str(announcement.time), str(announcement.title), str(announcement.body)])


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