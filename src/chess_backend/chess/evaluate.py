# src/chess_backend/chess/evaluate.py
import chess
from typing import List, Dict, Optional

# -------------------------
# Valores base (centipawns)
# -------------------------
VALUES: Dict[int, int] = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

# -------------------------
# Piece-square tables (medio juego)
#
# -------------------------
PST_PAWN = [
     0,   0,   0,   0,   0,   0,   0,   0,
     5,  10,  10, -20, -20,  10,  10,   5,
     5,  -5, -10,   0,   0, -10,  -5,   5,
     0,   0,   0,  20,  20,   0,   0,   0,
     5,   5,  10,  25,  25,  10,   5,   5,
    10,  10,  20,  30,  30,  20,  10,  10,
    50,  50,  50,  50,  50,  50,  50,  50,
     0,   0,   0,   0,   0,   0,   0,   0
]

PST_KNIGHT = [
   -50,-40,-30,-30,-30,-30,-40,-50,
   -40,-20,  0,  5,  5,  0,-20,-40,
   -30,  5, 10, 15, 15, 10,  5,-30,
   -30,  0, 15, 20, 20, 15,  0,-30,
   -30,  5, 15, 20, 20, 15,  5,-30,
   -30,  0, 10, 15, 15, 10,  0,-30,
   -40,-20,  0,  0,  0,  0,-20,-40,
   -50,-40,-30,-30,-30,-30,-40,-50
]

PST_BISHOP = [
   -20,-10,-10,-10,-10,-10,-10,-20,
   -10,  5,  0,  0,  0,  0,  5,-10,
   -10, 10, 10, 10, 10, 10, 10,-10,
   -10,  0, 10, 10, 10, 10,  0,-10,
   -10,  5,  5, 10, 10,  5,  5,-10,
   -10,  0,  5, 10, 10,  5,  0,-10,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -20,-10,-10,-10,-10,-10,-10,-20
]

PST_ROOK = [
     0,  0,  5, 10, 10,  5,  0,  0,
     0,  0,  5, 10, 10,  5,  0,  0,
     0,  0,  5, 10, 10,  5,  0,  0,
     0,  0,  5, 10, 10,  5,  0,  0,
     0,  0,  5, 10, 10,  5,  0,  0,
     0,  0,  5, 10, 10,  5,  0,  0,
    25, 25, 25, 25, 25, 25, 25, 25,
     0,  0,  5, 10, 10,  5,  0,  0
]

PST_QUEEN = [
   -20,-10,-10, -5, -5,-10,-10,-20,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
     0,  0,  5,  5,  5,  5,  0, -5,
   -10,  5,  5,  5,  5,  5,  0,-10,
   -10,  0,  5,  0,  0,  0,  0,-10,
   -20,-10,-10, -5, -5,-10,-10,-20
]

PST_KING_MID = [
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -20,-30,-30,-40,-40,-30,-30,-20,
   -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

PST_KING_END = [
   -50,-40,-30,-20,-20,-30,-40,-50,
   -30,-20,-10,  0,  0,-10,-20,-30,
   -30,-10, 20, 30, 30, 20,-10,-30,
   -30,-10, 30, 40, 40, 30,-10,-30,
   -30,-10, 30, 40, 40, 30,-10,-30,
   -30,-10, 20, 30, 30, 20,-10,-30,
   -30,-30,  0,  0,  0,  0,-30,-30,
   -50,-30,-30,-30,-30,-30,-30,-50
]

PST: Dict[int, List[int]] = {
    chess.PAWN: PST_PAWN,
    chess.KNIGHT: PST_KNIGHT,
    chess.BISHOP: PST_BISHOP,
    chess.ROOK: PST_ROOK,
    chess.QUEEN: PST_QUEEN,
    # KING table chosen dynamically by phase
}

CENTER_SQUARES = {chess.D4, chess.D5, chess.E4, chess.E5}

# -------------------------
# Parámetros ajustables (tuning)
# -------------------------
WEIGHTS = {
    "bishop_pair": 40,
    "passed_pawn_base": 30,
    "passed_pawn_advance": 10,
    "isolated_pawn": -15,
    "doubled_pawn": -10,
    "outpost_knight": 25,
    "outpost_bishop": 15,
    "rook_open_file": 20,
    "rook_semiopen_file": 10,
    "connected_rooks": 20,
    "king_shield": 8,
    "space": 6,
    "tempo": 10,
    "exchange_when_ahead": 30,
    "avoid_exchange_when_ahead": -20,
    "pawn_majority": 12,
    "king_activity_endgame": 30,
    "book_bias": 25,  # small bias for opening book moves
}

# -------------------------
# Opening bias (muy pequeño). No es un libro completo.
# Mapea FEN prefix (solo apertura) a movimientos UCI comunes.
# Puedes ampliar con un PGN externo si quieres.
# -------------------------
OPENING_BIAS = {
    # posición inicial -> favorece e2e4, d2d4, g1f3, c2c4
    "start": ["e2e4", "d2d4", "g1f3", "c2c4"],
    # Ejemplo: Sicilian after 1.e4 c5 -> favorece Nf3, d4
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq -": ["g1f3", "d2d4"],
}

# -------------------------
# Utilidades de estructura de peones y posición
# -------------------------
def is_passed(board: chess.Board, sq: int, color: bool) -> bool:
    file = chess.square_file(sq)
    rank = chess.square_rank(sq)
    if color == chess.WHITE:
        rng = range(rank + 1, 8)
    else:
        rng = range(0, rank)
    for f in range(max(0, file - 1), min(7, file + 1) + 1):
        for r in rng:
            s = chess.square(f, r)
            if board.piece_type_at(s) == chess.PAWN and board.color_at(s) != color:
                return False
    return True

def is_isolated(board: chess.Board, sq: int, color: bool) -> bool:
    file = chess.square_file(sq)
    for f in (file - 1, file + 1):
        if 0 <= f <= 7:
            for r in range(8):
                s = chess.square(f, r)
                if board.piece_type_at(s) == chess.PAWN and board.color_at(s) == color:
                    return False
    return True

def count_doubled(board: chess.Board, file: int, color: bool) -> int:
    return sum(1 for sq in board.pieces(chess.PAWN, color) if chess.square_file(sq) == file)

# -------------------------
# SEE simplificado (para ordering)
# -------------------------
def see_gain(board: chess.Board, move: chess.Move) -> int:
    if not board.is_capture(move):
        return 0
    captured = board.piece_type_at(move.to_square)
    attacker = board.piece_type_at(move.from_square)
    if captured is None or attacker is None:
        return 0
    return VALUES.get(captured, 0) - VALUES.get(attacker, 0)

# -------------------------
# Helpers posicionales
# -------------------------
def pst_value(piece_type: int, square: int, color: bool, phase: float) -> int:
    # phase: 0.0 = opening/midgame, 1.0 = endgame
    if piece_type == chess.KING:
        table = PST_KING_END if phase > 0.6 else PST_KING_MID
    else:
        table = PST.get(piece_type)
    if not table:
        return 0
    idx = square if color == chess.WHITE else chess.square_mirror(square)
    return table[idx]

def game_phase(board: chess.Board) -> float:
    """
    Calcula fase de juego en [0,1]: 0 = medio/apertura, 1 = final.
    Basado en material restante (simplificado).
    """
    total = 0
    max_phase = 0
    # pesos para fase (mayor peso = acelera hacia final)
    phase_weights = {
        chess.QUEEN: 4,
        chess.ROOK: 2,
        chess.BISHOP: 1,
        chess.KNIGHT: 1,
        chess.PAWN: 0.5,
    }
    for pt, w in phase_weights.items():
        count = len(list(board.pieces(pt, chess.WHITE))) + len(list(board.pieces(pt, chess.BLACK)))
        total += count * w
        max_phase += 2 * w  # máximo por pieza (ambos lados)
    # normalizar y convertir a 0..1 inverso (menos material -> más endgame)
    if max_phase == 0:
        return 1.0
    frac = total / max_phase
    # frac cerca de 1 => mucha material => apertura/medio => phase ~0
    return max(0.0, min(1.0, 1.0 - frac))

def is_outpost(board: chess.Board, sq: int, color: bool) -> bool:
    """
    Detecta outpost: casilla avanzada (no puede ser atacada por peones enemigos desde atrás)
    y controlada por piezas propias (ideal para caballos).
    """
    file = chess.square_file(sq)
    rank = chess.square_rank(sq)
    # outpost debe estar en la mitad del rival (rank alto para blancas)
    if color == chess.WHITE and rank < 3:
        return False
    if color == chess.BLACK and rank > 4:
        return False
    # no debe poder ser atacada por peones enemigos desde atrás (simplificado)
    for df in (-1, 1):
        f = file + df
        r = rank - 1 if color == chess.WHITE else rank + 1
        if 0 <= f <= 7 and 0 <= r <= 7:
            s = chess.square(f, r)
            if board.piece_type_at(s) == chess.PAWN and board.color_at(s) != color:
                return False
    return True

def rook_on_open_file(board: chess.Board, sq: int, color: bool) -> int:
    """
    Devuelve 2 si la torre está en columna abierta (sin peones de ambos colores),
    1 si semiabierta (sin peones propios), 0 si bloqueada.
    """
    file = chess.square_file(sq)
    pawns_in_file = [board.piece_type_at(chess.square(file, r)) for r in range(8)]
    has_white_pawn = any(board.piece_type_at(chess.square(file, r)) == chess.PAWN and board.color_at(chess.square(file, r)) == chess.WHITE for r in range(8))
    has_black_pawn = any(board.piece_type_at(chess.square(file, r)) == chess.PAWN and board.color_at(chess.square(file, r)) == chess.BLACK for r in range(8))
    if not has_white_pawn and not has_black_pawn:
        return 2
    if color == chess.WHITE and not has_white_pawn:
        return 1
    if color == chess.BLACK and not has_black_pawn:
        return 1
    return 0

def pawn_majority_score(board: chess.Board, color: bool) -> int:
    """
    Calcula ventaja de mayoría de peones en flanco (simplificado: cuenta peones en cada mitad).
    """
    left_white = sum(1 for sq in board.pieces(chess.PAWN, color) if chess.square_file(sq) <= 3)
    right_white = sum(1 for sq in board.pieces(chess.PAWN, color) if chess.square_file(sq) >= 4)
    return abs(left_white - right_white)

def king_activity_score(board: chess.Board, color: bool, phase: float) -> int:
    """
    En endgame, rey activo es valioso. Devuelve bonus según centralidad del rey.
    """
    kings = list(board.pieces(chess.KING, color))
    if not kings:
        return 0
    ksq = kings[0]
    file = chess.square_file(ksq)
    rank = chess.square_rank(ksq)
    # distancia al centro
    dist = abs(3.5 - file) + abs(3.5 - rank)
    # menor distancia => más activo => bonus en endgame
    return int((4.0 - dist) * WEIGHTS["king_activity_endgame"] * phase)

# -------------------------
# Opening bias helper
# -------------------------
def opening_book_bonus(board: chess.Board) -> int:
    """
    Si la posición coincide con una clave simple del opening bias y la jugada
    recomendada está disponible, devuelve un pequeño bonus para favorecerla.
    """
    # clave simple: si posición es inicial
    if board.fullmove_number == 1 and board.turn == chess.WHITE:
        key = "start"
    else:
        # buscar coincidencia exacta en OPENING_BIAS keys (puedes ampliar)
        fen_prefix = board.board_fen()
        key = None
        for k in OPENING_BIAS.keys():
            if k != "start" and fen_prefix.startswith(k):
                key = k
                break
    if key is None:
        return 0
    moves = OPENING_BIAS.get(key, [])
    for uci in moves:
        try:
            mv = chess.Move.from_uci(uci)
        except Exception:
            continue
        if mv in board.legal_moves:
            return WEIGHTS["book_bias"]
    return 0

# -------------------------
# Evaluación principal mejorada
# -------------------------
def evaluate(board: chess.Board) -> int:
    """
    Evaluación estratégica mejorada.
    Retorna centipawns (positivo = ventaja blanca).
    """
    # Terminales
    if board.is_checkmate():
        return -100000 if board.turn == chess.WHITE else 100000
    if board.is_stalemate():
        return 0

    phase = game_phase(board)  # 0..1 (1 = endgame)
    score = 0.0

    # Material y PST
    material_white = 0
    material_black = 0
    for sq, piece in board.piece_map().items():
        pt = piece.piece_type
        color = piece.color
        sign = 1 if color == chess.WHITE else -1
        score += sign * VALUES.get(pt, 0)
        score += sign * pst_value(pt, sq, color, phase)
        if color == chess.WHITE:
            material_white += VALUES.get(pt, 0)
        else:
            material_black += VALUES.get(pt, 0)

    # Pawn structure: passed, isolated, doubled
    for sq, piece in board.piece_map().items():
        if piece.piece_type != chess.PAWN:
            continue
        color = piece.color
        sign = 1 if color == chess.WHITE else -1
        # passed pawn bonus (más si avanzado)
        if is_passed(board, sq, color):
            rank = chess.square_rank(sq)
            advance = rank if color == chess.WHITE else (7 - rank)
            bonus = WEIGHTS["passed_pawn_base"] + WEIGHTS["passed_pawn_advance"] * advance
            score += sign * bonus
        # isolated
        if is_isolated(board, sq, color):
            score += sign * WEIGHTS["isolated_pawn"]
        # doubled
        file = chess.square_file(sq)
        count = count_doubled(board, file, color)
        if count > 1:
            score += sign * WEIGHTS["doubled_pawn"] * (count - 1)

    # Bishop pair
    if len(list(board.pieces(chess.BISHOP, chess.WHITE))) >= 2:
        score += WEIGHTS["bishop_pair"]
    if len(list(board.pieces(chess.BISHOP, chess.BLACK))) >= 2:
        score -= WEIGHTS["bishop_pair"]

    # Mobility y actividad de piezas (ponderado por tipo)
    mobility_score = 0
    for move in board.legal_moves:
        mobility_score += 3 if board.is_capture(move) else 1
    score += (mobility_score if board.turn == chess.WHITE else -mobility_score) * 0.2

    # Outposts y piezas activas
    for sq, piece in board.piece_map().items():
        pt = piece.piece_type
        color = piece.color
        sign = 1 if color == chess.WHITE else -1
        # knights on outpost
        if pt == chess.KNIGHT and is_outpost(board, sq, color):
            score += sign * WEIGHTS["outpost_knight"]
        # bishops on outpost (lesser)
        if pt == chess.BISHOP and is_outpost(board, sq, color):
            score += sign * WEIGHTS["outpost_bishop"]
        # queen centralization bonus
        if pt == chess.QUEEN:
            if sq in CENTER_SQUARES:
                score += sign * 12 * (1 - phase)  # queen center more valuable in midgame

    # Rooks on open/semi-open files and connected rooks
    for color in (chess.WHITE, chess.BLACK):
        rooks = list(board.pieces(chess.ROOK, color))
        for r in rooks:
            rscore = rook_on_open_file(board, r, color)
            sign = 1 if color == chess.WHITE else -1
            if rscore == 2:
                score += sign * WEIGHTS["rook_open_file"]
            elif rscore == 1:
                score += sign * WEIGHTS["rook_semiopen_file"]
        # connected rooks bonus
        if len(rooks) >= 2:
            # si hay dos torres en la misma fila o columna sin piezas entre ellas, bonus
            for i in range(len(rooks)):
                for j in range(i + 1, len(rooks)):
                    a = rooks[i]; b = rooks[j]
                    af = chess.square_file(a); ar = chess.square_rank(a)
                    bf = chess.square_file(b); br = chess.square_rank(b)
                    if af == bf or ar == br:
                        # comprobar si hay piezas entre ellas
                        between = False
                        if af == bf:
                            for r in range(min(ar, br) + 1, max(ar, br)):
                                if board.piece_type_at(chess.square(af, r)) is not None:
                                    between = True; break
                        else:
                            for f in range(min(af, bf) + 1, max(af, bf)):
                                if board.piece_type_at(chess.square(f, ar)) is not None:
                                    between = True; break
                        if not between:
                            score += (WEIGHTS["connected_rooks"] if color == chess.WHITE else -WEIGHTS["connected_rooks"])

    # King safety: shield and exposure (menos importante en endgame)
    score += king_shield_score(board, chess.WHITE) * (1 - phase)
    score -= king_shield_score(board, chess.BLACK) * (1 - phase)

    # King activity in endgame
    score += king_activity_score(board, chess.WHITE, phase)
    score -= king_activity_score(board, chess.BLACK, phase)

    # Pawn majority (flank majority) incentive
    for color in (chess.WHITE, chess.BLACK):
        maj = pawn_majority_score(board, color)
        sign = 1 if color == chess.WHITE else -1
        score += sign * maj * WEIGHTS["pawn_majority"]

    # Space control: casillas controladas en el centro y avance
    center_control_white = 0
    center_control_black = 0
    for sq in CENTER_SQUARES:
        attackers_w = board.attackers(chess.WHITE, sq)
        attackers_b = board.attackers(chess.BLACK, sq)
        center_control_white += len(attackers_w)
        center_control_black += len(attackers_b)
    score += (center_control_white - center_control_black) * WEIGHTS["space"]

    # Tempo: si la última jugada fue desarrollo o enroque, pequeño bonus
    # (no siempre disponible; usamos heurística: si hay menos piezas desarrolladas, premiar desarrollo)
    # Conteo simple: piezas menores desarrolladas (no en su casilla inicial)
    def development_score(color: bool) -> int:
        dev = 0
        for sq in board.pieces(chess.KNIGHT, color):
            if (color == chess.WHITE and sq not in (chess.B1, chess.G1)) and (color == chess.BLACK and sq not in (chess.B8, chess.G8)):
                dev += 1
        for sq in board.pieces(chess.BISHOP, color):
            # bishop initial squares: c1,f1 for white; c8,f8 for black
            if color == chess.WHITE and sq not in (chess.C1, chess.F1):
                dev += 1
            if color == chess.BLACK and sq not in (chess.C8, chess.F8):
                dev += 1
        return dev
    score += (development_score(chess.WHITE) - development_score(chess.BLACK)) * WEIGHTS["tempo"]

    # Exchange preference: si estamos materialmente por delante, favorecer simplificaciones
    material_diff = material_white - material_black
    if material_diff > 150:  # ~1.5 pawns advantage
        # favorecer cambios: small bonus to positions that reduce opponent activity
        score += WEIGHTS["exchange_when_ahead"]
    elif material_diff < -150:
        # si estamos por detrás, evitar cambios
        score += WEIGHTS["avoid_exchange_when_ahead"]

    # Opening bias (pequeño)
    score += opening_book_bonus(board)

    # Final rounding
    return int(score)

def king_shield_score(board: chess.Board, color: bool) -> int:
    kings = list(board.pieces(chess.KING, color))
    if not kings:
        return 0
    ksq = kings[0]
    kf = chess.square_file(ksq)
    kr = chess.square_rank(ksq)
    shield = 0
    ranks = range(kr, min(7, kr + 2) + 1) if color == chess.WHITE else range(max(0, kr - 1), kr + 1)
    for f in range(max(0, kf - 1), min(7, kf + 1) + 1):
        for r in ranks:
            s = chess.square(f, r)
            if board.piece_type_at(s) == chess.PAWN and board.color_at(s) == color:
                shield += 1
    return shield * WEIGHTS["king_shield"]
