"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"

interface ChessBoardProps {
  gameState: string | null
  onMove: (move: { move: string }) => void
  turn?: string // "w" o "b"
}

const PIECE_SYMBOLS: Record<string, string> = {
  K: "♔", Q: "♕", R: "♖", B: "♗", N: "♘", P: "♙",
  k: "♚", q: "♛", r: "♜", b: "♝", n: "♞", p: "♟",
}

const colToFile = ["a","b","c","d","e","f","g","h"]
function coordsToSquare(row: number, col: number) {
  const file = colToFile[col]
  const rank = 8 - row
  return `${file}${rank}`
}

function parseFEN(fen: string): (string | null)[][] {
  const rows = fen.split(" ")[0].split("/")
  return rows.map(row => {
    const squares: (string | null)[] = []
    for (const char of row) {
      if (/[1-8]/.test(char)) {
        for (let i = 0; i < parseInt(char); i++) squares.push(null)
      } else {
        squares.push(char)
      }
    }
    return squares
  })
}

export default function ChessBoard({ gameState, onMove, turn }: ChessBoardProps) {
  const [selectedSquare, setSelectedSquare] = useState<[number, number] | null>(null)
  const [board, setBoard] = useState<(string | null)[][]>(Array(8).fill(null).map(() => Array(8).fill(null)))
  const [isFlipped, setIsFlipped] = useState(false) // blancas abajo por defecto

  useEffect(() => {
    if (gameState) {
      setBoard(parseFEN(gameState))
    }
  }, [gameState])

  const canSelectPiece = (piece: string | null) => {
    if (!piece) return false
    if (turn === "w") return piece === piece.toUpperCase()
    if (turn === "b") return piece === piece.toLowerCase()
    return false
  }

  const handleSquareClick = (row: number, col: number) => {
    if (selectedSquare) {
      const from = coordsToSquare(selectedSquare[0], selectedSquare[1])
      const to = coordsToSquare(row, col)
      onMove({ move: from + to })
      setSelectedSquare(null)
    } else if (board[row][col] && canSelectPiece(board[row][col])) {
      setSelectedSquare([row, col])
    }
  }

  const displayedBoard = isFlipped ? board.slice().reverse() : board

  return (
    <div className="chess-board-3d p-4 md:p-8">
      <div className="flex justify-end mb-2">
        <Button variant="outline" onClick={() => setIsFlipped(!isFlipped)}>
          Cambiar orientación
        </Button>
      </div>
      <div className="wood-texture bg-gradient-to-br from-primary to-primary/80 p-6 rounded-2xl shadow-2xl border-4 border-primary/30">
        <div className="grid grid-cols-8 gap-1 bg-muted/20 p-2 rounded-xl">
          {displayedBoard.map((row, rowIndex) =>
            row.map((piece, colIndex) => {
              const isLight = (rowIndex + colIndex) % 2 === 0
              const isSelected = selectedSquare && selectedSquare[0] === (isFlipped ? 7 - rowIndex : rowIndex) && selectedSquare[1] === colIndex
              return (
                <div
                  key={`${rowIndex}-${colIndex}`}
                  onClick={() => handleSquareClick(isFlipped ? 7 - rowIndex : rowIndex, colIndex)}
                  className={`
                    aspect-square flex items-center justify-center
                    rounded-md cursor-pointer
                    ${isLight ? "bg-secondary/90 hover:bg-secondary" : "bg-primary/60 hover:bg-primary/70"}
                    ${isSelected ? "ring-4 ring-accent shadow-lg" : ""}
                  `}
                >
                  {piece && (
                    <span className="text-4xl md:text-5xl select-none">
                      {PIECE_SYMBOLS[piece]}
                    </span>
                  )}
                </div>
              )
            }),
          )}
        </div>
        <div className="flex justify-between mt-3 px-2 text-xs font-mono text-primary-foreground/70">
          {["a","b","c","d","e","f","g","h"].map((letter) => (
            <span key={letter}>{letter}</span>
          ))}
        </div>
      </div>
    </div>
  )
}
