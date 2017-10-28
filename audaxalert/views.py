from flask import Flask, render_template, url_for, request, redirect, flash
from audaxalert import app, db, login_manager
from . forms import LoginForm, SignupForm
from . models import User
from flask_login import login_required, login_user, logout_user, current_user

bookmarks = []

# @login_manager.user_loader
# def load_user(userid):
#     return User.query.get(int(userid))

@login_manager.user_loader
def logged_in_user(userid):
    return User.query.get(int(userid))

def store_bookmark(url):
    bookmarks.append(dict( 
        url = url,
        user = "reindert",
        date = datetime.utcnow()
    ))

def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=new_bookmarks(5))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    print('add route')
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmark(url)
        flash('stored : {}'.format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/user/<audax_membership_id>')
def user(audax_membership_id):
    user = User.query.filter_by(audax_membership_id=audax_membership_id).first_or_404()
    return render_template('user.html', user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_userid(form.userid.data)
        user = User.query.filter_by(audax_membership_id=form.userid.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.email))
            return redirect(request.args.get('next') or url_for('user',audax_membership_id=user.audax_membership_id))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, 
                    audax_membership_id=form.userid.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.email))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


#if __name__ == '__main__':  
    #app.run(debug=True)
