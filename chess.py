from ollama import Client
import tkinter as tk
from tkinter import messagebox
import chess
import chess.svg
import requests
from stockfish import Stockfish
from PIL import Image, ImageTk
from io import BytesIO
import PySimpleGUI as sg
import chess
import chess.svg
import requests
from stockfish import Stockfish
from PIL import Image, ImageTk
from io import BytesIO
import cairosvg

# Initialize Stockfish
STOCKFISH_PATH = "path/to/stockfish/"
stockfish = Stockfish(STOCKFISH_PATH)

# Ollama API Configuration
OLLAMA_MODEL = "llama3.2:1b"
OLLAMA_URL = "http://x.y.z.k:11434/"


def query_ollama(board_fen):
    """Query the Ollama API for the LLM's move."""
    print("Query sedning")
    #print(prompt)
    client = Client(host='http://192.168.20.110:11434/', headers={'x-some-header': 'some-value'})

    prompt = f"You are a chess solving agent (black color). We will give you the current chessboard FEN.  Give the next move only. The current chessboard FEN is {board_fen}. What is your next move? Give only one move in Universal Chess Interface (UCI) format like d6d1. Where d6 is the old position and d1 is the new position. Answer in Universal Chess Interface (UCI) format like d6d1. You can only write 4 character."
    print(prompt)
    response = client.chat(model='llama3.2', messages=[{'role': 'user','content': prompt,},])

    #move = response.json()['content'].strip()
    print(response['message']['content'])
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
                print (f"Error: {e}")
                return f"Error: {e}"              
            self.current_player = "stockfish"

        if self.board.is_game_over():
            return f"Game Over! Result: {self.board.result()}"

        return None

# Initialize game
game = ChessGame()

# GUI Layout
layout = [
    [sg.Text("Stockfish  Chess", size=(30, 1), justification="center", font=("Helvetica", 16))],
    [sg.Image(key="-BOARD-")],
    [sg.Button("Next Move"), sg.Button("Reset Game"), sg.Button("Exit")],
    [sg.Text("", size=(40, 1), key="-STATUS-")]
]

# Create the window
window = sg.Window("Chess Game", layout, finalize=True)

# Initial board display
board_image = ImageTk.PhotoImage(render_board(game.board))
window["-BOARD-"].update(data=board_image)

# Event loop
while True:
    event, values = window.read(timeout=100)
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    elif event == "Next Move":
        status = game.next_move()
        board_image = ImageTk.PhotoImage(render_board(game.board))
        window["-BOARD-"].update(data=board_image)
        if status:
            window["-STATUS-"].update(status)
    elif event == "Reset Game":
        game.reset_game()
        board_image = ImageTk.PhotoImage(render_board(game.board))
        window["-BOARD-"].update(data=board_image)
        window["-STATUS-"].update("")

# Close the window
window.close()
