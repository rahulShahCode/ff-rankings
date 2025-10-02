import pandas
import requests
from bs4 import BeautifulSoup
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import get_subvertadown_cookie
from constants import SUBVERTADOWN_URL, SUBVERTADOWN_PARAMS, DEFAULT_USER_AGENT

def get_rankings(url:str, header:str, pos:str) -> pandas.DataFrame:
    html = requests.get(url.format(pos), headers=header).text
    return pandas.read_html(html, header=1)

def init() -> dict:
    subvertadown_rankings = {}
    position = ['kicker', 'defense']

    cookie = get_subvertadown_cookie()
    header = {
        "User-Agent" : DEFAULT_USER_AGENT,
        "Cookie" : cookie
    }

    for p in position:
        resp = requests.get(SUBVERTADOWN_URL.format(p),params=SUBVERTADOWN_PARAMS,headers=header)
        soup = BeautifulSoup(resp.content, 'html.parser')

        spans_text = [] 
        table = soup.find('table', class_='sub-table')
        if table: 
            for td in table.find_all('td', class_='-sticky'):
                span = td.find('span')
                if span:
                    spans_text.append(span.get_text(strip=True))
        subvertadown_rankings[p] = spans_text 
    return subvertadown_rankings            

if __name__ == '__main__':
    print(init())