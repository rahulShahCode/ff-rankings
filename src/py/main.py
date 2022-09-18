import rankings
import yahoo 
import boris 
import os.path
import json 
import mfl 

def main(): 
    data_dict = {
        "home" : {},
        "work" : {}, 
        "mfl" : {},
        "rankings" : {}
    }
    positions = ['QB', 'RB','WR','TE', 'FLX']
    subvertadown = rankings.init()
    data_dict['rankings']['K'] = subvertadown[0]
    data_dict['rankings']['DEF'] = subvertadown[1]
    for pos in positions: 
        tiers = boris.get_rankings(pos)
        data_dict['rankings'][pos] = tiers 
    data_dict['mfl']['available'] = mfl.get_available_players()
    data_dict['mfl']['rostered'] = mfl.get_team_roster()
    data_dict['home']['available'] = yahoo.get_available_players(yahoo.home_league_id)
    data_dict['home']['rostered'] = yahoo.get_team_roster(yahoo.home_league_id,yahoo.home_team_id) 
    data_dict['work']['available'] = yahoo.get_available_players(yahoo.work_league_id)
    data_dict['work']['rostered'] = yahoo.get_team_roster(yahoo.work_league_id,yahoo.work_team_id) 
    with open(os.path.expanduser('~/workspace/ff-rankings/data.json'), 'w') as fp: 
        json.dump(data_dict, fp)


if __name__ == "__main__":
    main()

