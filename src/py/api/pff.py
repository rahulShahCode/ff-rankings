import requests
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import get_pff_api_key
from constants import PFF_WEEKLY_API, PFF_POSITIONS

def get_pff_rankings(scoring_type='ppr', max_pages=1):
    """
    Fetch fantasy football weekly rankings from Pro Football Focus (PFF)

    Args:
        scoring_type: ppr, standard, half_ppr
        max_pages: Maximum number of pages to fetch per position (default 1)

    Returns:
        dict: Organized rankings by position with metadata
    """

    api_key = get_pff_api_key()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://www.pff.com/',
        'api-key': api_key,
        'Origin': 'https://www.pff.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=4',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
    }

    # Positions to fetch (D for defense in weekly rankings)
    positions = PFF_POSITIONS
    all_rankings = {}
    metadata = {}

    for position in positions:
        all_rankings[position] = []
        page = 1

        while page <= max_pages:
            url = f'https://consumer-api.pff.com/football/v1/fantasy/weekly-rankings?position={position}&scoringType={scoring_type}&page={page}'

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()

                if 'rankings' not in data or not data['rankings']:
                    break

                all_rankings[position].extend(data['rankings'])

                # Store metadata from first request
                if page == 1 and 'lastUpdatedAt' in data:
                    metadata['lastUpdatedAt'] = data.get('lastUpdatedAt')
                    metadata['currentGameWeek'] = data.get('currentGameWeek')

                print(f"Fetched PFF {position} page {page}: {len(data['rankings'])} players")

                # Check if there are more pages
                if len(data['rankings']) < 50:  # Assuming ~50 items per page
                    break

                page += 1

            except Exception as e:
                print(f"Error fetching PFF {position} rankings page {page}: {e}")
                break

    # Organize by position with cleaned data
    rankings_by_position = {'metadata': metadata}

    for position, players in all_rankings.items():
        rankings_by_position[position] = []

        for player in players:
            # Extract relevant data
            # For defense, use city + team name (e.g., "Minnesota Vikings")
            if position == 'D':
                city = player.get('city', '')
                team = player.get('name', '')
                player_name = f"{city} {team}".strip() if city and team else (team or player.get('teamAbbreviation', ''))
            else:
                player_name = f"{player.get('firstName', '')} {player.get('lastName', '')}".strip()

            player_data = {
                'name': player_name,
                'team': player.get('teamAbbreviation', ''),
                'position': position,
                'rank': player.get('rank', {}).get('current'),
                'positionRank': player.get('rank', {}).get('position'),
                'projection': player.get('projection', {}),
                'tags': [tag.get('name', '') for tag in player.get('tags', [])] if player.get('tags') else [],
                'byeWeek': player.get('byeWeek'),
                'nextOpponent': player.get('nextOpponentAbbreviation', ''),
                'nextGameWeek': player.get('nextGameWeek'),
                'gameStatus': player.get('gameStatus'),
                'jerseyNumber': player.get('jerseyNumber')
            }

            rankings_by_position[position].append(player_data)

        # Sort each position by rank
        rankings_by_position[position].sort(key=lambda x: x.get('rank', 999))

    return rankings_by_position


def get_pff_player_list():
    """
    Get a simplified list of players with their PFF rankings

    Returns:
        list: List of player names in rank order
    """
    rankings = get_pff_rankings()
    all_players = []

    for position, players in rankings.items():
        if position == 'metadata':
            continue
        for player in players:
            all_players.append({
                'name': player['name'],
                'position': position,
                'rank': player['rank'],
                'positionRank': player['positionRank']
            })

    # Sort by overall rank
    all_players.sort(key=lambda x: x.get('rank', 999))

    return all_players


if __name__ == '__main__':
    # Test the module
    rankings = get_pff_rankings()

    # Print metadata
    if 'metadata' in rankings:
        meta = rankings['metadata']
        print(f"\nWeek {meta.get('currentGameWeek', 'N/A')} Rankings")
        print(f"Last Updated: {meta.get('lastUpdatedAt', 'N/A')}")

    # Print player rankings
    for position, players in rankings.items():
        if position == 'metadata':
            continue
        print(f"\n{position} ({len(players)} players):")
        for i, player in enumerate(players[:5]):  # Print top 5
            tags_str = f" [{', '.join(player['tags'])}]" if player['tags'] else ""
            proj = player.get('projection', {}).get('points', {}).get('mid', 'N/A')
            print(f"  {player['rank']}. {player['name']} ({player['team']}) - Proj: {proj}{tags_str}")
