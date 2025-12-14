import { toSquare, squareColor } from "../utils/chessUtils";

export default function Square({ row, col, cell, selected, onClick }) {
  const sq = toSquare(row, col);
  const isSelected = selected === sq;
  const bg = squareColor(row, col);

  function renderPiece(cell) {
    if (!cell) return null;

    // Mapear tipo de pieza a nombre en español
    const map = {
      p: "peon",
      r: "torre",
      n: "caballo",
      b: "alfil",
      q: "reina",
      k: "rey",
    };

    const nombre = map[cell.type]; // ej. "torre"
    const color = cell.color === "w" ? "B" : "N"; // B = blancas, N = negras
    const src = `/pieces/${nombre}${color}.svg`;

    return (
      <img
        src={src}
        alt={`${nombre}-${color}`}
        style={{ width: "48px", height: "48px" }}
      />
    );
  }

  return (
    <button
      onClick={() => onClick(row, col)}
      style={{
        width: "62px",
        height: "62px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        border: "none",
        cursor: "pointer",
        background: isSelected ? "#f6f669" : bg,
      }}
    >
      {renderPiece(cell)}
    </button>
  );
}
