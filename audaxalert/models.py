import datetime
from audaxalert import db

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    audax_membership_id = db.Column(db.Integer, nullable=False, unique=True)
    current_season_rides = db.Column(db.Integer, nullable=False)
    club = db.Column(db.String(80))
    current_season_club_points = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)    

    def __rep__(self):
        return '<User %r>' % self.email

