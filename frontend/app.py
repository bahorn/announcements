from flask import Flask, render_template
from flask_assets import Bundle, Environment
from flask_bootstrap import Bootstrap

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
    return render_template('index.html', posts=[])


app.run(host='0.0.0.0', port=5000)
