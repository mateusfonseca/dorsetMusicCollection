// CA1: CRUD Application

// This function displays or hides elements from a list depending on
// whether the element contains at least one of the search terms

function listSearch() {
    let filter, list, visible, hidden
    filter = document.getElementById('filter').value.toUpperCase()
    list = Array.from(document.getElementById("list-to-search").getElementsByTagName("li"))
    visible = list.filter(el => el.classList.contains("visible"))
    hidden = list.filter(el => el.classList.contains("hidden"))

    list.forEach(el => {
        if (filter.length === 0) {
            visible.forEach(el => {
                el.style.display = "initial"
            })
            hidden.forEach(el => {
                el.style.display = "none"
            })
        } else if (filter.split(" ").filter(term => term).every(term => el.getElementsByTagName("a")[0].textContent.toUpperCase().includes(term))) {
            el.style.display = "initial"
        } else {
            el.style.display = "none"
        }
    })
}
