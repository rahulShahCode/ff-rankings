import requests 
from yahoo_oauth import OAuth2
import xml.etree.ElementTree as ET
import os.path 

home_league_id = 'nfl.l.136310'
home_team_id = 1
work_league_id = 'nfl.l.1348306'
work_team_id = 7
url = 'https://fantasysports.yahooapis.com/fantasy/v2/league/{}'
secrets_path = "~/workspace/ff-rankings/secrets.json"
oauth = OAuth2(None, None, from_file=os.path.expanduser(secrets_path))


def write(filename:str, txt:str) -> None: 
    with open(os.path.expanduser(filename), 'w') as f: 
        f.write(txt)

def parse_xml(xml, type:str): 
    ns = '{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}'
    players_xpath = f'.//{ns}league/{ns}players'
    player_name_xpath=f'./{ns}name/{ns}full'
    team_name_xpath = f'./{ns}editorial_team_full_name'
    root = ET.fromstring(xml)
    if type == "available":
        players_lst = list(root.find(players_xpath))
        available = [] 
        for child in players_lst: 
            name = child.find(player_name_xpath)
            available.append(name.text)
        return available 
    elif type == "rostered":
        rostered_xpath = f'.//{ns}team/{ns}roster/{ns}players'
        players_lst = list(root.find(rostered_xpath))
        rostered = []
        for child in players_lst:
            name = child.find(player_name_xpath)
            rostered.append(name.text)

        return rostered 

def get_available_players(league_id):
    params = "/players;status=A;start={};count=25"
    start = 0
    done = False 
    available = []
    while not done: 
        response = oauth.session.get(url.format(league_id) + params.format(start))
        write('~/workspace/ff-rankings/output/yahoo_debug',response.text)
        parsed_response = parse_xml(response.text, "available")
        available.extend(parsed_response)
        start+= 25
        if len(parsed_response) < 25:
            done = True 
    return available  
def get_team_roster(league_id, team_id): 
    id = league_id + '.t.' + str(team_id)
    rostered_url = f"https://fantasysports.yahooapis.com/fantasy/v2/team/{id}/roster/players"
    response = oauth.session.get(rostered_url)
    return parse_xml(response.text, "rostered")


if __name__ == '__main__':
    val = get_available_players()
    print(val)