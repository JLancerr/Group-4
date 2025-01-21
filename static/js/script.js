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
var deleteClassModal = document.getElementById('delete-class-modal');
var joinClassBtn = document.getElementById('join-class-btn');
var addClassBtn = document.getElementById('add-class-btn');
var closeJoinClass = document.getElementById('close-join-class');
var closeAddClass = document.getElementById('close-add-class');
var closeDeleteClass = document.getElementById('close-delete-class');
var deleteClassForm = document.getElementById('delete-class-form');
var deleteClassId = document.getElementById('delete-class-id');

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

closeDeleteClass.onclick = function() {
    deleteClassModal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == joinClassModal) {
        joinClassModal.style.display = 'none';
    }
    if (event.target == addClassModal) {
        addClassModal.style.display = 'none';
    }
    if (event.target == deleteClassModal) {
        deleteClassModal.style.display = 'none';
    }
}

// Delete button functionality
document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function() {
        var classroomId = this.getAttribute('data-classroom-id');
        deleteClassId.value = classroomId;
        deleteClassModal.style.display = 'block';
    });
});