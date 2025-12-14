import chess
from .search import find_best

def best_move(board: chess.Board, depth: int = 3, time_limit: float = 1.0) -> chess.Move:
    # si quieres priorizar tiempo sobre profundidad, pasa time_limit
    return find_best(board, max_depth=depth, time_limit=time_limit)
