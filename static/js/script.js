// Sidebar functionality
const body = document.querySelector("body");
const sidebar = body.querySelector(".sidebar");
const toggle = body.querySelector(".bx.bx-chevron-left.toggle");

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});
