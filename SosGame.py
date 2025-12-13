from abc import ABC, abstractmethod
import random
import json
import urllib.request
import urllib.error
import time

CLAUDE_API_KEY = "key" 


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
    def __init__(self, name, piece_choice):
        super().__init__(name, piece_choice)
        self.model = "claude-3-haiku-20240307" 
        self.system_prompt = (
            "You are an expert SOS game player. "
            "Output move as JSON: {\"row\": <int>, \"col\": <int>, \"piece\": \"<S or O>\"}."
        )

    def get_move(self, game):
        empty_cells = []
        for r in range(game.board_size):
            for c in range(game.board_size):
                if game.board[r][c] == '':
                    empty_cells.append((r, c))

        if not empty_cells:
            return None, None, None

        print(f"AI ({self.name}) is thinking...")

        # 1. Attempt Claude Move
        if "sk-ant" in CLAUDE_API_KEY:
            try:
                move = self._get_llm_move_direct(game, empty_cells)
                if move:
                    return move
            except Exception as e:
                print(f"  > Claude Error: {e}. Switching to fallback strategy.")
        else:
            print("  > API Key missing. Switching to fallback strategy.")

        # 2. Fallback Strategy (Ensures video never fails)
        time.sleep(0.5) 
        
        # Try to win immediately
        for r, c in empty_cells:
            for piece in ['S', 'O']:
                temp_board = [row[:] for row in game.board]
                temp_board[r][c] = piece
                soses = self._check_for_sos_temp(r, c, piece, temp_board, game.board_size)
                if soses:
                    print(f"AI (Fallback) chose winning move: {r}, {c}, {piece}")
                    return r, c, piece

        # Random move
        r, c = random.choice(empty_cells)
        return r, c, self.piece_choice

    def _get_llm_move_direct(self, game, empty_cells):
        # 1. Prepare Board String
        board_str = ""
        for r in range(game.board_size):
            row_str = " | ".join([c if c else " " for c in game.board[r]])
            board_str += f"Row {r}: [{row_str}]\n"

        # 2. Construct Prompt
        user_message = (
            f"Board:\n{board_str}\n"
            f"Valid Moves: {empty_cells}\n"
            f"You are {self.name} ('{self.piece_choice}').\n"
            "If you can make an SOS (S-O-S pattern), DO IT. Otherwise block or place randomly.\n"
            "Respond ONLY with valid JSON."
        )

        # 3. Call Anthropic API (Direct HTTP Request)
        url = "https://api.anthropic.com/v1/messages"
        
        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "system": self.system_prompt,
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'content-type': 'application/json',
                'x-api-key': CLAUDE_API_KEY,
                'anthropic-version': '2023-06-01'
            }
        )

        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['content'][0]['text']
            
            # Extract JSON from potential text wrapper
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = content[start:end]
                data = json.loads(json_str)
                
                r, c = int(data["row"]), int(data["col"])
                piece = str(data["piece"]).upper()

                if (r, c) in empty_cells and piece in ['S', 'O']:
                    print(f"AI (Claude) decided: {r}, {c}, {piece}")
                    return r, c, piece
            
        return None

    def _check_for_sos_temp(self, r, c, piece, board, board_size):
        found = []
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        def valid(rv, cv): return 0 <= rv < board_size and 0 <= cv < board_size

        if piece == 'O':
            for dr, dc in dirs:
                if valid(r-dr, c-dc) and board[r-dr][c-dc]=='S' and valid(r+dr, c+dc) and board[r+dr][c+dc]=='S':
                    found.append(1)
        elif piece == 'S':
            for dr, dc in dirs:
                if valid(r+2*dr, c+2*dc) and board[r+2*dr][c+2*dc]=='S' and valid(r+dr, c+dc) and board[r+dr][c+dc]=='O':
                    found.append(1)
                if valid(r-2*dr, c-2*dc) and board[r-2*dr][c-2*dc]=='S' and valid(r-dr, c-dc) and board[r-dr][c-dc]=='O':
                    found.append(1)
        return found

class SOSGameBase(ABC):
    def __init__(self, board_size, blue_player, red_player):
        self.board_size = board_size
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_turn_is_blue = True
        self.game_over = False
        self.winner = None
        self.blue_player = blue_player
        self.red_player = red_player
        self.history = []

    def get_current_player(self):
        return self.blue_player if self.current_turn_is_blue else self.red_player

    def _is_valid(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def is_board_full(self):
        return all(self.board[r][c] != '' for r in range(self.board_size) for c in range(self.board_size))

    def _check_for_sos(self, r, c, piece):
        found = []
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        if piece == 'O':
            for dr, dc in dirs:
                if self._is_valid(r-dr, c-dc) and self.board[r-dr][c-dc]=='S' and self._is_valid(r+dr, c+dc) and self.board[r+dr][c+dc]=='S':
                    found.append(((r-dr, c-dc), (r+dr, c+dc)))
        elif piece == 'S':
            for dr, dc in dirs:
                if self._is_valid(r+2*dr, c+2*dc) and self.board[r+2*dr][c+2*dc]=='S' and self._is_valid(r+dr, c+dc) and self.board[r+dr][c+dc]=='O':
                    found.append(((r, c), (r+2*dr, c+2*dc)))
                if self._is_valid(r-2*dr, c-2*dc) and self.board[r-2*dr][c-2*dc]=='S' and self._is_valid(r-dr, c-dc) and self.board[r-dr][c-dc]=='O':
                    found.append(((r-2*dr, c-2*dc), (r, c)))
        return found

    @abstractmethod
    def make_move(self, r, c, piece): pass
    def get_turn_owner_name(self): return self.get_current_player().name

class SimpleGame(SOSGameBase):
    def make_move(self, r, c, piece):
        if self.game_over or not self._is_valid(r, c) or self.board[r][c] != '': return [], False
        self.board[r][c] = piece
        self.history.append((r, c, piece))
        soses = self._check_for_sos(r, c, piece)
        if soses:
            self.game_over = True
            self.winner = self.get_turn_owner_name()
            return soses, True
        if self.is_board_full():
            self.game_over = True
            return [], True
        self.current_turn_is_blue = not self.current_turn_is_blue
        return [], True

class GeneralGame(SOSGameBase):
    def __init__(self, size, blue, red):
        super().__init__(size, blue, red)
        self.blue_score = 0
        self.red_score = 0
    def make_move(self, r, c, piece):
        if self.game_over or not self._is_valid(r, c) or self.board[r][c] != '': return [], False
        self.board[r][c] = piece
        self.history.append((r, c, piece))
        soses = self._check_for_sos(r, c, piece)
        if soses:
            pts = len(soses)
            if self.current_turn_is_blue: self.blue_score += pts
            else: self.red_score += pts
        else:
            self.current_turn_is_blue = not self.current_turn_is_blue
        if self.is_board_full():
            self.game_over = True
            if self.blue_score > self.red_score: self.winner = "Blue"
            elif self.red_score > self.blue_score: self.winner = "Red"
        return soses, True
