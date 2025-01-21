from ollama import Client
import tkinter as tk
from tkinter import messagebox
import chess
import chess.svg
import requests
from stockfish import Stockfish
from PIL import Image, ImageTk
from io import BytesIO
import cairosvg

# Initialize Stockfish
STOCKFISH_PATH = "/pathg/stockfish_14_linux_x64_avx2/stockfish_14_linux_x64_avx2/stockfish_14_x64_avx2"
stockfish = Stockfish(STOCKFISH_PATH)

# Ollama API Configuration
OLLAMA_URL = "http://192.168.201.10:11434/"


def query_ollama(board_fen):
    """Query the Ollama API for the LLM's move."""
    client = Client(host=OLLAMA_URL, headers={'x-some-header': 'some-value'})
    prompt = f"You are a expert chess player (black color). We will give you the current chessboard FEN.  Give the next move only. The current chessboard FEN is {board_fen}. What is your next move? Do not repeat. Give only one move in Universal Chess Interface (UCI) format like d6d1. Where d6 is the old position and d1 is the new position. Answer in Universal Chess Interface (UCI) format like d6d1. You can only write 4 characters."
    response = client.chat(model='hermes3:70B', messages=[{'role': 'user', 'content': prompt}])
    print(response['message']['content'][-4:])
    return response['message']['content'][-4:]


def render_board(board):
    """Render the current board to an image."""
    svg_board = chess.svg.board(board, size=400)
    png_image = BytesIO()
    cairosvg.svg2png(bytestring=svg_board, write_to=png_image)
    return Image.open(png_image)


class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.current_player = "stockfish"  # Stockfish moves first

    def reset_game(self):
        """Reset the chess game."""
        self.board.reset()
        self.current_player = "stockfish"

    def next_move(self):
        """Make the next move depending on the current player."""
        if self.board.is_game_over():
            return f"Game Over! Result: {self.board.result()}"

        if self.current_player == "stockfish":
            stockfish.set_fen_position(self.board.fen())
            move = stockfish.get_best_move()
            if move:
                self.board.push(chess.Move.from_uci(move))
            self.current_player = "llm"
        else:
            try:
                move = query_ollama(self.board.fen())
                self.board.push(chess.Move.from_uci(move))
            except Exception as e:
                return f"Error: {e}"
            self.current_player = "stockfish"

        if self.board.is_game_over():
            return f"Game Over! Result: {self.board.result()}"

        return None


# Initialize game
game = ChessGame()

# Tkinter GUI
root = tk.Tk()
root.title("Chess Game")

# Create GUI elements
board_canvas = tk.Label(root)
board_canvas.pack()

status_label = tk.Label(root, text="", font=("Helvetica", 14))
status_label.pack()

button_frame = tk.Frame(root)
button_frame.pack()

next_move_button = tk.Button(button_frame, text="Next Move", command=lambda: make_next_move())
reset_button = tk.Button(button_frame, text="Reset Game", command=lambda: reset_game())
exit_button = tk.Button(button_frame, text="Exit", command=root.destroy)

next_move_button.grid(row=0, column=0, padx=5, pady=5)
reset_button.grid(row=0, column=1, padx=5, pady=5)
exit_button.grid(row=0, column=2, padx=5, pady=5)


def update_board_image():
    """Update the displayed board image."""
    board_image = render_board(game.board)
    photo = ImageTk.PhotoImage(board_image)
    board_canvas.config(image=photo)
    board_canvas.image = photo


def make_next_move():
    """Make the next move and update the board."""
    status = game.next_move()
    update_board_image()
    status_label.config(text=status or "")


def reset_game():
    """Reset the game and update the board."""
    game.reset_game()
    update_board_image()
    status_label.config(text="")


# Initialize board display
update_board_image()

# Run the Tkinter event loop
root.mainloop()
