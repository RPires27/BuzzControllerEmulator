from flask import Flask, render_template
from flask_socketio import SocketIO
from pynput.keyboard import Controller, Key

app = Flask(__name__)
socketio = SocketIO(app)
keyboard = Controller()

# Define the key mappings for each player
player_keys = {
    1: {'red': 'q', 'blue': 'w', 'orange': 'e', 'green': 'r', 'yellow': 't'},
    2: {'red': 'y', 'blue': 'u', 'orange': 'i', 'green': 'o', 'yellow': 'p'},
    # Add more players as needed
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('buzz')
def handle_buzz(data):
    player = data['player']
    button_color = data['color']

    if player in player_keys and button_color in player_keys[player]:
        key_to_press = player_keys[player][button_color]
        keyboard.press(key_to_press)
        keyboard.release(key_to_press)
        print(f"Player {player} pressed {button_color} (key: {key_to_press})")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
