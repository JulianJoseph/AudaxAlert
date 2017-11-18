from flask import Flask
app = Flask(__name__)

#@app.route('/')
#def home():
#    return 'Under Construction'

if __name__ == '__main__':
    app.run()

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = '\xba\x18<\xafuN9\xf9x\xaf1\xe0E\x88O\xf1Z{\xacN\xaf\xfa\xf6\xcc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'audaxalert.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 'false'
app.config['DEBUG'] = True
db = SQLAlchemy(app)

import models
import views
