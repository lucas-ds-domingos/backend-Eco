from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas, crud

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/", response_model=list[schemas.CategoriaOut])
def listar(db: Session = Depends(get_db)):
    return crud.listar_categorias(db)

@router.get("/{categoria_id}", response_model=schemas.CategoriaOut)
def buscar(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.buscar_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="categoria não encontrado")
    return categoria
    

@router.post("/", response_model=schemas.CategoriaOut)
def criar(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.criar_categoria(db, categoria)

@router.delete("/{categoria_id}", response_model=schemas.CategoriaOut)
def deletar(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.deletar_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrado")
    return categoria
