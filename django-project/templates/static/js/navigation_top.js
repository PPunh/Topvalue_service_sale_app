
function w3_open() {
document.getElementById("mySidebar").style.display = "block";
}

function w3_close() {
document.getElementById("mySidebar").style.display = "none";
}

function toggleDropdown(id) {
const el = document.getElementById(id);
el.classList.toggle("w3-show");
el.classList.toggle("w3-hide");
}