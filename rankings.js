function getCheckedVal() {
    let values = document.getElementsByName('league')
    for (let x of values) {
        if (x.checked)
            return x 
    }
}
function openPosition(pos, button) {
    let checkedVal = getCheckedVal();
    let leagues = $('#content > div');
    let currLeague = '#content > #'
    for (let x of leagues) {
        if (x.id !== checkedVal.value) {
            x.style = 'display:none'
        } else {
            x.style = 'display:flex'
            currLeague = currLeague.concat(x.id);
        }
    }
    currLeague = $(currLeague).children();
    for (let x of currLeague) {
        if (x.id === pos) {
            x.style['display'] = 'block';
            button.class
        } else {
            x.style['display'] = 'none';
        }
    }
}
function openLeague() {
    let checkedVal = getCheckedVal();
    let leagues = $('#content > div');
    let currLeague = '#content > #'
    for (let x of leagues) {
        if (x.id !== checkedVal.value) {
            x.style = 'display:none'
        } else {
            x.style = 'display:flex'
            currLeague = currLeague.concat(x.id);
        }
    }
}
function loadDataHelper(json,leagueName) {
    let html = `<div id='${leagueName}'`
    if (leagueName !== 'home') {
        html = html.concat("style='display:none'")
    } 
    html = html.concat('>');
    for (let pos in json['rankings']) {
        if(pos !== 'K' && pos !== 'DEF') {
            var pos_str = `<div class ='${leagueName}' id='${pos}'`
            if (pos !== 'QB') 
                pos_str = pos_str.concat("style='display:none'");
            pos_str = pos_str.concat(">")
            for (let tier in json['rankings'][pos]) {
                var tier_str = `<p>${tier}: `
                for (player in json['rankings'][pos][tier]) {
                    if (json[leagueName]['available'].includes(json['rankings'][pos][tier][player])) {
                        tier_str = tier_str.concat("<span id='available'>",json['rankings'][pos][tier][player] , "</span>")
                    } else if (json[leagueName]['rostered'].includes(json['rankings'][pos][tier][player])) {
                        tier_str = tier_str.concat("<span id='rostered'>",json['rankings'][pos][tier][player] , "</span>")
                    } else {
                        tier_str = tier_str.concat(json['rankings'][pos][tier][player])
                    } 
                    if(player === json['rankings'][pos][tier].length - 1) 
                        tier_str = tier_str.concat('</p>')
                    else 
                        tier_str = tier_str.concat(', ')
                }
                pos_str = pos_str.concat(tier_str);
            }
            pos_str = pos_str.concat('</div>')
        }
        if(pos_str !== undefined)
            html = html.concat(pos_str)
    }
    html = html.concat('</div>')
    document.getElementById('content').innerHTML = document.getElementById('content').innerHTML.concat(html);
}

function loadData(json) {
    let leagues = ["home", 'work', 'mfl']
    for (i in leagues) {
        if (Object.keys(json[leagues[i]]).length !== 0) {
            loadDataHelper(json, leagues[i])   
        }
    }
}

window.onload = (event) => {
    fetch("data.json")
    .then(response => response.json())
    .then(json => loadData(json))
};