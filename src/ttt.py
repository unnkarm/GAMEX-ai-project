"""Tic-Tac-Toe implementation of the generic GameState interface."""
from copy import deepcopy
from .engine import GameState

WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

class TicTacToe(GameState):
    def __init__(self, board=None, player="X"):
        self.board = list(board) if board is not None else [" "] * 9
        self.player = player

    def current_player(self): return self.player
    def legal_moves(self): return [i for i, cell in enumerate(self.board) if cell == " "]
    def apply_move(self, move):
        new = TicTacToe(self.board, self.player)
        new.board[move] = self.player
        new.player = "O" if self.player == "X" else "X"
        return new
    def winner(self):
        for a,b,c in WIN_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None
    def is_terminal(self):
        return self.winner() is not None or not self.legal_moves()
    def utility(self, maximizing_player):
        win = self.winner()
        if win is None: return 0
        return 1 if win == maximizing_player else -1
    def heuristic(self, maximizing_player):
        """Count open lines with a small preference for two-in-a-row opportunities."""
        opponent = "O" if maximizing_player == "X" else "X"
        score = 0.0
        for line in WIN_LINES:
            vals = [self.board[i] for i in line]
            if opponent not in vals:
                score += vals.count(maximizing_player) * 0.15
            if maximizing_player not in vals:
                score -= vals.count(opponent) * 0.15
        return max(-0.8, min(0.8, score))
