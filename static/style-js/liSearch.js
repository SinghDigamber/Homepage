function liSearch() {
    // Declare variables
    var filter, li, i;
    filter = document.getElementById('liSearchInput');
    filter = filter.value.toUpperCase();

    li = document.getElementById("liSearchUL");
    li = li.getElementsByTagName('li');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        if (li[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}