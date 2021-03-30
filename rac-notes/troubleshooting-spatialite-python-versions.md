# SQLite, Spatialite, Mac OS X, and Python versions

## Resources

[Spatialite Tutorial on Geoalchemy](https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html)

## Problem

[The sqlite3 module is not built with loadable extension support by default, because some platforms (notably Mac OS X) have SQLite libraries which are compiled without this feature. To get loadable extension support, you must pass –enable-loadable-sqlite-extensions to configure.](https://stackoverflow.com/questions/57977481/how-to-use-enable-load-extension-from-sqlite3)

### How to check it

Call sqlite3 in the command line:

`sqlite3`

Once in sqlite, run `.dbconfig`. Here is what it looks like:

```bash
sqlite> .dbconfig
    ...
    load_extension off
   	...
```

The source of all the trouble!

## Fixing

### Steps

1. Reinstall sqlite
2. Install Python with certain configs (should be done with pyenv, a Python version manager)
3. Enable pyenv to manage Python versions
4. Use pyenv inside the project's local folder

### Walkthrough & resources

#### Installations

- [Homebrew: sqlite](https://formulae.brew.sh/formula/sqlite)
- [Homebrew: pyenv](https://formulae.brew.sh/formula/pyenv)

1. `brew reinstall sqlite`
1. `brew install pyenv`
1. `brew install openssl xz gdbm`

#### Python configuration

The following installs Python 3.8.2 with pyenv with the necessary configurations:

`PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions --enable-optimizations --with-openssl=/usr/bin/openssl" LDFLAGS="-L/usr/local/opt/sqlite/lib" CPPFLAGS="-I/usr/local/opt/sqlite/include" pyenv install 3.8.2`

#### Managing Python versions

- [documentation + an interesting read on how pyenv works](https://github.com/pyenv/pyenv)
- [another guide on pyenv](https://realpython.com/intro-to-pyenv/)

Adding pyenv init to your shell to enable shims and autocompletion ([command from the pyenv documentation page](https://github.com/pyenv/pyenv#basic-github-checkout)):

```bash
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
```

(this command from the Homebrew log did **NOT** work (I used the one above!): `if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi`)

#### Managing Python versions in a local virtual environment

Read about using pyenv with virtualenv: [https://github.com/pyenv/pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

Creating a global virtual environment with python 3.8.2:

`pyenv virtualenv 3.8.2 venv-rac`

The following creates a `.python-version` file in the project directory ([pyenv local guide](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-local)):

```bash
pyenv local 3.8.2 # (maybe this is not needed)
pyenv local venv-rac
```

Creating a virtual environment in the project (before this, I saved all the depencencies with `pip freeze > requirements.txt` and simply deleted the old virtual environment folder):

```bash
pip install virtualenv
virtualenv -p python venv
source venv/bin/activate
pip install -r requirements.txt # reinstalls the dependencies
```

## LOG

Refer to [LOG](./log-sqlite-spatialite-pyenv.txt) to see CLI commands & errors (this is after I reinstalled sqlite)

## `__init__.py`

**Note:** I haven't created the blueprints for the project at this stage

```python

# all the imports, also:
from sqlalchemy import event
from sqlalchemy.sql import select
from sqlalchemy.pool import Pool

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SPATIALITE_LIBRARY_PATH'] = '/usr/local/lib/mod_spatialite.dylib'

db = SQLAlchemy(app)

def load_spatialite(dbapi_conn, connection_record):
	dbapi_conn.enable_load_extension(True)
	dbapi_conn.load_extension('/usr/local/lib/mod_spatialite.dylib')
	dbapi_conn.execute('SELECT InitSpatialMetaData()')

event.listen(Pool, "connect", load_spatialite)

```

## Post-fixing ERRORS

1. Launch with `python main.py`: all works, connection established
2. Registration: all good
3. Login: redirects to Dashboard, throws this:
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: profiles.profile_location
(seemed like the Profile model could not be even read because of that column)
```
1. At some point, I had 2 files called `site.db`, one in my project folder, the other one one level higher. I also could see 21 geocolumns added in SQLiteStudio
2. I deleted the `site.db` file (the top one), exited the app and the terminal session
3. I ran the app again. In Python CLI, I imported the db and created all columns... and it worked! The user is being created, sent to Dashboard and then to `create_profile` --> Profile successfully created and location column showing in SQLiteStudio
