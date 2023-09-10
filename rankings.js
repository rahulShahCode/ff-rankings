function getCheckedVal() {
    let values = document.getElementsByName('league')
    for (let x of values) {
        if (x.checked)
            return x 
    }
}
function updateSelectedButton(button) {
    let currSelected = document.querySelector('.selected')
    if (currSelected !== null) 
        currSelected.classList.remove('selected');
    button.classList.add('selected')
}
function openPosition(pos, button) {
    let checkedVal = getCheckedVal();
    updateSelectedButton(button)
    let leagues = $('#content > div');
    let currLeague = '#content > #'
    for (let x of leagues) {
        if (x.id !== checkedVal.value.slice(0,-7)) {
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
        if (x.id !== checkedVal.value.slice(0,-7)) {
            x.style = 'display:none'
        } else {
            x.style = 'display:flex'
            currLeague = currLeague.concat(x.id);
        }
    }
    openPosition($('.selected').text(), $('.selected')[0])
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
                    if (json[leagueName]['rostered'].includes(json['rankings'][pos][tier][player])) {
                        tier_str = tier_str.concat("<span class='rostered'>",json['rankings'][pos][tier][player] , "</span>")
                    } 
                    else if (json[leagueName]['available'].includes(json['rankings'][pos][tier][player])) {
                        tier_str = tier_str.concat("<span class='available'>",json['rankings'][pos][tier][player] , "</span>")
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
            html = html.concat(pos_str);
        } else {
            var list_str = `<ol class ='${leagueName}' id='${pos}' style='display:none'>`
            for (player in json['rankings'][pos]) {
                if (json[leagueName]['rostered'].includes(json['rankings'][pos][player])) {
                    list_str = list_str.concat("<li class='rostered'>", json['rankings'][pos][player], "</li>");
                }
                else if (json[leagueName]['available'].includes(json['rankings'][pos][player])) {
                    list_str = list_str.concat("<li class='available'>", json['rankings'][pos][player], "</li>");
                } 
                else {
                    list_str = list_str.concat("<li>", json['rankings'][pos][player], "</li>");
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

window.onload = (event) => {
    fetch("data.json")
    .then(response => response.json())
    .then(json => loadData(json))
};