"use client";

import { useState, useEffect } from "react";
import ChessBoard from "@/components/chess-board";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface GameState {
  fen: string;
  turn?: string;
  game_over?: boolean;
  result?: string | null;
}

interface ChessGameProps {
  token: string;
  onLogout: () => void;
}

export default function ChessGame({ token, onLogout }: ChessGameProps) {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchGameState = async () => {
    try {
      const response = await fetch("/chess/state", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Error al obtener el estado del juego");
      const state = await response.json();
      setGameState(state);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setIsLoading(false);
    }
  };

  const handleMove = async (move: { move: string }) => {
    try {
      const response = await fetch("/chess/move", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(move),
      });
      if (!response.ok) throw new Error("Movimiento inválido");
      await fetchGameState();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Error al realizar movimiento"
      );
    }
  };

  const handleReset = async () => {
    try {
      setIsLoading(true);
      const response = await fetch("/chess/reset", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Error al reiniciar el juego");
      await fetchGameState();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al reiniciar");
    }
  };

  useEffect(() => {
    fetchGameState();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-muted/10 to-background p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl md:text-3xl font-bold">Chess Maestro</h1>
          <div className="flex gap-2">
            <Button onClick={handleReset} variant="outline">
              Reiniciar
            </Button>
            <Button onClick={onLogout} variant="outline">
              Salir
            </Button>
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="flex items-center justify-center h-[600px]">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
          </div>
        ) : (
          <div className="grid lg:grid-cols-[1fr,300px] gap-6">
            <div className="flex items-center justify-center">
              <ChessBoard
                gameState={gameState?.fen || null}
                onMove={handleMove}
                turn={gameState?.turn}
              />
            </div>
            <div className="space-y-4">
              <Card className="bg-card/60 backdrop-blur-sm border-2">
                <CardHeader>
                  <CardTitle>Estado del Juego</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p>
                    <strong>FEN:</strong> {gameState?.fen}
                  </p>
                  <p>
                    <strong>Turno:</strong>{" "}
                    {gameState?.turn === "w" ? "Blancas" : "Negras"}
                  </p>
                  <p>
                    <strong>Juego terminado:</strong>{" "}
                    {gameState?.game_over ? "Sí" : "No"}
                  </p>
                  <p>
                    <strong>Resultado:</strong>{" "}
                    {gameState?.result || "En curso"}
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
