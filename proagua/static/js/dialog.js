const backdrop = document.getElementById('dialog-backdrop')

function closeDialog(element_id) {
    document.getElementById(element_id).hidden = true;
    backdrop.hidden = true;
}

function openDialog(element_id) {
    document.getElementById(element_id).hidden = false;
    backdrop.hidden = false;
}
