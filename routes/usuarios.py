from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=schemas.UsuarioOut)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.criar_usuario(db, usuario)

@router.get("/", response_model=list[schemas.UsuarioOut])
def listar(db: Session = Depends(get_db)):
    return crud.listar_usuarios(db)

@router.get("/{usuario_id}", response_model=schemas.UsuarioOut)
def buscar(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.buscar_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario
