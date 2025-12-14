# src/chess_backend/chess/search.py
import time
import math
import chess
from chess_backend.chess.evaluate import evaluate, see_gain  # IMPORTAR AQUÍ (no al revés)

# Transposition table simple: fen -> (value, depth, flag, best_move)
TT = {}

INFTY = 999999

def quiescence(board: chess.Board, alpha: int, beta: int) -> int:
    """
    Búsqueda de quiescencia: explora capturas (y checks) hasta que la posición esté quieta.
    """
    stand_pat = evaluate(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    # Ordenar capturas por SEE (mejores primero)
    captures = [m for m in board.legal_moves if board.is_capture(m)]
    captures.sort(key=lambda m: see_gain(board, m), reverse=True)

    for m in captures:
        board.push(m)
        score = -quiescence(board, -beta, -alpha)
        board.pop()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

def alphabeta(board: chess.Board, depth: int, alpha: int, beta: int) -> int:
    """
    Alpha-beta con TT y ordenación básica de jugadas.
    """
    key = board.fen()
    tt = TT.get(key)
    if tt and tt[1] >= depth:
        # Devolvemos el valor cacheado si la profundidad es suficiente
        return tt[0]

    if depth == 0 or board.is_game_over():
        val = quiescence(board, alpha, beta)
        TT[key] = (val, depth, 'EXACT', None)
        return val

    best = -INFTY
    best_move = None

    moves = list(board.legal_moves)
    # Ordering: capturas (por SEE) primero, luego quiet moves
    moves.sort(key=lambda m: (board.is_capture(m), see_gain(board, m)), reverse=True)

    for m in moves:
        board.push(m)
        val = -alphabeta(board, depth - 1, -beta, -alpha)
        board.pop()

        if val > best:
            best = val
            best_move = m
        if val > alpha:
            alpha = val
        if alpha >= beta:
            break

    TT[key] = (best, depth, 'EXACT', best_move)
    return best

def find_best(board: chess.Board, max_depth: int = 4, time_limit: float = 1.0) -> chess.Move:
    """
    Iterative deepening simple con control de tiempo.
    Devuelve la mejor jugada encontrada (chess.Move) o None si no hay jugadas.
    """
    start = time.time()
    best_move = None

    # Si no hay jugadas legales, devolver None
    legal = list(board.legal_moves)
    if not legal:
        return None

    for depth in range(1, max_depth + 1):
        best_score = -INFTY
        # Recolectar lista de jugadas y ordenarlas por heurística simple
        moves = list(board.legal_moves)
        moves.sort(key=lambda m: (board.is_capture(m), see_gain(board, m)), reverse=True)

        for m in moves:
            # Comprobar tiempo antes de cada evaluación pesada
            if time.time() - start > time_limit:
                return best_move

            board.push(m)
            score = -alphabeta(board, depth - 1, -INFTY, INFTY)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = m

        # Si se agotó el tiempo, salimos con la mejor encontrada hasta ahora
        if time.time() - start > time_limit:
            break

    return best_move
