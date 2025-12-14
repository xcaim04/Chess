export const PIECE_UNICODE = {
  p: "♟", r: "♜", n: "♞", b: "♝", q: "♛", k: "♚",
  P: "♙", R: "♖", N: "♘", B: "♗", Q: "♕", K: "♔",
};

export function toSquare(row, col) {
  const file = "abcdefgh"[col];
  const rank = 8 - row;
  return `${file}${rank}`;
}

export function squareColor(row, col) {
  return (row + col) % 2 === 0 ? "#f0d9b5" : "#b58863";
}
