import requests 
url = "https://api.myfantasyleague.com/2022/export"
league_id = 71437
POS = ["RB", "WR", "TE"]
fa_payload = {
    "TYPE": "freeAgents",
    'L':league_id,
    'POSITION':'RB',    
    'JSON':1
}
player_id_payload = {
    "TYPE" : "players",
    "JSON" : 1
}
def get_player_names(ids):
    player_id_payload['PLAYERS'] = ','.join([id['id'] for id in ids])
    
    data = requests.get(url, player_id_payload).json()['players']['player']
    pass

data = requests.get(url,params=fa_payload).json()['freeAgents']['leagueUnit']['player']
get_player_names(data)