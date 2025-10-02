import os.path
import json
from datetime import datetime

# Import from reorganized structure
from api import boris, pff, mfl, sleeper
from utils import rankings, player_metadata 

team_name_map = {
    'Commanders': 'Washington Commanders',
    'Ravens': 'Baltimore Ravens',
    'Vikings': 'Minnesota Vikings',
    'Falcons': 'Atlanta Falcons',
    'Broncos': 'Denver Broncos',
    'Bills': 'Buffalo Bills',
    'Jaguars': 'Jacksonville Jaguars',
    'Seahawks': 'Seattle Seahawks',
    '49ers': 'San Francisco 49ers',
    'Cowboys': 'Dallas Cowboys',
    'Bengals': 'Cincinnati Bengals',
    'Eagles': 'Philadelphia Eagles',
    'Saints': 'New Orleans Saints',
    'Raiders': 'Las Vegas Raiders',
    'Bears': 'Chicago Bears',
    'Packers': 'Green Bay Packers',
    'Cardinals': 'Arizona Cardinals',
    'Steelers': 'Pittsburgh Steelers',
    'Jets': 'New York Jets',
    'Titans': 'Tennessee Titans',
    'Panthers': 'Carolina Panthers',
    'Chargers': 'Los Angeles Chargers',
    'Patriots': 'New England Patriots',
    'Giants': 'New York Giants',
    'Browns': 'Cleveland Browns',
    'Chiefs': 'Kansas City Chiefs',
    'Rams': 'Los Angeles Rams',
    'Buccaneers': 'Tampa Bay Buccaneers',
    'Colts': 'Indianapolis Colts',
    'Texans': 'Houston Texans',
    'Dolphins': 'Miami Dolphins',
    'Lions': 'Detroit Lions'
}


def main():
    data_dict = {
        "home" : {},
        "mfl" : {},
        "rankings" : {},
        "pff" : {}
    }
    positions = ['QB', 'RB','WR','TE', 'FLX']
    subvertadown = rankings.init()
    data_dict['rankings']['K'] = subvertadown['kicker']
    data_dict['rankings']['DEF'] = [team_name_map[team] for team in subvertadown['defense']]

    
    for pos in positions: 
        tiers = boris.get_rankings(pos)
        data_dict['rankings'][pos] = tiers 
    data_dict['mfl']['available'] = mfl.get_available_players()
    data_dict['mfl']['rostered'] = mfl.get_team_roster()
    data_dict['home']['available'] = sleeper.get_available_players(sleeper.home_league_id)
    data_dict['home']['rostered'] = sleeper.get_team_roster(sleeper.home_league_id, sleeper.home_team_id)

    # Add PFF rankings
    try:
        pff_rankings = pff.get_pff_rankings()
        data_dict['pff']['rankings'] = pff_rankings
        print("Successfully added PFF rankings")
    except Exception as e:
        print(f"Warning: Could not fetch PFF rankings: {e}")
        data_dict['pff']['rankings'] = {}

    # Add player metadata
    try:
        pm = player_metadata.PlayerMetadata()
        metadata = pm.compile_metadata()
        data_dict['metadata'] = metadata
        print("Successfully added player metadata")
    except Exception as e:
        print(f"Warning: Could not add metadata: {e}")
        data_dict['metadata'] = {}

    # Add timestamp
    data_dict['last_updated'] = datetime.now().isoformat()

    with open(os.path.expanduser('~/workspace/ff-rankings/data.json'), 'w') as fp:
        json.dump(data_dict, fp)


if __name__ == "__main__":
    main()

