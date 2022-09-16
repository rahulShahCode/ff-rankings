import rankings
import yahoo 
import boris 
import os.path
import json 


def main(): 
    data_dict = {"position" : {}}
    positions = ['QB', 'RB','WR','TE', 'FLX', 'K' , 'DEF']
    available = yahoo.get_available_players()
    for pos in positions: 
        rankings = boris.get_rankings(pos)
        data_dict['position'][pos] = {        
            "available" : available,
            "rankings" : rankings
        
        }
    data_dict['rostered'] = yahoo.get_team_roster(1) 
    with open(os.path.expanduser('~/workspace/ff-rankings/output/data.json'), 'w') as fp: 
        json.dump(data_dict, fp)


if __name__ == "__main__":
    main()