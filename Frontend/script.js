// ============================================================================
// script.js
// This file handles everything that happens AFTER the page has loaded:
// grabbing what the user types, sending it to the FastAPI backend, and
// showing the response in the chat window.
// ============================================================================

// ---- 1. Grab references to the HTML elements we'll need to work with ----
// (These IDs match the id="..." attributes in index.html)
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatLog = document.getElementById("chat-log");
const sendButton = document.getElementById("send-button");
const typingIndicator = document.getElementById("typing-indicator");

// ---- 2. The backend endpoint we'll send questions to ----
const API_URL = "http://127.0.0.1:8000/ask";

// ---- 3. Listen for the form being submitted ----
// This fires both when the send button is clicked AND when the user
// presses Enter while the input is focused — a <form> gives us both for free.
chatForm.addEventListener("submit", async function (event) {
  // Prevent the browser's default behavior, which would reload the page
  event.preventDefault();

  const question = userInput.value.trim(); // trim() removes leading/trailing spaces

  // Don't send empty (or whitespace-only) messages
  if (question === "") {
    return;
  }

  // Show the user's message in the chat immediately
  addMessage(question, "user");

  // Clear the input box so it's ready for the next message
  userInput.value = "";

  // Ask the backend for an answer
  await askBackend(question);
});

/**
 * Sends the user's question to the FastAPI backend and displays the answer.
 * This function is declared "async" because it needs to "await" the network
 * request — see the explanation of async/await further down in the chat.
 */
async function askBackend(question) {
  setLoading(true); // disable input + show typing dots while we wait

  try {
    // fetch() sends an HTTP request to the given URL.
    // We configure it as a POST request carrying JSON data.
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // tells FastAPI "the body is JSON"
      },
      body: JSON.stringify({ question: question }), // convert JS object -> JSON text
    });

    // If the server responded with an error status (like 500), treat it as a failure
    if (!response.ok) {
      throw new Error("Server responded with status " + response.status);
    }

    // Parse the JSON text coming back into a usable JS object
    const data = await response.json();

    // Our FastAPI backend returns: { "question": "...", "answer": "..." }
    addMessage(data.answer, "bot");

  } catch (error) {
    // This runs if the fetch failed entirely (backend not running, no internet,
    // CORS blocked, etc.) or if we manually threw an error above.
    console.error("Request to backend failed:", error);
    addMessage(
      "Sorry, I couldn't reach the server. Please make sure the backend is running and try again.",
      "error"
    );
  } finally {
    // "finally" always runs, whether the request succeeded or failed —
    // so the loading state is always cleaned up.
    setLoading(false);
  }
}

/**
 * Adds a new message bubble to the chat log.
 * @param {string} text - the message text to display
 * @param {"user"|"bot"|"error"} sender - who the message is from, controls styling
 */
function addMessage(text, sender) {
  const messageEl = document.createElement("div");
  messageEl.classList.add("message", `message--${sender}`);

  // Bot and error messages show a small "K" avatar; user messages don't need one
  if (sender === "bot" || sender === "error") {
    const avatar = document.createElement("div");
    avatar.classList.add("message__avatar");
    avatar.textContent = "K";
    messageEl.appendChild(avatar);
  }

  const bubble = document.createElement("div");
  bubble.classList.add("message__bubble");
  bubble.textContent = text; // textContent (not innerHTML) keeps this safe from HTML injection
  messageEl.appendChild(bubble);

  chatLog.appendChild(messageEl);

  scrollToBottom();
}

/**
 * Shows/hides the typing indicator and enables/disables the send button
 * while a request is in progress.
 */
function setLoading(isLoading) {
  typingIndicator.hidden = !isLoading;
  sendButton.disabled = isLoading;

  if (isLoading) {
    scrollToBottom();
  }
}

/**
 * Scrolls the chat log to the most recent message.
 */
function scrollToBottom() {
  chatLog.scrollTop = chatLog.scrollHeight;
}
