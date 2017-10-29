import datetime
from audaxalert import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    audax_id = db.Column(db.Integer, nullable=False, unique=True)
    current_season_rides = db.Column(db.Integer, default=0)
    club = db.Column(db.String(80))
    current_season_club_points = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)    

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_audax_id(audax_id):
        return User.query.filter_by(audax_id=audax_id).first()

    def __rep__(self):
        return '<User %r>' % self.audax_id

