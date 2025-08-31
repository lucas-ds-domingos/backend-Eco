from sqlalchemy.orm import Session
from models import Produto
from schemas import ProdutoCreate, UsuarioUpdate, ProdutoUpdate
import models, schemas
from passlib.hash import bcrypt
from auth import gerar_hash_senha
from fastapi import HTTPException

#  Produtos

def listar_produtos(db: Session):
    return db.query(Produto).all()

def buscar_produto(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id == produto_id).first()

def criar_produto(db: Session, produto: ProdutoCreate):
    db_produto = Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def deletar_produto(db: Session, produto_id: int):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        db.delete(produto)
        db.commit()
    return produto

def atualizar_produto(db: Session, produto_id: int, dados: ProdutoUpdate):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        return None
    for key, value in dados.dict(exclude_unset=True).items():
        setattr(produto, key, value)
    db.commit()
    db.refresh(produto)
    return produto


# Categorias

def criar_categoria(db: Session, categoria: schemas.CategoriaCreate):
    nova_categoria = models.Categoria(nome=categoria.nome)
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria

def listar_categorias(db: Session):
    return db.query(models.Categoria).all()

def buscar_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

def deletar_categoria(db: Session, categoria_id: int):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if categoria:
        db.delete(categoria)
        db.commit()
    return categoria

# Produto categoria ========

def definir_categoria(db: Session, produto_id: int, categoria_id: int):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

    if not produto or not categoria:
        raise ValueError("Produto ou Categoria não encontrados")

    # Garante que não será adicionada duas vezes
    if categoria not in produto.categorias:
        produto.categorias.append(categoria)
        db.commit()
        db.refresh(produto)

    return produto

# Usuarios ===========

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    usuario_db = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha)
    )
    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

def listar_usuarios(db: Session):
    return db.query(models.Usuario).all()

def buscar_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def excluir_usuario(db: Session, usuario_id: int):
    usuario_db = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(usuario_db)
    db.commit()
    return {"detail": "Usuário excluído com sucesso"}

def atualizar_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    usuario_db = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario_db:
        return None

    if usuario.nome is not None:
        usuario_db.nome = usuario.nome
    if usuario.email is not None:
        usuario_db.email = usuario.email
    if usuario.senha is not None:
        usuario_db.senha = gerar_hash_senha(usuario.senha)

    db.commit()
    db.refresh(usuario_db)
    return usuario_db