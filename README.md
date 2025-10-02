# Fantasy Football Rankings

A web-based fantasy football rankings dashboard that aggregates data from multiple sources including Boris Chen tier-based rankings and PFF weekly rankings.

## Features

- **Dual Rankings Sources**
  - **Boris Chen**: Tier-based consensus rankings from expert aggregation
  - **PFF (Pro Football Focus)**: Weekly rankings with projections and matchup analysis

- **League Integration**
  - MyFantasyLeague (MFL) roster tracking
  - Sleeper league support
  - Automatic player availability highlighting

- **Enhanced UI**
  - Dark mode support
  - Mobile-responsive design
  - Swipe navigation between positions
  - Filter by available/rostered players
  - Player metadata (injuries, bye weeks, matchups)

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ff-rankings
   ```

2. **Configure secrets**
   ```bash
   cp secrets.json.example secrets.json
   ```

   Edit `secrets.json` and add your API credentials:
   - Yahoo Fantasy API credentials (for Boris Chen data)
   - PFF API key (for weekly rankings)

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Update league IDs**
   - Edit `src/py/constants.py` - Set your MFL `league_id` and `team_id`
   - Edit `src/py/api/sleeper.py` - Set your Sleeper `home_league_id` and `home_team_id`

## Usage

### Generate Rankings Data

Run the main script to fetch latest rankings:

```bash
cd src/py
python main.py
```

This generates `data.json` with:
- Boris Chen tier-based rankings
- PFF weekly rankings
- Your league rosters (MFL and Sleeper)
- Player metadata

### View Rankings

Open `index.html` in your web browser.

**Switch between sources:**
- Click **"Boris Chen"** for tier-based season-long rankings
- Click **"PFF"** for weekly matchup-based rankings

**Toggle leagues:**
- Switch between MFL and HOME (Sleeper) leagues

**Filter players:**
- All Players
- Available Only
- My Roster
- Top Available

## Project Structure

```
ff-rankings/
├── index.html              # Main web interface
├── requirements.txt        # Python dependencies
├── secrets.json            # API keys (gitignored)
├── secrets.json.example    # Template for API configuration
├── data.json               # Generated rankings data (gitignored)
└── src/
    ├── css/
    │   └── style-compact.css   # Responsive app styling with dark mode
    ├── js/
    │   ├── core/
    │   │   └── rankings.js     # Core UI functions (position switching, league toggle)
    │   └── features/
    │       └── enhanced.js     # Enhanced features + PFF integration
    └── py/
        ├── __init__.py
        ├── config.py           # Centralized secret/API key loading
        ├── constants.py        # Configuration constants and URLs
        ├── main.py             # Main data generation script
        ├── api/                # External API integrations
        │   ├── __init__.py
        │   ├── boris.py        # Boris Chen tier-based rankings fetcher
        │   ├── pff.py          # PFF weekly rankings API integration
        │   ├── mfl.py          # MyFantasyLeague API integration
        │   └── sleeper.py      # Sleeper league API integration
        └── utils/              # Utility modules
            ├── __init__.py
            ├── rankings.py     # Subvertadown K/DEF rankings
            └── player_metadata.py # Player metadata aggregation
```

### File Purposes

- **src/js/core/rankings.js**: Base functionality - position navigation, league switching, dark mode
- **src/js/features/enhanced.js**: Advanced features - PFF integration, fuzzy name matching, filters, swipe navigation
- **Both JavaScript files are required** - enhanced.js extends rankings.js functionality
- **src/py/config.py**: Centralized secret loading from secrets.json
- **src/py/constants.py**: All configuration values and API URLs

## Data Sources

- **Boris Chen**: https://www.borischen.co/ (Tier-based expert consensus)
- **PFF**: https://www.pff.com/ (Weekly rankings and projections)
- **Subvertadown**: K/DEF rankings
- **MyFantasyLeague**: League roster data
- **Sleeper**: League roster data

## Notes

- Rankings are cached in `data.json` - regenerate weekly for latest data
- PFF rankings are matchup-specific (update weekly)
- Boris Chen tiers update multiple times per week during season
- The PFF API key in the code is a public key from their website

## License

MIT
