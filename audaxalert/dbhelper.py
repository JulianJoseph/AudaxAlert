import sqlite3
import os

def get_db_connection():
    basedir = os.path.abspath(os.path.dirname(__file__))
    databaseUri = os.path.join(basedir, "audaxalert.db")
    conn = sqlite3.connect(databaseUri)
    return conn    