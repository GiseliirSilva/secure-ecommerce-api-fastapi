# ================================================================
# ? Importações necessárias do SQLAlchemy para definir os modelos
# ================================================================
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import (
    Base,
)  # Importa a base declarativa onde os modelos serão registrados


# ===================================
# ? Modelo para a tabela de Produtos
# ===================================
class Product(Base):
    __tablename__ = "products"  # Nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True)  # ID do produto, chave primária
    name = Column(String, index=True, nullable=False)  # Nome do produto (obrigatório)
    description = Column(String)  # Descrição do produto (opcional)
    price = Column(Float, nullable=False)  # Preço do produto (obrigatório)
    stock = Column(Integer, default=0)  # Quantidade em estoque, padrão é 0

    # Relacionamento: CartItem (um produto pode estar em muitos itens de carrinho)
    cart_items = relationship("CartItem", back_populates="product")

    def __repr__(self):
        # Representação legível do objeto para debug/log
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


# ==================================================
# ? Modelo para a tabela de Usuários (simplificado)
# ==================================================
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )  # Exemplo com Mapped
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    full_name: Mapped[str | None] = mapped_column(String, default=None)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Um usuário pode ter vários pedidos
    orders = relationship("Order", back_populates="user")
    # Um usuário tem um carrinho (relação 1:1)
    cart = relationship("Cart", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


# ===============================================================
# ? Modelo para a tabela de Carrinhos (um carrinho por usuário)
# ===============================================================
class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)  # ID do carrinho
    user_id = Column(
        Integer, ForeignKey("users.id"), unique=True
    )  # Relaciona com um único usuário
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )  # Data de criação automática
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now()
    )  # Atualiza automaticamente ao editar

    # Relacionamento com o usuário
    user = relationship("User", back_populates="cart")
    # Relacionamento com os itens do carrinho
    cart_items = relationship("CartItem", back_populates="cart")

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id})>"


# ====================================================================
# ? Modelo para os Itens do Carrinho (produtos dentro de um carrinho)
# ====================================================================
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)  # ID do item do carrinho
    cart_id = Column(
        Integer, ForeignKey("carts.id")
    )  # FK para o carrinho ao qual pertence
    product_id = Column(Integer, ForeignKey("products.id"))  # FK para o produto
    quantity = Column(Integer, default=1)  # Quantidade do produto nesse item

    # Relacionamento com o carrinho
    cart = relationship("Cart", back_populates="cart_items")
    # Relacionamento com o produto
    product = relationship("Product", back_populates="cart_items")

    def __repr__(self):
        return f"<CartItem(id={self.id}, cart_id={self.cart_id}, product_id={self.product_id}, quantity={self.quantity})>"


# ==========================
# ? Modelo para os Pedidos
# ==========================
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)  # ID do pedido
    user_id = Column(
        Integer, ForeignKey("users.id")
    )  # FK para o usuário que fez o pedido
    total_amount = Column(Float, nullable=False)  # Valor total do pedido
    status = Column(
        String, default="pending"
    )  # Status do pedido: pending, completed, cancelled, etc.
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )  # Data de criação
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now()
    )  # Data de última atualização

    # Relacionamento com o usuário
    user = relationship("User", back_populates="orders")
    # Relacionamento com os itens do pedido
    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total_amount={self.total_amount})>"


# ===================================================================
# ? Modelo para os Itens do Pedido (detalhes dos produtos comprados)
# ===================================================================
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)  # ID do item do pedido
    order_id = Column(Integer, ForeignKey("orders.id"))  # FK para o pedido
    product_id = Column(
        Integer, ForeignKey("products.id")
    )  # FK para o produto comprado
    quantity = Column(Integer, nullable=False)  # Quantidade do produto no pedido
    price_at_order = Column(
        Float, nullable=False
    )  # Preço do produto no momento da compra

    # Relacionamento com o pedido
    order = relationship("Order", back_populates="order_items")
    # Relacionamento com o produto (sem back_populates, pois não é necessário aqui)
    product = relationship("Product")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"
