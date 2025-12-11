import chess
import math
from evaluate import evaluate as evals

def minmax(table, depth, alfa, beta, isMax):
    if depth == 0 or table.is_game_over():
        return evals(table)

    if isMax:
        value = -math.inf
        for mov in table.legal_moves:
            table.push(mov)
            value = max(value, minmax(table, depth-1, alfa, beta, False))
            table.pop()
            alfa = max(alfa, value)
            if alfa >= beta:
                break
            return value
        return None
    else:
        value = math.inf
        for mov in table.legal_moves:
            table.push(mov)
            value = max(value, minmax(table, depth-1, alfa, beta, True))
            table.pop()
            beta = min(alfa, value)
            if alfa >= beta:
                break
        return value

def best_move(table, depth):
    best_value = -math.inf
    best_move = None
    for mov in table.legal_moves:
        table.push(mov)
        value = minmax(table, depth-1, -math.inf, math.inf, False)
        table.pop()
        if value > best_value:
            best_value = value
            best_move = mov
    return best_move