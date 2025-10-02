function getCheckedVal() {
    let values = document.getElementsByName('league')
    for (let x of values) {
        if (x.checked)
            return x 
    }
}
function updateSelectedButton(button) {
    // Remove selected class from all position buttons
    document.querySelectorAll('.position-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    // Add selected class to clicked button
    button.classList.add('selected');
}
function openPosition(pos, button) {
    let checkedVal = getCheckedVal();
    updateSelectedButton(button);

    // Update state to track current position
    if (window.state) {
        window.state.currentPosition = pos;
    }

    // Get the current league name
    let leagueName = checkedVal.value.slice(0, -7); // 'home' or 'mfl'

    // Hide all leagues except the current one
    let leagues = $('#content > div');
    for (let x of leagues) {
        if (x.id !== leagueName) {
            x.style.display = 'none';
        } else {
            x.style.display = 'block';
        }
    }

    // Hide all positions within the current league
    let allPositions = $(`#${leagueName} > div, #${leagueName} > ol`);
    allPositions.hide();

    // Show only the selected position
    $(`#${leagueName} #${pos}`).show();

    // Update filter controls if they exist
    if (window.updateFilterCounts) {
        window.updateFilterCounts();
    }
}
function openLeague() {
    let checkedVal = getCheckedVal();
    let leagueName = checkedVal.value.slice(0, -7); // 'home' or 'mfl'
    let leagues = $('#content > div');

    // Hide all league content first
    for (let x of leagues) {
        if (x.id !== leagueName) {
            x.style.display = 'none';
        } else {
            x.style.display = 'block';
        }
    }

    // Get the currently selected position button
    let selectedBtn = document.querySelector('.position-btn.selected') || document.querySelector('.bar-item.selected');
    if (selectedBtn) {
        let position = selectedBtn.textContent.trim() || selectedBtn.dataset.position || 'QB';

        // Hide all positions within the active league
        let allPositions = $(`#${leagueName} > div, #${leagueName} > ol`);
        allPositions.hide();

        // Show the selected position within the active league
        $(`#${leagueName} #${position}`).show();
    }
}
function loadDataHelper(json,leagueName) {
    let html = `<div id='${leagueName}' class='league-content' `
    if (leagueName !== 'home') {
        html = html.concat("style='display:none'")
    }
    html = html.concat('>');
    for (let pos in json['rankings']) {
        if(pos !== 'K' && pos !== 'DEF') {
            var pos_str = `<div class='position-content ${leagueName}' id='${pos}' `
            if (pos !== 'QB')
                pos_str = pos_str.concat("style='display:none'");
            pos_str = pos_str.concat(">")
            for (let tier in json['rankings'][pos]) {
                var tier_str = `<p data-tier="${tier}">`
                for (player in json['rankings'][pos][tier]) {
                    const playerName = json['rankings'][pos][tier][player];
                    if (json[leagueName]['rostered'].includes(playerName)) {
                        tier_str = tier_str.concat("<span class='rostered'>", playerName, "</span>")
                    }
                    else if (json[leagueName]['available'].includes(playerName)) {
                        tier_str = tier_str.concat("<span class='available'>", playerName, "</span>")
                    } else {
                        tier_str = tier_str.concat("<span class='player-name'>", playerName, "</span>")
                    }

                    if(player < json['rankings'][pos][tier].length - 1) {
                        tier_str = tier_str.concat(' ');
                    }
                }
                tier_str = tier_str.concat('</p>');
                pos_str = pos_str.concat(tier_str);
            }
            pos_str = pos_str.concat('</div>')
            html = html.concat(pos_str);
        } else {
            var list_str = `<ol class='position-content ${leagueName}' id='${pos}' style='display:none'>`
            for (player in json['rankings'][pos]) {
                if (json[leagueName]['rostered'].includes(json['rankings'][pos][player])) {
                    list_str = list_str.concat("<li><span class='rostered'>", json['rankings'][pos][player], "</span></li>");
                }
                else if (json[leagueName]['available'].includes(json['rankings'][pos][player])) {
                    list_str = list_str.concat("<li><span class='available'>", json['rankings'][pos][player], "</span></li>");
                } 
                else {
                    list_str = list_str.concat("<li>", json['rankings'][pos][player], "</span></li>");
                }
            }
            list_str = list_str.concat("</ol>");
            html = html.concat(list_str);
        }
    }
    html = html.concat('</div>')
    document.getElementById('content').innerHTML = document.getElementById('content').innerHTML.concat(html);
}

function loadData(json) {
    let leagues = ['home', 'mfl']
    for (i in leagues) {
        if (Object.keys(json[leagues[i]]).length !== 0) {
            loadDataHelper(json, leagues[i])   
        }
    }
}

// Store original onload for compatibility
const originalOnload = window.onload;

window.onload = (event) => {
    // Initialize dark mode based on saved preference
    initDarkMode();

    // Show loading spinner
    showLoading();

    // Fetch data with loading states
    fetch("data.json")
        .then(response => response.json())
        .then(json => {
            loadData(json);
            hideLoading();

            // Store data for enhanced features if available
            if (window.state) {
                window.state.cachedData = json;
            }

            // Add fade-in animation to content
            const contentElements = document.querySelectorAll('#content > div');
            contentElements.forEach(element => {
                addFadeInAnimation(element);
            });

            // Initialize enhanced features if available
            if (window.loadDataEnhanced) {
                // Show filter controls
                const filterControls = document.getElementById('filterControls');
                if (filterControls) filterControls.style.display = 'flex';

                // Update filter counts
                if (window.updateFilterCounts) {
                    window.updateFilterCounts();
                }
            }
        })
        .catch(error => {
            console.error('Error loading data:', error);
            hideLoading();

            // Show error message
            const content = document.getElementById('content');
            content.innerHTML = `
                <div style="text-align: center; color: var(--error); padding: 2rem;">
                    <h3>Error loading rankings</h3>
                    <p>Please try refreshing the page.</p>
                </div>
            `;
        });
};
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');

    // Save the user's preference in localStorage
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
    } else {
        localStorage.setItem('darkMode', 'disabled');
    }
}

// Check for saved dark mode preference
function initDarkMode() {
    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'enabled') {
        document.body.classList.add('dark-mode');
    }
}

function showLoading() {
    const loading = document.getElementById('loading');
    const content = document.getElementById('content');
    if (loading) loading.style.display = 'flex';
    if (content) content.style.display = 'none';
}

function hideLoading() {
    const loading = document.getElementById('loading');
    const content = document.getElementById('content');
    if (loading) loading.style.display = 'none';
    if (content) content.style.display = 'block';
}

function addFadeInAnimation(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(10px)';
    element.style.transition = 'all 0.5s ease';

    setTimeout(() => {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 50);
}
