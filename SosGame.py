from abc import ABC, abstractmethod
import random

# Base class for the 2 types of players
class PlayerBase(ABC):
    def __init__(self, name, piece_choice):
        self.name = name
        self.piece_choice = piece_choice

    @abstractmethod
    def get_move(self, game):
        pass

# this is a human player
class HumanPlayer(PlayerBase):
    # Humans use the GUI to move, so this returns nothing
    def get_move(self, game):
        return None, None, None

# This is the computer player
class ComputerPlayer(PlayerBase):
    # Decides where the computer should move
    def get_move(self, game):
        empty_cells = []
        for r in range(game.board_size):
            for c in range(game.board_size):
                if game.board[r][c] == '':
                    empty_cells.append((r, c))

        if not empty_cells:
            return None, None, None

        # Try to find a winning move first
        for r, c in empty_cells:
            for piece in ['S', 'O']:
                temp_board = [row[:] for row in game.board]
                temp_board[r][c] = piece
                soses = self._check_for_sos_temp(r, c, piece, temp_board, game.board_size)
                if soses:
                    return r, c, piece

        # If no winning move pick a random area
        r, c = random.choice(empty_cells)
        piece = self.piece_choice
            
        return r, c, piece

    # Helper to check for sos on a temporary board
    def _check_for_sos_temp(self, r, c, piece, board, board_size):
        found_soses = []
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        def _is_valid(r_val, c_val):
            return 0 <= r_val < board_size and 0 <= c_val < board_size

        if piece == 'O':
            for dr, dc in directions:
                if _is_valid(r - dr, c - dc) and board[r - dr][c - dc] == 'S' and \
                   _is_valid(r + dr, c + dc) and board[r + dr][c + dc] == 'S':
                    found_soses.append(((r - dr, c - dc), (r + dr, c + dc)))
                    
        elif piece == 'S':
            for dr, dc in directions:
                r_o, c_o = r + dr, c + dc
                r_s, c_s = r + 2*dr, c + 2*dc
                if _is_valid(r_s, c_s) and board[r_s][c_s] == 'S' and \
                   _is_valid(r_o, c_o) and board[r_o][c_o] == 'O':
                    found_soses.append(((r, c), (r_s, c_s)))

                r_o, c_o = r - dr, c - dc
                r_s, c_s = r - 2*dr, c - 2*dc
                if _is_valid(r_s, c_s) and board[r_s][c_s] == 'S' and \
                   _is_valid(r_o, c_o) and board[r_o][c_o] == 'O':
                    found_soses.append(((r_s, c_s), (r, c)))
        
        return found_soses

# Base class for the game logic
class SOSGameBase(ABC):
    # Sets up the board and players
    def __init__(self, board_size, blue_player, red_player):
        if board_size < 3:
            raise ValueError("Board size must be at least 3")
        self.board_size = board_size
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_turn_is_blue = True
        self.game_over = False
        self.winner = None
        self.blue_player = blue_player
        self.red_player = red_player
        self.history = []  # Added to track the history of moves

    # Returns the player object for whoever's turn it is
    def get_current_player(self):
        return self.blue_player if self.current_turn_is_blue else self.red_player

    # Checks if a coordinate is on the board
    def _is_valid(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    # Checks if there are no empty spots left
    def is_board_full(self):
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == '':
                    return False
        return True

    # Looks for any sos patterns made by the last move
    def _check_for_sos(self, r, c, piece):
        found_soses = []
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        if piece == 'O':
            for dr, dc in directions:
                if self._is_valid(r - dr, c - dc) and self.board[r - dr][c - dc] == 'S' and \
                   self._is_valid(r + dr, c + dc) and self.board[r + dr][c + dc] == 'S':
                    found_soses.append(((r - dr, c - dc), (r + dr, c + dc)))
                    
        elif piece == 'S':
            for dr, dc in directions:
                r_o, c_o = r + dr, c + dc
                r_s, c_s = r + 2*dr, c + 2*dc
                if self._is_valid(r_s, c_s) and self.board[r_s][c_s] == 'S' and \
                   self._is_valid(r_o, c_o) and self.board[r_o][c_o] == 'O':
                    found_soses.append(((r, c), (r_s, c_s)))

                r_o, c_o = r - dr, c - dc
                r_s, c_s = r - 2*dr, c - 2*dc
                if self._is_valid(r_s, c_s) and self.board[r_s][c_s] == 'S' and \
                   self._is_valid(r_o, c_o) and self.board[r_o][c_o] == 'O':
                    found_soses.append(((r_s, c_s), (r, c)))
        
        return found_soses

    @abstractmethod
    def make_move(self, r, c, piece):
        pass

    # Gets the name of the current player
    def get_turn_owner_name(self):
        return self.get_current_player().name

# Logic for the Simple Game mode
class SimpleGame(SOSGameBase):
    def __init__(self, board_size, blue_player, red_player):
        super().__init__(board_size, blue_player, red_player)

    # Places a piece and checks if someone won
    def make_move(self, r, c, piece):
        if self.game_over or not self._is_valid(r, c) or self.board[r][c] != '':
            return [], False
            
        self.board[r][c] = piece
        self.history.append((r, c, piece)) # Record the move
        soses_found = self._check_for_sos(r, c, piece)
        
        if soses_found:
            self.game_over = True
            self.winner = self.get_turn_owner_name()
            return soses_found, True
            
        if self.is_board_full():
            self.game_over = True
            self.winner = None
            return [], True
            
        self.current_turn_is_blue = not self.current_turn_is_blue
        return [], True

# Logic for the General Game mode
class GeneralGame(SOSGameBase):
    def __init__(self, board_size, blue_player, red_player):
        super().__init__(board_size, blue_player, red_player)
        self.blue_score = 0
        self.red_score = 0

    # Places a piece and updates scores
    def make_move(self, r, c, piece):
        if self.game_over or not self._is_valid(r, c) or self.board[r][c] != '':
            return [], False
            
        self.board[r][c] = piece
        self.history.append((r, c, piece)) # Record the move
        soses_found = self._check_for_sos(r, c, piece)
        
        scored = bool(soses_found)
        
        if scored:
            points = len(soses_found)
            if self.current_turn_is_blue:
                self.blue_score += points
            else:
                self.red_score += points
        else:
            self.current_turn_is_blue = not self.current_turn_is_blue
            
        if self.is_board_full():
            self.game_over = True
            if self.blue_score > self.red_score:
                self.winner = "Blue"
            elif self.red_score > self.blue_score:
                self.winner = "Red"
            else:
                self.winner = None
                
        return soses_found, True
