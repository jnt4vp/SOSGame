class SOSGame:
    def __init__(self, board_size=3):
        self.board_size = board_size
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_turn_is_blue = True 
        self.game_mode = 'simple' 

    def new_game(self, board_size, game_mode):
        self.board_size = board_size
        self.game_mode = game_mode
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_turn_is_blue = True
        print(f"New game started. Mode: {self.game_mode}, Size: {self.board_size}x{self.board_size}")

    def make_move(self, row, col, piece):
        if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == '':
            self.board[row][col] = piece.upper()
            self.current_turn_is_blue = not self.current_turn_is_blue
            return True
        return False
        
    def get_turn_owner_name(self):
        return "Blue" if self.current_turn_is_blue else "Red"