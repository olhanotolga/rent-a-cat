from flask import Flask

app = Flask(__name__)

from rentacat import routes
