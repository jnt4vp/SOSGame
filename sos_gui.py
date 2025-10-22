import tkinter as tk
from tkinter import messagebox
from SosGame import SOSGame

class SOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        self.game = SOSGame()

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

        self.players_frame = tk.Frame(root)
        self.players_frame.pack(pady=5)

        self.blue_player_frame = tk.Frame(self.players_frame, padx=10, pady=5, relief="groove", borderwidth=2)
        self.blue_player_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(self.blue_player_frame, text="Blue player").pack()
        self.blue_piece_var = tk.StringVar(value="S")
        tk.Radiobutton(self.blue_player_frame, text="S", variable=self.blue_piece_var, value="S").pack(anchor=tk.W)
        tk.Radiobutton(self.blue_player_frame, text="O", variable=self.blue_piece_var, value="O").pack(anchor=tk.W)

        self.red_player_frame = tk.Frame(self.players_frame, padx=10, pady=5, relief="groove", borderwidth=2)
        self.red_player_frame.pack(side=tk.RIGHT, padx=20)
        tk.Label(self.red_player_frame, text="Red player").pack()
        self.red_piece_var = tk.StringVar(value="S")
        tk.Radiobutton(self.red_player_frame, text="S", variable=self.red_piece_var, value="S").pack(anchor=tk.W)
        tk.Radiobutton(self.red_player_frame, text="O", variable=self.red_piece_var, value="O").pack(anchor=tk.W)

        self.canvas_size = 300
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
        size = self.game.board_size
        cell_size = self.canvas_size / size
        
        col = int(event.x // cell_size)
        row = int(event.y // cell_size)

        piece = self.blue_piece_var.get() if self.game.current_turn_is_blue else self.red_piece_var.get()

        if self.game.make_move(row, col, piece):
            self.draw_piece(row, col, piece)
            self.update_turn_indicator()
            
    def draw_piece(self, row, col, piece):
        size = self.game.board_size
        cell_size = self.canvas_size / size
        x = col * cell_size + cell_size / 2
        y = row * cell_size + cell_size / 2
        self.canvas.create_text(x, y, text=piece.upper(), font=('Helvetica', int(cell_size * 0.6)))

    def draw_board(self):
        self.canvas.delete("all") 
        size = self.game.board_size
        cell_size = self.canvas_size / size

        for i in range(1, size):

            self.canvas.create_line(i * cell_size, 0, i * cell_size, self.canvas_size)
            self.canvas.create_line(0, i * cell_size, self.canvas_size, i * cell_size)

    def start_new_game(self):
        try:
            size = int(self.board_size_var.get())
            if size < 3:
                messagebox.showerror("Invalid Size", "Board size must be at least 3.")
                return
            mode = self.game_mode_var.get()
            self.game.new_game(size, mode)
            self.draw_board() 
            self.update_turn_indicator()
        except ValueError:
            messagebox.showerror("Invalid Size", "Please enter a valid number for board size.")

    def update_turn_indicator(self):
        self.turn_label.config(text=f"Current turn: {self.game.get_turn_owner_name()}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SOSGUI(root)
    root.mainloop()
