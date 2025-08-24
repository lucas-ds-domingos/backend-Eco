from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import produtos, categorias, produto_categorias, usuarios, auth_routes

app = FastAPI()

# Lista de origens permitidas
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:8000",  # pode incluir os dois se estiver usando diferente
]

# Adicionando o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Ou ["*"] para permitir todos (não recomendado em produção)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produtos.router)
app.include_router(categorias.router)
app.include_router(produto_categorias.router)
app.include_router(usuarios.router)
app.include_router(auth_routes.router)
