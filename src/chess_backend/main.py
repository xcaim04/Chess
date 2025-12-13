from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from auth.routes import router as auth_router
from chess_backend.auth.routes import router as auth_router
from chess_backend.chess.routes import router as chess_router

app = FastAPI(title="Chess API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chess_router, prefix="/chess", tags=["chess"])
