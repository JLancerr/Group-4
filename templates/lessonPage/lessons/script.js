const body = document.querySelector('body');
const sidebar = body.querySelector('.sidebar');
const toggle = body.querySelector('.bx.bx-chevron-right.toggle');

toggle.addEventListener("click", () => {
  sidebar.classList.toggle('close');
});

// Get elements from the DOM
const lessonTitle = document.getElementById('lesson-title');
const container = document.getElementById('flashcard-container');

// Flashcard contents: [id, question, answer]
const contents = [
  [1, "What is 2 + 2?", "4"],
  [2, "What is the square root of 16?", "4"],
  [3, "What is 10 divided by 2?", "5"],
  [4, "What is 5 times 6?", "30"],[1, "What is 2 + 2?", "4"],
  [2, "What is the square root of 16?", "4"],
  [3, "What is 10 divided by 2?", "5"],
  [4, "What is 5 times 6?", "30"],[1, "What is 2 + 2?", "4"],
  [2, "What is the square root of 16?", "4"],
  [3, "What is 10 divided by 2?", "5"],
  [4, "What is 5 times 6?", "30"],[1, "What is 2 + 2?", "4"],
  [2, "What is the square root of 16?", "4"],
  
  
];

// Authorization flag
const authored = 1; // 1 for editor, 0 otherwise

// Update the lesson title (if applicable)
lessonTitle.textContent = "Basic Math Lesson";

// Function to populate flashcards
function populateFlashcards() {
  contents.forEach(([id, question, answer]) => {
    const flashcard = document.createElement('div');
    flashcard.classList.add('flashcard');
    flashcard.innerHTML = `
      <div class="flashcard__content">
        <div class="flashcard__front">
          <p>${question}</p>
        </div>
        <div class="flashcard__back">
          <p>${answer}</p>
        </div>
        ${authored ? `
          <button class="delete-btn" data-id="${id}">
           <i class='bx bxs-trash'></i>
          </button>
        ` : ''}
      </div>
    `;
    container.appendChild(flashcard);
  });


}

// Call the function to populate flashcards on page load
populateFlashcards();







