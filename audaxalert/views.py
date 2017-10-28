from flask import Flask, render_template, url_for, request, redirect, flash
from audaxalert import app, db
#from forms import BookmarkForm
from . models import User

bookmarks = []

#fake login
def logged_in_user():
    return User.query.filter_by(email='jules@joseph-net.co.uk'),first()

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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


#if __name__ == '__main__':  
    #app.run(debug=True)
