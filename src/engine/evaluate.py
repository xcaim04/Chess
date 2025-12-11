import chess

def evaluate(table):
    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0,
    }
    score = 0
    for piece in table.piece_map().values():
        if piece.color == chess.WHITE:
            score += values[piece.piece_type]
        else:
            score -= values[piece.piece_type]
    return score
