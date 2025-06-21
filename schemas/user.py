# ========================================
# ? Importação de Bibliotecas necessárias
# ========================================
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


# =======================================================
# ? Schema Base para campos comuns de User (sem a senha)
# =======================================================
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr  # O Pydantic valida se é um email válido
    full_name: Optional[str] = Field(None, max_length=100)
    disabled: Optional[bool] = False  # Campo para indicar se o usuário está desativado


# =============================================
# ? Schema para criar um User (inclui a senha)
# =============================================
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)  # A senha é obrigatória na criação
    is_admin: bool = False


# ================================================================
# ? Schema para atualizar um User (A senha não é atualizada aqui)
# ================================================================
class UserUpdate(UserBase):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    disabled: Optional[bool] = None
    is_admin: bool
    # Não incluído 'password' aqui, pois a atualização de senha geralmente
    # é feita em uma rota separada por questões de segurança.


# ================================================================
# ? Schema para a resposta de um User (nunca retorna a senha!)
# ================================================================
class UserResponse(UserBase):
    id: int  # O ID é gerado pelo banco de dados
    disabled: bool = False  # Inclui o campo disabled na resposta
    is_admin: bool

    class Config:
        from_attributes = True  # Habilita atributos do modelo SQLAlchemy
