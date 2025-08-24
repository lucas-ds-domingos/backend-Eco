from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from auth import verificar_senha, criar_token_dados
import models

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()
    if not usuario or not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = criar_token_dados({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}
