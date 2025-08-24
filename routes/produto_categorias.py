
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/produto-categoria", tags=["ProdutoCategoria"])

@router.post("/")
def associar_categoria(
    dados: schemas.ProdutoCategoriaCreate, db: Session = Depends(get_db)
):
    try:
        produto = crud.definir_categoria(
            db, produto_id=dados.produto_id, categoria_id=dados.categoria_id
        )
        return {"mensagem": "Categoria associada com sucesso!", "produto_id": produto.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
