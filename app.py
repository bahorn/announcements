import argparse
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/announce')
def hello():
    announce('hello there!')
    return 'done'

def announce(message):
    socketio.emit('announcement', message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='run the flask server in debug mode')
    args = parser.parse_args()

    socketio.run(app, host='0.0.0.0', port=8000, debug=args.debug)