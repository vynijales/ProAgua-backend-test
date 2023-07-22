const backdrop = document.getElementById('dialog-backdrop');
var currentDialog = '';

function closeDialog(element_id) {
    var el = document.getElementById(element_id)
    if (el !== null) {
        el.hidden = true;
        currentDialog = element_id;
    }
    backdrop.hidden = true;
}

function openDialog(element_id) {
    document.getElementById(element_id).hidden = false;
    backdrop.hidden = false;
    currentDialog = '';
}

backdrop.addEventListener('click', (e) => {
    if (e.target === backdrop) {
        closeDialog(currentDialog);
    }
})
