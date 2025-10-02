"""
Constants and configuration values for FF Rankings
"""

# League IDs (configure these for your leagues)
MFL_LEAGUE_ID = 62247
MFL_TEAM_ID = '0011'

# Sleeper league IDs will be loaded from sleeper.py
# They are defined there to keep league-specific code together

# Position order for display
POSITIONS = ['QB', 'RB', 'WR', 'TE', 'FLX', 'K', 'DEF']

# Data source URLs
BORIS_CHEN_URL = "https://s3-us-west-1.amazonaws.com/fftiers/out/text_{}.txt"
PFF_WEEKLY_API = "https://consumer-api.pff.com/football/v1/fantasy/weekly-rankings"
SUBVERTADOWN_URL = "https://subvertadown.com/weekly/{}"
MFL_API_URL = "https://api.myfantasyleague.com/2025/export"
SLEEPER_API_BASE = "https://api.sleeper.app/v1"

# PFF API configuration
PFF_POSITIONS = ['QB', 'RB', 'WR', 'TE', 'K', 'D']  # D for defense in weekly rankings
PFF_SCORING_TYPES = ['ppr', 'standard', 'half_ppr']

# Subvertadown configuration
SUBVERTADOWN_POSITIONS = ['kicker', 'defense']
SUBVERTADOWN_PARAMS = {
    'sort': 'current_week_projection',
    'sort_direction': 'desc',
    'platform': 'yahoo'
}

# HTTP headers
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
