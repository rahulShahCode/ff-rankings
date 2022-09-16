function openPosition(pos, button) {
    let tabContent = document.getElementsByClassName("position");
    for (let i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }
    let showContent = document.getElementById(pos);
    showContent.style.display = "block";
    let button_lst = document.getElementsByClassName("bar-item");
    for (let i = 0; i < button_lst.length; i++) {
        button_lst[i].classList.remove('selected')
    }
    button.classList.add('selected')
}
function handlePosition(pos, data, rostered) {
    let html = `<div class=position id=${pos}>`
    for (const tier in data.rankings) {
        let tier_str = `<p>${tier}: `
        data.rankings[tier].forEach(
            (player, index, array) => {
                if (data.available.includes(player)) {
                    tier_str = tier_str.concat("<span id='available'>", player,"</span>")
                } else if(rostered.includes(player)) {
                    tier_str = tier_str.concat("<span id='rostered'>", player, "</span>")
                } 
                else {
                    tier_str = tier_str.concat(player)
                }
                if (index === (array.length -1)) {
                    tier_str = tier_str.concat("</p>")
                } else {
                    tier_str = tier_str.concat(", ")
                }
            })
        html = html.concat(tier_str);
    }
    return html 
}

function updateHTML(json) {
    let divContent = document.getElementById('content')
    divContent.innerHTML = ""
    Object.keys(json.position).forEach(
        (key) => {
            divContent.innerHTML = divContent.innerHTML.concat(handlePosition(key,json.position[key], json.rostered))
        })
    document.getElementsByClassName('bar-item')[0].click()
}

window.onload = (event) => {
    fetch("data.json")
    .then(response => response.json())
    .then(json => updateHTML(json))
};