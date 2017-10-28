#! /usr/bin/env python

from audaxalert import app, db
from audaxalert.models import User
from flask.ext.script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.drop_all()
    db.create_all()
    #db.session.add(User(email="jules@joseph-net.co.uk", audax_membership_id=12348, current_season_rides=0, club="Dulwich Paragon", current_season_club_points=0))
    #db.session.commit()  
    print("Initialised the database")

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop the db?"):
        print(db)
        db.drop_all()
        print("Dropped the database")

if __name__ == '__main__':
    manager.run()