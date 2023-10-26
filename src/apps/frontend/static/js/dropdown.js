function setupDropdown() {
    let dropdowns = document.getElementsByClassName("dropdown")
    for (let i = 0; i < dropdowns.length; i++) {
        let dropdown = dropdowns[i];
        let button = dropdown.querySelector("#dropdown-bt")

        dropdown.classList.add('collapsed')
        button.onclick = () => {
            if (dropdown.classList.contains('collapsed')) {
                dropdown.classList.remove('collapsed')
            } else {
                dropdown.classList.add('collapsed')
            }
        }
    }
}

