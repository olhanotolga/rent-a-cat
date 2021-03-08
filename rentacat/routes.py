from flask import render_template, url_for, flash, redirect
from rentacat import app
from rentacat.forms import RegistrationForm, LoginForm

@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
	return render_template("index.html", title="Home", h1="Rent a Cat")

@app.route("/about")
def about():
	return render_template("about.html", title="About")

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@rac.com' and form.password.data == 'qwerty':
			flash('You\'re in!', 'success')
			#! REDIRECT to profile or views later
			return redirect(url_for('index'))
		else:
			flash('Nope. Please check if your email and/or password are correct.', 'danger')
	return render_template("login.html", title="Log in", form=form)

@app.route("/signup", methods=["GET", "POST"])
def registration():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Welcome aboard, {form.username.data}!', 'success')
		#! REDIRECT to profile or views later
		return redirect(url_for('index'))
	return render_template("registration.html", title="Sign up", form=form)

@app.route("/profile")
def profile():
	return render_template("profile.html", title="Your profile")

# potentially: all updates as a list and map
@app.route("/view")
def view():
	return render_template("view.html", title="View")

@app.route("/terms")
def terms():
	return render_template("terms.html", title="Terms")

@app.errorhandler(404)
def page_not_found(error):
	return render_template("notfound.html", title="Not found"), 404
