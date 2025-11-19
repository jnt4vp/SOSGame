from abc import ABC, abstractmethod
import random

class PlayerBase(ABC):
    def __init__(self, name, piece_choice):
        self.name = name
        self.piece_choice = piece_choice

    @abstractmethod
    def get_move(self, game):
        pass

class HumanPlayer(PlayerBase):
    def get_move(self, game):
        return None, None, None

class ComputerPlayer(PlayerBase):
    def get_move(self, game):
        empty_cells = []
        for r in range(game.board_size):
            for c in range(game.board_size):
                if game.board[r][c] == '':
                    empty_cells.append((r, c))

        if not empty_cells:
            return None, None, None

        for r, c in empty_cells:
            for piece in ['S', 'O']:
                temp_board = [row[:] for row in game.board]
                temp_board[r][c] = piece
                soses = self._check_for_sos_temp(r, c, piece, temp_board, game.board_size)
                if soses:
                    return r, c, piece

        r, c = random.choice(empty_cells)
        piece = self.piece_choice
            
        return r, c, piece

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

class SOSGameBase(ABC):
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

    def get_current_player(self):
        return self.blue_player if self.current_turn_is_blue else self.red_player

    def _is_valid(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def is_board_full(self):
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == '':
                    return False
        return True

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

    def get_turn_owner_name(self):
        return self.get_current_player().name

class SimpleGame(SOSGameBase):
    def __init__(self, board_size, blue_player, red_player):
        super().__init__(board_size, blue_player, red_player)

    def make_move(self, r, c, piece):
        if self.game_over or not self._is_valid(r, c) or self.board[r][c] != '':
            return [], False
            
        self.board[r][c] = piece
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

class GeneralGame(SOSGameBase):
    def __init__(self, board_size, blue_player, red_player):
        super().__init__(board_size, blue_player, red_player)
        self.blue_score = 0
        self.red_score = 0

    def make_move(self, r, c, piece):
        if self.game_over or not self._is_valid(r, c) or self.board[r][c] != '':
            return [], False
            
        self.board[r][c] = piece
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
