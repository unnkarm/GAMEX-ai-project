import unittest
from src.engine import minimax
from src.ttt import TicTacToe

class TestMinimaxTicTacToe(unittest.TestCase):
    def test_empty_board_returns_legal_move(self):
        state = TicTacToe()
        move, value, stats = minimax(state, 9, "O")
        self.assertIn(move, state.legal_moves())
        self.assertEqual(value, 0)
        self.assertGreater(stats.nodes, 0)

    def test_ai_takes_immediate_win(self):
        # O has two in a row and can win at position 2
        state = TicTacToe(["O","O"," ","X","X"," "," "," "," "], player="O")
        move, value, stats = minimax(state, 9, "O")
        self.assertEqual(move, 2)
        self.assertEqual(value, 1)

    def test_ai_blocks_human_win(self):
        state = TicTacToe(["X","X"," ","O"," "," "," "," "," "], player="O")
        move, value, stats = minimax(state, 9, "O")
        self.assertEqual(move, 2)

    def test_depth_zero_reject(self):
        with self.assertRaises(ValueError):
            minimax(TicTacToe(), -1, "O")

    def test_terminal_board_has_no_move(self):
        state = TicTacToe(["X","X","X","O","O"," "," "," "," "])
        move, value, stats = minimax(state, 9, "O")
        self.assertIsNone(move)
        self.assertEqual(value, -1)
        self.assertEqual(stats.nodes, 0)

if __name__ == "__main__":
    unittest.main()
