import os

SECRET_KEY = os.getenv("SECRET_KEY", "cambia_esta_clave_por_una_larga_y_segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
