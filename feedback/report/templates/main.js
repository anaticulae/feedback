selected = null

function show(id) {
    if (selected != null) {
        // hide open element
        document.getElementById(selected).classList.add('hidden')
        // remove selection
        document.getElementById("selected_" + selected).classList.remove("highlighted")
        document.getElementById("selected_" + selected).classList.add("linter_list")
    }
    var span = document.getElementById(id);
    span.classList.remove("hidden")

    document.getElementById("selected_" + id).classList.add("highlighted")
    document.getElementById("selected_" + id).classList.remove("linter_list")
    selected = id
}

function next(min_element, max_element) {
    next_id = selected + 1
    if (next_id < max_element) {
        show(next_id)
    } else {
        // start with first element
        show(min_element)
    }
}

function previous(min_element, max_element) {
    next_id = selected - 1
    if (next_id >= min_element) {
        show(next_id)
    } else {
        // go to last element
        show(max_element - 1)
    }
}

function loaded() {
    show(0)
}
