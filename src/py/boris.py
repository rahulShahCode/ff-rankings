import requests 
import re 
template_url = "https://s3-us-west-1.amazonaws.com/fftiers/out/text_{}.txt"


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