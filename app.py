import argparse
from flask import Flask, render_template, redirect
from flask_socketio import SocketIO
from flask_assets import Environment, Bundle

import threading
from sheet import Sheets

def background():
    s = Sheets('13_6S-dBLfNY0eKRULjIliKjr-sLfuv4iS5mX-0e78pA','A1:C')
    s.credentials()
    s.build_service()
    announce(s.get_first()[1])
    

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
    return redirect('/')

def announce(message):
    socketio.emit('announcement', message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='run the flask server in debug mode')
    args = parser.parse_args()

    socketio.run(app, host='0.0.0.0', port=8000, debug=args.debug)