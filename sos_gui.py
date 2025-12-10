import tkinter as tk
from tkinter import messagebox
import random
import math
from SosGame import SimpleGame, GeneralGame, HumanPlayer, ComputerPlayer

#Theme configuration
THEME = {
    "bg_main": "#222222",
    "bg_panel": "#FFFFFF",
    "fg_text": "#000000",
    "board_bg": "#FFF8E1",
    "grid_color": "#000000",
    "highlight": "#FFD700",
    "red_player": "#DA291C",
    "blue_player": "#00A4EF",
    "font_main": ("Helvetica", 10, "bold"),
    "font_title": ("Impact", 14),
    "font_piece": ("Arial", 12, "bold")
}

class SOSGUI:
    # Sets up the window and all the buttons
    def __init__(self, root):
        self.root = root
        self.root.title("SOS: Incredible Edition")
        self.root.configure(bg=THEME["bg_main"])
        
        self.game = None
        self.cell_size = 100
        self.canvas_size = 500
        self.board_size = 3
        self.is_processing_move = False
        self.is_replaying = False
        self.replay_moves = []
        
        # Animation control
        self.animation_running = False
        self.animation_objects = []

        # Options Frame
        self.options_frame = tk.Frame(root, bg=THEME["bg_panel"], bd=2, relief="raised")
        self.options_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(self.options_frame, text="GAME MODE", bg=THEME["bg_panel"], font=THEME["font_main"]).pack(side=tk.LEFT, padx=10)
        self.game_mode_var = tk.StringVar(value="simple")
        tk.Radiobutton(self.options_frame, text="Simple", variable=self.game_mode_var, value="simple", command=self.on_mode_change, bg=THEME["bg_panel"]).pack(side=tk.LEFT)
        tk.Radiobutton(self.options_frame, text="General", variable=self.game_mode_var, value="general", command=self.on_mode_change, bg=THEME["bg_panel"]).pack(side=tk.LEFT)

        tk.Label(self.options_frame, text="Board Size:", bg=THEME["bg_panel"], font=THEME["font_main"]).pack(side=tk.LEFT, padx=(20, 5))
        self.board_size_var = tk.StringVar(value="3")
        self.board_size_entry = tk.Entry(self.options_frame, textvariable=self.board_size_var, width=3, font=("Arial", 12))
        self.board_size_entry.pack(side=tk.LEFT)

        # Players Frame
        self.players_frame = tk.Frame(root, bg=THEME["bg_main"])
        self.players_frame.pack(pady=5, fill="x")

        # Blue Player
        self.blue_player_frame = tk.Frame(self.players_frame, bg="white", bd=3, relief="ridge")
        self.blue_player_frame.pack(side=tk.LEFT, padx=20, fill="x", expand=True)
        tk.Label(self.blue_player_frame, text="BLUE TEAM", fg=THEME["blue_player"], font=THEME["font_title"], bg="white").pack(pady=5)
        self.blue_player_type_var = tk.StringVar(value="human")
        tk.Radiobutton(self.blue_player_frame, text="Human", variable=self.blue_player_type_var, value="human", command=self.on_player_change, bg="white").pack(anchor=tk.W)
        tk.Radiobutton(self.blue_player_frame, text="Computer", variable=self.blue_player_type_var, value="computer", command=self.on_player_change, bg="white").pack(anchor=tk.W)
        tk.Frame(self.blue_player_frame, height=2, bg=THEME["blue_player"]).pack(fill="x", pady=5)
        self.blue_piece_var = tk.StringVar(value="S")
        tk.Radiobutton(self.blue_player_frame, text="S", variable=self.blue_piece_var, value="S", bg="white").pack(anchor=tk.W)
        tk.Radiobutton(self.blue_player_frame, text="O", variable=self.blue_piece_var, value="O", bg="white").pack(anchor=tk.W)
        self.blue_score_label = tk.Label(self.blue_player_frame, text="Score: 0", fg=THEME["blue_player"], font=("Arial", 12, "bold"), bg="white")
        self.blue_score_label.pack(pady=5)

        # Red Player
        self.red_player_frame = tk.Frame(self.players_frame, bg="white", bd=3, relief="ridge")
        self.red_player_frame.pack(side=tk.RIGHT, padx=20, fill="x", expand=True)
        tk.Label(self.red_player_frame, text="RED TEAM", fg=THEME["red_player"], font=THEME["font_title"], bg="white").pack(pady=5)
        self.red_player_type_var = tk.StringVar(value="human")
        tk.Radiobutton(self.red_player_frame, text="Human", variable=self.red_player_type_var, value="human", command=self.on_player_change, bg="white").pack(anchor=tk.W)
        tk.Radiobutton(self.red_player_frame, text="Computer", variable=self.red_player_type_var, value="computer", command=self.on_player_change, bg="white").pack(anchor=tk.W)
        tk.Frame(self.red_player_frame, height=2, bg=THEME["red_player"]).pack(fill="x", pady=5)
        self.red_piece_var = tk.StringVar(value="S")
        tk.Radiobutton(self.red_player_frame, text="S", variable=self.red_piece_var, value="S", bg="white").pack(anchor=tk.W)
        tk.Radiobutton(self.red_player_frame, text="O", variable=self.red_piece_var, value="O", bg="white").pack(anchor=tk.W)
        self.red_score_label = tk.Label(self.red_player_frame, text="Score: 0", fg=THEME["red_player"], font=("Arial", 12, "bold"), bg="white")
        self.red_score_label.pack(pady=5)

        # Canvas 
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg=THEME["board_bg"], highlightthickness=0)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Bottom Frame
        self.bottom_frame = tk.Frame(root, bg=THEME["bg_panel"], bd=2, relief="raised")
        self.bottom_frame.pack(pady=10, fill="x", padx=10)
        
        self.turn_label = tk.Label(self.bottom_frame, text="Current turn: Blue", font=("Impact", 14), bg=THEME["bg_panel"])
        self.turn_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.record_game_var = tk.IntVar()
        self.record_cb = tk.Checkbutton(self.bottom_frame, text="Record", variable=self.record_game_var, bg=THEME["bg_panel"], font=THEME["font_main"])
        self.record_cb.pack(side=tk.LEFT, padx=10)

        self.replay_button = tk.Button(self.bottom_frame, text="Replay", command=self.start_replay, bg="black", fg="black", font=THEME["font_main"])
        self.replay_button.pack(side=tk.LEFT, padx=10)

        self.new_game_button = tk.Button(self.bottom_frame, text="Reset", command=self.start_new_game_manual, bg=THEME["red_player"], fg="black", font=THEME["font_main"])
        self.new_game_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.start_new_game()

    # Starts a game when the button is clicked
    def start_new_game_manual(self):
        self.stop_mlg_chaos()
        self.is_replaying = False
        self.start_new_game()

    # Restarts the game if the mode changes
    def on_mode_change(self):
        if not self.is_replaying:
            self.stop_mlg_chaos()
            self.start_new_game()

    # Restarts the game if the player type changes
    def on_player_change(self):
        if not self.is_replaying:
            self.stop_mlg_chaos()
            self.start_new_game()

    # Highlights the box under the mouse
    def on_mouse_move(self, event):
        if self.game is None or self.game.game_over or self.is_replaying:
            return
            
        current_player = self.game.get_current_player()
        if not isinstance(current_player, HumanPlayer):
            return

        col = int(event.x // self.cell_size)
        row = int(event.y // self.cell_size)

        self.canvas.delete("highlight")

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=THEME["highlight"], outline="", tags="highlight")
            self.canvas.tag_lower("highlight")

    # Handles what happens when you click the board
    def on_canvas_click(self, event):
        if self.game is None or self.game.game_over or self.is_processing_move or self.is_replaying:
            return

        current_player = self.game.get_current_player()
        if isinstance(current_player, HumanPlayer):
            col = int(event.x // self.cell_size)
            row = int(event.y // self.cell_size)
            
            piece = self.blue_piece_var.get() if self.game.current_turn_is_blue else self.red_piece_var.get()
            
            soses_found, move_made = self.game.make_move(row, col, piece)

            if move_made:
                self.handle_move_result(row, col, piece, soses_found)
                self.handle_turn()
                self.canvas.delete("highlight")

    # Updates the board after a move is made
    def handle_move_result(self, row, col, piece, soses_found):
        self.draw_piece(row, col, piece)
        if soses_found:
            player_name = self.game.get_turn_owner_name() 
            color = THEME["blue_player"] if "Blue" in player_name else THEME["red_player"]
            self.draw_sos_lines(soses_found, color)
        
        self.update_game_status()
        self.check_for_game_over()
        
    # Logic for the computer to take its turn
    def handle_computer_move(self):
        if self.game.game_over:
            return

        current_player = self.game.get_current_player()
        if isinstance(current_player, ComputerPlayer):
            self.is_processing_move = True
            
            r, c, piece = current_player.get_move(self.game)
            
            if r is not None:
                soses_found, move_made = self.game.make_move(r, c, piece)
                if move_made:
                    self.handle_move_result(r, c, piece, soses_found)
                    self.root.after(500, self.handle_turn)
                else:
                    self.is_processing_move = False
            else:
                self.is_processing_move = False

    # Decides whose turn it is
    def handle_turn(self):
        if self.game.game_over or self.is_replaying:
            self.is_processing_move = False
            return
            
        current_player = self.game.get_current_player()
        
        if isinstance(current_player, ComputerPlayer):
            self.handle_computer_move()
        else:
            self.is_processing_move = False
            
    # Draws the S or O on the screen
    def draw_piece(self, row, col, piece):
        x = col * self.cell_size + self.cell_size / 2
        y = row * self.cell_size + self.cell_size / 2
        self.canvas.create_text(x, y, text=piece.upper(), fill="black", font=("Arial", int(self.cell_size * 0.6), "bold"))

    # Draws the line when a point is scored
    def draw_sos_lines(self, soses, color):
        for (r1, c1), (r2, c2) in soses:
            x1 = c1 * self.cell_size + self.cell_size / 2
            y1 = r1 * self.cell_size + self.cell_size / 2
            x2 = c2 * self.cell_size + self.cell_size / 2
            y2 = r2 * self.cell_size + self.cell_size / 2
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=5, capstyle=tk.ROUND)

    # Draws the grid lines
    def draw_board(self):
        self.canvas.delete("all")
        desired_size = self.board_size * 80
        available_height = self.root.winfo_height() - 250
        available_width = self.root.winfo_width() - 50
        
        if available_height < 100: available_height = 800
        if available_width < 100: available_width = 800
        
        self.canvas_size = max(min(available_height, available_width, desired_size), 300)
        self.cell_size = self.canvas_size / self.board_size
        self.canvas.config(width=self.canvas_size, height=self.canvas_size)

        for i in range(1, self.board_size):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.canvas_size, width=2, fill=THEME["grid_color"])
            self.canvas.create_line(0, i * self.cell_size, self.canvas_size, i * self.cell_size, width=2, fill=THEME["grid_color"])
        
        if self.game:
            for r in range(self.board_size):
                for c in range(self.board_size):
                    piece = self.game.board[r][c]
                    if piece:
                        self.draw_piece(r, c, piece)

    # Resets everything and starts a fresh game
    def start_new_game(self):
        if self.is_processing_move:
            return
            
        self.stop_mlg_chaos()

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
        
        blue_type = self.blue_player_type_var.get()
        red_type = self.red_player_type_var.get()
        blue_piece_choice = self.blue_piece_var.get()
        red_piece_choice = self.red_piece_var.get()
        
        if blue_type == "human":
            blue_player = HumanPlayer("Blue", blue_piece_choice)
        else:
            blue_player = ComputerPlayer("Blue", blue_piece_choice)

        if red_type == "human":
            red_player = HumanPlayer("Red", red_piece_choice)
        else:
            red_player = ComputerPlayer("Red", red_piece_choice)
        
        mode = self.game_mode_var.get()
        if mode == "simple":
            self.game = SimpleGame(self.board_size, blue_player, red_player)
        else:
            self.game = GeneralGame(self.board_size, blue_player, red_player)
            
        self.draw_board()
        self.update_game_status()
        
        if not self.is_replaying:
            self.handle_turn()

    # Updates the labels for whose turn it is and the score
    def update_game_status(self):
        if self.game is None:
            return

        player_name = self.game.get_turn_owner_name()
        fg_color = THEME["blue_player"] if "Blue" in player_name else THEME["red_player"]
        self.turn_label.config(text=f"Current Turn: {player_name}", fg=fg_color)

        if isinstance(self.game, GeneralGame):
            self.blue_score_label.config(text=f"Score: {self.game.blue_score}")
            self.red_score_label.config(text=f"Score: {self.game.red_score}")
        else:
            self.blue_score_label.config(text="")
            self.red_score_label.config(text="")

    # Checks if the game has ended and shows the winner
    def check_for_game_over(self):
        if self.game.game_over:
            if not self.is_replaying and self.record_game_var.get() == 1:
                self.save_game_to_file()
                
            winner = self.game.winner
            # Trigger the Insane MLG Mode
            self.trigger_mlg_chaos(winner)

            self.is_processing_move = False
            self.is_replaying = False

    # Saves the move history to a text file
    def save_game_to_file(self):
        try:
            with open("game_record.txt", "w") as f:
                mode = self.game_mode_var.get()
                blue_type = self.blue_player_type_var.get()
                red_type = self.red_player_type_var.get()
                f.write(f"{self.board_size}\n")
                f.write(f"{mode}\n")
                f.write(f"{blue_type}\n")
                f.write(f"{red_type}\n")
                
                for move in self.game.history:
                    f.write(f"{move[0]},{move[1]},{move[2]}\n")
            print("Game recorded to game_record.txt")
        except Exception as e:
            print(f"Error saving game: {e}")

    # Reads the file and starts the replay mode
    def start_replay(self):
        self.stop_mlg_chaos()
        try:
            with open("game_record.txt", "r") as f:
                lines = f.readlines()
            
            if not lines:
                messagebox.showerror("Error", "Game record is empty.")
                return

            self.is_replaying = True
            
            size = int(lines[0].strip())
            mode = lines[1].strip()
            blue_type = lines[2].strip()
            red_type = lines[3].strip()
            
            self.board_size_var.set(str(size))
            self.game_mode_var.set(mode)
            self.blue_player_type_var.set(blue_type)
            self.red_player_type_var.set(red_type)
            
            self.start_new_game()
            
            self.replay_moves = []
            for line in lines[4:]:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    self.replay_moves.append((int(parts[0]), int(parts[1]), parts[2]))
            
            self.process_next_replay_move()
            
        except FileNotFoundError:
            messagebox.showerror("Error", "No recorded game found (game_record.txt).")
        except Exception as e:
            self.is_replaying = False
            messagebox.showerror("Error", f"Error reading replay file: {e}")

    # Plays the next move in the replay list
    def process_next_replay_move(self):
        if not self.is_replaying or not self.replay_moves:
            return

        r, c, piece = self.replay_moves.pop(0)
        soses_found, move_made = self.game.make_move(r, c, piece)
        self.handle_move_result(r, c, piece, soses_found)
        
        if self.replay_moves and not self.game.game_over:
            self.root.after(1000, self.process_next_replay_move)

    
    # Makes the screen go crazy when someone wins
    def trigger_mlg_chaos(self, winner):
        self.animation_running = True
        self.animation_objects = []
        
        win_text = f"{winner} WINS!" if winner else "DRAW!"
        mlg_phrases = ["MOM GET THE CAMERA", "EZ GAME", "OH BABY A TRIPLE!", "SAMPLE TEXT", "SOS CONFIRMED", "NO SCOPE", "REKT", "GG"]
        colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF"]
        
        def animate_frame():
            if not self.animation_running:
                return

            random_bg = random.choice(colors)
            self.canvas.configure(bg=random_bg)

            if random.random() < 0.3: # 30% chance per frame
                text = random.choice(mlg_phrases)
                x = random.randint(0, self.canvas_size)
                y = random.randint(0, self.canvas_size)
                color = random.choice(colors)
                size = random.randint(20, 40)
                font = ("Impact", size)
                tag = f"chaos_{random.randint(0, 10000)}"
                self.canvas.create_text(x, y, text=text, fill=color, font=font, tags=("chaos", tag))
                self.animation_objects.append(tag)

            for _ in range(5):
                x = random.randint(0, self.canvas_size)
                y = random.randint(0, self.canvas_size)
                color = random.choice(colors)
                size = random.randint(5, 15)
                self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color, tags="chaos")

            self.canvas.delete("winner_text")
            pulse_size = 40 + int(20 * math.sin(time.time() * 10))
            self.canvas.create_text(self.canvas_size/2, self.canvas_size/2, text=win_text, 
                                    font=("Impact", pulse_size), fill="white", tags="winner_text")
            
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            self.canvas.move("all", dx, dy)

            # Loop
            self.root.after(100, animate_frame)

        import time
        animate_frame()

    # Stops the animation
    def stop_mlg_chaos(self):
        self.animation_running = False
        self.canvas.delete("chaos")
        self.canvas.delete("winner_text")
        self.canvas.configure(bg=THEME["board_bg"])
