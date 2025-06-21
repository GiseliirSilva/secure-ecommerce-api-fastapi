# ========================================
# ? Importação de Bibliotecas necessárias
# ========================================
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv
from database.models import Base

# ===================================
# ? Configuração Inicial do Ambiente
# ===================================

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Obtém o objeto de configuração do Alembic, que contém informações
# do alembic.ini, como a URL do banco de dados (se definida lá).
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# ====================================
# ? Funções de Execução das Migrações
# ====================================
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    if url is None:  # Adicionado para caso a URL não esteja no alembic.ini
        url = os.getenv("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # CONEXÃO: pega DATABASE_URL diretamente do .env
    connectable = os.getenv("DATABASE_URL")

    if connectable is None:
        raise Exception(
            "DATABASE_URL não configurada no arquivo .env ou ambiente para o Alembic."
        )

    # Cria o engine a partir da URL
    engine = engine_from_config(
        {"sqlalchemy.url": connectable},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ========================================
# ? Ponto de Entrada Principal
# ========================================


# Verifica se o Alembic está sendo executado no modo offline ou online
# e chama a função apropriada.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
