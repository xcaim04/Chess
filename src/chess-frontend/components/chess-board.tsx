"use client"

import React, { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"

interface ChessBoardProps {
  gameState: string | null
  onMove: (move: { move: string }) => void
  turn?: string // "w" | "b"
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
  if (!fen) return Array(8).fill(null).map(() => Array(8).fill(null))
  const rows = fen.split(" ")[0].split("/")
  return rows.map(row => {
    const squares: (string | null)[] = []
    for (const char of row) {
      if (/[1-8]/.test(char)) {
        for (let i = 0; i < parseInt(char, 10); i++) squares.push(null)
      } else {
        squares.push(char)
      }
    }
    return squares
  })
}

export default function ChessBoard({ gameState, onMove, turn }: ChessBoardProps) {
  const [selectedSquare, setSelectedSquare] = useState<[number, number] | null>(null)
  const [hoverSquare, setHoverSquare] = useState<[number, number] | null>(null)
  const [board, setBoard] = useState<(string | null)[][]>(Array(8).fill(null).map(() => Array(8).fill(null)))
  const [legalTargets, setLegalTargets] = useState<Record<string, { san: string; to: string }[]>>({})
  const [isFlipped, setIsFlipped] = useState(false)

  useEffect(() => {
    if (!gameState) return
    setBoard(parseFEN(gameState))
    if (selectedSquare) {
      const from = coordsToSquare(selectedSquare[0], selectedSquare[1])
      computeLegalMoves(gameState, from)
    } else {
      setLegalTargets({})
    }
  }, [gameState])

  // computeLegalMoves: usa chess.js en frontend o tu backend
  function computeLegalMoves(fen: string, fromSquare: string) {
    try {
      // import dinámico para evitar aumentar bundle si no se usa
      // eslint-disable-next-line @typescript-eslint/no-var-requires
      const { Chess } = require("chess.js")
      const chess = new Chess(fen)
      const moves = chess.moves({ square: fromSquare, verbose: true }) as any[]
      const targets = moves.map(m => ({ san: m.san, to: m.to }))
      setLegalTargets(prev => ({ ...prev, [fromSquare]: targets }))
    } catch (err) {
      console.error("Error computing moves:", err)
      setLegalTargets({})
    }
  }

  const canSelectPiece = (piece: string | null) => {
    if (!piece) return false
    if (turn === "w") return piece === piece.toUpperCase()
    if (turn === "b") return piece === piece.toLowerCase()
    return false
  }

  function isLegalTarget(row: number, col: number) {
    if (!selectedSquare) return false
    const from = coordsToSquare(selectedSquare[0], selectedSquare[1])
    const targets = legalTargets[from] || []
    const sq = coordsToSquare(row, col)
    return targets.some(t => t.to === sq)
  }

  const handleSquareClick = (row: number, col: number) => {
    const clickedSquare = coordsToSquare(row, col)
    const clickedPiece = board[row][col]

    if (selectedSquare) {
      const from = coordsToSquare(selectedSquare[0], selectedSquare[1])
      if (from === clickedSquare) {
        setSelectedSquare(null)
        setLegalTargets({})
        return
      }
      if (clickedPiece && canSelectPiece(clickedPiece)) {
        setSelectedSquare([row, col])
        computeLegalMoves(gameState || "", clickedSquare)
        return
      }
      if (isLegalTarget(row, col)) {
        onMove({ move: from + clickedSquare })
        setSelectedSquare(null)
        setLegalTargets({})
        return
      }
      setSelectedSquare(null)
      setLegalTargets({})
      return
    }

    if (clickedPiece && canSelectPiece(clickedPiece)) {
      setSelectedSquare([row, col])
      computeLegalMoves(gameState || "", clickedSquare)
      return
    }
  }

  const handleSquareMouseEnter = (row: number, col: number) => {
    setHoverSquare([row, col])
    const piece = board[row][col]
    if (!selectedSquare && piece && canSelectPiece(piece)) {
      const square = coordsToSquare(row, col)
      computeLegalMoves(gameState || "", square)
    }
  }
  const handleSquareMouseLeave = () => {
    setHoverSquare(null)
    if (!selectedSquare) setLegalTargets({})
  }

  const displayedBoard = isFlipped ? board.slice().reverse() : board

  return (
    <div className="chess-board-3d p-3 md:p-6">
      <div className="flex justify-between items-center mb-3 gap-2">
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => setIsFlipped(!isFlipped)}>Cambiar orientación</Button>
        </div>

        {/* Opcional: botón para expandir a pantalla completa (implementar handler si quieres) */}
        {/* <Button onClick={enterFullscreen}>Expandir</Button> */}
      </div>

      <div className="bg-gradient-to-br from-primary to-primary/80 rounded-2xl shadow-2xl border-4 border-primary/30 p-3">
        {/* Contenedor responsive: en móvil usa casi todo el ancho, en escritorio tiene tope */}
        <div className="relative w-[95vw] sm:w-[90vw] md:w-full md:max-w-[min(95vw,1000px)] mx-auto">
          {/* Mantener proporción cuadrada */}
          <div className="w-full aspect-square rounded-lg overflow-hidden touch-none" style={{ touchAction: "manipulation" }}>
            <div className="grid grid-cols-8 grid-rows-8 w-full h-full gap-0">
              {displayedBoard.map((row, rowIndex) =>
                row.map((piece, colIndex) => {
                  const isLight = (rowIndex + colIndex) % 2 === 0
                  const actualRow = isFlipped ? 7 - rowIndex : rowIndex
                  const actualCol = colIndex
                  const isSelected =
                    selectedSquare &&
                    selectedSquare[0] === actualRow &&
                    selectedSquare[1] === actualCol
                  const isHover =
                    hoverSquare &&
                    hoverSquare[0] === actualRow &&
                    hoverSquare[1] === actualCol
                  const legal = isLegalTarget(actualRow, actualCol)

                  return (
                    <button
                      key={`${rowIndex}-${colIndex}`}
                      onClick={() => handleSquareClick(actualRow, actualCol)}
                      onMouseEnter={() => handleSquareMouseEnter(actualRow, actualCol)}
                      onMouseLeave={handleSquareMouseLeave}
                      className={`
                        relative w-full h-full flex items-center justify-center
                        ${isLight ? "bg-secondary/95 hover:bg-secondary" : "bg-primary/65 hover:bg-primary/70"}
                        ${isSelected ? "ring-4 ring-accent shadow-lg" : ""}
                        focus:outline-none
                      `}
                      aria-label={`Casilla ${coordsToSquare(actualRow, actualCol)}`}
                    >
                      {/* pieza: tamaño mayor en móvil con clamp */}
                      {piece && (
                        <span
                          className="select-none transition-transform duration-300 ease-in-out"
                          style={{ fontSize: "clamp(24px, 9vw, 72px)" }}
                        >
                          {PIECE_SYMBOLS[piece]}
                        </span>
                      )}

                      {/* highlight para destino legal */}
                      {legal && (
                        piece ? (
                          <div className="absolute w-8 h-8 md:w-10 md:h-10 rounded-full bg-accent/90 pointer-events-none" />
                        ) : (
                          <div className="absolute w-3 h-3 md:w-4 md:h-4 rounded-full bg-accent/100 pointer-events-none" />
                        )
                      )}

                      {/* hover preview: puntos en overlay */}
                      {isHover && !selectedSquare && piece && canSelectPiece(piece) && (
                        <div className="absolute inset-0 pointer-events-none">
                          {(() => {
                            const from = coordsToSquare(actualRow, actualCol)
                            const targets = legalTargets[from] || []
                            return targets.map(t => {
                              const file = t.to[0]
                              const rank = parseInt(t.to[1], 10)
                              const col = colToFile.indexOf(file)
                              const row = 8 - rank
                              const r = isFlipped ? 7 - row : row
                              const c = isFlipped ? 7 - col : col
                              const top = `${r * 12.5}%`
                              const left = `${c * 12.5}%`
                              return (
                                <div key={t.to} style={{ position: "absolute", top, left, width: "12.5%", height: "12.5%", display: "flex", alignItems: "center", justifyContent: "center", pointerEvents: "none" }}>
                                  <div className="w-3 h-3 md:w-4 md:h-4 rounded-full bg-accent/80" />
                                </div>
                              )
                            })
                          })()}
                        </div>
                      )}
                    </button>
                  )
                }),
              )}
            </div>
          </div>

          {/* coordenadas debajo del tablero */}
          <div className="flex justify-between mt-3 px-2 text-xs font-mono text-primary-foreground/70">
            {["a","b","c","d","e","f","g","h"].map((letter) => (
              <span key={letter}>{letter}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
