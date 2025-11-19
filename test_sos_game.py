import unittest
from SosGame import SimpleGame, GeneralGame, HumanPlayer, ComputerPlayer

H_BLUE = HumanPlayer("Blue", "S")
H_RED = HumanPlayer("Red", "S")
C_BLUE_S = ComputerPlayer("Blue", "S")
C_RED_O = ComputerPlayer("Red", "O")
C_RED_S = ComputerPlayer("Red", "S")

class TestPlayerHierarchy(unittest.TestCase):
    def test_human_player_move(self):
        player = HumanPlayer("Test", "S")
        r, c, piece = player.get_move(None)
        self.assertIsNone(r)
        self.assertIsNone(c)
        self.assertIsNone(piece)

    def test_computer_player_random_move(self):
        game = SimpleGame(3, C_BLUE_S, H_RED)
        r, c, piece = C_BLUE_S.get_move(game)
        self.assertIsNotNone(r)
        self.assertIsNotNone(c)
        self.assertIn(piece, ['S', 'O'])

class TestSimpleGame(unittest.TestCase):

    def setUp(self):
        self.game = SimpleGame(3, H_BLUE, H_RED)

    def test_initialization(self):
        self.assertEqual(self.game.board_size, 3)
        self.assertFalse(self.game.game_over)
        self.assertIsNone(self.game.winner)
        self.assertTrue(self.game.current_turn_is_blue)

    def test_turn_switch(self):
        self.game.make_move(0, 0, 'S')
        self.assertFalse(self.game.current_turn_is_blue)
        self.game.make_move(0, 1, 'O')
        self.assertTrue(self.game.current_turn_is_blue)

    def test_horizontal_win(self):
        self.game.make_move(0, 0, 'S')
        self.game.make_move(1, 0, 'S')
        self.game.make_move(0, 1, 'O')
        self.game.make_move(1, 1, 'S')
        
        soses, _ = self.game.make_move(0, 2, 'S')

        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, "Blue")
        self.assertEqual(len(soses), 1)

    def test_draw_game(self):
        # Set up a board that has no SOS opportunities on the last move
        # The new configuration ensures no SOS is formed when 'S' is placed at (2, 2)
        self.game.board = [
            ['S', 'O', 'S'],
            ['O', 'S', 'S'], # Changed (1, 2) from 'O' to 'S'
            ['S', 'S', '']  # Changed (2, 1) from 'O' to 'S'
        ]
        # Set the turn to Blue for the final move
        self.game.current_turn_is_blue = True
        
        # Blue makes the final move with 'S'
        soses, _ = self.game.make_move(2, 2, 'S') 
        
        # Verify the game is over, no SOS was formed, and the winner is None (Draw)
        self.assertTrue(self.game.game_over)
        self.assertEqual(len(soses), 0) # Should now pass as 0
        self.assertIsNone(self.game.winner) # Should now pass as None (draw)

class TestGeneralGame(unittest.TestCase):

    def setUp(self):
        self.game = GeneralGame(3, H_BLUE, H_RED)

    def test_initialization(self):
        self.assertEqual(self.game.board_size, 3)
        self.assertEqual(self.game.blue_score, 0)
        self.assertEqual(self.game.red_score, 0)

    def test_score_and_extra_turn(self):
        self.game.make_move(0, 0, 'S')
        self.assertFalse(self.game.current_turn_is_blue)
        self.game.make_move(0, 1, 'O')
        self.assertTrue(self.game.current_turn_is_blue)

        soses, _ = self.game.make_move(0, 2, 'S')
        
        self.assertEqual(len(soses), 1)
        self.assertEqual(self.game.blue_score, 1)
        self.assertTrue(self.game.current_turn_is_blue)
        self.assertFalse(self.game.game_over)

    def test_no_score_turn_switch(self):
        self.game.make_move(0, 0, 'S')
        self.assertEqual(self.game.get_turn_owner_name(), "Red")
        self.game.make_move(1, 1, 'S')
        self.assertEqual(self.game.get_turn_owner_name(), "Blue")

    def test_win_on_full_board(self):
        self.game.make_move(0, 0, 'S')
        self.game.make_move(0, 1, 'O')
        self.game.make_move(0, 2, 'S')
        self.assertEqual(self.game.blue_score, 1)
        self.assertTrue(self.game.current_turn_is_blue)

        self.game.board = [
            ['S', 'O', 'S'],
            ['S', 'O', 'S'],
            ['O', 'S', '']
        ]
        self.game.make_move(2, 2, 'O')
        
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.blue_score, 1)
        self.assertEqual(self.game.red_score, 0)
        self.assertEqual(self.game.winner, "Blue")

class TestComputerPlayerStrategy(unittest.TestCase):
    
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
        self.assertFalse(game.game_over)
        self.assertEqual(game.blue_score, 1)
        self.assertTrue(game.current_turn_is_blue)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
