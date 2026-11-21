"""Generic two-player zero-sum game engine using depth-limited Minimax."""
from dataclasses import dataclass
from typing import Any

@dataclass
class SearchStats:
    nodes: int = 0
    max_depth: int = 0
    utility: float = 0.0
    best_move: Any = None

class GameState:
    """Interface expected by the generic Minimax engine."""
    def current_player(self): raise NotImplementedError
    def legal_moves(self): raise NotImplementedError
    def apply_move(self, move): raise NotImplementedError
    def is_terminal(self): raise NotImplementedError
    def utility(self, maximizing_player): raise NotImplementedError
    def heuristic(self, maximizing_player): return 0.0

def minimax(state: GameState, depth_limit: int, maximizing_player: str):
    """Return (best_move, utility, statistics) using depth-limited alpha-beta search."""
    stats = SearchStats()
    if depth_limit < 0:
        raise ValueError("Depth must be >= 0")

    def search(node, depth, is_max, alpha, beta):
        stats.nodes += 1
        stats.max_depth = max(stats.max_depth, depth)
        if node.is_terminal():
            return node.utility(maximizing_player)
        if depth >= depth_limit:
            return node.heuristic(maximizing_player)
        moves = node.legal_moves()
        if not moves:
            return node.utility(maximizing_player)
        if is_max:
            value = float("-inf")
            for move in moves:
                child = node.apply_move(move)
                value = max(value, search(child, depth + 1, False, alpha, beta))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        value = float("inf")
        for move in moves:
            child = node.apply_move(move)
            value = min(value, search(child, depth + 1, True, alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

    if state.is_terminal():
        stats.utility = state.utility(maximizing_player)
        return None, stats.utility, stats

    moves = state.legal_moves()
    if not moves:
        stats.utility = state.utility(maximizing_player)
        return None, stats.utility, stats
    # Root move selection separately records best move and its utility.
    is_max = state.current_player() == maximizing_player
    best_move = None
    best_value = float("-inf") if is_max else float("inf")
    alpha = float("-inf")
    beta = float("inf")
    for move in moves:
        child = state.apply_move(move)
        value = search(child, 1, not is_max, alpha, beta)
        if (is_max and value > best_value) or (not is_max and value < best_value):
            best_value, best_move = value, move
        if is_max:
            alpha = max(alpha, best_value)
        else:
            beta = min(beta, best_value)
    stats.best_move = best_move
    stats.utility = best_value
    return best_move, best_value, stats
