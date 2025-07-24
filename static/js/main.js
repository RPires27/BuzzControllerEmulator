const socket = io();
let selectedPlayer = null;
let mySid = null;

// --- DOM Elements ---
const modal = document.getElementById("player-modal");
const openModalBtn = document.getElementById("open-modal-btn");
const playerSelector = document.getElementById("player-selector");
const playerDisplay = document.getElementById("player-display");

// --- Modal Logic ---
openModalBtn.onclick = () => {
  modal.style.display = "flex";
};

// Close modal if user clicks outside the content
window.onclick = (event) => {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

// --- Player Selection ---
function createPlayerButtons() {
  playerSelector.innerHTML = ""; // Clear existing buttons
  for (let i = 1; i <= 8; i++) {
    const button = document.createElement("div");
    button.classList.add("player-button");
    button.dataset.player = i;
    button.textContent = i;
    button.addEventListener("click", () => selectPlayer(i));
    playerSelector.appendChild(button);
  }
}

function selectPlayer(player) {
  const button = document.querySelector(`.player-button[data-player='${player}']`);
  if (button.classList.contains('locked') && !button.classList.contains('selected')) {
      return; // Can't select a button locked by others
  }
  socket.emit("select_player", { player: player });
}

socket.on("connect", () => {
  mySid = socket.id;
  createPlayerButtons();
});

socket.on("update_players", (lockedPlayers) => {
  let wasSelected = false;
  selectedPlayer = null;
  const allPlayerButtons = document.querySelectorAll(".player-button");

  allPlayerButtons.forEach((button) => {
    const playerId = button.dataset.player;
    const lockingSid = lockedPlayers[playerId];

    button.classList.remove("locked", "selected");

    if (lockingSid) {
      if (lockingSid === mySid) {
        button.classList.add("selected");
        selectedPlayer = playerId;
        playerDisplay.textContent = `Player ${playerId}`;
        wasSelected = true;
      } else {
        button.classList.add("locked");
      }
    }
  });

  if (!selectedPlayer) {
    playerDisplay.textContent = "Not Selected";
  }

  // If a player was just successfully selected, close the modal
  if (wasSelected) {
    modal.style.display = "none";
  }
});

// --- Buzz Action ---
function buzz(color) {
  if (!selectedPlayer) {
    alert("Please select a player first!");
    return;
  }
  socket.emit("buzz", { player: selectedPlayer, color: color });
}

// --- Fullscreen Logic ---
function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(err => {
      console.error(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
    });
  } else {
    document.exitFullscreen();
  }
}

document.addEventListener("fullscreenchange", updateFullscreenButton);
function updateFullscreenButton() {
  const button = document.querySelector(".fullscreen-toggle");
  button.innerHTML = document.fullscreenElement ? "⛶" : "⛶";
  button.title = document.fullscreenElement ? "Exit Fullscreen" : "Enter Fullscreen";
}

// Initial setup
createPlayerButtons();