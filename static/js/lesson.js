// Sidebar functionality
const body = document.querySelector("body");
const sidebar = body.querySelector(".sidebar");
const toggle = body.querySelector(".bx.bx-chevron-left.toggle");

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});

// Modal functionality
function setupModal(modalId, openBtnId, closeBtnId) {
  const modal = document.getElementById(modalId);
  const openBtn = document.getElementById(openBtnId);
  const closeBtn = document.getElementById(closeBtnId);

  if (openBtn) {
    openBtn.onclick = function () {
      modal.style.display = "block";
    };
  }

  if (closeBtn) {
    closeBtn.onclick = function () {
      modal.style.display = "none";
    };
  }

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };
}

// Setup modals for lessons.html
setupModal("add-lesson-modal", "add-lesson-btn", "close-add-lesson");
setupModal("delete-lesson-modal", null, "close-delete-lesson");
setupModal("rename-lesson-modal", null, "close-rename-lesson");

// Delete button functionality for lessons.html
document.querySelectorAll(".delete-icon").forEach((button) => {
    button.addEventListener("click", function () {
      const lessonId = this.getAttribute("data-lesson-id");
      const deleteLessonId = document.getElementById("delete-lesson-id");
      deleteLessonId.value = lessonId;
      const deleteLessonModal = document.getElementById("delete-lesson-modal");
      deleteLessonModal.style.display = "block";
    });
  });

// Edit button functionality for subjects.html
document.querySelectorAll(".edit-icon").forEach((button) => {
    button.addEventListener("click", function () {
        const subjectId = this.getAttribute("data-lesson-id");
        const renameSubjectId = document.getElementById("rename-lesson-id");
        renameSubjectId.value = subjectId;
        document.getElementById("rename-lesson-modal").style.display = "block";
    });
});