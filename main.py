import vgamepad as vg
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
socketio = SocketIO(app)

# --- Player and Gamepad Management ---

# Dictionary to track which player is controlled by which session ID (sid)
# Key: player_id (e.g., '1'), Value: session_id
locked_players = {}

# Initialize 8 virtual Xbox 360 controllers
print("Initializing virtual gamepads...")
try:
    gamepads = [vg.VX360Gamepad() for _ in range(8)]
    print("Virtual gamepads initialized successfully.")
except Exception as e:
    print(f"Error initializing gamepads: {e}")
    print("Please ensure you have installed the necessary drivers and have the correct permissions.")
    exit()

# Define the button mappings for an Xbox 360 controller
button_mapping = {
    'red': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    'blue': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    'orange': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    'green': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    'yellow': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
}

# --- Flask Routes ---

@app.route('/')
def index():
    return render_template('index.html')

# --- SocketIO Event Handlers ---

@socketio.on('connect')
def handle_connect():
    """
    When a new client connects, send them the current list of locked players.
    """
    print(f"Client connected: {request.sid}")
    emit('update_players', locked_players)

@socketio.on('disconnect')
def handle_disconnect():
    """
    When a client disconnects, check if they had a player locked.
    If so, release the lock and notify all other clients.
    """
    print(f"Client disconnected: {request.sid}")
    player_to_remove = None
    for player_id, sid in locked_players.items():
        if sid == request.sid:
            player_to_remove = player_id
            break
    
    if player_to_remove:
        del locked_players[player_to_remove]
        # Notify all clients that the player is now available
        socketio.emit('update_players', locked_players)
        print(f"Player {player_to_remove} is now free.")

@socketio.on('select_player')
def handle_select_player(data):
    """
    Handles a client's request to select and lock a player.
    """
    player_id = str(data.get('player'))
    sid = request.sid

    # Check if the player_id is valid
    if not player_id or not player_id.isdigit() or not 1 <= int(player_id) <= 8:
        print(f"Invalid player selection attempt from {sid}: {player_id}")
        return

    # Remove any existing lock this user might have
    existing_lock = None
    for p_id, s_id in locked_players.items():
        if s_id == sid:
            existing_lock = p_id
            break
    if existing_lock:
        del locked_players[existing_lock]

    # If the requested player is not already locked, lock it for this user
    if player_id not in locked_players:
        locked_players[player_id] = sid
        print(f"Player {player_id} locked by {sid}")
        # Broadcast the updated player list to all clients
        socketio.emit('update_players', locked_players)
    else:
        # If the player was already locked by someone else, send the current state back
        # to the requester to ensure their UI is up-to-date.
        emit('update_players', locked_players)
        print(f"Player {player_id} is already locked. Request from {sid} denied.")


@socketio.on('buzz')
def handle_buzz(data):
    """
    Handles a buzz event from a client.
    """
    try:
        player_id = str(data.get('player'))
        button_color = data.get('color')
        sid = request.sid

        # Security check: Ensure the buzz is coming from the client who locked the player
        if locked_players.get(player_id) != sid:
            print(f"Unauthorized buzz attempt from {sid} for player {player_id}")
            return

        player_index = int(player_id) - 1

        if 0 <= player_index < 8 and button_color in button_mapping:
            gamepad = gamepads[player_index]
            button_to_press = button_mapping[button_color]

            print(f"Player {player_index + 1} pressed {button_color}")

            # Press and release the button
            gamepad.press_button(button=button_to_press)
            gamepad.update()
            time.sleep(0.1)
            gamepad.release_button(button=button_to_press)
            gamepad.update()

    except (KeyError, IndexError, ValueError) as e:
        print(f"Error processing buzz event: {e}. Data: {data}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Cleanup ---

def cleanup():
    """
    Resets all virtual gamepads on application exit.
    """
    print("\nResetting all virtual gamepads...")
    for gamepad in gamepads:
        gamepad.reset()
        gamepad.update()
    print("Cleanup complete. Exiting.")

# --- Main Execution ---

if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', port=5000)
    finally:
        cleanup()