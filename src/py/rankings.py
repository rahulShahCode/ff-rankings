import pandas
import requests

def get_rankings(url:str, header:str, pos:str) -> pandas.DataFrame:                     
    html = requests.get(url.format(pos), headers=header).text
    return pandas.read_html(html, header=1)
def init() -> list: 
    url = "https://subvertadown.com/weekly/{}?sort=current_week_projection&sort_direction=desc&platform=yahoo"
    header = { "cookie" : "__stripe_mid=5a7cef6d-e0b2-4515-a6c3-019c8fc06ea3c57892; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Imc2aTgzWHF3R1pseXcxWXlEMXpKRHc9PSIsInZhbHVlIjoiUnBzR0tWRkRuRzhYN3NMN0FmdDBHMVdsUWF0ZGM1S2hGVThzYkdJayszb0hCTGpIeXNqUzN1MHFHL1Z1SkhXcHBCVFlibnRGRXJlbjdub2xEZ0MxSUxHNHYxc3dzMjBxNkRlQ0I5Zm9rbGR0R2RxRGV5Mjgyekp5cm1jdFN1WGdtNi9veFV5WjdhOUhNb016alZUY3orWi92YnFlS3pPb2pzTld5RFd5a2lsMjNFc2VsRzVZOUtiVUxHU2lFMVRYbzZNYTBmRTY4N0NzOWl1QlhGdVFkNFRNdytXRHpUdzN5Nyt3eW5pcTZJRT0iLCJtYWMiOiI3MjBjZGRiZDA4NjZkZGZmZGI3NzY2YzVkNWFiMjYyMjdjNzEzZDZhNTdlNTM2ZDU1ZGNmNDgyNDc1OWEwNTljIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6IjVhNUdFa2VkaVBtNzVUY3BialFpNWc9PSIsInZhbHVlIjoiTHVpZnlubU5scmNHS2h4ZXZncmxGdVpCaHVzWlJPQlRydCtBSWtkMUtncEtHdEJDbWg3T0lGM0wyZHUxOHBXSmRPcW5aT0c3Y0FmVW52TmFuZXJFSUJPejZHanQ3dTI0dkNBcHY0VUlCUVBSRmNqL1JCL1ZjTDFEb1RQWVJPbCsiLCJtYWMiOiI5MGVlNTVmOWM4MWJlNDhlYzU1MjRlMjI3ZjM0N2Y1ZTY4NGFhNjBiOTBmNmEzZmZiNjVkYWEyY2VkMDA3NDExIiwidGFnIjoiIn0%3D; subvertadown_session=eyJpdiI6IkRMUjB1dFNjKyswVktoVmlyZWx4Q2c9PSIsInZhbHVlIjoiYW9wWlFCS3pCcWJEa1NGYTlVaGgyOW5rV2x6Ymt1YkNmeTdBSHFzNE1KbWg4ZkFkcXc2T3BlYndGTVJMSElHVE5LZVdOODBnTHd5Q25QVXFJSDZqeU02YUpuZmJKUCtxWTBaSFVNdmNvL3N6ZUFWbHhDSXZmVlpKMG96ZWVFUmQiLCJtYWMiOiJlZjEwMDA1NGViMmZiZjBhMGViMTM2NDY1OWMyZDM0ZDMyYTBlYmVjOGY2OWQ3YTdmYzFkNGZlY2U0NWVkMDE2IiwidGFnIjoiIn0%3D; __stripe_sid=96a2a545-3fbc-49ac-ba71-c4b3dd56053bbaed6e"
    }
    def convert(df:pandas.DataFrame, pos:str) -> list:
        lst = [] 
        for i in range(len(df)):
            if pos == 'K':
                lst.append(df.iloc[i][0].split(' ')[0])
            elif pos == 'DEF':
                team_str = df.iloc[i][0]
                if 'vs.' in team_str:
                    team_str = team_str.split('vs.')[0]
                else:
                    team_str = team_str.split('@')[0]
                team_str = team_str.strip()
                lst.append(team_str)
        return lst 
    
    lst = []
    lst.append(convert(get_rankings(url,header,"kicker")[0], 'K'))
    lst.append(convert(get_rankings(url,header,"defense")[0], 'DEF'))
    return lst

if __name__ == '__main__':
    print(init())