from fastapi import APIRouter, Depends, HTTPException
import chess
from chess_backend.chess.engine import best_move
from chess_backend.auth.utils import get_current_user

router = APIRouter()

board = chess.Board()

def serialize_state():
    return {
        "fen": board.fen(),
        "turn": "w" if board.turn else "b",
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None
    }

@router.get("/state")
def get_state(user=Depends(get_current_user)):
    return serialize_state()

@router.post("/move")
def move(payload: dict, user=Depends(get_current_user)):
    human_move = payload.get("move")
    if not human_move:
        raise HTTPException(status_code=400, detail="Falta 'move'")

    try:
        if len(human_move) in (4, 5):  # UCI
            board.push(chess.Move.from_uci(human_move))
        else:  # SAN
            board.push_san(human_move)
    except Exception:
        raise HTTPException(status_code=400, detail="Jugada inválida")

    if board.is_game_over():
        return serialize_state()

    ai_move = best_move(board, 3)
    if ai_move not in board.legal_moves:
        raise HTTPException(status_code=400, detail=f"IA sugirió jugada ilegal: {ai_move}")

    ai_move_san = board.san(ai_move)
    board.push(ai_move)

    return {
        "ai_move_uci": ai_move.uci(),
        "ai_move_san": ai_move_san,
        **serialize_state()
    }

@router.post("/reset")
def reset(user=Depends(get_current_user)):
    global board
    board = chess.Board()
    return serialize_state()
