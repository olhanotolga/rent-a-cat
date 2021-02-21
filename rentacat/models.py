import enum
from datetime import datetime
from rentacat import db



class UserTypes(enum.Enum):
	Admin = 1
	Regular = 2

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(65), unique=True, nullable=False)
	password = db.Column(db.String(30), nullable=False)
	user_type = db.Column(db.Enum(UserTypes), nullable=False, default=UserTypes.Regular)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	#! last login ???
	last_login = db.Column(db.DateTime)

	user_profile = db.relationship('Profile', back_populates='user', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', type:{self.user_type})"


class Profile(db.Model):
	__tablename__ = 'profiles'

	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(25), nullable=False)
	last_name = db.Column(db.String(25), nullable=False)
	about = db.Column(db.Text)
	address = db.Column(db.String(200), nullable=False)
	phone_number = db.Column(db.Integer, nullable=False)
	facebook_username = db.Column(db.String(50))
	telegram_username = db.Column(db.String(32))
	profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	updates = db.relationship('Update', backref='author', lazy=True)

	def __repr__(self):
		return f"Profile('{self.first_name}', '{self.last_name}', '{self.profile_image}')"


class Update(db.Model):
	__tablename__ = 'updates'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(65))
	description = db.Column(db.Text, nullable=False)
	photo_1 = db.Column(db.String(30))
	photo_2 = db.Column(db.String(30))
	photo_3 = db.Column(db.String(30))
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	published_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	closed_on = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Update('{self.title}', '{self.published_on}')"
	

# association table (for exchanges made between users):
exchanges_table = db.Table('catsitting_exchanges', db.Model.metadata, db.Column('left_id', db.Integer, db.ForeignKey('profiles.id')), db.Column('right_id', db.Integer, db.ForeignKey('profiles.id')))