import pandas
import requests
from bs4 import BeautifulSoup

def get_rankings(url:str, header:str, pos:str) -> pandas.DataFrame:                     
    html = requests.get(url.format(pos), headers=header).text
    return pandas.read_html(html, header=1)
def init() -> dict: 
    subvertadown_rankings = {}
    position = ['kicker', 'defense']
    url = "https://subvertadown.com/weekly/{}"
    params = {
        'sort' : 'current_week_projection',
        'sort_direction' : 'desc',
        'platform' : 'yahoo'
    }
    header = { "User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        "Cookie" : "__stripe_mid=ffc09ada-d8e3-4b8c-ad09-0d8b80ba44db3ce6e8; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImNlRlR5MmRGeWJ1TGVaSzJoNzNPckE9PSIsInZhbHVlIjoiY1FmcHhFSis2ejA2VnFhbk9BTVZaaWkwWVRyRC80dWRyTzFKTzNsMWRqS0pXMXNqZkFxaTRBbVNibGRVcnQrMUtObzBuS1pKSTVQTTh2SDBva3B0andPZ1lVUnZRdzY1R1R4YktsaUdKVkNHTi9vWHBkOU4rYTdqK20rREh2Rm5nK3g0VzlQWklrUWYzTzBCMXRxT3FiR3k1RDhCbWhxaElianVpb1R1U1ExNUFnaTFYYUFsYU50S1huTkNJLzdCKzZKcXAxSHJGZGxXUlFwMkxUSTBIbDNMQ1ZiSlRYUFFCT1JBdkpBam5IUT0iLCJtYWMiOiIwMWM0MDQ0MjdmODU0Zjg1NTQ3ODk5YWM4NTAzNmIyMWQ3NWE4MmJjMjg5OTYyNzQ4Y2UyNWVmOGZlYjc4OWQyIiwidGFnIjoiIn0%3D; __stripe_sid=8b3cd079-6e4b-4389-a9b0-de534c7ce01c87a4c3; XSRF-TOKEN=eyJpdiI6InZ4Y3I3K3NISlNHNjJndjY0OGFmY3c9PSIsInZhbHVlIjoiSUdCRk5CUHNTR3ozSE5mMjgwSWZQbGdpa0t6K3BDUFZXY0k1eGo2UXB1dk8xVFY2b1ZMbzZXUXF1ZzhYNVF3ZENnV1pjNHkvVDZtWW5aTzljSEt4Z3k1SHpRdVlpaTE0K1pnbHBJQ1VQT2R2U01yOEpabDQwYk81ckdCOXRHbVUiLCJtYWMiOiI1ZGQyOWYzMmNmZjAxMWYwZDIyNjA0OTk4OTRhZGI1NjBiMDc5YjI3NTYzYTg0MTQwNjdiOWYzMWM4NjYxYjZiIiwidGFnIjoiIn0%3D; subvertadown_session=eyJpdiI6Ii9LMDVZMzhTT1VXSi9vY1hsWTQ1ZVE9PSIsInZhbHVlIjoiM2xMd2llS2tBWXovWkRabVkyM2VGT3hBTnp3TjBjMUpiQ2Z0cjhYckRndk9kZk80ak9EU25XZzRxWUVhRWQxN3Qya0lYdDRLTTRHNjhhaGRWOWFXMnRML3RRVk9UNGtpRGN3ZWVNejNobEF4QVNCdm5VOWd0Unk2VmNPNWFYR3EiLCJtYWMiOiI1MTc4MmE2YzIwYjBiNDcwMGZkNGQ2MzkyMDgzNTVjNzAyZTExNDg4MmFmOTEwYjZjNjA2NjI5YzU4MGJlZWNmIiwidGFnIjoiIn0%3D"}

    for p in position:       
        resp = requests.get(url.format(p),params=params,headers=header)
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