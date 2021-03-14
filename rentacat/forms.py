from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_login import current_user
from rentacat.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
	agree = BooleanField("I agree to Terms*")
	submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Log in')


class UpdateProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	about = TextAreaField('About', validators=[Length(max=1000)])
	address = StringField('Address (street/PLZ)', validators=[DataRequired(), Length(min=5, max=200)])
	phone = TelField('Phone')
	facebook = StringField('Facebook username', validators=[Length(max=50)])
	telegram = StringField('Telegram username', validators=[Length(max=32)])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	preferred_profile_type = RadioField('First of all, you are a', choices=[('CatKeeper', 'Cat Keeper'), ('CatSitter', 'Cat Sitter')], default='CatKeeper')
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username is taken. Please choose a different one.')
	
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('A user with this email already exists. Did you want to log in?')
