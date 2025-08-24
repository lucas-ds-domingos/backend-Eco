from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Produtos
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int
    imagem_url: Optional[str] = None
    ativo: Optional[bool] = True

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int
    criado_em: datetime

    class Config:
        orm_mode = True

# Categoria =============

class CategoriaBase(BaseModel):
    nome: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaOut(CategoriaBase):
    id: int

    class Config:
        from_attibutes = True

# Produto Categoria =========

class ProdutoCategoriaCreate(BaseModel):
    produto_id: int
    categoria_id: int


# Usuarios ============

class UsuarioBase(BaseModel):
    nome: str
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioOut(UsuarioBase):
    id: int
    tipo_usuario: str
    criado_em: datetime

    class Config:
        orm_mode = True  
