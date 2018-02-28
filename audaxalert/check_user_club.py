from bs4 import BeautifulSoup
import requests
import dbhelper


RIDER_LIST_URL = "http://www.aukweb.net/results/archive/{}/listride/?Rider={}"
CURRENT_SEASON = 2018
URL_PREFIX = "http://www.aukweb.net"

def process_user_club_membership():
    conn = dbhelper.get_db_connection()
    user_cursor = conn.cursor()
    user_cursor.execute("SELECT id, audax_id FROM user")

    for user in user_cursor.fetchall():
        audax_id = user[1]
        event_url = get_event_url_for_user(audax_id)
        if event_url:
            user_club = get_club_from_event_data(event_url, audax_id)
            if user_club:
                add_club(conn, user_club)
                update_user_club(conn, user_club, audax_id)
                print(user[1])
                print(user_club)


def add_club(cn, club_name):
    sql = "INSERT INTO Club (name, created_date) SELECT '{}', DateTime('now') WHERE NOT EXISTS (SELECT * FROM Club WHERE name = '{}')".format(club_name, club_name)
    cn.execute(sql)
    cn.commit()   

def update_user_club(cn, club_name, audax_id):
    sql = "UPDATE user SET club = '{}' WHERE audax_id = {}".format(club_name, audax_id)
    cn.execute(sql)
    cn.commit
    

def get_club_name_from_result_row(row):
    club_name_text = row.contents[4]
    club = ""
    for i in range(len(club_name_text)):
        club = club + club_name_text[i]
        if club.count(" ") > 4:
            break
    club = club.strip()
    return club
    
def get_club_from_event_data(url, audax_id):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    rider_data = soup.find_all("span", { "class" : ["stripe2", "stripe0"]})
    for row in rider_data:
        link = row.find('a')
        if link and link.text.strip() == str(audax_id):
            club = get_club_name_from_result_row(row)
            return club

def get_event_url_for_user(audax_id):
    url = RIDER_LIST_URL.format(CURRENT_SEASON, audax_id)

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    table = soup.find("table", { "class" : "ridelist smaller" })    

    urls = table.find_all('a', href=True)
    if urls:
        event_url = URL_PREFIX + urls[0]['href']
        return event_url
        

if __name__ == "__main__":
    process_user_club_membership()


