import chess

VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

CENTER_SQUARES = [chess.D4, chess.D5, chess.E4, chess.E5]

def evaluate(board: chess.Board) -> int:
    score = 0

    # Material + desarrollo + centro
    for square, piece in board.piece_map().items():
        val = VALUES[piece.piece_type]
        score += val if piece.color == chess.WHITE else -val

        # Desarrollo: caballos y alfiles fuera de la primera fila
        if piece.piece_type in (chess.KNIGHT, chess.BISHOP):
            if piece.color == chess.WHITE and chess.square_rank(square) > 0:
                score += 10
            if piece.color == chess.BLACK and chess.square_rank(square) < 7:
                score -= 10

        # Control del centro
        if square in CENTER_SQUARES:
            score += 20 if piece.color == chess.WHITE else -20

    # Movilidad
    mobility = len(list(board.legal_moves))
    score += mobility if board.turn == chess.WHITE else -mobility

    # Seguridad del rey: penalizar si no está enrocado
    if not board.has_castling_rights(chess.WHITE):
        score -= 15
    if not board.has_castling_rights(chess.BLACK):
        score += 15

    # Peones doblados y aislados
    for file in range(8):
        white_pawns = [sq for sq in board.pieces(chess.PAWN, chess.WHITE) if chess.square_file(sq) == file]
        black_pawns = [sq for sq in board.pieces(chess.PAWN, chess.BLACK) if chess.square_file(sq) == file]
        if len(white_pawns) > 1:
            score -= 10 * (len(white_pawns) - 1)
        if len(black_pawns) > 1:
            score += 10 * (len(black_pawns) - 1)

    # Checkmate
    if board.is_checkmate():
        return 10000 if board.turn == chess.BLACK else -10000

    return score
