import os
import secrets
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user, login_user, logout_user
from PIL import Image
from rentacat import app, db, bcrypt
from rentacat.forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm
from rentacat.models import User, Profile, Request, Offer


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

		return redirect(url_for('login'))

	return render_template("registration.html", title="Sign up", form=form, h2="Create an account")


@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			# update last login
			user.last_login = datetime.utcnow
			# redirect to the page user was initially interested in (if any)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('dashboard'))
		else:
			flash('Nope. Please check if your email and/or password are correct.', 'error')
	return render_template("login.html", title="Log in", form=form, h2="Log in")


@app.route("/dashboard")
@login_required
def dashboard():
	profile_types = {
		'CatKeeper': 'Cat Keeper',
		'CatSitter': 'Cat Sitter'
	}

	current_profile = current_user.profile
	# show if profile has been created,
	# otherwise send to create_profile
	if not current_profile:
			return redirect(url_for('create_profile'))
	
	profile_image=current_profile.profile_image
	username = current_user.username
	profile_type = current_profile.profile_type.name

	current_type = None
	other_type = None
	for p in profile_types:
		if p == profile_type:
			current_type = profile_types[p]
		else:
			other_type = profile_types[p]
	
	requests = current_profile.requests
	offers = current_profile.offers

	return render_template("dashboard.html", title="Dashboard", h2=f"{username}'s Dashboard", profile=current_type, other_profile=other_type, username=username, profile_image=profile_image, requests=requests, offers=offers)


@app.route("/profile/create", methods=['GET', 'POST'])
@login_required
def create_profile():
	# ! show only if there is no profile!
	# ! otherwise: show create profile page (new route/same template with conditional rendering)
	picture_file = url_for('static', filename='profile_pics/default.jpg')
	form = UpdateProfileForm()
	if form.validate_on_submit():
		lat = form.lat.data
		lng = form.lng.data
		location = Profile.point_rep(lng, lat)
		#? transform the lat and lng into a point (DO I NEED IT?)
		profile = Profile(name=form.name.data, about=form.about.data, address=form.acAddress.data, profile_location=location, phone_number=form.phone.data, facebook_username=form.facebook.data, telegram_username=form.telegram.data, user_id=current_user.id, profile_type=form.preferred_profile_type.data)
		db.session.add(profile)
		db.session.commit()

		if form.picture.data:
			picture_file = save_image(form.picture.data)
			current_user.profile.profile_image = picture_file
			db.session.commit()
		
		flash('Your profile has been created', 'success')
		return redirect(url_for('dashboard'))

	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		
		if current_user.profile:
			picture_file = url_for('static', filename='profile_pics/' + current_user.profile.profile_image)
		else:
			picture_file = url_for('static', filename='profile_pics/default.jpg')
	
	script = 'mapsInput.js'

	map_key = app.config['GOOGLE_MAPS_API_KEY']
	map_string = "https://maps.googleapis.com/maps/api/js?key=" + map_key + "&callback=initAutocomplete&libraries=places&v=weekly"

	return render_template("update_profile.html", title="Create profile", h2="Create profile", username=current_user.username, email=current_user.email, profile_image=picture_file, form=form, map_string=map_string, script=script)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))



# *** LEAVE FOR NOW!!! *** ↓↓↓
# !!! LEAVE FOR NOW!!! *** ↓↓↓
# *** LEAVE FOR NOW!!! *** ↓↓↓
# !!! LEAVE FOR NOW!!! *** ↓↓↓
# *** LEAVE FOR NOW!!! *** ↓↓↓

# @app.route("/profile")
# @login_required
# def own_profile():
# 	# ! show if there is profile,
# 	# ! otherwise: render create_profile page
# 	# first name + last name
# 	# username
# 	username = current_user.username
# 	# email
# 	# address
# 	# phone number
# 	# facebook username
# 	# telegram username
# 	# about

# 	return render_template("profile.html", title="Your profile", h2=f"{username}'s Profile")


# *** LEAVE FOR NOW!!! *** ↓↓↓
# !!! LEAVE FOR NOW!!! *** ↓↓↓
# *** LEAVE FOR NOW!!! *** ↓↓↓
# !!! LEAVE FOR NOW!!! *** ↓↓↓
# *** LEAVE FOR NOW!!! *** ↓↓↓

# @app.route("/profile/update", methods=['GET', 'POST'])
# @login_required
# def update_profile():
# 	# ! show only if there is a profile to update!
# 	# ! otherwise: show create profile page (new route/same template with conditional rendering)
# 	form = UpdateProfileForm()
# 	if form.validate_on_submit():
		
# 		profile = Profile(name=form.name.data, about=form.about.data, address=form.addresscA.data, phone_number=form.phone.data, facebook_username=form.facebook.data, telegram_username=form.telegram.data, user_id=current_user.id)
# 		db.session.add(profile)
# 		db.session.commit()

# 		if form.picture.data:
# 			picture_file = save_image(form.picture.data)
# 			current_user.user_profile.profile_image = picture_file
		
# 		current_user.username = form.username.data
# 		current_user.email = form.email.data
		
# 		# ! location / Geometry
# 		# location = db.Column(Geometry("POINT", srid=SpatialConstants.SRID, dimension=2, management=True))
		
# 		flash('Your profile info has been updated', 'success')
# 		return redirect(url_for('own_profile'))

# 	elif request.method == 'GET':
# 		form.username.data = current_user.username
# 		form.email.data = current_user.email
		
# 		profile = Profile.query.filter_by(user_id=current_user.id).first()
		
# 		if profile:
# 			if profile.name:
# 				form.name.data = profile.name
# 			if profile.about:
# 				form.about.data = profile.about
# 			if profile.address:
# 				form.addresscA.data = profile.address
# 			if profile.phone_number:
# 				form.phone.data = profile.phone_number
# 			if profile.facebook_username:
# 				form.facebook.data = profile.facebook_username
# 			if profile.telegram_username:
# 				form.telegram.data = profile.telegram_username
			
# 		else:
# 			form.name.data = current_user.username
# 			form.addresscA.data = "Berlin, Germany"
			
# 			current_user.profile.name = current_user.username
# 			current_user.profile.address = "Berlin, Germany"

# 	profile = Profile.query.filter_by(user_id=current_user.id).first()	
# 	if profile:
# 		profile_image = url_for('static', filename='profile_pics/' + profile.profile_image)
# 	else:
# 		profile_image = url_for('static', filename='profile_pics/' + 'default.jpg')

# 	db.session.commit()
	
# 	return render_template("update_profile.html", title="Update profile", h2="Update profile", username=current_user.username, email=current_user.email, profile_image=profile_image, form=form)


@app.route("/user/<string:username>")
def user_profile(username):
	# if current_user.username == username:
	# 	return redirect(url_for('own_profile'))
	return render_template("profile.html", title=f"{username}'s profile", h2=f"{username}'s profile")



# * ADD UPDATES (REQUESTS OR OFFERS)
@app.route('/request/new', methods=['GET', 'POST'])
@login_required
def new_request():
	form = PostForm()
	if form.validate_on_submit():
		# ? take the cat home or visit only?
		request = Request(title=form.title.data, description=form.content.data, cat_keeper_id=current_user.profile.id, start_date=form.start_date.data, end_date=form.end_date.data, cat_sitting_mode=form.cat_sitting_mode.data)
		db.session.add(request)
		db.session.commit()

		if form.picture_1.data:
			picture_file = save_image(form.picture_1.data)
			request.photo_1 = picture_file
			db.session.commit()
		if form.picture_2.data:
			picture_file = save_image(form.picture_2.data)
			request.photo_2 = picture_file
			db.session.commit()
		if form.picture_3.data:
			picture_file = save_image(form.picture_3.data)
			request.photo_3 = picture_file
			db.session.commit()

		flash('Your request has been created!', 'success')
		return redirect(url_for('dashboard'))
	return render_template('new_update.html', title='New Request', form=form, legend='New request')


# @app.route("/get_updates")
# def get_updates():



# potentially: all updates as a list and map
@app.route("/view")
@login_required
def view():
	profile_types = {
		'CatKeeper': 'Cat Keeper',
		'CatSitter': 'Cat Sitter'
	}
	current_profile_type = current_user.profile.profile_type.name

	profile_type = None
	other_type = None
	for p in profile_types:
		if p == current_profile_type:
			profile_type = profile_types[p]
		else:
			other_type = profile_types[p]
	
	requests = current_user.profile.requests
	offers = current_user.profile.offers
	# requests = Request.query.filter_by(cat_keeper=current_profile).order_by(Request.date_posted.desc())
	# offers = Offer.query.filter_by(cat_sitter=current_profile).order_by(Offer.date_posted.desc())

	script = 'maps.js'
	map_key = app.config['GOOGLE_MAPS_API_KEY']
	map_string = "https://maps.googleapis.com/maps/api/js?key=" + map_key + "&callback=initMap&libraries=places&v=weekly"

	return render_template("view.html", title="View", h2=f"View {other_type}s nearby", script=script, map_string=map_string, requests=requests, offers=offers)


@app.errorhandler(404)
def page_not_found(error):
	return render_template("notfound.html", title="Not found", h2="No such page"), 404
