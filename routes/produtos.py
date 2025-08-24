from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas, crud

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/", response_model=list[schemas.ProdutoOut])
def listar(db: Session = Depends(get_db)):
    return crud.listar_produtos(db)

@router.get("/{produto_id}", response_model=schemas.ProdutoOut)
def buscar(produto_id: int, db: Session = Depends(get_db)):
    produto = crud.buscar_produto(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/", response_model=schemas.ProdutoOut)
def criar(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.criar_produto(db, produto)

@router.delete("/{produto_id}", response_model=schemas.ProdutoOut)
def deletar(produto_id: int, db: Session = Depends(get_db)):
    produto = crud.deletar_produto(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto
