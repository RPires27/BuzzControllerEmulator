# Buzz! Controller

A web-based controller that emulates the classic Buzz! quiz game buzzers, allowing multiple players to interact with quiz games through their mobile devices or computers. This project creates a virtual keyboard input system that maps player actions to specific keyboard keys.

## Features

- **Multi-player support**: Up to 8 players can connect simultaneously
- **Mobile-friendly**: Responsive design optimized for touch devices
- **Real-time communication**: Instant key press simulation via WebSocket
- **Color-coded buttons**: Red (Buzz), Blue, Orange, Green, and Yellow buttons for each player
- **Player selection**: Easy switching between players 1-8
- **Cross-platform**: Works on any device with a web browser

## How It Works

The system consists of:

1. A Flask web server with SocketIO for real-time communication
2. A mobile-responsive web interface for player interaction
3. A keyboard controller that simulates key presses based on player actions

Each player is assigned specific keyboard keys:

- **Player 1**: Q (red), W (blue), E (orange), R (green), T (yellow)
- **Player 2**: Y (red), U (blue), I (orange), O (green), P (yellow)
- **Player 3**: A (red), S (blue), D (orange), F (green), G (yellow)
- **Player 4**: H (red), J (blue), K (orange), L (green), ; (yellow)
- **Player 5**: Z (red), X (blue), C (orange), V (green), B (yellow)
- **Player 6**: 1 (red), 2 (blue), 3 (orange), 4 (green), 5 (yellow)
- **Player 7**: 6 (red), 7 (blue), 8 (orange), 9 (green), 0 (yellow)
- **Player 8**: 7 (red), 8 (blue), 9 (orange), + (green), - (yellow)

## Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) - A fast Python package installer and resolver

### Using uv (Recommended)

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd buzzEmulation
   ```

2. **Install dependencies with uv**:

   ```bash
   uv sync
   ```

3. **Activate the virtual environment**:

   ```bash
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```

4. **Run the application**:
   ```bash
   uv run python main.py
   ```

### Alternative: Manual Installation

If you prefer not to use uv:

1. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

1. **Start the server**: Run the application using one of the methods above
2. **Access the controller**: Open a web browser and navigate to `http://localhost:5000`
3. **Connect devices**: Multiple players can connect from different devices on the same network
4. **Select player**: Each player chooses their player number from the dropdown
5. **Play**: Use the colored buttons to send key presses to the host computer

### Network Setup

- **Local play**: Use `http://localhost:5000` on the host computer
- **LAN play**: Find your computer's IP address and use `http://<your-ip>:5000`
- **Mobile devices**: Ensure all devices are on the same WiFi network

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

- **New button colors**: Modify the CSS in `templates/index.html`
- **Additional players**: Update the `player_keys` dictionary in `main.py`
- **Custom key mappings**: Edit the key assignments in `main.py`

### Running in Development Mode

For development with auto-reload:

```bash
uv run flask --app main.py --debug run --host=0.0.0.0 --port=5000
```

## Troubleshooting

### Common Issues

1. **Port already in use**:

   ```bash
   lsof -i :5000  # Find process using port 5000
   kill -9 <PID>  # Kill the process
   ```

2. **Connection issues**:

   - Ensure all devices are on the same network
   - Check firewall settings
   - Verify the server is accessible via IP address

3. **Key presses not working**:
   - Ensure the target application has focus
   - Check if the application requires administrator privileges
   - Verify the key mappings match your game requirements

### Debug Mode

Enable debug logging by setting the environment variable:

```bash
export FLASK_ENV=development  # Unix/macOS
set FLASK_ENV=development     # Windows
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Inspired by the classic Buzz! quiz game series
- Built with Flask, SocketIO, and pynput
- Designed for educational and entertainment purposes
