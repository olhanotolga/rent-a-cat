import os
import secrets
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user, login_user, logout_user
from PIL import Image
from rentacat import app, db, bcrypt
from rentacat.forms import RegistrationForm, LoginForm, UpdateProfileForm
from rentacat.models import User, Profile


def save_image(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

	output_size = (256, 256)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	
	return picture_fn


@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
	return render_template("index.html", title="Home", h1="Rent a Cat", h2="Join the community", header_h2_only=True)


@app.route("/about")
def about():
	return render_template("about.html", h2="About Rent a Cat", title="About")


@app.route("/signup", methods=["GET", "POST"])
def registration():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard'))
	
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		flash(f'Welcome aboard, {form.username.data}! You can now log in!', 'success')
		
		return redirect(url_for('dashboard'))
	return render_template("registration.html", title="Sign up", form=form, h2="Create an account")


@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
		# 'admin@rac.com' and 'qwerty':
		# 'third.user@email.com' and 'thirduser'
			login_user(user, remember=form.remember.data)
			# update last login field
			user.last_login = datetime.utcnow
			# redirect to the page user was initially interested in (if any)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('dashboard'))
		else:
			flash('Nope. Please check if your email and/or password are correct.', 'error')
	return render_template("login.html", title="Log in", form=form, h2="Log in")


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route("/dashboard")
@login_required
def dashboard():
	username = current_user.username
	return render_template("dashboard.html", title="Dashboard", h2=f"{username}'s Dashboard")


@app.route("/profile")
@login_required
def own_profile():
	# first name + last name
	# username
	username = current_user.username
	# email
	# address
	# phone number
	# facebook username
	# telegram username
	# about

	return render_template("profile.html", title="Your profile", h2=f"{username}'s Profile")


@app.route("/profile/update", methods=['GET', 'POST'])
@login_required
def update_profile():
	form = UpdateProfileForm()
	if form.validate_on_submit():
		
		profile = Profile(name=form.name.data, about=form.about.data, address=form.address.data, phone_number=form.phone.data, facebook_username=form.facebook.data, telegram_username=form.telegram.data, user_id=current_user.id)
		db.session.add(profile)
		db.session.commit()

		if form.picture.data:
			picture_file = save_image(form.picture.data)
			current_user.user_profile.profile_image = picture_file
		
		current_user.username = form.username.data
		current_user.email = form.email.data
		
		# ! location / Geometry
		# location = db.Column(Geometry("POINT", srid=SpatialConstants.SRID, dimension=2, management=True))
		
		flash('Your profile info has been updated', 'success')
		return redirect(url_for('own_profile'))

	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		
		profile = Profile.query.filter_by(user_id=current_user.id).first()
		
		if profile:
			if profile.name:
				form.name.data = profile.name
			if profile.about:
				form.about.data = profile.about
			if profile.address:
				form.address.data = profile.address
			if profile.phone_number:
				form.phone.data = profile.phone_number
			if profile.facebook_username:
				form.facebook.data = profile.facebook_username
			if profile.telegram_username:
				form.telegram.data = profile.telegram_username
			
		else:
			form.name.data = current_user.username
			form.address.data = "Berlin, Germany"
			
			current_user.user_profile.name = current_user.username
			current_user.user_profile.address = "Berlin, Germany"

	profile = Profile.query.filter_by(user_id=current_user.id).first()	
	if profile:
		profile_image = url_for('static', filename='profile_pics/' + profile.profile_image)
	else:
		profile_image = url_for('static', filename='profile_pics/' + 'default.jpg')

	db.session.commit()
	
	return render_template("update_profile.html", title="Update profile", h2="Update profile", username=current_user.username, email=current_user.email, profile_image=profile_image, form=form)


@app.route("/user/<string:username>")
def user_profile(username):
	if current_user.username == username:
		return redirect(url_for('own_profile'))
	return render_template("profile.html", title=f"{username}'s profile", h2=f"{username}'s profile")


# potentially: all updates as a list and map
@app.route("/view")
def view():
	return render_template("view.html", title="View", h2="View updates nearby")


@app.errorhandler(404)
def page_not_found(error):
	return render_template("notfound.html", title="Not found", h2="No such page"), 404
