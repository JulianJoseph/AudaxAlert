from flask import Flask, render_template, url_for, request, redirect, flash
from audaxalert import app, db
from . emailhandler import send_email
from . forms import SignupForm
from . models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(audax_id=form.userid.data,
                    email = form.email.data)
        db.session.add(user)
        db.session.commit()

        subject = "AudaxAlert - Registration Confirmation - Member {}".format(user.audax_id)
        msg = "You will now receive an email when new rides are registered on the Audax website.<br><br>"
        msg = msg + "Please reply to this email with any questions"
        send_email(user.email, subject, msg)


        return redirect(url_for('confirm'))
    return render_template("signup.html", form=form)

@app.route("/confirm")
def confirm():
    return render_template('confirm.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


