import math
import chess
from chess_backend.chess.evaluate import evaluate

def alphabeta(board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing:
        value = -math.inf
        for move in board.legal_moves:
            board.push(move)
            value = max(value, alphabeta(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = math.inf
        for move in board.legal_moves:
            board.push(move)
            value = min(value, alphabeta(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

def best_move(board: chess.Board, depth: int = 3) -> chess.Move:
    best_val = -math.inf
    best = None
    moves = list(board.legal_moves)
    moves.sort(key=lambda m: board.is_capture(m), reverse=True)

    for move in moves:
        board.push(move)
        val = alphabeta(board, depth - 1, -math.inf, math.inf, False)
        board.pop()
        if val > best_val:
            best_val = val
            best = move

    # Garantizar que el movimiento final sea legal
    if best not in board.legal_moves:
        best = list(board.legal_moves)[0]

    return best
