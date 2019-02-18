import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'xxxx' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'audaxalert.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 'false'
app.config['DEBUG'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = 'xxxx'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'xxxx'




db = SQLAlchemy(app)

from . import models
from . import views
