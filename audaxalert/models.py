import datetime
from audaxalert import db


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    audax_id = db.Column(db.Integer, nullable=False, unique=True)
    current_season_rides = db.Column(db.Integer, default=0)
    club = db.Column(db.String(80))
    current_season_club_points = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow) 
    last_checked = db.Column(db.DateTime)  


