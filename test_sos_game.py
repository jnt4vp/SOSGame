import unittest
from SosGame import SOSGame

class TestSOSGame(unittest.TestCase):

    def setUp(self):
        self.game = SOSGame(board_size=3)

    def test_initialization(self):
        self.assertEqual(self.game.board_size, 3)
        self.assertEqual(len(self.game.board), 3)
        self.assertTrue(self.game.current_turn_is_blue)
        self.assertEqual(self.game.game_mode, 'simple')
        self.assertEqual(self.game.get_turn_owner_name(), "Blue")

    def test_new_game(self):

        self.game.make_move(0, 0, 'S') 
        
        self.game.new_game(board_size=5, game_mode='general')

        self.assertEqual(self.game.board_size, 5)
        self.assertEqual(len(self.game.board), 5)
        self.assertEqual(self.game.game_mode, 'general')
        self.assertTrue(self.game.current_turn_is_blue) 
        self.assertEqual(self.game.board[0][0], '') 

    def test_make_valid_move(self):
        self.assertTrue(self.game.current_turn_is_blue)
        result = self.game.make_move(1, 1, 'S')
        
        self.assertTrue(result)
        self.assertEqual(self.game.board[1][1], 'S')
        
        self.assertFalse(self.game.current_turn_is_blue)
        self.assertEqual(self.game.get_turn_owner_name(), "Red")

    def test_make_invalid_move_occupied_cell(self):

        self.game.make_move(0, 0, 'S')
        self.assertFalse(self.game.current_turn_is_blue) 


        result = self.game.make_move(0, 0, 'O')

        self.assertFalse(result)
        self.assertEqual(self.game.board[0][0], 'S') 
        
        self.assertFalse(self.game.current_turn_is_blue)

    def test_make_invalid_move_out_of_bounds(self):
        result = self.game.make_move(3, 3, 'S') 

        self.assertFalse(result)
        
        self.assertTrue(self.game.current_turn_is_blue)


if __name__ == '__main__':
    unittest.main(verbosity=2)
