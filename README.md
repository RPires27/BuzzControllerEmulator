# Buzz! Controller for PCSX2

A web-based controller designed for playing Buzz! quiz games on the PCSX2 emulator. This project creates a virtual keyboard input system that maps player actions from mobile devices to keyboard keys, enabling multiplayer Buzz! gameplay on PCSX2.

## Features

- **PCSX2 Integration**: Optimized for Buzz! games on PCSX2 emulator
- **Multi-player Support**: Up to 8 players can connect simultaneously
- **Mobile-friendly**: Responsive design optimized for touch devices
- **Real-time Communication**: Instant key press simulation via WebSocket
- **Color-coded Buttons**: Red (Buzz), Blue, Orange, Green, and Yellow buttons for each player
- **Player Selection**: Easy switching between players 1-8
- **Cross-platform**: Works on any device with a web browser

## How It Works

The system consists of:

1. A Flask web server with SocketIO for real-time communication
2. A mobile-responsive web interface for player interaction
3. A keyboard controller that simulates key presses based on player actions
4. **PCSX2 Integration**: Key presses are sent directly to PCSX2, allowing mobile devices to act as Buzz! controllers

## PCSX2 Setup Guide

### Prerequisites

- PCSX2 emulator (version 2.0 or later) installed and configured
- Buzz! game ISO (any Buzz! game supporting multiplayer)
- This controller application running on the same computer as PCSX2

### PCSX2 Configuration

Configuring PCSX2 correctly is critical for the Buzz! Controller to work. You must set PCSX2 to recognize Buzz! Controller inputs mapped to specific keyboard keys.

1. **Open PCSX2 Controller Settings**:

   - Launch PCSX2 and go to `Config` → `Controllers (PAD)` → `Plugin Settings...`.

2. **Select Buzz! Controller for Each Player**:

   - In the `General` tab, select the port for each player (e.g., `Pad 1` for Player 1).
   - In the `Device` dropdown, choose **Buzz Controller** (not DualShock 2).
   - The interface will display the Buzz! buttons: `Red (Buzz)`, `Blue`, `Orange`, `Green`, and `Yellow`.

3. **Map Keys for Each Button**:

   - Click on each button name (e.g., `Red (Buzz)`) in the configuration window.
   - Press the corresponding keyboard key from the table below when prompted.
   - Repeat for all buttons and players (up to `Pad 8` for 8 players).

4. **Save Configuration**:

   - Click `Apply` or `OK` to save your settings.
   - Ensure PCSX2 is running in windowed mode for better focus handling during gameplay.

### Key Mappings for PCSX2

| Player | Red (Buzz) | Blue | Orange | Green | Yellow |
| ------ | ---------- | ---- | ------ | ----- | ------ |
| **1**  | Q          | W    | E      | R     | T      |
| **2**  | Y          | U    | I      | O     | P      |
| **3**  | A          | S    | D      | F     | G      |
| **4**  | H          | J    | K      | L     | ;      |
| **5**  | Z          | X    | C      | V     | B      |
| **6**  | 1          | 2    | 3      | 4     | 5      |
| **7**  | 6          | 7    | 8      | 9     | 0      |
| **8**  | T          | U    | I      | O     | P      |

**Note**: Ensure no other applications are intercepting these keys. Close unnecessary programs to avoid conflicts.

## Installation

### Prerequisites

- Python 3.13 or higher
- uv - A fast Python package installer and resolver
- PCSX2 emulator (version 2.0 or later) with a Buzz! game

### Using uv (Recommended)

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/RPires27/BuzzControllerEmulator
   cd BuzzControllerEmulator
   ```

2. **Install Dependencies with uv**:

   ```bash
   uv sync
   ```

3. **Activate the Virtual Environment**:

   ```bash
   source .venv/bin/activate  # On Unix/macOS
   .venv\Scripts\activate     # On Windows
   ```

4. **Run the Application**:

   ```bash
   uv run python main.py
   ```

### Alternative: Manual Installation

If you prefer not to use uv:

1. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   venv\Scripts\activate     # On Windows
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:

   ```bash
   python main.py
   ```

## Usage with PCSX2

1. **Start PCSX2**: Launch PCSX2 and load your Buzz! game.
2. **Start the Controller**: Run the application using one of the methods above.
3. **Configure PCSX2**: Follow the PCSX2 setup guide above to map the keys.
4. **Access the Controller**: Open a web browser and navigate to `http://localhost:5000`.
5. **Connect Devices**: Multiple players can connect from different devices on the same network.
6. **Select Player**: Each player chooses their player number from the dropdown menu.
7. **Play**: Use the colored buttons to control the game in PCSX2.

### Network Setup for Multiplayer

- **Local Play**: Use `http://localhost:5000` on the host computer.
- **LAN Play**: Find your computer's IP address (e.g., `192.168.x.x`) and use `http://<your-ip>:5000`.
- **Mobile Devices**: Ensure all devices are on the same WiFi network.

## Development

### Project Structure

```
buzzEmulation/
├── main.py              # Flask application with SocketIO
├── templates/
│   └── index.html       # Web interface
├── pyproject.toml       # Project configuration
├── uv.lock             # uv dependency lock file
├── .python-version     # Python version specification
└── README.md           # This file
```

### Adding New Features

The application is built with extensibility in mind:

- **New Button Colors**: Modify the CSS in `templates/index.html`.
- **Additional Players**: Update the `player_keys` dictionary in `main.py`.
- **Custom Key Mappings**: Edit the key assignments in `main.py`.

### Running in Development Mode

For development with auto-reload:

```bash
uv run flask --app main.py --debug run --host=0.0.0.0 --port=5000
```

## Troubleshooting

### PCSX2 Issues

1. **Keys Not Responding in PCSX2**:

   - Ensure PCSX2 has window focus when pressing buttons.
   - Verify key mappings in PCSX2 match the table above.
   - Confirm the Buzz! game supports the number of players configured.
   - Check that PCSX2 is set to use the Buzz Controller plugin, not DualShock 2.

2. **Controller Not Connecting**:

   - Ensure the controller server is running before starting PCSX2.
   - Check firewall settings to allow connections on port 5000.
   - Verify the server is accessible via `http://localhost:5000` or the IP address.

### Common Issues

1. **Port Already in Use**:

   ```bash
   lsof -i :5000  # Find process using port 5000 (Unix/macOS)
   kill -9 <PID>  # Kill the process
   ```

   On Windows, use:

   ```cmd
   netstat -aon | findstr :5000
   taskkill /PID <PID> /F
   ```

2. **Connection Issues**:

   - Ensure all devices are on the same network.
   - Check firewall settings to allow traffic on port 5000.
   - Verify the server is accessible via the IP address.

3. **Key Presses Not Working**:

   - Ensure PCSX2 has focus and is not minimized.
   - Check if the application requires administrator privileges (run `main.py` as admin if needed).
   - Verify key mappings match the game’s requirements.

### Debug Mode

Enable debug logging by setting the environment variable:

```bash
export FLASK_ENV=development  # Unix/macOS
set FLASK_ENV=development     # Windows
```

## Contributing

Contributions are welcome! Please submit a Pull Request or open an issue to discuss major changes.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Designed specifically for PCSX2 Buzz! games
- Inspired by the classic Buzz! quiz game series
- Built with Flask, SocketIO, and pynput

Optimized for multiplayer Buzz! gameplay on PCSX2
