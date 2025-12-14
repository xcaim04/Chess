import { useState, useMemo } from "react";
import { Chess } from "chess.js";
import Board from "./Board";
import Panel from "./Panel";
import { toSquare } from "../utils/chessUtils";

const API_URL = "http://127.0.0.1:5000/chess/move";

export default function ChessApp({ token }) {
  const [game, setGame] = useState(() => new Chess());
  const [selected, setSelected] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const board = useMemo(() => game.board(), [game]);

  async function handleSquareClick(row, col) {
    const square = toSquare(row, col);

    if (!selected) {
      const piece = game.get(square);
      if (!piece || piece.color !== game.turn()) {
        setStatus("Selecciona una pieza válida del turno actual");
        return;
      }
      setSelected(square);
      setStatus(`Origen: ${square}`);
      return;
    }

    if (selected === square) {
      setSelected(null);
      setStatus("");
      return;
    }

    const newGame = new Chess(game.fen());
    const move = newGame.move({ from: selected, to: square, promotion: "q" });

    if (move === null) {
      setStatus("Jugada inválida");
      return;
    }

    setGame(newGame);
    setSelected(null);
    setStatus(`Tu jugada: ${move.san}`);
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ move: move.from + move.to }),
      });


      const data = await res.json();
      
      if (data.fen) {
        setGame(new Chess(data.fen));
        setStatus("IA jugó");
      } else {
        setStatus("Respuesta sin FEN: tablero no actualizado");
      }
    } catch {
      setStatus("Error conectando con el backend");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: "flex", gap: "24px", justifyContent: "center", alignItems: "flex-start", padding: "24px" }}>
      <Board board={board} selected={selected} onSquareClick={handleSquareClick} />
      <Panel status={status} loading={loading} turn={game.turn()} fen={game.fen()} />
    </div>
  );
}
