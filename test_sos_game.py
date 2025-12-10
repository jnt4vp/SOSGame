import unittest
from SosGame import SimpleGame, GeneralGame, HumanPlayer, ComputerPlayer

# Setup some players for testing
H_BLUE = HumanPlayer("Blue", "S")
H_RED = HumanPlayer("Red", "S")
C_BLUE_S = ComputerPlayer("Blue", "S")
C_RED_O = ComputerPlayer("Red", "O")
C_RED_S = ComputerPlayer("Red", "S")

class TestPlayerHierarchy(unittest.TestCase):
    # Tests that a human player doesnt return a move automatically
    def test_human_player_move(self):
        player = HumanPlayer("Test", "S")
        r, c, piece = player.get_move(None)
        self.assertIsNone(r)
        self.assertIsNone(c)
        self.assertIsNone(piece)

    # Tests that the computer picks a valid spot on the board
    def test_computer_player_random_move(self):
        game = SimpleGame(3, C_BLUE_S, H_RED)
        r, c, piece = C_BLUE_S.get_move(game)
        self.assertIsNotNone(r)
        self.assertIsNotNone(c)
        self.assertIn(piece, ['S', 'O'])

class TestSimpleGame(unittest.TestCase):

    # Sets up a fresh game before each test
    def setUp(self):
        self.game = SimpleGame(3, H_BLUE, H_RED)

    # Checks if the game starts with the right settings
    def test_initialization(self):
        self.assertEqual(self.game.board_size, 3)
        self.assertFalse(self.game.game_over)
        self.assertIsNone(self.game.winner)
        self.assertTrue(self.game.current_turn_is_blue)
        self.assertEqual(self.game.history, []) 

    # Checks if the turn changes after a move
    def test_turn_switch(self):
        self.assertTrue(self.game.current_turn_is_blue)
        self.game.make_move(0, 0, 'S')
        self.assertFalse(self.game.current_turn_is_blue)
        self.game.make_move(0, 1, 'S')
        self.assertTrue(self.game.current_turn_is_blue)

    # Checks that you can't move in a spot that is taken
    def test_invalid_move_occupied(self):
        self.game.make_move(0, 0, 'S')
        soses, success = self.game.make_move(0, 0, 'O')
        self.assertFalse(success)
        self.assertEqual(len(self.game.history), 1)

    # Checks that you can't move outside the board
    def test_invalid_move_out_of_bounds(self):
        soses, success = self.game.make_move(3, 3, 'S')
        self.assertFalse(success)
        self.assertEqual(len(self.game.history), 0)

    # Tests if a player wins when they make an SOS
    def test_simple_game_win(self):
        self.game.make_move(0, 0, 'S') # Blue
        self.game.make_move(1, 1, 'O') # Red
        soses, success = self.game.make_move(2, 2, 'S') 
        
        self.assertTrue(success)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "Blue")
        self.assertEqual(len(self.game.history), 3)
        self.assertEqual(self.game.history[0], (0, 0, 'S'))
        self.assertEqual(self.game.history[2], (2, 2, 'S'))

    # Tests if the game ends in a draw when the board is full
    def test_board_full_draw(self):
        moves = [
            (0,0,'S'), (0,1,'S'), (0,2,'S'),
            (1,0,'S'), (1,1,'S'), (1,2,'S'),
            (2,0,'S'), (2,1,'S'), (2,2,'S')
        ]
        for r, c, p in moves:
            self.game.make_move(r, c, p)
            
        self.assertTrue(self.game.game_over)
        self.assertIsNone(self.game.winner)
        self.assertEqual(len(self.game.history), 9)

class TestGeneralGame(unittest.TestCase):
    # Sets up a general game before each test
    def setUp(self):
        self.game = GeneralGame(3, H_BLUE, H_RED)

    # Tests if the score goes up when an SOS is made
    def test_general_game_scoring(self):
        self.game.make_move(0, 0, 'S') # Blue
        self.game.make_move(0, 1, 'O') # Red
        soses, success = self.game.make_move(0, 2, 'S') # Blue completes SOS
        
        self.assertTrue(success)
        self.assertEqual(len(soses), 1)
        self.assertEqual(self.game.blue_score, 1)
        self.assertTrue(self.game.current_turn_is_blue) # Blue goes again
        
        # Verify history
        self.assertEqual(len(self.game.history), 3)
        self.assertEqual(self.game.history[-1], (0, 2, 'S'))

class TestComputerLogic(unittest.TestCase):
    # Tests if the computer finds a winning move with S
    def test_computer_simple_game_winning_move_S(self):
        game = SimpleGame(3, C_BLUE_S, H_RED)
        game.board = [
            ['S', 'O', ''],
            ['', '', ''],
            ['', '', '']
        ]
        game.current_turn_is_blue = True
        
        r, c, piece = C_BLUE_S.get_move(game)
        
        self.assertEqual(r, 0)
        self.assertEqual(c, 2)
        self.assertEqual(piece, 'S')
        
        soses, move_made = game.make_move(r, c, piece)
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, "Blue")
    
    # Tests if the computer finds a winning move with O
    def test_computer_simple_game_winning_move_O(self):
        game = SimpleGame(3, H_BLUE, C_RED_O)
        game.board = [
            ['S', '', 'S'],
            ['', '', ''],
            ['', '', '']
        ]
        game.current_turn_is_blue = False

        r, c, piece = C_RED_O.get_move(game)
        
        self.assertEqual(r, 0)
        self.assertEqual(c, 1)
        self.assertEqual(piece, 'O')
        
        soses, move_made = game.make_move(r, c, piece)
        self.assertTrue(game.game_over)
        self.assertEqual(game.winner, "Red")

    # Tests if the computer takes points in a general game
    def test_computer_general_game_scoring_move(self):
        game = GeneralGame(3, C_BLUE_S, H_RED)
        game.board = [
            ['S', 'O', ''],
            ['', '', ''],
            ['', '', '']
        ]
        game.current_turn_is_blue = True

        r, c, piece = C_BLUE_S.get_move(game)
        
        self.assertEqual(r, 0)
        self.assertEqual(c, 2)
        self.assertEqual(piece, 'S')
        
        soses, move_made = game.make_move(r, c, piece)
        self.assertEqual(game.blue_score, 1)

if __name__ == '__main__':
    unittest.main()
