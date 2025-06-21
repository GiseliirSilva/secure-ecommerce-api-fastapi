# ========================================
# ? Importação de Bibliotecas necessárias
# ========================================
from passlib.context import CryptContext

# Defido o contexto de hashing de senhas
# scrypt é outra boa opção, bcrypt é bastante comum e seguro.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================
# ? Modelo para hash de senha
# ============================
class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se uma senha em texto puro corresponde a um hash de senha.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Gera o hash de uma senha em texto puro.
        """
        return pwd_context.hash(password)
