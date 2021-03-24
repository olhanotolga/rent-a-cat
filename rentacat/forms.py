from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, HiddenField
from wtforms.fields.html5 import TelField, DateField
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
	
	# ADDRESS
	acAddress = StringField('Address/Location', validators=[DataRequired(), Length(min=5, max=200)])
	lat = HiddenField("lat", validators=[DataRequired()])
	lng = HiddenField("lng", validators=[DataRequired()])
	# POINT

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


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(max=100)])
	content = TextAreaField('Description', validators=[DataRequired(), Length(max=1000)])
	picture_1 = FileField('New photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	picture_2 = FileField('New photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	picture_3 = FileField('New photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	start_date = DateField('Start date', format='%Y-%m-%d')
	end_date = DateField('End date', format='%Y-%m-%d')
	cat_sitting_mode = RadioField('You would like the Cat Sitter to be able to', choices=[('Visit', 'visit your cat at home'), ('TakeHome', 'take your cat to their place'), ('VisitAndHome', 'visit your cat OR take it to their place')], default='VisitAndHome')
	submit = SubmitField('Post')

	def validate_end_date(form, field):
		if field.data < form.start_date.data:
			raise ValidationError("End date must not be earlier than start date.")