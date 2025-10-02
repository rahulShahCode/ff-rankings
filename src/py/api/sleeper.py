import requests
import os.path
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from constants import SLEEPER_API_BASE

# Sleeper API configuration
base_url = SLEEPER_API_BASE
home_league_id = '1256308417333559296'  # Replace with your actual Sleeper league ID
home_team_id = 1  # Replace with your actual team roster ID

def get_league_rosters(league_id):
    """Get all rosters for a league"""
    if not league_id or league_id == '1234567890123456789':
        print("Warning: Please set your actual Sleeper league ID in sleeper.py")
        return []
    url = f"{base_url}/league/{league_id}/rosters"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching rosters: {response.status_code}")
        return []
    return response.json()

def get_league_users(league_id):
    """Get all users in a league"""
    url = f"{base_url}/league/{league_id}/users"
    response = requests.get(url)
    return response.json()

def get_players():
    """Get all NFL players from Sleeper"""
    url = f"{base_url}/players/nfl"
    response = requests.get(url)
    return response.json()

def get_available_players(league_id):
    """Get available players in a league (not on any roster)"""
    rosters = get_league_rosters(league_id)
    if not rosters:
        return []
    
    players = get_players()
    if not players:
        return []
    
    # Get all rostered player IDs
    rostered_player_ids = set()
    for roster in rosters:
        if 'players' in roster:
            rostered_player_ids.update(roster['players'])
    
    # Filter out rostered players to get available ones
    available_players = []
    for player_id, player_data in players.items():
        if player_id not in rostered_player_ids:
            # Include active players and active defense units
            is_active = (player_data.get('status') == 'Active' or
                        (player_data.get('position') == 'DEF' and player_data.get('active') == True))

            if is_active:
                # Format player name (FirstName LastName)
                full_name = f"{player_data.get('first_name', '')} {player_data.get('last_name', '')}".strip()
                if full_name:
                    available_players.append(full_name)
    
    return available_players

def get_team_roster(league_id, team_id):
    """Get roster for a specific team"""
    rosters = get_league_rosters(league_id)
    if not rosters:
        return []
    
    players = get_players()
    if not players:
        return []
    
    # Find the roster for the specified team
    team_roster = None
    for roster in rosters:
        if roster.get('roster_id') == team_id:
            team_roster = roster
            break
    
    if not team_roster or 'players' not in team_roster:
        return []
    
    # Get player names for the team roster
    rostered_players = []
    for player_id in team_roster['players']:
        if player_id in players:
            player_data = players[player_id]
            # Format player name (works for both players and defenses)
            full_name = f"{player_data.get('first_name', '')} {player_data.get('last_name', '')}".strip()
            if full_name:
                rostered_players.append(full_name)
    
    return rostered_players

def get_league_info(league_id):
    """Get basic league information"""
    url = f"{base_url}/league/{league_id}"
    response = requests.get(url)
    return response.json()

def find_user_leagues(username):
    """Find all leagues for a given username"""
    # First get user ID
    user_url = f"{base_url}/user/{username}"
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print(f"Error finding user {username}: {user_response.status_code}")
        return []
    
    user_data = user_response.json()
    user_id = user_data['user_id']
    print(f"Found user ID: {user_id}")
    
    # Get all leagues for the user (try current year and previous year)
    current_year = 2024
    for year in [current_year, current_year - 1]:
        leagues_url = f"{base_url}/user/{user_id}/leagues/nfl/{year}"
        leagues_response = requests.get(leagues_url)
        if leagues_response.status_code == 200:
            leagues = leagues_response.json()
            if leagues:
                print(f"Found {len(leagues)} leagues for {year}")
                return leagues, user_id
    
    print("No leagues found for this user")
    return [], user_id

def find_league_by_name(username, league_name):
    """Find a specific league by name for a user"""
    leagues, user_id = find_user_leagues(username)
    
    if not leagues:
        return None, None, None
    
    print(f"\nSearching for league: '{league_name}'")
    for league in leagues:
        league_name_found = league.get('name', '')
        league_id = league.get('league_id')
        print(f"Found league: '{league_name_found}' (ID: {league_id})")
        
        if league_name.lower() in league_name_found.lower():
            print(f"✓ Match found: {league_name_found}")
            return league_id, league_name_found, user_id
    
    print(f"✗ No league found matching '{league_name}'")
    return None, None, user_id

def find_team_in_league(league_id, user_id):
    """Find the team/roster ID for a user in a specific league"""
    rosters = get_league_rosters(league_id)
    if not rosters:
        return None
    
    for roster in rosters:
        if roster.get('owner_id') == user_id:
            roster_id = roster.get('roster_id')
            print(f"✓ Found your team with roster ID: {roster_id}")
            return roster_id
    
    print("✗ Could not find your team in this league")
    return None

def print_league_setup_help():
    """Print instructions for setting up league and team IDs"""
    print("To set up your Sleeper league integration:")
    print("1. Go to your Sleeper league in a web browser")
    print("2. Look at the URL - it will be something like: https://sleeper.app/leagues/1234567890123456789")
    print("3. Copy the number (1234567890123456789) and set it as home_league_id in sleeper.py")
    print("4. To find your team ID, run: python sleeper.py find_teams YOUR_LEAGUE_ID")
    print("5. Set the roster_id of your team as home_team_id in sleeper.py")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 3 and sys.argv[1] == 'find_league':
        username = sys.argv[2]
        league_name = sys.argv[3]
        print(f"Searching for league '{league_name}' for user '{username}'...")
        
        league_id, found_league_name, user_id = find_league_by_name(username, league_name)
        if league_id:
            team_id = find_team_in_league(league_id, user_id)
            if team_id:
                print(f"\n🎉 SUCCESS! Here are your IDs:")
                print(f"League ID: {league_id}")
                print(f"Team ID: {team_id}")
                print(f"\nUpdate sleeper.py with these values:")
                print(f"home_league_id = '{league_id}'")
                print(f"home_team_id = {team_id}")
            else:
                print("Found league but could not find your team")
        else:
            print("Could not find the league")
            
    elif len(sys.argv) > 2 and sys.argv[1] == 'find_teams':
        league_id = sys.argv[2]
        print(f"Finding teams for league {league_id}...")
        rosters = get_league_rosters(league_id)
        users = get_league_users(league_id)
        
        if rosters and users:
            print("\nTeams in this league:")
            for roster in rosters:
                user_id = roster.get('owner_id')
                user_name = "Unknown"
                for user in users:
                    if user.get('user_id') == user_id:
                        user_name = user.get('display_name', user.get('username', 'Unknown'))
                        break
                print(f"  Roster ID: {roster.get('roster_id')} - {user_name}")
        else:
            print("Could not fetch league data. Check your league ID.")
    elif home_league_id and home_league_id != '1234567890123456789' and home_team_id:
        available = get_available_players(home_league_id)
        rostered = get_team_roster(home_league_id, home_team_id)
        print("Available players:", len(available))
        print("Rostered players:", len(rostered))
    else:
        print_league_setup_help()
        print(f"\nTo find your league and team IDs, run:")
        print(f"python sleeper.py find_league imperialrahl 'Dirty Dozen'")
