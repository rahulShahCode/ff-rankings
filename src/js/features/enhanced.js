// Enhanced Rankings JavaScript with all improvements

// Mock player data for enhanced features (will be replaced with real API data)
const playerMetadata = {
    injuries: {}, // Will store injury status
    byeWeeks: {}, // Will store bye week info
    teams: {}, // Will store team abbreviations
    trends: {}, // Will store ranking trends
    stats: {}, // Will store recent stats
    matchups: {} // Will store matchup difficulty
};

// Global state management
const state = {
    currentFilter: 'all',
    currentPosition: 'QB',
    currentLeague: 'home',
    rankingsSource: 'boris',
    availableCount: 0,
    rosteredCount: 0,
    swipeStartX: 0,
    swipeEndX: 0,
    isComparisonMode: false,
    cachedData: null,
    cacheTimestamp: null
};

// Export state to window so rankings.js can access it
window.state = state;

// Position order for swipe navigation
const positionOrder = ['QB', 'RB', 'WR', 'TE', 'FLX', 'K', 'DEF'];

// Compact player display
function createCompactPlayer(playerName, isRostered, isAvailable) {
    const playerData = playerMetadata[playerName] || {};

    // Simple inline display
    let playerHTML = '';

    // Player name with appropriate class
    if (isRostered) {
        playerHTML = `<span class="rostered">${playerName}`;
    } else if (isAvailable) {
        playerHTML = `<span class="available">${playerName}`;
    } else {
        playerHTML = `<span class="player-name">${playerName}`;
    }

    // Add inline indicators
    if (playerData.team) {
        playerHTML += ` <span class="player-team">${playerData.team}</span>`;
    }

    if (playerData.injury) {
        const injuryClass = playerData.injury === 'OUT' ? 'injury-out' :
                           playerData.injury === 'Q' ? 'injury-questionable' : 'injury-probable';
        playerHTML += ` <span class="injury-indicator ${injuryClass}"></span>`;
    }

    if (playerData.trend) {
        const trendIcon = playerData.trend === 'up' ? '↑' :
                         playerData.trend === 'down' ? '↓' : '';
        if (trendIcon) {
            const trendClass = playerData.trend === 'up' ? 'trend-up' : 'trend-down';
            playerHTML += ` <span class="player-trend ${trendClass}">${trendIcon}</span>`;
        }
    }

    playerHTML += '</span>';
    return playerHTML;
}

// Keep the original for backward compatibility
const createEnhancedPlayerCard = createCompactPlayer;

// Create hover card for player details
function createHoverCard(playerName, playerData) {
    return `
        <div class="player-hover-card">
            <div class="hover-card-header">
                <span class="hover-card-name">${playerName}</span>
                <span class="hover-card-position">${state.currentPosition}</span>
            </div>
            <div class="hover-card-stats">
                <div class="stat-item">
                    <span class="stat-label">Last 3 Games</span>
                    <span class="stat-value">${playerData.recentPoints || 'N/A'}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Season Avg</span>
                    <span class="stat-value">${playerData.seasonAvg || 'N/A'}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Ownership</span>
                    <span class="stat-value">${playerData.ownership || 'N/A'}%</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Rank Change</span>
                    <span class="stat-value">${playerData.rankChange || '—'}</span>
                </div>
            </div>
            <div class="matchup-difficulty ${getMatchupClass(playerData.matchup)}">
                <i class="fas fa-shield-alt"></i>
                Next: ${playerData.nextOpponent || 'TBD'} (${playerData.matchup || 'Medium'})
            </div>
        </div>
    `;
}

// Get matchup difficulty class
function getMatchupClass(difficulty) {
    if (difficulty === 'Easy') return 'matchup-easy';
    if (difficulty === 'Hard') return 'matchup-hard';
    return 'matchup-medium';
}

// Enhanced data loading with player metadata
function loadDataEnhanced(json) {
    // Store in cache
    state.cachedData = json;
    state.cacheTimestamp = Date.now();

    // Save to localStorage for offline access
    try {
        localStorage.setItem('ffRankingsData', JSON.stringify(json));
        localStorage.setItem('ffRankingsTimestamp', state.cacheTimestamp);
    } catch (e) {
        console.warn('Failed to cache data:', e);
    }

    // Load mock metadata (replace with real API calls)
    loadPlayerMetadata();

    // Count available and rostered players
    updatePlayerCounts(json);

    // Load data with enhanced formatting
    loadDataWithEnhancements(json);

    // Show filter controls
    document.getElementById('filterControls').style.display = 'flex';

    // Initialize swipe navigation
    initializeSwipeNavigation();
}

// Load player metadata (mock data for now)
function loadPlayerMetadata() {
    // This would be replaced with actual API calls
    // For demonstration, adding some mock data
    playerMetadata.injuries = {
        'Justin Herbert': 'Q',
        'Tua Tagovailoa': 'OUT'
    };

    playerMetadata.teams = {
        'Lamar Jackson': 'BAL',
        'Josh Allen': 'BUF',
        'Jalen Hurts': 'PHI',
        'Justin Herbert': 'LAC',
        'Patrick Mahomes': 'KC'
    };

    playerMetadata.trends = {
        'Lamar Jackson': 'up',
        'Dak Prescott': 'down',
        'Jordan Love': 'up'
    };

    playerMetadata.matchups = {
        'Lamar Jackson': 'Easy',
        'Josh Allen': 'Hard',
        'Patrick Mahomes': 'Medium'
    };
}

// Update player counts for filter badges
function updatePlayerCounts(json) {
    // Get current league from radio buttons
    const checkedVal = document.querySelector('input[name="league"]:checked');
    const league = checkedVal ? checkedVal.value.slice(0, -7) : 'home';
    state.currentLeague = league;

    if (json && json[league]) {
        state.availableCount = json[league].available ? json[league].available.length : 0;
        state.rosteredCount = json[league].rostered ? json[league].rostered.length : 0;

        const availCount = document.getElementById('availableCount');
        const rostCount = document.getElementById('rosteredCount');

        if (availCount) availCount.textContent = state.availableCount;
        if (rostCount) rostCount.textContent = state.rosteredCount;
    }
}

// Export function to global scope for access from rankings.js
window.updateFilterCounts = function() {
    if (state.cachedData) {
        updatePlayerCounts(state.cachedData);
    }
};

// Load data with enhanced formatting
function loadDataWithEnhancements(json) {
    // Use the source-aware loader with current source (defaults to 'boris')
    loadDataWithSource(json, state.rankingsSource);
}

// Render tiered positions with compact layout
function renderTieredPosition(json, leagueName, pos) {
    let html = `<div class='position-content ${leagueName}' id='${pos}' style='display:${pos === state.currentPosition ? 'block' : 'none'}'>`;

    let tierCount = 0;
    for (let tier in json['rankings'][pos]) {
        tierCount++;
        let tierPlayers = [];

        for (let player of json['rankings'][pos][tier]) {
            // Check with fuzzy name matching for suffixes
            const isRostered = json[leagueName]['rostered'].some(name => playerMatchesName(player, name));
            const isAvailable = json[leagueName]['available'].some(name => playerMatchesName(player, name));

            // Apply filter
            if (!shouldShowPlayer(isRostered, isAvailable)) continue;

            tierPlayers.push(createCompactPlayer(player, isRostered, isAvailable));
        }

        if (tierPlayers.length > 0) {
            html += `<p data-tier="${tier}" class="tier tier-${tierCount}">
                ${tierPlayers.join(' ')}
            </p>`;
        }
    }

    html += '</div>';
    return html;
}

// Render list positions (K, DEF) with compact display
function renderListPosition(json, leagueName, pos) {
    let html = `<ol class='position-content ${leagueName}' id='${pos}' style='display:${pos === state.currentPosition ? 'block' : 'none'}'>`;

    for (let player of json['rankings'][pos]) {
        // Check with fuzzy name matching for suffixes
        const isRostered = json[leagueName]['rostered'].some(name => playerMatchesName(player, name));
        const isAvailable = json[leagueName]['available'].some(name => playerMatchesName(player, name));

        if (!shouldShowPlayer(isRostered, isAvailable)) continue;

        html += `<li>${createCompactPlayer(player, isRostered, isAvailable)}</li>`;
    }

    html += '</ol>';
    return html;
}

// Filter logic
function shouldShowPlayer(isRostered, isAvailable) {
    switch (state.currentFilter) {
        case 'available':
            return isAvailable;
        case 'rostered':
            return isRostered;
        case 'top-available':
            return isAvailable; // Would add additional logic for "top"
        default:
            return true;
    }
}

// Apply filter
function applyFilter(filterType) {
    state.currentFilter = filterType;

    // Update button states
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.filter === filterType) {
            btn.classList.add('active');
        }
    });

    // Reload data with filter
    if (state.cachedData) {
        document.getElementById('content').innerHTML = '';
        loadDataWithEnhancements(state.cachedData);
    }
}

// Toggle comparison view
function toggleComparison() {
    state.isComparisonMode = !state.isComparisonMode;

    const comparisonView = document.getElementById('comparisonView');
    const contentView = document.getElementById('content');

    if (state.isComparisonMode) {
        comparisonView.style.display = 'flex';
        contentView.style.display = 'none';
        loadComparisonView();
    } else {
        comparisonView.style.display = 'none';
        contentView.style.display = 'block';
    }
}

// Load comparison view
function loadComparisonView() {
    if (!state.cachedData) return;

    const leagues = ['mfl', 'home'];
    leagues.forEach(league => {
        const column = document.querySelector(`#${league === 'mfl' ? 'league1' : 'league2'} .comparison-content`);
        let html = '';

        // Show top available players
        const available = state.cachedData[league].available || [];
        html += '<h4>Top Available</h4><ul>';
        available.slice(0, 10).forEach(player => {
            html += `<li>${player}</li>`;
        });
        html += '</ul>';

        column.innerHTML = html;
    });
}

// Initialize swipe navigation for mobile
function initializeSwipeNavigation() {
    const container = document.querySelector('.swipe-container');
    if (!container) return;

    let touchStartX = 0;
    let touchEndX = 0;

    container.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    });

    container.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            const currentIndex = positionOrder.indexOf(state.currentPosition);

            if (diff > 0 && currentIndex < positionOrder.length - 1) {
                // Swipe left - next position
                navigateToPosition(positionOrder[currentIndex + 1]);
            } else if (diff < 0 && currentIndex > 0) {
                // Swipe right - previous position
                navigateToPosition(positionOrder[currentIndex - 1]);
            }
        }
    }
}

// Navigate to position
function navigateToPosition(position) {
    state.currentPosition = position;

    // Update button states
    document.querySelectorAll('.position-btn').forEach(btn => {
        btn.classList.remove('selected');
        if (btn.dataset.position === position) {
            btn.classList.add('selected');
            openPosition(position, btn);
        }
    });
}

// Performance optimization: Implement lazy loading
function implementLazyLoading() {
    const observerOptions = {
        root: null,
        rootMargin: '50px',
        threshold: 0.01
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Load content when it comes into view
                entry.target.classList.add('loaded');
            }
        });
    }, observerOptions);

    // Observe all player cards
    document.querySelectorAll('.player-card').forEach(card => {
        observer.observe(card);
    });
}

// Cache management
function loadFromCache() {
    try {
        const cachedData = localStorage.getItem('ffRankingsData');
        const cacheTimestamp = localStorage.getItem('ffRankingsTimestamp');

        if (cachedData && cacheTimestamp) {
            const age = Date.now() - parseInt(cacheTimestamp);
            const maxAge = 5 * 60 * 1000; // 5 minutes

            if (age < maxAge) {
                return JSON.parse(cachedData);
            }
        }
    } catch (e) {
        console.warn('Failed to load from cache:', e);
    }
    return null;
}

// Enhanced window.onload with caching and error handling
window.onload = (event) => {
    initDarkMode();
    showLoading();

    // Add event listeners for league switching
    document.querySelectorAll('input[name="league"]').forEach(radio => {
        radio.addEventListener('change', () => {
            if (state.cachedData) {
                updatePlayerCounts(state.cachedData);

                // Update the current filter if active
                if (state.currentFilter !== 'all') {
                    applyFilter(state.currentFilter);
                }
            }
        });
    });

    // Skip localStorage cache - always fetch fresh data to avoid stale PFF rankings
    // const cachedData = loadFromCache();
    // if (cachedData) {
    //     console.log('Loading from cache...');
    //     loadDataEnhanced(cachedData);
    //     hideLoading();
    //     implementLazyLoading();
    //     return;
    // }

    // Fetch fresh data with retry logic (cache-busting with timestamp)
    const cacheBuster = `?t=${Date.now()}`;
    fetchWithRetry(`data.json${cacheBuster}`, 3)
        .then(response => response.json())
        .then(json => {
            loadDataEnhanced(json);
            hideLoading();
            implementLazyLoading();
        })
        .catch(error => {
            console.error('Error loading data:', error);
            hideLoading();
            showErrorMessage();
        });
};

// Fetch with retry logic
async function fetchWithRetry(url, retries) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(url);
            if (response.ok) return response;
        } catch (error) {
            if (i === retries - 1) throw error;
            await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
        }
    }
}

// Show error message
function showErrorMessage() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="error-message">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Unable to Load Rankings</h3>
            <p>Please check your connection and try again.</p>
            <button onclick="location.reload()" class="filter-btn">
                <i class="fas fa-redo"></i> Retry
            </button>
        </div>
    `;
}

// Export functionality
function exportToCSV() {
    if (!state.cachedData) return;

    let csv = 'Position,Tier,Player,Status\n';
    const league = state.currentLeague;

    for (let pos in state.cachedData.rankings) {
        for (let tier in state.cachedData.rankings[pos]) {
            for (let player of state.cachedData.rankings[pos][tier]) {
                const status = state.cachedData[league].rostered.includes(player) ? 'Rostered' :
                             state.cachedData[league].available.includes(player) ? 'Available' : 'Taken';
                csv += `${pos},${tier},${player},${status}\n`;
            }
        }
    }

    // Download CSV
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ff-rankings.csv';
    a.click();
}

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    const currentIndex = positionOrder.indexOf(state.currentPosition);

    if (e.key === 'ArrowLeft' && currentIndex > 0) {
        navigateToPosition(positionOrder[currentIndex - 1]);
    } else if (e.key === 'ArrowRight' && currentIndex < positionOrder.length - 1) {
        navigateToPosition(positionOrder[currentIndex + 1]);
    }
});

// Select rankings source (Boris Chen or PFF)
function selectRankingsSource(source, button) {
    console.log(`Switching to ${source} rankings`);
    console.log(`Current position: ${state.currentPosition}`);
    state.rankingsSource = source;

    // Update button states
    document.querySelectorAll('.source-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    button.classList.add('active');

    // Reload data with new source
    if (state.cachedData) {
        console.log(`Loading ${source} data for position ${state.currentPosition}...`);
        console.log('PFF data available:', !!state.cachedData.pff);
        console.log('PFF QB count:', state.cachedData.pff?.rankings?.QB?.length || 0);
        document.getElementById('content').innerHTML = '';
        loadDataWithSource(state.cachedData, source);
    }
}

// Load data with selected source
function loadDataWithSource(json, source) {
    let html = '';
    const leagues = ['home', 'mfl'];

    for (let leagueName of leagues) {
        if (Object.keys(json[leagueName]).length === 0) continue;

        html += `<div id='${leagueName}' class='league-content' style='display:${leagueName === state.currentLeague ? 'block' : 'none'}'>`;

        if (source === 'pff') {
            // Render PFF data
            html += renderPFFData(json, leagueName);
        } else {
            // Render Boris Chen data (default)
            for (let pos in json['rankings']) {
                if (pos !== 'K' && pos !== 'DEF') {
                    html += renderTieredPosition(json, leagueName, pos);
                } else {
                    html += renderListPosition(json, leagueName, pos);
                }
            }
        }

        html += '</div>';
    }

    document.getElementById('content').innerHTML += html;
}

// Render PFF data
function renderPFFData(json, leagueName) {
    let html = '';

    if (!json.pff || !json.pff.rankings) {
        console.error('PFF rankings not available in data');
        html += `<div class="error-message"><p>PFF rankings not available</p></div>`;
        return html;
    }

    const pffRankings = json.pff.rankings;
    console.log('Rendering PFF data for league:', leagueName);
    console.log('PFF positions available:', Object.keys(pffRankings));

    // Position mapping (PFF uses 'D' for defense)
    const positionMap = {
        'QB': 'QB',
        'RB': 'RB',
        'WR': 'WR',
        'TE': 'TE',
        'K': 'K',
        'DEF': 'D',  // Map DEF to D for PFF API
        'FLX': 'FLX' // Will combine RB, WR, TE
    };

    for (let pos of ['QB', 'RB', 'WR', 'TE', 'FLX', 'K', 'DEF']) {
        let posData = [];

        if (pos === 'FLX') {
            // Combine RB, WR, TE for FLX
            posData = [
                ...(pffRankings['RB'] || []),
                ...(pffRankings['WR'] || []),
                ...(pffRankings['TE'] || [])
            ].sort((a, b) => (a.rank || 999) - (b.rank || 999));
        } else {
            const pffPos = positionMap[pos];
            posData = pffRankings[pffPos] || [];
        }

        // All PFF positions use numbered list format
        html += renderPFFListPosition(posData, leagueName, pos, json);
    }

    return html;
}

// Render PFF tiered positions (using position rank groups instead of tiers for weekly rankings)
function renderPFFTieredPosition(players, leagueName, pos, json) {
    let html = `<div class='position-content pff-content ${leagueName}' id='${pos}' style='display:${pos === state.currentPosition ? 'block' : 'none'}'>`;

    // Group by position rank (top 10, 11-20, 21-30, etc.) to simulate tiers
    const tierSize = 10;
    const tierGroups = {};

    players.forEach(player => {
        const posRank = player.positionRank || 999;
        const tier = Math.ceil(posRank / tierSize);
        if (!tierGroups[tier]) tierGroups[tier] = [];
        tierGroups[tier].push(player);
    });

    for (let tier in tierGroups) {
        let tierPlayers = [];

        for (let player of tierGroups[tier]) {
            const playerName = player.name;
            // Check with fuzzy name matching for suffixes
            const isRostered = json[leagueName]['rostered'].some(name => playerMatchesName(playerName, name));
            const isAvailable = json[leagueName]['available'].some(name => playerMatchesName(playerName, name));

            if (!shouldShowPlayer(isRostered, isAvailable)) continue;

            tierPlayers.push(createPFFPlayerDisplay(player, isRostered, isAvailable));
        }

        if (tierPlayers.length > 0) {
            html += `<p data-tier="${tier}" class="tier tier-${tier}">
                ${tierPlayers.join(' ')}
            </p>`;
        }
    }

    html += '</div>';
    return html;
}

// Render PFF list positions
function renderPFFListPosition(players, leagueName, pos, json) {
    let html = `<ol class='position-content pff-content ${leagueName}' id='${pos}' style='display:${pos === state.currentPosition ? 'block' : 'none'}'>`;

    for (let player of players) {
        const playerName = player.name;
        // Check with fuzzy name matching for suffixes
        const isRostered = json[leagueName]['rostered'].some(name => playerMatchesName(playerName, name));
        const isAvailable = json[leagueName]['available'].some(name => playerMatchesName(playerName, name));

        if (!shouldShowPlayer(isRostered, isAvailable)) continue;

        html += `<li>${createPFFPlayerDisplay(player, isRostered, isAvailable)}</li>`;
    }

    html += '</ol>';
    return html;
}

// Normalize player name for matching (remove suffixes)
function normalizePlayerName(name) {
    // Remove common suffixes for matching purposes
    return name.replace(/\s+(Jr\.|Sr\.|II|III|IV|V)\.?$/i, '').trim();
}

// Check if player matches roster/available (with fuzzy name matching)
function playerMatchesName(playerName, rosterName) {
    // Exact match first
    if (playerName === rosterName) return true;

    // Try normalized match (without suffixes)
    return normalizePlayerName(playerName) === normalizePlayerName(rosterName);
}

// Create PFF player display with additional info
function createPFFPlayerDisplay(player, isRostered, isAvailable) {
    let className = 'player-name';
    if (isRostered) className = 'rostered';
    if (isAvailable) className = 'available';

    let html = `<span class="${className}" title="${getPFFPlayerTooltip(player)}">`;
    html += player.name;

    // Add team abbreviation
    if (player.team) {
        html += ` <span class="player-team">${player.team}</span>`;
    }

    // Add rank badge
    if (player.positionRank) {
        html += ` <span class="rank-badge">#${player.positionRank}</span>`;
    }

    // Add tags if available
    if (player.tags && player.tags.length > 0) {
        player.tags.forEach(tag => {
            html += ` <span class="player-tag tag-${tag}">${tag}</span>`;
        });
    }

    html += '</span>';
    return html;
}

// Get tooltip text for PFF player
function getPFFPlayerTooltip(player) {
    let tooltip = `${player.name} - ${player.position}`;

    if (player.team) tooltip += ` (${player.team})`;
    if (player.rank) tooltip += `\nOverall Rank: ${player.rank}`;
    if (player.adp) tooltip += `\nADP: ${player.adp}`;
    if (player.byeWeek) tooltip += `\nBye: Week ${player.byeWeek}`;
    if (player.projection && player.projection.points) {
        tooltip += `\nProjection: ${player.projection.points.mid || 'N/A'} pts`;
    }

    return tooltip;
}

// Make function globally available
window.selectRankingsSource = selectRankingsSource;

console.log('Enhanced Rankings loaded successfully!');