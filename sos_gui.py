# sos_gui.py

import tkinter as tk
from tkinter import messagebox
from sos_game import SOSGame

class SOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        self.game = SOSGame()

        # --- Top Frame for Game Options ---
        self.options_frame = tk.Frame(root)
        self.options_frame.pack(pady=5)

        self.game_mode_var = tk.StringVar(value="simple")
        tk.Label(self.options_frame, text="SOS").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(self.options_frame, text="Simple game", variable=self.game_mode_var, value="simple").pack(side=tk.LEFT)
        tk.Radiobutton(self.options_frame, text="General game", variable=self.game_mode_var, value="general").pack(side=tk.LEFT)

        tk.Label(self.options_frame, text="Board size").pack(side=tk.LEFT, padx=(20, 5))
        self.board_size_var = tk.StringVar(value="3")
        self.board_size_entry = tk.Entry(self.options_frame, textvariable=self.board_size_var, width=3)
        self.board_size_entry.pack(side=tk.LEFT)

        # NEW: --- Middle Frame for Player Controls ---
        self.players_frame = tk.Frame(root)
        self.players_frame.pack(pady=5)

        # Blue Player Controls
        self.blue_player_frame = tk.Frame(self.players_frame, padx=10, pady=5, relief="groove", borderwidth=2)
        self.blue_player_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(self.blue_player_frame, text="Blue player").pack()
        self.blue_piece_var = tk.StringVar(value="S")
        tk.Radiobutton(self.blue_player_frame, text="S", variable=self.blue_piece_var, value="S").pack(anchor=tk.W)
        tk.Radiobutton(self.blue_player_frame, text="O", variable=self.blue_piece_var, value="O").pack(anchor=tk.W)

        # Red Player Controls
        self.red_player_frame = tk.Frame(self.players_frame, padx=10, pady=5, relief="groove", borderwidth=2)
        self.red_player_frame.pack(side=tk.RIGHT, padx=20)
        tk.Label(self.red_player_frame, text="Red player").pack()
        self.red_piece_var = tk.StringVar(value="S")
        tk.Radiobutton(self.red_player_frame, text="S", variable=self.red_piece_var, value="S").pack(anchor=tk.W)
        tk.Radiobutton(self.red_player_frame, text="O", variable=self.red_piece_var, value="O").pack(anchor=tk.W)

        # --- Canvas for the Game Board ---
        self.canvas_size = 300
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(pady=10)
        # NEW: Bind the click event
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # --- Bottom Frame for Turn Indicator and New Game ---
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(pady=5)
        
        self.turn_label = tk.Label(self.bottom_frame, text="Current turn: Blue", font=('Helvetica', 12))
        self.turn_label.pack(side=tk.LEFT, padx=10)
        
        self.new_game_button = tk.Button(self.bottom_frame, text="New Game", command=self.start_new_game)
        self.new_game_button.pack(side=tk.RIGHT, padx=10)

        self.start_new_game()

    # NEW: Method to handle clicks on the board
    def on_canvas_click(self, event):
        size = self.game.board_size
        cell_size = self.canvas_size / size
        
        col = int(event.x // cell_size)
        row = int(event.y // cell_size)

        # Determine which player's piece to use
        piece = self.blue_piece_var.get() if self.game.current_turn_is_blue else self.red_piece_var.get()

        # Attempt to make a move in the game logic
        if self.game.make_move(row, col, piece):
            # If successful, draw the piece and update the turn display
            self.draw_piece(row, col, piece)
            self.update_turn_indicator()
            
    # NEW: Method to draw a single S or O
    def draw_piece(self, row, col, piece):
        size = self.game.board_size
        cell_size = self.canvas_size / size
        x = col * cell_size + cell_size / 2
        y = row * cell_size + cell_size / 2
        self.canvas.create_text(x, y, text=piece.upper(), font=('Helvetica', int(cell_size * 0.6)))

    # NEW: Method to draw the board gridlines
    def draw_board(self):
        self.canvas.delete("all") # Clear the canvas
        size = self.game.board_size
        cell_size = self.canvas_size / size

        for i in range(1, size):
            # Vertical lines
            self.canvas.create_line(i * cell_size, 0, i * cell_size, self.canvas_size)
            # Horizontal lines
            self.canvas.create_line(0, i * cell_size, self.canvas_size, i * cell_size)

    def start_new_game(self):
        try:
            size = int(self.board_size_var.get())
            if size < 3:
                messagebox.showerror("Invalid Size", "Board size must be at least 3.")
                return
            mode = self.game_mode_var.get()
            self.game.new_game(size, mode)
            self.draw_board() # MODIFIED: Call draw_board instead of printing
            self.update_turn_indicator()
        except ValueError:
            messagebox.showerror("Invalid Size", "Please enter a valid number for board size.")

    def update_turn_indicator(self):
        self.turn_label.config(text=f"Current turn: {self.game.get_turn_owner_name()}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SOSGUI(root)
    root.mainloop()