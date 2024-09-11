import requests 
url = "https://api.myfantasyleague.com/2024/export"
league_id = 62247
my_team_id = '0011'
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