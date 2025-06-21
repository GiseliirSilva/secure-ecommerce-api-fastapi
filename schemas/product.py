# ========================================
# ? Importação de Bibliotecas necessárias
# ========================================
from pydantic import BaseModel, Field
from typing import Optional


# ============================================
# ? Schema Base para campos comuns de Product
# ============================================
class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)  # gt=0 significa "maior que zero"
    stock: int = Field(..., ge=0)  # ge=0 significa "maior ou igual a zero"


# =================================================
# ? Schema para criar um Product (usa ProductBase)
# =================================================
class ProductCreate(ProductBase):
    pass


# ===================================
# ? Schema para atualizar um Product
# ===================================
class ProductUpdate(ProductBase):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)


# =====================================================================
# ? Schema para a resposta de um Product (inclui o 'id' que vem do DB)
# =====================================================================
class ProductResponse(ProductBase):
    id: int  # O ID é gerado pelo banco de dados

    class Config:
        from_attributes = (
            True  # Habilita o modo ORM para ler dados de objetos SQLAlchemy
        )
