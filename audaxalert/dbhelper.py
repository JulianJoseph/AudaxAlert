import sqlite3
import os
import datetime

def get_db_connection():
    basedir = os.path.abspath(os.path.dirname(__file__))
    databaseUri = os.path.join(basedir, "audaxalert.db")
    conn = sqlite3.connect(databaseUri)
    return conn    

def run_every_hour(hours):
    now = datetime.datetime.now()
    current_hours = now.hour
    print (current_hours)    
    if current_hours % hours == 0:
        return True
    return False


if __name__ == "__main__":
    if run_every_hour(2):
        print ('run')