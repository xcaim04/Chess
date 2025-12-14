import Square from "./Square";

export default function Board({ board, selected, onSquareClick }) {
  return (
    <div style={{ display: "grid", gridTemplateRows: "repeat(8, 62px)", border: "4px solid #333", borderRadius: "6px" }}>
      {board.map((rowArr, row) => (
        <div key={row} style={{ display: "grid", gridTemplateColumns: "repeat(8, 62px)" }}>
          {rowArr.map((cell, col) => (
            <Square key={col} row={row} col={col} cell={cell} selected={selected} onClick={onSquareClick} />
          ))}
        </div>
      ))}
    </div>
  );
}
