import tkinter as tk
from tkinter import messagebox
from SosGame import SimpleGame, GeneralGame

class SOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        self.game = None
        self.cell_size = 100
        self.canvas_size = 300
        self.board_size = 3

        self.options_frame = tk.Frame(root)
        self.options_frame.pack(pady=5)

        self.game_mode_var = tk.StringVar(value="simple")
        tk.Label(self.options_frame, text="SOS").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(self.options_frame, text="Simple game", variable=self.game_mode_var, value="simple", command=self.start_new_game).pack(side=tk.LEFT)
        tk.Radiobutton(self.options_frame, text="General game", variable=self.game_mode_var, value="general", command=self.start_new_game).pack(side=tk.LEFT)

        tk.Label(self.options_frame, text="Board size").pack(side=tk.LEFT, padx=(20, 5))
        self.board_size_var = tk.StringVar(value="3")
        self.board_size_entry = tk.Entry(self.options_frame, textvariable=self.board_size_var, width=3)
        self.board_size_entry.pack(side=tk.LEFT)

        self.players_frame = tk.Frame(root)
        self.players_frame.pack(pady=5)

        self.blue_player_frame = tk.Frame(self.players_frame, padx=10, pady=5)
        self.blue_player_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(self.blue_player_frame, text="Blue player", fg="blue").pack()
        self.blue_piece_var = tk.StringVar(value="S")
        tk.Radiobutton(self.blue_player_frame, text="S", variable=self.blue_piece_var, value="S").pack(anchor=tk.W)
        tk.Radiobutton(self.blue_player_frame, text="O", variable=self.blue_piece_var, value="O").pack(anchor=tk.W)
        self.blue_score_label = tk.Label(self.blue_player_frame, text="Score: 0", fg="blue")
        self.blue_score_label.pack()

        self.red_player_frame = tk.Frame(self.players_frame, padx=10, pady=5)
        self.red_player_frame.pack(side=tk.RIGHT, padx=20)
        tk.Label(self.red_player_frame, text="Red player", fg="red").pack()
        self.red_piece_var = tk.StringVar(value="S")
        tk.Radiobutton(self.red_player_frame, text="S", variable=self.red_piece_var, value="S").pack(anchor=tk.W)
        tk.Radiobutton(self.red_player_frame, text="O", variable=self.red_piece_var, value="O").pack(anchor=tk.W)
        self.red_score_label = tk.Label(self.red_player_frame, text="Score: 0", fg="red")
        self.red_score_label.pack()

        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(pady=5)
        
        self.turn_label = tk.Label(self.bottom_frame, text="Current turn: Blue", font=('Helvetica', 12))
        self.turn_label.pack(side=tk.LEFT, padx=10)
        
        self.new_game_button = tk.Button(self.bottom_frame, text="New Game", command=self.start_new_game)
        self.new_game_button.pack(side=tk.RIGHT, padx=10)

        self.start_new_game()

    def on_canvas_click(self, event):
        if self.game is None or self.game.game_over:
            return

        col = int(event.x // self.cell_size)
        row = int(event.y // self.cell_size)

        player_making_move = self.game.get_turn_owner_name()
        piece = self.blue_piece_var.get() if player_making_move == "Blue" else self.red_piece_var.get()

        soses_found, move_made = self.game.make_move(row, col, piece)

        if move_made:
            self.draw_piece(row, col, piece)
            if soses_found:
                self.draw_sos_lines(soses_found, player_making_move.lower())
            
            self.update_game_status()
            self.check_for_game_over()
            
    def draw_piece(self, row, col, piece):
        x = col * self.cell_size + self.cell_size / 2
        y = row * self.cell_size + self.cell_size / 2
        self.canvas.create_text(x, y, text=piece.upper(), font=('Helvetica', int(self.cell_size * 0.6)))

    def draw_sos_lines(self, soses, color):
        for (r1, c1), (r2, c2) in soses:
            x1 = c1 * self.cell_size + self.cell_size / 2
            y1 = r1 * self.cell_size + self.cell_size / 2
            x2 = c2 * self.cell_size + self.cell_size / 2
            y2 = r2 * self.cell_size + self.cell_size / 2
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=3)

    def draw_board(self):
        self.canvas.delete("all")
        self.canvas_size = min(max(self.board_size * 30, 200), 500) 
        self.cell_size = self.canvas_size / self.board_size
        self.canvas.config(width=self.canvas_size, height=self.canvas_size)

        for i in range(1, self.board_size):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.canvas_size)
            self.canvas.create_line(0, i * self.cell_size, self.canvas_size, i * self.cell_size)

    def start_new_game(self):
        try:
            size = int(self.board_size_var.get())
            if size < 3:
                messagebox.showerror("Invalid Size", "Board size must be at least 3.")
                self.board_size_var.set(str(self.board_size))
                return
            self.board_size = size
        except ValueError:
            messagebox.showerror("Invalid Size", "Please enter a valid number for board size.")
            self.board_size_var.set(str(self.board_size))
            return
        
        mode = self.game_mode_var.get()
        if mode == "simple":
            self.game = SimpleGame(self.board_size)
        else:
            self.game = GeneralGame(self.board_size)
            
        self.draw_board()
        self.update_game_status()

    def update_game_status(self):
        if self.game is None:
            return

        self.turn_label.config(text=f"Current turn: {self.game.get_turn_owner_name()}")

        if isinstance(self.game, GeneralGame):
            self.blue_score_label.config(text=f"Score: {self.game.blue_score}")
            self.red_score_label.config(text=f"Score: {self.game.red_score}")
        else:
            self.blue_score_label.config(text="")
            self.red_score_label.config(text="")

    def check_for_game_over(self):
        if self.game.game_over:
            winner = self.game.winner
            if winner:
                message = f"{winner} wins!"
            else:
                message = "It's a draw!"
            messagebox.showinfo("Game Over", message)
