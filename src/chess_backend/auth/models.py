from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class User(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str
    password: str