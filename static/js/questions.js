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

// Setup modals for questions.html
setupModal("edit-question-modal", null, "close-edit-question");
setupModal("delete-question-modal", null, "close-delete-question");
setupModal("add-question-modal", "add-card-btn", "close-add-question");

// Delete button functionality for questions.html
document.querySelectorAll(".delete-icon").forEach((button) => {
  button.addEventListener("click", function () {
    const questionId = this.getAttribute("data-question-id");
    const deleteQuestionId = document.getElementById("delete-question-id");
    deleteQuestionId.value = questionId;
    const deleteQuestionModal = document.getElementById("delete-question-modal");
    deleteQuestionModal.style.display = "block";
  });
});

// Edit button functionality for questions.html
document.querySelectorAll(".edit-icon").forEach((button) => {
  button.addEventListener("click", function () {
    const questionId = this.getAttribute("data-question-id");
    const editQuestionId = document.getElementById("edit-question-id");
    editQuestionId.value = questionId;
    document.getElementById("edit-question-modal").style.display = "block";
  });
});

document.getElementById("close-edit-question").addEventListener("click", () => {
  document.getElementById("edit-question-modal").style.display = "none";
});

document.getElementById("close-delete-question").addEventListener("click", () => {
  document.getElementById("delete-question-modal").style.display = "none";
});

document.getElementById("close-add-question").addEventListener("click", () => {
  document.getElementById("add-question-modal").style.display = "none";
});

// Get elements from the DOM
const lessonTitle = document.getElementById("lesson-title");
const container = document.getElementById("flashcard-container");
const searchBar = document.getElementById("search-bar");

// Function to truncate text
function truncateText(text, maxLength) {
  if (text.length > maxLength) {
    return text.substring(0, maxLength) + "...";
  }
  return text;
}

// Function to populate flashcards
function populateFlashcards() {
  const flashcards = document.querySelectorAll(".flashcard");
  flashcards.forEach((flashcard) => {
    const question = flashcard.querySelector(".flashcard__front p").textContent;
    const answer = flashcard.querySelector(".flashcard__back p").textContent;
    flashcard.querySelector(".flashcard__front p").textContent = truncateText(
      question,
      30
    );
    flashcard.querySelector(".flashcard__back p").textContent = truncateText(
      answer,
      30
    );
  });
}

// Function to handle search
function handleSearch() {
  const searchTerm = searchBar.value.toLowerCase();
  const flashcards = container.querySelectorAll(".flashcard");
  flashcards.forEach((flashcard) => {
    const question = flashcard
      .querySelector(".flashcard__front p")
      .textContent.toLowerCase();
    const answer = flashcard
      .querySelector(".flashcard__back p")
      .textContent.toLowerCase();
    if (question.includes(searchTerm) || answer.includes(searchTerm)) {
      flashcard.style.display = "block";
    } else {
      flashcard.style.display = "none";
    }
  });
}

// Add event listener to search bar
searchBar.addEventListener("input", handleSearch);

// Call the function to populate flashcards on page load
populateFlashcards();

// Popup functionality for study mode
const studyBtn = document.getElementById("study-btn");
const popupOverlay = document.getElementById("popupOverlay");
const closePopup = document.getElementById("closePopup");

studyBtn.addEventListener("click", () => {
  popupOverlay.style.display = "flex";
});

closePopup.addEventListener("click", () => {
  popupOverlay.style.display = "none";
});