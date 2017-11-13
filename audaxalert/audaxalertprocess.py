from bs4 import BeautifulSoup
import requests
import sqlite3
import os
from emailhandler import send_email

CURRENT_SEASON = 2018
ALERT_SUBJECT = "Audax Alert"
RIDER_LIST_URL = "http://www.aukweb.net/results/archive/{}/listride/?Rider={}"

def process_users():

    conn = get_db_connection()
    user_cursor = conn.cursor()
    user_cursor.execute("SELECT id, email, audax_id, current_season_rides, last_checked FROM user")

    for user in user_cursor.fetchall():
        user_id = user[0]
        email = user[1]
        audax_id = user[2]
        stored_current_season_rides = user[3]
        last_checked = user[4]
        latest_current_season_rides = check_rider_list(audax_id, CURRENT_SEASON)

        if last_checked is None:
            update_last_checked(conn, user_id)
            continue

        print("AudaxID: {} Stored Rides: {} Current Rides: {}".format(audax_id, stored_current_season_rides, latest_current_season_rides))
        if(latest_current_season_rides > stored_current_season_rides):
            update_stored_current_rides(conn, user_id, latest_current_season_rides)
            send_alert(email, audax_id)

        update_last_checked(conn, user_id)


def send_alert(address, audax_id):
    url = RIDER_LIST_URL.format(CURRENT_SEASON, audax_id)
    msg = "<b>New activity has been logged for {} season, membership number {} on Audax website</b><br><br>".format(CURRENT_SEASON, audax_id)
    msg = msg + "Please check the following URL for details:<br><br>{}".format(url)
    send_email(address, ALERT_SUBJECT, msg)
    
def update_last_checked(cn, user_id):
    sql = "UPDATE user SET last_checked = DateTime('now') WHERE id={}".format(user_id)
    cn.execute(sql)
    cn.commit()

def update_stored_current_rides(cn, user_id, rides):
    sql = "UPDATE user SET current_season_rides = {} WHERE id={}".format(rides, user_id)
    cn.execute(sql)
    cn.commit()

def get_db_connection():
    basedir = os.path.abspath(os.path.dirname(__file__))
    databaseUri = os.path.join(basedir, "audaxalert.db")
    conn = sqlite3.connect(databaseUri)
    return conn    

def check_rider_list(audax_id, season):
    url = RIDER_LIST_URL.format(season, audax_id)
    print(url)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    table = soup.find("table", { "class" : "ridelist smaller" })

    ride_count = 0
    for row in table.findAll("tr"):
        cells = row.find_all("td")
        if(len(cells) == 9):
            event_name = cells[4]
            #print(event_name.text)
            ride_count = ride_count + 1

    return ride_count
    
if __name__ == "__main__":
    process_users();