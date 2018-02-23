from bs4 import BeautifulSoup
import requests

# Method:
# get list of users
# 1: get url for user
# 2: get first event url for that user
# 3: get html back for the event url
# 4: find first result for current user in the event html
# 5: get club from club column
# 6: get list of clubs from table
# 7: if club not in table then insert


RIDER_LIST_URL = "http://www.aukweb.net/results/archive/{}/listride/?Rider={}"
CURRENT_SEASON = 2018
URL_PREFIX = "http://www.aukweb.net"

#event_url = get_event_url_for_user(12348)
#get_event_data(event_url)

def get_club_name_from_result_row(row):
    club_name_text = row.contents[4]
    club = ""
    for i in range(len(club_name_text)):
        club = club + club_name_text[i]
        if club.count(" ") > 4:
            break
    club = club.strip()
    return club
    
def get_event_data(url, audax_id):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    rider_data = soup.find_all("span", { "class" : ["stripe2", "stripe0"]})
    for row in rider_data:
        link = row.find('a')
        if link and link.text.strip() == str(audax_id):
            club = get_club_name_from_result_row(row)
            print(club)
            break

def get_event_url_for_user(audax_id):
    print(audax_id)
    url = RIDER_LIST_URL.format(CURRENT_SEASON, audax_id)

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    table = soup.find("table", { "class" : "ridelist smaller" })    

    urls = table.find_all('a', href=True)
    if urls:
        event_url = URL_PREFIX + urls[0]['href']
        print(event_url)
        return event_url
        

if __name__ == "__main__":
    get_event_data("http://www.aukweb.net/results/detail/2018/listevent/?Ride=17-681", 12348)
#    get_event_url_for_user(12348);

