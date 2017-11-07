from flask import Flask, render_template, url_for, request, redirect, flash
from audaxalert import app, db
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
        return redirect(url_for('index'))
    return render_template("signup.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


