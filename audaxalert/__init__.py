import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = '\xba\x18<\xafuN9\xf9x\xaf1\xe0E\x88O\xf1Z{\xacN\xaf\xfa\xf6\xcc' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'audaxalert.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 'false'
app.config['DEBUG'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdFBzoUAAAAAO4mIRuyvATCSf9RkghyQzKY5LV5'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdFBzoUAAAAAF3sF68GirLn6UgQXoT3hd4qcs8O'




db = SQLAlchemy(app)

from . import models
from . import views
