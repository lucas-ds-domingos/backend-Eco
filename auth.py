from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "sua_chave_ultra_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plain: str, senha_hashed: str):
    return pwd_context.verify(senha_plain, senha_hashed)

def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)

def criar_token_dados(dados: dict, expira_em_min: Optional[int] = None):
    to_encode = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=expira_em_min or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        dados = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return dados
    except JWTError:
        return None
