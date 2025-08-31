from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Usuario  
from database import get_db  

router = APIRouter()

@router.get("/usuarios/search")
def buscar_usuarios_parcial(nome: str, db: Session = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.nome.ilike(f"%{nome}%")).all()
