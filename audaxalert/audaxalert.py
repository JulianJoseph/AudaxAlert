#hello
# import os
# from datetime import datetime
# from flask import Flask, render_template, url_for, request, redirect, flash
# from flask_sqlalchemy import SQLAlchemy
# from forms import BookmarkForm

# basedir = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# #for session encryption - generated via python
# app.config['SECRET_KEY'] = '\xba\x18<\xafuN9\xf9x\xaf1\xe0E\x88O\xf1Z{\xacN\xaf\xfa\xf6\xcc' 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'audaxalert.db')
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 'false'
# db = SQLAlchemy(app)

# bookmarks = []

# def store_bookmark(url):
#     bookmarks.append(dict( 
#         url = url,
#         user = "reindert",
#         date = datetime.utcnow()
#     ))

# def new_bookmarks(num):
#     return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]

# @app.route('/')
# @app.route('/index')
# def index():
#     return render_template('index.html', new_bookmarks=new_bookmarks(5))


# @app.route('/add', methods=['GET', 'POST'])
# def add():
#     print('add route')
#     form = BookmarkForm()
#     if form.validate_on_submit():
#         url = form.url.data
#         description = form.description.data
#         store_bookmark(url)
#         flash('stored : {}'.format(description))
#         return redirect(url_for('index'))
#     return render_template('add.html', form=form)


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404


# @app.errorhandler(500)
# def page_not_found(e):
#     return render_template('500.html'), 500


# if __name__ == '__main__':  
#     app.run(debug=True)
