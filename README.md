# llm-chess
A simple chess game where stockfish plays against a LLM


This project implements a chess game where the renowned **Stockfish engine** plays against a **Large Language Model (LLM)** (e.g. `llama3.2`). The game is presented with a GUI built using **PySimpleGUI**, allowing users to observe the moves made by both engines in real-time.

---

## Features

- **Stockfish Integration**: Leverages Stockfish for calculating optimal chess moves.
- **LLM Integration**: Uses the `Ollama` API to query the LLM for its chess moves.
- **Interactive GUI**: Built with PySimpleGUI, showing the chessboard and allowing users to control the game.
- **FEN Support**: Chessboard states are encoded in Forsyth–Edwards Notation (FEN).
- **Error Handling**: Handles invalid moves and displays errors in the GUI.
- **Game Reset and Replay**: Allows resetting the board to start a new game.

---

## Installation

### Prerequisites
1. **Python 3.8+** installed on your system.
2. **Stockfish Binary**:
   - Download Stockfish from the [official website](https://stockfishchess.org/download/).
   - Note the path to the executable.

3. **Dependencies**: Install the required Python libraries:
   ```bash
   pip install chess cairosvg ollama PySimpleGUI Pillow stockfish
   ```



## Configuration

1. **Set the Stockfish Path**:
   Update the `STOCKFISH_PATH` variable in the script with the path to your Stockfish executable.

2. **Configure the Ollama API**:
   Update the `OLLAMA_URL` and `OLLAMA_MODEL` variables with your API's endpoint and model name.

---

## Usage

1. **Run the Script**:
   ```bash
   python chess_game.py
   ```

2. **Game Controls**:
   - **Next Move**: Progresses the game by alternating between Stockfish and the LLM.
   - **Reset Game**: Resets the chessboard to the initial position.
   - **Exit**: Closes the application.

3. **Observe the Moves**:
   - Moves are calculated by Stockfish and the LLM and displayed on the chessboard.
   - Game status (e.g., errors, checkmate) is shown in the status bar.

---

## Architecture

### Key Components:
1. **Stockfish Engine**: Calculates moves using the Stockfish library.
2. **LLM Query**: Communicates with the LLM using the `Ollama` API for its move.
3. **Chess Logic**: Uses the `python-chess` library for board management and FEN encoding.
4. **GUI**: Provides an interactive chessboard using PySimpleGUI.

---

## Troubleshooting

- **Stockfish Not Found**:
  - Ensure the `STOCKFISH_PATH` is correctly set to the Stockfish executable.
- **Ollama API Errors**:
  - Verify the API URL and that the server is running.
  - Check your API credentials or endpoint permissions.
- **Invalid Moves**:
  - Ensure the LLM responds with a valid UCI move (e.g., `e2e4`).

---

## Future Enhancements

- **Customizable Game Options**:
  - Support for time limits and difficulty levels.
- **Human Player Mode**:
  - Allow a human player to compete against Stockfish or the LLM.
- **Enhanced LLM Prompts**:
  - Experiment with prompt engineering to improve LLM move quality.

---

## License

All rights reserved.






--- 

