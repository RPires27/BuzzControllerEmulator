import vgamepad as vg
from flask import Flask, render_template
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize 8 virtual Xbox 360 controllers
print("Initializing virtual gamepads...")
try:
    gamepads = [vg.VX360Gamepad() for _ in range(8)]
    print("Virtual gamepads initialized successfully.")
except Exception as e:
    print(f"Error initializing gamepads: {e}")
    print("Please ensure you have installed the necessary drivers and have the correct permissions.")
    # Exit if gamepads can't be initialized
    exit()

# Define the button mappings for an Xbox 360 controller
button_mapping = {
    'red': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,      # Red (Buzz) -> A button
    'blue': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,     # Blue -> X button
    'orange': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,   # Orange -> B button
    'green': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,    # Green -> Y button
    'yellow': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,  # Yellow -> Right Shoulder
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('buzz')
def handle_buzz(data):
    try:
        player_index = int(data['player']) - 1
        button_color = data['color']

        if 0 <= player_index < 8 and button_color in button_mapping:
            gamepad = gamepads[player_index]
            button_to_press = button_mapping[button_color]

            print(f"Player {player_index + 1} pressed {button_color}")

            # Press the button
            gamepad.press_button(button=button_to_press)
            gamepad.update()
            
            # Keep the button pressed for a short duration
            time.sleep(0.1)

            # Release the button
            gamepad.release_button(button=button_to_press)
            gamepad.update()

    except (KeyError, IndexError, ValueError) as e:
        print(f"Error processing buzz event: {e}. Data: {data}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def cleanup():
    print("\nResetting all virtual gamepads...")
    for gamepad in gamepads:
        gamepad.reset()
        gamepad.update()
    print("Cleanup complete. Exiting.")

if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', port=5000)
    finally:
        cleanup()