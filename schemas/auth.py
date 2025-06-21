# ========================================
# ? Importação de Bibliotecas necessárias
# ========================================
from pydantic import BaseModel, EmailStr, Field


# ============================================================
# ? Schema para as credenciais de login que o usuário enviará
# ============================================================
class TokenRequest(BaseModel):
    username: str = Field(..., example="john_doe")  # Pode ser username ou email
    password: str = Field(..., example="senha_segura123")


# ============================================================
# ? Schema para a resposta da API após um login bem-sucedido
# ============================================================
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
