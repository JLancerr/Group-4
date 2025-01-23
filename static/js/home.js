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

// Setup modals for home.html
setupModal("join-class-modal", "join-class-btn", "close-join-class");
setupModal("add-class-modal", "add-class-btn", "close-add-class");
setupModal("delete-class-modal", null, "close-delete-class");
setupModal("rename-class-modal", null, "close-rename-class");

// Delete button functionality for home.html
document.querySelectorAll(".delete-icon").forEach((button) => {
    button.addEventListener("click", function () {
      const classroomId = this.getAttribute("data-classroom-id");
      const deleteClassId = document.getElementById("delete-class-id");
      deleteClassId.value = classroomId;
      document.getElementById("delete-class-modal").style.display = "block";
    });
  });
  
  // Edit button functionality for home.html
  document.querySelectorAll(".edit-icon").forEach((button) => {
    button.addEventListener("click", function () {
      const classroomId = this.getAttribute("data-classroom-id");
      const renameClassId = document.getElementById("rename-class-id");
      renameClassId.value = classroomId;
      document.getElementById("rename-class-modal").style.display = "block";
    });
  });
  
  document.getElementById("close-rename-class").addEventListener("click", () => {
    document.getElementById("rename-class-modal").style.display = "none";
  });