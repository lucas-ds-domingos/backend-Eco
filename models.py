from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, ForeignKey, TIMESTAMP, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    senha = Column(Text, nullable=False)
    tipo_usuario = Column(Text, default='cliente')
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

    enderecos = relationship('Endereco', back_populates='usuario')
    favoritos = relationship('Favorito', back_populates='usuario')
    carrinhos = relationship('Carrinho', back_populates='usuario')
    pedidos = relationship('Pedido', back_populates='usuario')
    avaliacoes = relationship('Avaliacao', back_populates='usuario')
    mensagens = relationship('Mensagem', back_populates='usuario')
    tokens = relationship('Token', back_populates='usuario')

class Endereco(Base):
    __tablename__ = 'enderecos'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    cep = Column(Text)
    rua = Column(Text)
    numero = Column(Text)
    complemento = Column(Text)
    bairro = Column(Text)
    cidade = Column(Text)
    estado = Column(Text)

    usuario = relationship('Usuario', back_populates='enderecos')

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False)
    descricao = Column(Text)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False)
    imagem_url = Column(Text)
    ativo = Column(Boolean, default=True)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

    imagens = relationship('ProdutoImagem', back_populates='produto')
    promocoes = relationship('Promocao', back_populates='produto')
    favoritos = relationship('Favorito', back_populates='produto')
    categorias = relationship('Categoria', secondary='produto_categorias', back_populates='produtos')
    pedido_itens = relationship('PedidoItem', back_populates='produto')
    carrinho_itens = relationship('CarrinhoItem', back_populates='produto')
    avaliacoes = relationship('Avaliacao', back_populates='produto')

class ProdutoImagem(Base):
    __tablename__ = 'produto_imagens'

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    imagem_url = Column(Text, nullable=False)

    produto = relationship('Produto', back_populates='imagens')

class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nome = Column(Text, nullable=False)

    produtos = relationship('Produto', secondary='produto_categorias', back_populates='categorias')

produto_categorias = Table(
    'produto_categorias', Base.metadata,
    Column('produto_id', Integer, ForeignKey('produtos.id')),
    Column('categoria_id', Integer, ForeignKey('categorias.id'))
)

class Promocao(Base):
    __tablename__ = 'promocoes'

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    percentual_desconto = Column(Numeric(5, 2))
    inicio = Column(TIMESTAMP)
    fim = Column(TIMESTAMP)

    produto = relationship('Produto', back_populates='promocoes')

class Favorito(Base):
    __tablename__ = 'favoritos'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

    usuario = relationship('Usuario', back_populates='favoritos')
    produto = relationship('Produto', back_populates='favoritos')

class Carrinho(Base):
    __tablename__ = 'carrinho'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

    usuario = relationship('Usuario', back_populates='carrinhos')
    itens = relationship('CarrinhoItem', back_populates='carrinho')

class CarrinhoItem(Base):
    __tablename__ = 'carrinho_itens'

    id = Column(Integer, primary_key=True)
    carrinho_id = Column(Integer, ForeignKey('carrinho.id'))
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    quantidade = Column(Integer)

    carrinho = relationship('Carrinho', back_populates='itens')
    produto = relationship('Produto', back_populates='carrinho_itens')

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    status = Column(Text, nullable=False)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)
    total = Column(Numeric(10, 2))

    usuario = relationship('Usuario', back_populates='pedidos')
    itens = relationship('PedidoItem', back_populates='pedido')
    status_hist = relationship('PedidoStatus', back_populates='pedido')
    pagamento = relationship('Pagamento', back_populates='pedido', uselist=False)
    nota_fiscal = relationship('NotaFiscal', back_populates='pedido', uselist=False)

class PedidoItem(Base):
    __tablename__ = 'pedido_itens'

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    quantidade = Column(Integer)
    preco_unitario = Column(Numeric(10, 2))

    pedido = relationship('Pedido', back_populates='itens')
    produto = relationship('Produto', back_populates='pedido_itens')

class PedidoStatus(Base):
    __tablename__ = 'pedido_status'

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    status = Column(Text)
    atualizado_em = Column(TIMESTAMP, default=datetime.utcnow)

    pedido = relationship('Pedido', back_populates='status_hist')

class Pagamento(Base):
    __tablename__ = 'pagamentos'

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    metodo = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    valor = Column(Numeric(10, 2))
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

    pedido = relationship('Pedido', back_populates='pagamento')

class NotaFiscal(Base):
    __tablename__ = 'notas_fiscais'

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    numero_nota = Column(Text)
    emitida_em = Column(TIMESTAMP, default=datetime.utcnow)

    pedido = relationship('Pedido', back_populates='nota_fiscal')

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    nota = Column(Integer)
    comentario = Column(Text)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

    usuario = relationship('Usuario', back_populates='avaliacoes')
    produto = relationship('Produto', back_populates='avaliacoes')

class Mensagem(Base):
    __tablename__ = 'mensagens'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    assunto = Column(Text)
    mensagem = Column(Text, nullable=False)
    resposta = Column(Text)
    enviada_em = Column(TIMESTAMP, default=datetime.utcnow)
    respondida_em = Column(TIMESTAMP)

    usuario = relationship('Usuario', back_populates='mensagens')

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    token = Column(Text)
    expiracao = Column(TIMESTAMP)

    usuario = relationship('Usuario', back_populates='tokens')

class NewsletterEmail(Base):
    __tablename__ = 'newsletter_emails'

    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True, nullable=False)
    inscrito_em = Column(TIMESTAMP, default=datetime.utcnow)
