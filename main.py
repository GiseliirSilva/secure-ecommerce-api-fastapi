# ========================================
# ? Importação de Bibliotecas necessárias
# ========================================

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta  # Necessário para manipular tempo de expiração do token
from sqlalchemy.orm import Session
from sqlalchemy.exc import (IntegrityError)  # Importa para lidar com erros de integridade (ex: email/username duplicado)
from dotenv import load_dotenv  # Para carregar variáveis de ambiente do .env
import os  # Para acessar variáveis de ambiente

# =============================================================
# ? Importa os modelos do SQLAlchemy e a função de sessão do DB
# ==============================================================
from database import models
from database.database import engine, get_db

# ==============================
# ? Importa os schemas Pydantic
# ==============================
from schemas import product as product_schemas
from schemas import user as user_schemas
from schemas import (
    auth as auth_schemas,
)  # Schemas para autenticação (TokenRequest, TokenResponse)

# ==========================================================
# ? Importa o Hasher para lidar com senhas de forma segura
# ==========================================================
from utils.security import Hasher
from utils import jwt as jwt_utils  # Módulo para JWT (geração e verificação)

# Carrega as variáveis do arquivo .env
load_dotenv()

# Cria todas as tabelas no banco de dados, se ainda não existirem
models.Base.metadata.create_all(bind=engine)

# Instância da aplicação FastAPI
app = FastAPI(title="API de E-commerce Simplificada")

# Configuração do OAuth2 para autenticação via Bearer token
# tokenUrl="token" aponta para a rota onde o cliente pode obter o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ==================================================
# ? FUNÇÕES AUXILIARES DE AUTENTICAÇÃO E AUTORIZAÇÃO
# ==================================================


# Função auxiliar para autenticar o usuário
# Verifica se o username/email e a senha correspondem a um usuário existente
def authenticate_user(db: Session, username: str, password: str):
    # Busca o usuário pelo username OU email
    user = (
        db.query(models.User)
        .filter((models.User.username == username) | (models.User.email == username))
        .first()
    )
    if not user:
        return False  # Usuário não encontrado

    # Verifica a senha usando o Hasher
    if not Hasher.verify_password(password, user.hashed_password):
        return False  # Senha incorreta

    return user  # Retorna o objeto User se a autenticação for bem-sucedida


# Exceção padrão para credenciais inválidas ou não validadas
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


# Função de dependência para obter o usuário atualmente logado
# Usada em rotas protegidas (Requires login)
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # Verifica o token JWT para extrair o username (subject)
    username = jwt_utils.verify_token(token, credentials_exception)

    # Busca o usuário no banco de dados pelo username extraído do token
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception  # Se o usuário não for encontrado (ex: foi deletado)

    # Verifica se o usuário está desativado
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return user  # Retorna o objeto User do banco de dados


# ======================
# ? ROTAS GERAIS DA API
# ======================


# Rota de exemplo para verificar se a API está funcionando
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de E-commerce!"}


# --- Rota para o Login e Geração de Token ---
# Recebe username e password e retorna um access token JWT
@app.post("/token", response_model=auth_schemas.TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),  # Captura username e password de um formulário
    db: Session = Depends(get_db),  # Injeta a sessão do banco de dados
):
    # Tenta autenticar o usuário usando a função auxiliar
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Se o usuário for desativado, proíbe o login
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    # Gera o token de acesso usando a utilidade JWT
    access_token = jwt_utils.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# =======================
# ? ROTAS PARA PRODUTOS
# =======================


# --- Rota para criar um novo produto ---
@app.post(
    "/products/",
    response_model=product_schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: product_schemas.ProductCreate,  # Recebe os dados do produto conforme o schema ProductCreate
    db: Session = Depends(get_db),  # Injeta a sessão do banco de dados
    current_user: user_schemas.UserResponse = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create products",
        )

    # Cria uma instância do modelo Product do SQLAlchemy com os dados recebidos
    db_product = models.Product(
        **product.model_dump()
    )  # .model_dump() converte o Pydantic em dict

    # Adiciona o produto ao banco de dados e o "commit"
    db.add(db_product)
    db.commit()
    db.refresh(
        db_product
    )  # Atualiza o objeto db_product com o ID gerado pelo DB e outros campos padrão
    return (
        db_product  # Retorna o objeto completo que será validado pelo ProductResponse
    )


# --- Rota para listar todos os produtos ---
@app.get("/products/", response_model=list[product_schemas.ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


# --- Rota para obter um produto específico pelo ID ---
@app.get("/products/{product_id}", response_model=product_schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


# --- Rota para atualizar um produto ---
@app.put("/products/{product_id}", response_model=product_schemas.ProductResponse)
def update_product(
    product_id: int,
    product_update: product_schemas.ProductUpdate,
    # Recebe o product_id do caminho da URL e um product_update (que usa o ProductUpdate schema, onde todos os campos são opcionais) no corpo da requisição.
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update products",
        )

    # Primeiro, ele tenta encontrar o produto no banco de dados pelo ID. Se não encontrar, ele retorna um erro 404 Not Found.
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # Atualiza apenas os campos que foram fornecidos na requisição
    # exclude_unset=True garante que apenas os campos que vieram no payload sejam atualizados
    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.add(db_product)  # Adiciona o objeto modificado de volta à sessão
    db.commit()  # Salva as alterações no banco
    db.refresh(db_product)  # Atualiza o objeto para refletir as alterações do banco
    return db_product


# --- Rota para deletar um produto ---
# Recebe o product_id do caminho da URL. Busca o produto. Se não encontrar, retorna 404.
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete products",
        )

    # para ser removido do banco de dados.
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    db.delete(db_product)  # Marca o objeto para ser deletado
    db.commit()  # Executa a deleção no banco
    """Para operações de deleção bem-sucedidas, o código de status 204 No Content é o mais apropriado. Ele indica que a requisição foi processada com sucesso, mas não há conteúdo para retornar no corpo da resposta. Por isso, a função return está vazia.
    """
    return


# =======================
# ? ROTAS PARA USUÁRIOS
# =======================


# --- Rota para criar um novo usuário (registro) ---
@app.post(
    "/users/",
    response_model=user_schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: user_schemas.UserCreate,  # Recebe os dados do usuário, incluindo a senha
    db: Session = Depends(get_db),
):
    # Verifica se já existe um usuário com o mesmo email ou username
    existing_user_email = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    existing_user_username = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if existing_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    # Cria o hash da senha usando o Hasher definido no utils/security.py
    # Hash da senha antes de armazenar
    hashed_password = Hasher.get_password_hash(user.password)

    # Cria uma instância do modelo User do SQLAlchemy com os dados recebidos
    # Note que a senha é armazenada como um hash, não em texto puro!
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,  # <--- Armazenando a senha hashed!
        full_name=user.full_name,
        disabled=user.disabled,
        is_admin=user.is_admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# --- Rota para listar todos os usuários ---
# Esta rota agora está protegida e exige autenticação
@app.get("/users/", response_model=list[user_schemas.UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(
        get_current_user
    ),  # Exige autenticação
):
    # O 'current_user' contém os dados do usuário logado, você pode usá-lo para
    # verificações de permissão (ex: if not current_user.is_admin: ...)
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


# --- Rota para obter um usuário específico pelo ID ---
@app.get("/users/{user_id}", response_model=user_schemas.UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_user),
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user's profile",
        )

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


# --- Rota para atualizar um usuário ---
@app.put("/users/{user_id}", response_model=user_schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: user_schemas.UserUpdate,  # Usa o schema de atualização (sem senha)
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_user),
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's profile",
        )

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Verifica se o email ou username está sendo atualizado para um valor já existente por outro usuário
    if user_update.email and user_update.email != db_user.email:
        existing_user = (
            db.query(models.User).filter(models.User.email == user_update.email).first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered by another user",
            )

    if user_update.username and user_update.username != db_user.username:
        existing_user = (
            db.query(models.User)
            .filter(models.User.username == user_update.username)
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered by another user",
            )

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# --- Rota para deletar um usuário ---
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_user),
):

    if current_user.id != user_id and not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.delete(db_user)
    db.commit()
    return
