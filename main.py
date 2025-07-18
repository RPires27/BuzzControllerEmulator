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
    3: {'red': 'a', 'blue': 's', 'orange': 'd', 'green': 'f', 'yellow': 'g'},
    4: {'red': 'h', 'blue': 'j', 'orange': 'k', 'green': 'l', 'yellow': ';'},
    5: {'red': 'z', 'blue': 'x', 'orange': 'c', 'green': 'v', 'yellow': 'b'},
    6: {'red': '1', 'blue': '2', 'orange': '3', 'green': '4', 'yellow': '5'},
    7: {'red': '6', 'blue': '7', 'orange': '8', 'green': '9', 'yellow': '0'},
    8: {'red': '7', 'blue': '8', 'orange': '9', 'green': '+', 'yellow': '-'},
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
