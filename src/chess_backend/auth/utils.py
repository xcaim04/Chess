from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError
from ..core.security import create_access_token, decode_token

# Remplazar en la DB luego, solo para pruebas
_fake_users_db = {
    "carlos": {"username": "carlos", "hashed_password": ""},
    "demo": {"username": "demo", "hashed_password": ""},
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Inicializa contraseñas demo en memoria (solo para pruebas)
if not _fake_users_db["carlos"]["hashed_password"]:
    _fake_users_db["carlos"]["hashed_password"] = get_password_hash("1234")
if not _fake_users_db["demo"]["hashed_password"]:
    _fake_users_db["demo"]["hashed_password"] = get_password_hash("demo")

def authenticate_user(username: str, password: str):
    user = _fake_users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def issue_token_for_user(username: str) -> str:
    return create_access_token(username)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user = _fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user

def register_user(username: str, password: str):
    if username in _fake_users_db:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    _fake_users_db[username] = {
        "username": username,
        "hashed_password": get_password_hash(password)
    }
    return {"username": username}