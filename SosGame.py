from abc import ABC, abstractmethod

class SOSGameBase(ABC):
    def __init__(self, board_size):
        if board_size < 3:
            raise ValueError("Board size must be at least 3")
        self.board_size = board_size
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_turn_is_blue = True
        self.game_over = False
        self.winner = None

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
                for mult in [-1, 1]:
                    dr_m, dc_m = dr * mult, dc * mult
                    if self._is_valid(r + dr_m, c + dc_m) and self.board[r + dr_m][c + dc_m] == 'O' and \
                       self._is_valid(r + 2*dr_m, c + 2*dc_m) and self.board[r + 2*dr_m][c + 2*dc_m] == 'S':
                        found_soses.append(((r, c), (r + 2*dr_m, c + 2*dc_m)))
        
        return found_soses

    @abstractmethod
    def make_move(self, r, c, piece):
        pass

    def get_turn_owner_name(self):
        return "Blue" if self.current_turn_is_blue else "Red"

class SimpleGame(SOSGameBase):
    def __init__(self, board_size):
        super().__init__(board_size)

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
    def __init__(self, board_size):
        super().__init__(board_size)
        self.blue_score = 0
        self.red_score = 0

    def make_move(self, r, c, piece):
        if self.game_over or not self._is_valid(r, c) or self.board[r][c] != '':
            return [], False
            
        self.board[r][c] = piece
        soses_found = self._check_for_sos(r, c, piece)
        
        if soses_found:
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
