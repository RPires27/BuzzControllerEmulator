# Buzz! Controller for PCSX2

A web-based controller designed for playing Buzz! quiz games on the PCSX2 emulator. This project creates virtual Xbox 360 gamepads, allowing players to use their mobile devices as Buzz! controllers for a seamless multiplayer experience.

## Features

- **Native Gamepad Emulation**: Uses `vgamepad` to create virtual Xbox 360 controllers, offering better compatibility and performance than keyboard simulation.
- **Multi-player Support**: Up to 8 players can connect and play simultaneously, each with their own virtual gamepad.
- **Mobile-friendly**: Responsive design optimized for touch devices.
- **Real-time Communication**: Instant button presses via WebSocket.
- **Color-coded Buttons**: Standard Buzz! controller layout (Red/Buzz, Blue, Orange, Green, Yellow).
- **Cross-platform**: Works on any device with a web browser, with server support for both Windows and Linux.

## How It Works

The system consists of:

1.  A Flask web server with SocketIO for real-time communication.
2.  A mobile-responsive web interface for player interaction.
3.  A `vgamepad` backend that creates and manages 8 virtual Xbox 360 controllers.
4.  **PCSX2 Integration**: Player inputs from the web interface are translated into gamepad button presses that PCSX2 can recognize natively.

## System Requirements

Before running the application, you must install the necessary drivers for `vgamepad`.

### Windows

1.  **Install ViGEmBus Driver**: Download and install the latest version of [ViGEmBus](https://github.com/ViGEm/ViGEmBus/releases). This is required for creating virtual gamepads.

### Linux

1.  **Install Kernel Headers and Development Tools**:
    ```bash
    sudo apt update
    sudo apt install -y build-essential python3-dev linux-headers-$(uname -r)
    ```
2.  **Install `libusb` and `libudev`**:
    ```bash
    sudo apt install -y libusb-1.0-0-dev libudev-dev
    ```
3.  **Enable the `uinput` Kernel Module**: This module allows userspace programs to create virtual input devices.
    ```bash
    sudo modprobe uinput
    ```
4.  **Set Permissions**: Add your user to the `input` group to grant permissions to manage virtual input devices.
    ```bash
    sudo usermod -a -G input $USER
    ```
    **Important**: You must **log out and log back in** for this change to take effect.

## PCSX2 Setup Guide

With the migration to `vgamepad`, you no longer need to map individual keyboard keys. Instead, you will configure PCSX2 to use the virtual Xbox 360 controllers.

### Prerequisites

- PCSX2 emulator installed and configured.
- Buzz! game ISO.
- This controller application running on the same computer as PCSX2.
- System requirements from the section above are met.

### PCSX2 Configuration

1.  **Start the Buzz! Controller Application**: Run `uv run python main.py` before launching PCSX2. This will create the 8 virtual gamepads.
2.  **Open PCSX2 Controller Settings**:
    - Launch PCSX2 and go to `Settings` -> `Controllers`.
3.  **Enable Multitap**:
    - To play with more than 2 players, you need to enable the multitap. In the controller settings, for `Port 1`, select `Multitap 1`. This will enable up to 4 players on the first port. For players 5-8, enable `Multitap 2` on `Port 2`.
4.  **Map the Virtual Controllers**:
    - Select `Controller Port 1` (or the port you enabled multitap on).
    - For the `Device API`, select `XInput`.
    - In the `Device` dropdown, you should see multiple "Xbox 360 Controller" entries. Select the first one for Player 1.
    - PCSX2 should automatically map the buttons. The button mapping is as follows:
        - **Red (Buzz)** -> `A` Button
        - **Blue** -> `X` Button
        - **Orange** -> `B` Button
        - **Green** -> `Y` Button
        - **Yellow** -> `Right Shoulder`
    - Repeat this process for each player, selecting a different "Xbox 360 Controller" from the device list for each port (Pad 1, Pad 2, etc.).
5.  **Save Configuration**:
    - Click `Apply` or `OK` to save your settings.

## Installation

### Prerequisites

- Python 3.13 or higher
- `uv` - A fast Python package installer and resolver
- PCSX2 emulator with a Buzz! game

### Using uv (Recommended)

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/RPires27/BuzzControllerEmulator
    cd BuzzControllerEmulator
    ```
2.  **Install Dependencies with uv**:
    ```bash
    uv sync
    ```
3.  **Activate the Virtual Environment**:
    ```bash
    source .venv/bin/activate  # On Unix/macOS
    .venv\Scripts\activate     # On Windows
    ```
4.  **Run the Application**:
    ```bash
    uv run python main.py
    ```

## Usage with PCSX2

1.  **Start the Controller**: Run the application. You should see a confirmation that the virtual gamepads were initialized.
2.  **Start PCSX2**: Launch PCSX2 and load your Buzz! game.
3.  **Configure PCSX2**: Follow the new PCSX2 setup guide above.
4.  **Access the Controller**: Open a web browser and navigate to `http://localhost:5000`.
5.  **Connect Devices**: Players can connect from any device on the same network by navigating to `http://<your-ip>:5000`.

## Troubleshooting

### Gamepad & Controller Issues

1.  **"Error initializing gamepads" on startup**:
    - **Windows**: Ensure the ViGEmBus driver is installed correctly.
    - **Linux**:
        - Make sure you have run `sudo modprobe uinput`.
        - Confirm you have added your user to the `input` group with `sudo usermod -a -G input $USER` and that you have **logged out and back in**.
        - Run the script with `sudo` as a last resort if permissions are still an issue.
2.  **PCSX2 does not detect the controllers**:
    - Make sure you started the Buzz! Controller application **before** opening PCSX2.
    - In PCSX2 controller settings, ensure the `Device API` is set to `XInput`.
    - If the controllers still don't appear, try restarting your computer after installing the necessary drivers and setting permissions.
3.  **Buttons are not responding**:
    - Verify in the web interface that button presses are being registered (check the server console output).
    - Double-check the controller mappings in PCSX2 for each player pad.

## Acknowledgments

- Designed specifically for PCSX2 Buzz! games
- Built with Flask, SocketIO, and `vgamepad`
- Inspired by the classic Buzz! quiz game series