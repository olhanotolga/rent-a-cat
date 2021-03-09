from flask import render_template, url_for, flash, redirect
from flask_login import login_required, current_user, login_user
from rentacat import app, db, bcrypt
from rentacat.forms import RegistrationForm, LoginForm
from rentacat.models import User


@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
	return render_template("index.html", title="Home", h1="Rent a Cat")


@app.route("/about")
def about():
	return render_template("about.html", h1="About Rent a Cat", title="About")


@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard.html'))
	form = LoginForm()
	#? last login — update every time user logs in
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if form.email.data == 'admin@rac.com' and form.password.data == 'qwerty':
			login_user(user, remember=form.remember.data)
			flash('You\'re in!', 'success')
			# db.user.
			#! REDIRECT to profile or views later
			return redirect(url_for('index'))
		else:
			flash('Nope. Please check if your email and/or password are correct.', 'error')
	return render_template("login.html", title="Log in", form=form)


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
		#! REDIRECT to profile or views later
		return redirect(url_for('dashboard'))
	return render_template("registration.html", title="Sign up", form=form)


@app.route("/profile")
@login_required
def own_profile():
	# first name + last name
	# username
	#? username = current_user.username
	# email
	# address
	# phone number
	# facebook username
	# telegram username
	# about

	return render_template("profile.html", title="Your profile", h1="Profile")


@app.route("/profile/update", methods=['GET', 'POST'])
@login_required
def update_profile():
	return render_template("profile.html", title="Your profile", h1="Profile")


@app.route("/user/<string:username>")
def user_profile(username):
	if current_user.username == username:
		return redirect(url_for('own_profile'))
	return render_template("profile.html", title=f"{username}'s profile", h1=f"{username}'s profile")


@app.route("/dashboard")
@login_required
def dashboard():
	return render_template("dashboard.html", title="Dashboard", h1="Dashboard")


# potentially: all updates as a list and map
@app.route("/view")
def view():
	return render_template("view.html", title="View")


@app.errorhandler(404)
def page_not_found(error):
	return render_template("notfound.html", title="Not found"), 404
