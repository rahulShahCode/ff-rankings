"""
Player Metadata Module
Fetches additional player information including injury status, bye weeks,
team info, trends, and matchup data
"""

import requests
import json
from datetime import datetime

class PlayerMetadata:
    def __init__(self):
        self.injuries = {}
        self.bye_weeks = {}
        self.teams = {}
        self.trends = {}
        self.matchups = {}
        self.stats = {}

        # 2024 NFL Bye Weeks (example data - update with actual schedule)
        self.team_bye_weeks = {
            'ARI': 11, 'ATL': 12, 'BAL': 14, 'BUF': 13,
            'CAR': 11, 'CHI': 7, 'CIN': 12, 'CLE': 5,
            'DAL': 7, 'DEN': 9, 'DET': 5, 'GB': 10,
            'HOU': 14, 'IND': 14, 'JAX': 12, 'KC': 6,
            'LAC': 5, 'LAR': 6, 'LV': 13, 'MIA': 10,
            'MIN': 13, 'NE': 14, 'NO': 11, 'NYG': 11,
            'NYJ': 12, 'PHI': 10, 'PIT': 6, 'SEA': 5,
            'SF': 9, 'TB': 5, 'TEN': 7, 'WAS': 14
        }

        # Matchup difficulty rankings (example - replace with actual data)
        self.defense_rankings = {
            'BAL': 1, 'SF': 2, 'NYJ': 3, 'CLE': 4, 'BUF': 5,
            'PHI': 6, 'PIT': 7, 'DAL': 8, 'KC': 9, 'NE': 10,
            'NO': 11, 'DEN': 12, 'GB': 13, 'MIN': 14, 'LAR': 15,
            'CHI': 16, 'SEA': 17, 'IND': 18, 'TEN': 19, 'MIA': 20,
            'TB': 21, 'CIN': 22, 'JAX': 23, 'HOU': 24, 'LAC': 25,
            'DET': 26, 'NYG': 27, 'LV': 28, 'ATL': 29, 'CAR': 30,
            'WAS': 31, 'ARI': 32
        }

    def get_sleeper_metadata(self):
        """Fetch metadata from Sleeper API"""
        try:
            # Get all players from Sleeper
            url = "https://api.sleeper.app/v1/players/nfl"
            response = requests.get(url)

            if response.status_code == 200:
                players = response.json()

                for player_id, player_data in players.items():
                    if player_data.get('active'):
                        full_name = f"{player_data.get('first_name', '')} {player_data.get('last_name', '')}".strip()

                        # Store team info
                        if player_data.get('team'):
                            self.teams[full_name] = player_data['team']

                            # Calculate bye week
                            if player_data['team'] in self.team_bye_weeks:
                                self.bye_weeks[full_name] = self.team_bye_weeks[player_data['team']]

                        # Store injury status
                        if player_data.get('injury_status'):
                            self.injuries[full_name] = player_data['injury_status']

                        # Store position
                        if player_data.get('position'):
                            if full_name not in self.stats:
                                self.stats[full_name] = {}
                            self.stats[full_name]['position'] = player_data['position']

                        # Store fantasy positions
                        if player_data.get('fantasy_positions'):
                            if full_name not in self.stats:
                                self.stats[full_name] = {}
                            self.stats[full_name]['fantasy_positions'] = player_data['fantasy_positions']

        except Exception as e:
            print(f"Error fetching Sleeper metadata: {e}")

    def calculate_matchup_difficulty(self, player_team, opponent_team):
        """Calculate matchup difficulty based on defensive rankings"""
        if not opponent_team or opponent_team not in self.defense_rankings:
            return "Medium"

        rank = self.defense_rankings[opponent_team]

        if rank <= 10:
            return "Hard"
        elif rank <= 22:
            return "Medium"
        else:
            return "Easy"

    def get_trend(self, player_name, previous_rank=None, current_rank=None):
        """Calculate player trend based on ranking changes"""
        # This would be calculated based on historical data
        # For now, return mock data
        import random
        trends = ["up", "down", "neutral"]
        return random.choice(trends) if random.random() > 0.5 else "neutral"

    def get_recent_stats(self, player_name):
        """Get recent player statistics"""
        # This would fetch from a stats API
        # For now, return mock data
        if player_name in self.stats:
            return {
                "last_3_games": f"{round(15 + (hash(player_name) % 10), 1)} pts",
                "season_avg": f"{round(12 + (hash(player_name) % 8), 1)} pts",
                "ownership": f"{50 + (hash(player_name) % 40)}",
                "rank_change": f"+{hash(player_name) % 5}" if hash(player_name) % 2 == 0 else f"-{hash(player_name) % 5}"
            }
        return {}

    def get_weather_data(self, game_location):
        """Get weather data for outdoor games"""
        # This would fetch from a weather API
        # For now, return mock data
        outdoor_stadiums = ['BUF', 'CHI', 'CLE', 'DEN', 'GB', 'KC', 'NE', 'NYJ', 'PHI', 'PIT', 'SEA', 'WAS']

        if game_location in outdoor_stadiums:
            import random
            conditions = ["Clear", "Rain", "Snow", "Wind", "Cold"]
            return random.choice(conditions)
        return None

    def compile_metadata(self):
        """Compile all metadata into a single dictionary"""
        self.get_sleeper_metadata()

        metadata = {
            "injuries": self.injuries,
            "bye_weeks": self.bye_weeks,
            "teams": self.teams,
            "trends": {},
            "stats": {},
            "matchups": {},
            "weather": {}
        }

        # Add trends and stats for each player
        for player_name in self.teams.keys():
            metadata["trends"][player_name] = self.get_trend(player_name)
            metadata["stats"][player_name] = self.get_recent_stats(player_name)

            # Calculate matchup difficulty (would need actual schedule data)
            if player_name in self.teams:
                # Mock opponent - in reality, would look up actual schedule
                metadata["matchups"][player_name] = {
                    "difficulty": "Medium",
                    "opponent": "TBD"
                }

        return metadata

    def save_to_file(self, filename="player_metadata.json"):
        """Save metadata to JSON file"""
        metadata = self.compile_metadata()

        with open(filename, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"Metadata saved to {filename}")
        return metadata

def update_main_data_with_metadata():
    """Update the main data.json file with metadata"""
    import os

    # Get metadata
    pm = PlayerMetadata()
    metadata = pm.compile_metadata()

    # Load existing data.json
    data_path = os.path.expanduser('~/workspace/ff-rankings/data.json')

    try:
        with open(data_path, 'r') as f:
            data = json.load(f)

        # Add metadata to the data
        data['metadata'] = metadata

        # Add timestamp
        data['last_updated'] = datetime.now().isoformat()

        # Save updated data
        with open(data_path, 'w') as f:
            json.dump(data, f)

        print(f"Updated {data_path} with player metadata")

    except Exception as e:
        print(f"Error updating data.json: {e}")
        # Save metadata separately if main file update fails
        pm.save_to_file()

if __name__ == "__main__":
    # Run metadata update
    update_main_data_with_metadata()