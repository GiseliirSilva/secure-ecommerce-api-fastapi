# ========================================
# ? Importação de Bibliotecas necessárias
# ========================================
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Garante que as variáveis de ambiente sejam carregadas
load_dotenv()

# Pega a URL do banco de dados do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Verifica se a URL do banco de dados foi carregada
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está configurada no arquivo .env")

# Cria o engine do SQLAlchemy
# O pool_pre_ping é bom para conexões persistentes em longo prazo
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Cria a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para seus modelos (tabelas)
Base = declarative_base()


# ============================================================
# ? Função utilitária para obter uma sessão de banco de dados
# ============================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
