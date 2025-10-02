import requests
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from constants import MFL_API_URL, MFL_LEAGUE_ID, MFL_TEAM_ID

url = MFL_API_URL
league_id = MFL_LEAGUE_ID
my_team_id = MFL_TEAM_ID
POS = ["RB", "WR", "TE"]


def get_player_names(ids):
    player_id_payload = {
    "TYPE" : "players",
    "JSON" : 1
    }
    '''Last, First -> First Last'''
    def reverse_name(name:str) -> str:
        arr = name.split(', ') 
        return arr[1] + ' ' + arr[0]
    ids_len_1 = int(len(ids)/2)
    player_id_payload['PLAYERS'] = ','.join([id['id'] for id in ids[0:ids_len_1]])
    data = requests.get(url, player_id_payload).json()['players']['player']
    player_id_payload['PLAYERS'] = ','.join([id['id'] for id in ids[ids_len_1:len(ids)]])
    data.extend(requests.get(url, player_id_payload).json()['players']['player'])
    return [reverse_name(d['name']) for d in data]

def get_available_players():
    fa_payload = {
    "TYPE": "freeAgents",
    'L':league_id,
    'JSON':1}
    return get_player_names(requests.get(url,params=fa_payload).json()['freeAgents']['leagueUnit']['player'])
def get_team_roster(team_id=my_team_id):
    payload = { "TYPE" : "rosters",
                "L" : league_id,
                "FRANCHISE" : my_team_id,
                "JSON" : 1} 
    return get_player_names(requests.get(url, params=payload).json()['rosters']['franchise']['player'])

if __name__ == '__main__':
    print(get_team_roster())