// Sidebar functionality
const body = document.querySelector('body');
const sidebar = body.querySelector('.sidebar');
const toggle = body.querySelector('.bx.bx-chevron-left.toggle');

toggle.addEventListener("click", () => {
  sidebar.classList.toggle('close');
});

// Modal functionality
function setupModal(modalId, openBtnId, closeBtnId) {
  const modal = document.getElementById(modalId);
  const openBtn = document.getElementById(openBtnId);
  const closeBtn = document.getElementById(closeBtnId);

  if (openBtn) {
    openBtn.onclick = function() {
      modal.style.display = 'block';
    }
  }

  if (closeBtn) {
    closeBtn.onclick = function() {
      modal.style.display = 'none';
    }
  }

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = 'none';
    }
  }
}

// Setup modals for home.html
setupModal('join-class-modal', 'join-class-btn', 'close-join-class');
setupModal('add-class-modal', 'add-class-btn', 'close-add-class');
setupModal('delete-class-modal', null, 'close-delete-class');

// Setup modals for subjects.html
setupModal('add-subject-modal', 'add-subject-btn', 'close-add-subject');
setupModal('delete-subject-modal', null, 'close-delete-subject');
setupModal('leave-class-modal', 'leave-class-btn', 'close-leave-class');
setupModal('kick-user-modal', null, 'close-kick-user');

// Setup modals for lessons.html
setupModal('add-lesson-modal', 'add-lesson-btn', 'close-add-lesson');
setupModal('delete-lesson-modal', null, 'close-delete-lesson');

// Delete button functionality for home.html
document.querySelectorAll('.delete-icon').forEach(button => {
  button.addEventListener('click', function() {
    const classroomId = this.getAttribute('data-classroom-id');
    const deleteClassId = document.getElementById('delete-class-id');
    deleteClassId.value = classroomId;
    const deleteClassModal = document.getElementById('delete-class-modal');
    deleteClassModal.style.display = 'block';
  });
});

// Delete button functionality for subjects.html
document.querySelectorAll('.delete-icon').forEach(button => {
  button.addEventListener('click', function() {
    const subjectId = this.getAttribute('data-subject-id');
    const deleteSubjectId = document.getElementById('delete-subject-id');
    deleteSubjectId.value = subjectId;
    const deleteSubjectModal = document.getElementById('delete-subject-modal');
    deleteSubjectModal.style.display = 'block';
  });
});

// Delete button functionality for lessons.html
document.querySelectorAll('.delete-icon').forEach(button => {
    button.addEventListener('click', function() {
      const lessonId = this.getAttribute('data-lesson-id');
      const deleteLessonId = document.getElementById('delete-lesson-id');
      deleteLessonId.value = lessonId;
      const deleteLessonModal = document.getElementById('delete-lesson-modal');
      deleteLessonModal.style.display = 'block';
    });
  });

// Kick button functionality for subjects.html
document.querySelectorAll('.kick-btn').forEach(button => {
  button.addEventListener('click', function() {
    const userId = this.getAttribute('data-user-id');
    const kickUserId = document.getElementById('kick-user-id');
    kickUserId.value = userId;
    const kickUserModal = document.getElementById('kick-user-modal');
    kickUserModal.style.display = 'block';
  });
});