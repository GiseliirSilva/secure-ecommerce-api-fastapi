# ========================================
# ? Importação de Bibliotecas necessárias
# ========================================
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# =======================
# ? Configurações do JWT
# =======================

# É CRUCIAL que esta chave seja mantida em segredo e não seja exposta!
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set.")

ALGORITHM = "HS256"  # Algoritmo de hashing para o JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tempo de expiração do token de acesso em minutos


# ============================================
# ? Funções para criar e verificar tokens JWT
# ============================================
def create_access_token(data: dict):
    """
    Cria um token de acesso JWT.
    data: Dicionário contendo os dados a serem codificados no token (ex: {"sub": "username"}).
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verifica a validade de um token JWT.
    token: O token JWT a ser verificado.
    credentials_exception: Uma exceção a ser levantada se o token for inválido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username  # Retorna o assunto (geralmente o username) do token
    except JWTError:
        raise credentials_exception
