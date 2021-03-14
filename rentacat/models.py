import enum
from datetime import datetime
from rentacat import db, login_manager, app
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class UserTypes(enum.Enum):
	Admin = 1
	Regular = 2


class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(65), unique=True, nullable=False)
	password = db.Column(db.String(50), nullable=False)
	user_type = db.Column(db.Enum(UserTypes), nullable=False, default=UserTypes.Regular)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	#? last login — update every time user logs in
	last_login = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	
	# profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
	profile = db.relationship('Profile', back_populates='user', uselist=False, lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', type:{self.user_type})"

#######################
class SpatialConstants:
	# SRID
	SRID = 4326
#######################

class ProfileTypes(enum.Enum):
	CatKeeper = 1
	CatSitter = 2

class Profile(db.Model):
	__tablename__ = 'profiles'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	about = db.Column(db.Text)
	address = db.Column(db.String(200), nullable=False)
	# ! location / Geometry
	# location = db.Column(Geometry("POINT", srid=SpatialConstants.SRID, dimension=2, management=True))
	phone_number = db.Column(db.Integer)
	facebook_username = db.Column(db.String(50))
	telegram_username = db.Column(db.String(32))
	profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
	profile_type = db.Column(db.Enum(ProfileTypes), nullable=False, default=ProfileTypes.CatKeeper)
	
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	user = db.relationship('User', back_populates='profile', lazy=True)
	
	cat_keeper = db.relationship('CatKeeper', back_populates='profile', uselist=False, lazy=True)
	cat_sitter = db.relationship('CatSitter', back_populates='profile', uselist=False, lazy=True)

	def __repr__(self):
		return f"Profile('{self.name}', '{self.profile_image}')"


class CatKeeper(db.Model):
	__tablename__ = 'cat_keepers'

	id = db.Column(db.Integer, primary_key=True)
	
	profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
	profile = db.relationship('Profile', back_populates='cat_keeper', uselist=False, lazy=True)
	
	# backref — in parent object only
	# back_populates — in both child and parent
	requests = db.relationship('Request', back_populates='cat_keeper', lazy=True)


class CatSitter(db.Model):
	__tablename__ = 'cat_sitters'

	id = db.Column(db.Integer, primary_key=True)
	
	profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
	profile = db.relationship('Profile', back_populates='cat_sitter', uselist=False, lazy=True)

	offers = db.relationship('Offer', back_populates='cat_sitter', lazy=True)


class Request(db.Model):
	__tablename__ = 'requests'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(65))
	description = db.Column(db.Text, nullable=False)
	photo_1 = db.Column(db.String(30))
	photo_2 = db.Column(db.String(30))
	photo_3 = db.Column(db.String(30))
	start_date = db.Column(db.DateTime, nullable=False)
	end_date = db.Column(db.DateTime, nullable=False)
	published_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	
	cat_keeper_id = db.Column(db.Integer, db.ForeignKey('cat_keepers.id'), nullable=False)
	cat_keeper = db.relationship('CatKeeper', back_populates='requests', lazy=True)

	def __repr__(self):
		return f"Request('{self.title}', '{self.published_on}')"

class Offer(db.Model):
	__tablename__ = 'offers'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(65))
	description = db.Column(db.Text, nullable=False)
	start_date = db.Column(db.DateTime, nullable=False)
	end_date = db.Column(db.DateTime, nullable=False)
	published_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	cat_sitter_id = db.Column(db.Integer, db.ForeignKey('cat_sitters.id'), nullable=False)
	cat_sitter = db.relationship('CatSitter', back_populates='offers', lazy=True)

	def __repr__(self):
		return f"Offer('{self.title}', '{self.published_on}')"
	
