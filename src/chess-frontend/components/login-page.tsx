"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

interface LoginPageProps {
  onLogin: (token: string) => void
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [loginData, setLoginData] = useState({ username: "", password: "" })
  const [registerData, setRegisterData] = useState({ username: "", password: "" })

  const doLogin = async (username: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append("grant_type", "password")
    formData.append("username", username)
    formData.append("password", password)

    const response = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    })

    if (!response.ok) throw new Error("Credenciales incorrectas")
    const data = await response.json()
    onLogin(data.access_token)
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)
    try {
      await doLogin(loginData.username, loginData.password)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al iniciar sesión")
    } finally {
      setIsLoading(false)
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)
    try {
      const response = await fetch("/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(registerData),
      })
      if (!response.ok) throw new Error("Error al registrar usuario")
      await doLogin(registerData.username, registerData.password)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al registrar")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-background via-muted/20 to-background">
      <div className="w-full max-w-md relative">
        <Card className="relative backdrop-blur-sm bg-card/95 border-2 shadow-2xl">
          <CardHeader className="space-y-3 text-center">
            <CardTitle className="text-3xl font-bold">Chess Maestro</CardTitle>
            <CardDescription>Juega ajedrez contra la IA en un tablero 3D realista</CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="login" className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-6">
                <TabsTrigger value="login">Iniciar Sesión</TabsTrigger>
                <TabsTrigger value="register">Registrarse</TabsTrigger>
              </TabsList>

              <TabsContent value="login">
                <form onSubmit={handleLogin} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="login-username">Usuario</Label>
                    <Input id="login-username" type="text" value={loginData.username}
                      onChange={(e) => setLoginData({ ...loginData, username: e.target.value })} required />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="login-password">Contraseña</Label>
                    <Input id="login-password" type="password" value={loginData.password}
                      onChange={(e) => setLoginData({ ...loginData, password: e.target.value })} required />
                  </div>
                  {error && <div className="text-sm text-destructive">{error}</div>}
                  <Button type="submit" disabled={isLoading}>{isLoading ? "Cargando..." : "Iniciar Sesión"}</Button>
                </form>
              </TabsContent>

              <TabsContent value="register">
                <form onSubmit={handleRegister} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="register-username">Usuario</Label>
                    <Input id="register-username" type="text" value={registerData.username}
                      onChange={(e) => setRegisterData({ ...registerData, username: e.target.value })} required />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="register-password">Contraseña</Label>
                    <Input id="register-password" type="password" value={registerData.password}
                      onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })} required />
                  </div>
                  {error && <div className="text-sm text-destructive">{error}</div>}
                  <Button type="submit" disabled={isLoading}>{isLoading ? "Creando..." : "Registrarse"}</Button>
                </form>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
