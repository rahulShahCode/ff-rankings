import requests
import re
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from constants import BORIS_CHEN_URL

template_url = BORIS_CHEN_URL


def parse_rankings(rankings:str) -> dict:
    rankings_dict = dict()
    tiers = rankings.splitlines()
    pattern = r'^Tier (\d+):\s(.*)$'
    for i in tiers:
        m = re.match(pattern,i) 
        players = [i.strip() for i in m.group(2).split(',')]
        rankings_dict["Tier {}".format(m.group(1))] = players 
    return rankings_dict
def get_rankings(pos: str) -> list:  
    pos = pos.upper()
    if pos in ('RB', 'WR', 'TE', 'FLX'):
        pos += '-PPR'
    return parse_rankings(requests.get(template_url.format(pos)).text)

if __name__ == '__main__':
    print(get_rankings('RB'))