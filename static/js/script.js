// Sidebar functionality
const body = document.querySelector('body');
const sidebar = body.querySelector('.sidebar');
const toggle = body.querySelector('.bx.bx-chevron-right.toggle');

toggle.addEventListener("click", () => {
  sidebar.classList.toggle('close');
});

// Modal functionality
var joinClassModal = document.getElementById('join-class-modal');
var addClassModal = document.getElementById('add-class-modal');
var joinClassBtn = document.getElementById('join-class-btn');
var addClassBtn = document.getElementById('add-class-btn');
var closeJoinClass = document.getElementById('close-join-class');
var closeAddClass = document.getElementById('close-add-class');

joinClassBtn.onclick = function() {
    joinClassModal.style.display = 'block';
}

addClassBtn.onclick = function() {
    addClassModal.style.display = 'block';
}

closeJoinClass.onclick = function() {
    joinClassModal.style.display = 'none';
}

closeAddClass.onclick = function() {
    addClassModal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == joinClassModal) {
        joinClassModal.style.display = 'none';
    }
    if (event.target == addClassModal) {
        addClassModal.style.display = 'none';
    }
}