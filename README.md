# Buzz! Controller for PCSX2

A web-based controller designed for playing Buzz! quiz games on the PCSX2 emulator. This project creates virtual Xbox 360 gamepads, allowing players to use their mobile devices as Buzz! controllers for a seamless multiplayer experience.

## Features

- **Native Gamepad Emulation**: Uses `vgamepad` to create virtual Xbox 360 controllers, offering better compatibility and performance than keyboard simulation
- **Multi-player Support**: Up to 8 players can connect and play simultaneously, each with their own virtual gamepad
- **Mobile-friendly**: Responsive design optimized for touch devices
- **Real-time Communication**: Instant button presses via WebSocket
- **Color-coded Buttons**: Standard Buzz! controller layout (Red/Buzz, Blue, Orange, Green, Yellow)
- **Cross-platform**: Works on any device with a web browser, with server support for both Windows and Linux

## How It Works

The system consists of:

1. A Flask web server with SocketIO for real-time communication
2. A mobile-responsive web interface for player interaction
3. A `vgamepad` backend that creates and manages 8 virtual Xbox 360 controllers
4. **PCSX2 Integration**: Player inputs from the web interface are translated into gamepad button presses that PCSX2 can recognize natively

## Installation

### Prerequisites

- Python 3.13 or higher
- `uv` - A fast Python package installer and resolver
- PCSX2 emulator with a Buzz! game

### Step 1: Clone the Repository

```bash
git clone https://github.com/RPires27/BuzzControllerEmulator
cd BuzzControllerEmulator
```

### Step 2: Install Dependencies

```bash
uv sync
```

**Note**: On Windows, `vgamepad` will automatically prompt you to install the required ViGEmBus driver during the dependency installation. Simply follow the installer prompts.

### Step 3: Platform-Specific Setup

#### Windows

No additional setup required! The `vgamepad` library will handle driver installation automatically during `uv sync`.

#### Linux

The installation process varies depending on your distribution:

##### Debian-based Distributions (Ubuntu, Debian, Linux Mint, etc.)

```bash
# Install required development packages
sudo apt update
sudo apt install -y build-essential python3-dev linux-headers-$(uname -r)

# Install USB and device libraries
sudo apt install -y libusb-1.0-0-dev libudev-dev

# Enable the uinput kernel module
sudo modprobe uinput

# Add it to load automatically on boot
echo 'uinput' | sudo tee -a /etc/modules

# Add your user to the input group
sudo usermod -a -G input $USER

# Set proper permissions for uinput device
sudo tee /etc/udev/rules.d/99-uinput.rules > /dev/null <<EOF
KERNEL=="uinput", MODE="0660", GROUP="input", OPTIONS+="static_node=uinput"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
```

##### Arch-based Distributions (Arch Linux, Manjaro, EndeavourOS, etc.)

```bash
# Install required development packages
sudo pacman -S base-devel python linux-headers

# Install USB and device libraries
sudo pacman -S libusb libudev0-shim

# Enable the uinput kernel module
sudo modprobe uinput

# Add it to load automatically on boot
echo 'uinput' | sudo tee -a /etc/modules-load.d/uinput.conf

# Add your user to the input group
sudo usermod -a -G input $USER

# Set proper permissions for uinput device
sudo tee /etc/udev/rules.d/99-uinput.rules > /dev/null <<EOF
KERNEL=="uinput", MODE="0660", GROUP="input", OPTIONS+="static_node=uinput"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
```

**Important for Linux users**: After completing the setup, you must **log out and log back in** (or reboot) for the group membership changes to take effect.

### Step 4: Run the Application

```bash
uv run main.py
```

You should see output similar to:

```
2025-07-26 12:21:18,650 - buzz_controller - INFO - Successfully initialized 8 out of 8 virtual gamepads.
2025-07-26 12:21:18,653 - buzz_controller - INFO - Starting server on 0.0.0.0:5000
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.234:5000
```

**Note**: You may see a warning about "development server" - this is normal and can be safely ignored since this application is designed for local gaming use.

## PCSX2 Setup Guide

### Prerequisites

- PCSX2 emulator installed and configured
- Buzz! game ISO
- This controller application running on the same computer as PCSX2
- Platform-specific setup completed (see Installation section above)

### Configuration Steps

1. **Start the Buzz! Controller Application**:

   ```bash
   uv run main.py
   ```

   You should see a message confirming that 8 virtual gamepads were initialized successfully.

2. **Connect a Mobile Device**:

   - On your mobile device, open a web browser and navigate to `http://<your-ip>:5000`
   - Select **Player 1** from the interface

3. **Launch PCSX2**: Start PCSX2 after the controller application is running.

4. **Open PCSX2 Controller Settings**:

   - In PCSX2, go to `Settings` → `Controllers`
   - In the left sidebar, click on `USB Port 1`
   - From the dropdown, select `Buzz Controller`

5. **Map Player 1 Buttons**:

   - In the PCSX2 interface, click on the **Red** button field for Player 1
   - On your mobile device, press the **Red (Buzz)** button
   - Repeat this process for each button:
     - Click **Blue** in PCSX2 → Press **Blue** on mobile
     - Click **Orange** in PCSX2 → Press **Orange** on mobile
     - Click **Green** in PCSX2 → Press **Green** on mobile
     - Click **Yellow** in PCSX2 → Press **Yellow** on mobile

6. **Configure Additional Players (2-4)**:

   - On the mobile device, switch to **Player 2**
   - In PCSX2, repeat the button mapping process for Player 2's column
   - Continue this process for Players 3 and 4

7. **Configure Players 5-8** (if needed):

   - In PCSX2, click on `USB Port 2` in the left sidebar
   - Select `Buzz Controller` from the dropdown
   - Have players 5-8 connect on their mobile devices and select their respective player numbers
   - Repeat the button mapping process for each player in USB Port 2

8. **Save Configuration**: Click `Apply` or `OK` to save your settings.

## Usage

1. **Start the Server**: Run `uv run main.py`
2. **Launch PCSX2**: Start PCSX2 and load your Buzz! game
3. **Access the Controller**:
   - Local access: `http://localhost:5000`
   - Network access: `http://<your-ip-address>:5000`
4. **Connect Players**: Each player can connect from their device using a web browser

## Troubleshooting

### Installation Issues

**"Error initializing gamepads" on startup**:

- **Windows**: If the driver installation failed during `uv sync`, manually run the installer from the vgamepad package directory
- **Linux**:
  - Verify the uinput module is loaded: `lsmod | grep uinput`
  - Check group membership: `groups` (should include "input")
  - Ensure you logged out and back in after adding yourself to the input group
  - As a last resort, try running with `sudo`

### PCSX2 Integration Issues

**Controllers not detected in PCSX2**:

- Ensure the Buzz! Controller application is running **before** starting PCSX2
- In PCSX2 Controllers settings, verify you've selected `Buzz Controller` in USB Port 1 (and USB Port 2 for players 5-8)
- Make sure at least one mobile device is connected and has selected a player number
- Try restarting both applications if the Buzz controller option doesn't appear

**Button mapping not working**:

- Ensure the mobile device shows the player number you're trying to configure in PCSX2
- Make sure you're clicking the correct button field in PCSX2 before pressing the button on mobile
- Verify the mobile device is connected to the server (check the server console output for connection messages)
- Try refreshing the mobile browser page if buttons aren't responding

### Network Issues

**Can't connect from other devices**:

- Ensure all devices are on the same network
- Check if your firewall is blocking port 5000
- Try accessing via the server's IP address instead of localhost

## Technical Details

### Button Mapping

The application maps Buzz! controller buttons to Xbox 360 gamepad buttons as follows:

- Red (Buzz) → A Button
- Blue → X Button
- Orange → B Button
- Green → Y Button
- Yellow → Right Shoulder

### Network Requirements

- Default port: 5000
- Protocol: HTTP/WebSocket
- Firewall: Ensure port 5000 is open for local network access

## Acknowledgments

- Designed specifically for PCSX2 Buzz! games
- Built with Flask, SocketIO, and `vgamepad`
- Inspired by the classic Buzz! quiz game series

## Contributing

Issues and pull requests are welcome! Please feel free to contribute to improve this project.

## License

This project is open source. Please check the repository for license details.
