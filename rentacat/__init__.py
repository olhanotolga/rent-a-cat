from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '3fb9e6ad18e3208bd36e1cdd0c3e21f7'

from rentacat import routes
