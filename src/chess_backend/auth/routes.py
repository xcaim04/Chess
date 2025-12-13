from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .models import Token, UserCreate
from .utils import authenticate_user, issue_token_for_user, register_user

router = APIRouter()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    token = issue_token_for_user(user["username"])
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register(payload: UserCreate):
    return register_user(payload.username, payload.password)