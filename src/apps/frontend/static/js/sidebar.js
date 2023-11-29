function openNav() {
    document.getElementById('sidebar').style.width = '15em';
}

function closeNav() {
    document.getElementById('sidebar').style.width = '0';
}

function change_modal_state(element) {
    var parentCard = element.parentNode;
    var modalDisplay = parentCard.querySelector(".modal").style.zIndex;

    parentCard.querySelector(".modal").style.zIndex = modalDisplay === "1" ? "-1" : "1";
}