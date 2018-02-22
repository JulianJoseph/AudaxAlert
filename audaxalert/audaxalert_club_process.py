from bs4 import BeautifulSoup
import requests
import sqlite3
import os
from emailhandler import send_email
import dbhelper

CURRENT_SEASON = 2018
ALERT_SUBJECT = "Audax Alert - Club Activity"
CLUB_URL = "http://www.aukweb.net/results/detail/{}/listclub/?Club={}"

def process_clubs():

    conn = dbhelper.get_db_connection()
    club_cursor = conn.cursor()
    club_cursor.execute("SELECT name, points, last_checked FROM club")

    for club in club_cursor.fetchall():
        club_name = club[0]
        club_current_season_points = int(club[1])
        last_checked = club[2]        

        club_points = check_club_list(get_club_name_for_url(club_name), CURRENT_SEASON)

        if last_checked is None:
            update_last_checked(conn, club_name)
            update_club_stored_points(conn, club_name, club_points)
            continue


        if club_points > club_current_season_points:
            #send alert to all club members
            update_club_stored_points(conn, club_name, club_points)
            send_alert_to_all_club_members(conn, club_name)

        update_last_checked(conn, club_name)


def get_club_name_for_url(club_name):  
    return str.replace(club_name, " ", "+")

def send_alert_to_all_club_members(cn, club_name):
    club_member_cursor = cn.cursor()
    sql = "SELECT email FROM user WHERE club = '{}'".format(club_name)   
    club_member_cursor.execute(sql)

    for club_member in club_member_cursor.fetchall():
        print(club_member[0])
        send_alert(club_member[0], club_name)

def send_alert(address, club_name):
    url = CLUB_URL.format(CURRENT_SEASON, get_club_name_for_url(club_name))
    msg = "<b>New activity has been logged for {} season by a member of your club {} on Audax website</b><br><br>".format(CURRENT_SEASON, club_name)
    msg = msg + "Please check the following URL for details:<br><br>{}".format(url)
    send_email(address, ALERT_SUBJECT, msg)
    
def update_last_checked(cn, club_name):
    sql = "UPDATE club SET last_checked = DateTime('now') WHERE name='{}'".format(club_name)
    cn.execute(sql)
    cn.commit()

def update_club_stored_points(cn, club_name, points):
    sql = "UPDATE club SET points = {} WHERE name='{}'".format(points, club_name)
    cn.execute(sql)
    cn.commit() 

def check_club_list(club_name, season):
    url = CLUB_URL.format(season, club_name)    
    print(url)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    table = soup.find("table", { "bgcolor" : "#eeeeee" })

    club_points = 0
    for row in table.findAll("tr"):
        cells = row.find_all("td")

        firstCellText = cells[0].text.strip()
        if firstCellText.startswith("6-rider total:"):
            continue
        
        rider_points = int(cells[3].text.strip())
        club_points = club_points + rider_points

    return club_points
    
if __name__ == "__main__":
    process_clubs();