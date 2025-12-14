"use client"

import { useState, useEffect } from "react"
import LoginPage from "@/components/login-page"
import ChessGame from "@/components/chess-game"

export default function Home() {
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const savedToken = localStorage.getItem("chess_token")
    if (savedToken) {
      setToken(savedToken)
    }
    setIsLoading(false)
  }, [])

  const handleLogin = (newToken: string) => {
    setToken(newToken)
    localStorage.setItem("chess_token", newToken)
  }

  const handleLogout = () => {
    setToken(null)
    localStorage.removeItem("chess_token")
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
      </div>
    )
  }

  if (!token) {
    return <LoginPage onLogin={handleLogin} />
  }

  return <ChessGame token={token} onLogout={handleLogout} />
}
