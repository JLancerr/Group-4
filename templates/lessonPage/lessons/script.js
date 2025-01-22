const body = document.querySelector('body');
const sidebar = body.querySelector('.sidebar');
const toggle = body.querySelector('.bx.bx-chevron-right.toggle');

toggle.addEventListener("click", () => {
  sidebar.classList.toggle('close');
});

// Get elements from the DOM
const lessonTitle = document.getElementById('lesson-title');
const container = document.getElementById('flashcard-container');
const searchBar = document.getElementById('search-bar');

// Flashcard contents: [id, question, answer]
const contents = [
  [1, "What is 2 + 2?", "4"],
  [2, "What is the square root of 16?", "4"],
  [3, "What is 10 divided by 2?", "5"],
  [4, "What is 5 times 6?", "30"],
  [1, "What is 2 + 2?", "4"],
  [2, "What is f 16?", "4"],
  [3, "What is 1qwertyuiopasdfghjk0 divided by 2?", "5"],
  [4, "What is 5 times 6?", "30"],
  [1, "What is 2 + 2?", "4"],
  [2, "What is the square root of 16?", "4"],
  [3, "What is 10 divided by 2?", "5"],
  [4, "What is 5 times 6?", "30"],
  [1, "What is 2 + 2?", "4"],
  [2, "What is the square root of 16?", "4"],
  [4, "What is 5 times 6?", "30"],
  [1, "What is 2 + 2?", "4"],
  [2, "What is the square root of 16?", "4"],
];

// Authorization flag
const authored = 1; // 1 for editor, 0 otherwise

// Update the lesson title (if applicable)
lessonTitle.textContent = "Basic Math Lesson";

// Function to truncate text
function truncateText(text, maxLength) {
  if (text.length > maxLength) {
    return text.substring(0, maxLength) + '...';
  }
  return text;
}

// Function to populate flashcards
function populateFlashcards(filteredContents = contents) {
  container.innerHTML = ''; // Clear existing flashcards
  filteredContents.forEach(([id, question, answer]) => {
    const flashcard = document.createElement('div');
    flashcard.classList.add('flashcard');
    flashcard.innerHTML = `
      <div class="flashcard__content">
        <div class="flashcard__front">
          <p>${truncateText(question, 30)}</p>
        </div>
        <div class="flashcard__back">
          <p>${truncateText(answer, 30)}</p>
        </div>
        ${authored ? `
          <div class="flashcard__actions">
            <button type="button" class="edit-icn" data-id="${id}">
              <i class='bx bxs-pencil'></i>
            </button>
            <button type="button" class="delete-icn" data-id="${id}">
              <i class='bx bxs-trash-alt'></i>
            </button>
          </div>
        ` : ''}
      </div>
    `;
    container.appendChild(flashcard);
  });
}

// Function to handle search
function handleSearch() {
  const searchTerm = searchBar.value.toLowerCase();
  const filteredContents = contents.filter(([id, question, answer]) => 
    question.toLowerCase().includes(searchTerm) || answer.toLowerCase().includes(searchTerm)
  );
  populateFlashcards(filteredContents);
}

// Add event listener to search bar
searchBar.addEventListener('input', handleSearch);

// Call the function to populate flashcards on page load
populateFlashcards();







