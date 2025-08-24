from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database import get_db
import models
from auth import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_usuario_logado(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
        if usuario is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return usuario
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
