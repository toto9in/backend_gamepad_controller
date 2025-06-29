# Gamepad Emulator

## Overview

Gamepad Emulator is a Python-based application that simulates a virtual Xbox 360 controller. It allows users to control the gamepad inputs remotely by sending JSON-formatted messages via WebSocket. The application listens for connection requests, receives data over a socket, and maps the incoming commands to simulate button presses and releases on a virtual controller using the vgamepad library.

## Libraries Used

- **vgamepad**: Emulates Xbox 360 gamepad inputs.
- **websockets**: Implements the WebSocket server for real-time communication.
- **asyncio**: Handles asynchronous tasks and concurrency.
- **threading**: Runs the asynchronous server on a separate thread.
- **json**: Parses the JSON messages received from clients.

## How It Works

The application consists of two main files:

- **main.py**: Entry point for the application (not detailed here but responsible for starting the server and integrating with the GUI or other components).
- **gamepad_server.py**: Contains the `GamepadServer` class which manages WebSocket connections and input command mapping.

### Data Flow

1. **WebSocket Connection**:
   The `GamepadServer` starts a WebSocket server on port `12345` and waits for client connections. When a client connects, the server logs the connection details.

2. **Receiving Data**:
   The server receives messages in JSON format. The expected JSON message structure is as follows:
   ```json
   {
     "message": {
       "a": true,
       "b": false,
       "x": false,
       "y": false,
       "up": false,
       "down": true,
       "left": false,
       "right": false,
       "l": false,
       "r": false,
       "select": false,
       "start": false
     }
   }
   ```
   Each key in the `message` object represents a gamepad button, and its boolean value signifies whether the button is pressed (`true`) or released (`false`).

3. **Mapping Commands**:
   The `_map_messages_to_command` method in `gamepad_server.py` performs the following tasks:
   - **JSON Parsing**: Converts the incoming message string into a JSON object.
   - **Validation**: Checks that the JSON object has a `message` key.
   - **Button State Comparison**: Iterates over the keys (button names). If the state of a button has changed (compared to the current stored state), it updates the state.
   - **Simulating Gamepad Input**:
     Uses the `vgamepad` library to call `press_button` when a button is pressed and `release_button` when released based on a pre-defined mapping:
     - `"a"` maps to the A button
     - `"b"` maps to the B button
     - `"x"` maps to the X button
     - `"y"` maps to the Y button
     - `"up"`, `"down"`, `"left"`, `"right"` map to the corresponding directional pad inputs
     - `"l"` and `"r"` map to the left and right shoulder buttons
     - `"select"` maps to the Back button
     - `"start"` maps to the Start button
   - **Updating the Virtual Controller**:
     After processing all button commands, the gamepad's state is updated to reflect the changes immediately.

## Usage

## Install Dependencies

### Option 1: Using a Virtual Environment
## Install Dependencies with uv

This project uses [uv](https://github.com/uv-dev/uv) to manage its virtual environment and dependencies.

1. **Install uv** (if you haven't already):

    ```sh
    pip install uv
    ```

2. **Create a uv virtual environment**:

    ```sh
    uv venv create
    ```

3. **Activate virtual environment**:

     **Linux/macOS:**
     ```sh
      source .venv/bin/activate
      ```
      **Windows**
      ```sh
      .venv\Scripts\activate
      ```

3. **Install the project dependencies**:

    ```sh
    uv run
    ```

4. **Run the application**:

    ```sh
    uv run main.py
    ```
```

2. **Run the Application**:
   Start the server by running `main.py`. The server will initialize the WebSocket listener and wait for remote control commands.

3. **Connect a Client**:
   Use any WebSocket-compatible client (such as a mobile app or a web interface) to connect to the server's IP address and port `12345`. Once connected, send JSON commands as described in the Data Flow section to simulate gamepad inputs.

## Project Structure

- `main.py`: Application entry point.
- `gamepad_server.py`: Implements the `GamepadServer` class responsible for:
  - Managing WebSocket connections
  - Receiving and mapping JSON messages to virtual gamepad input commands

## Conclusion

This project provides an easy way to simulate gamepad inputs remotely using WebSocket communication and virtual gamepad emulation. It can be extended or integrated into other systems that require remote controller inputs.