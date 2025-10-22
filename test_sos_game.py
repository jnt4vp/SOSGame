# test_sos_game.py

import unittest
from sos_game import SOSGame

class TestSOSGame(unittest.TestCase):

    def setUp(self):
        """This method is called before each test function."""
        self.game = SOSGame(board_size=3)

    def test_initialization(self):
        """
        User Story: Start a new game
        Tests if the game initializes correctly with a 3x3 board.
        """
        self.assertEqual(self.game.board_size, 3)
        self.assertEqual(len(self.game.board), 3)
        self.assertTrue(self.game.current_turn_is_blue)
        self.assertEqual(self.game.game_mode, 'simple')
        self.assertEqual(self.game.get_turn_owner_name(), "Blue")

    def test_new_game(self):
        """
        User Story: Start a new game of the chosen board size and game mode
        Tests the new_game method to ensure it resets the game state.
        """
        # Change some state first
        self.game.make_move(0, 0, 'S') 
        
        # Start a new game with different parameters
        self.game.new_game(board_size=5, game_mode='general')

        # Assert the new state is correct
        self.assertEqual(self.game.board_size, 5)
        self.assertEqual(len(self.game.board), 5)
        self.assertEqual(self.game.game_mode, 'general')
        self.assertTrue(self.game.current_turn_is_blue) # Turn should reset to Blue
        self.assertEqual(self.game.board[0][0], '') # Board should be empty

    def test_make_valid_move(self):
        """
        User Story: Make a move in a simple game
        Tests a valid move being placed on the board and the turn switching.
        """
        # Blue's turn
        self.assertTrue(self.game.current_turn_is_blue)
        result = self.game.make_move(1, 1, 'S')
        
        # Assert the move was successful
        self.assertTrue(result)
        self.assertEqual(self.game.board[1][1], 'S')
        
        # Assert the turn changed to Red
        self.assertFalse(self.game.current_turn_is_blue)
        self.assertEqual(self.game.get_turn_owner_name(), "Red")

    def test_make_invalid_move_occupied_cell(self):
        """
        User Story: Make a move in a simple game
        Tests that a player cannot place a piece in an already occupied cell.
        """
        self.game.make_move(0, 0, 'S') # Blue makes a move
        self.assertFalse(self.game.current_turn_is_blue) # It's now Red's turn

        # Red tries to make a move on the same cell
        result = self.game.make_move(0, 0, 'O')

        # Assert the move was rejected
        self.assertFalse(result)
        self.assertEqual(self.game.board[0][0], 'S') # The piece should not have changed
        
        # Assert the turn did NOT change
        self.assertFalse(self.game.current_turn_is_blue)

    def test_make_invalid_move_out_of_bounds(self):
        """
        User Story: Make a move in a simple game
        Tests that a player cannot place a piece outside the board dimensions.
        """
        result = self.game.make_move(3, 3, 'S') # 3,3 is out of bounds for a 3x3 board (0,1,2)

        # Assert the move was rejected
        self.assertFalse(result)
        
        # Assert the turn did NOT change
        self.assertTrue(self.game.current_turn_is_blue)


if __name__ == '__main__':
    # This allows you to run the tests directly from the command line
    unittest.main(verbosity=2)