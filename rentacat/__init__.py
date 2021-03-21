import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.sql import select
from sqlalchemy.pool import Pool

app = Flask(__name__)

app.config['SECRET_KEY'] = '3fb9e6ad18e3208bd36e1cdd0c3e21f7'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SPATIALITE_LIBRARY_PATH'] = '/usr/local/lib/mod_spatialite.dylib'

app.config['GOOGLE_MAPS_API_KEY'] = os.environ.get('API_KEY')


db = SQLAlchemy(app)

# @event.listens_for(db.engine, "connect")
def load_spatialite(dbapi_conn, connection_record):
	# From https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html
	print('AAAAAAA')
	dbapi_conn.enable_load_extension(True)
	dbapi_conn.load_extension('/usr/local/lib/mod_spatialite.dylib')
	dbapi_conn.execute('SELECT InitSpatialMetaData()')

# engine = create_engine('sqlite:///site.db', echo=True)
# event.listen(engine, 'connect', load_spatialite)
event.listen(Pool, "connect", load_spatialite)

# conn = engine.connect()

# conn.connection.enable_load_extension(True)
# conn.connection.load_extension('/usr/local/lib/mod_spatialite.dylib')
# print('CONNECTED?!')
# load_spatialite()


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'




from rentacat import routes
