import unittest
from sosUtilities import is_sos, count_sos_in_board

class TestSOSUtils(unittest.TestCase):
    def test_is_sos_basic(self):
        self.assertTrue(is_sos("SOS"))
        self.assertTrue(is_sos("sos"))
        self.assertFalse(is_sos("SO"))
        self.assertFalse(is_sos("S0S"))  

    def test_count_sos_rows_cols_diags(self):
        board = [
            ["S", "O", "S", ""],
            ["", "S", "O", "S"],
            ["S", "O", "S", ""],
            ["", "", "", ""],
        ]

        self.assertEqual(count_sos_in_board(board), 4)

    def test_empty_board(self):
        self.assertEqual(count_sos_in_board([]), 0)

    def test_noise(self):
        board = [
            [" s ", " o", " S "],
            [None, "   ", ""],
            ["X", "Y", "Z"],
        ]
        self.assertEqual(count_sos_in_board(board), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

