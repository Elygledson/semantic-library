from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import authentication, setup_docs, book, hybrid_search

app = FastAPI(title='COLEÇÃO DE LIVROS - DOT',
              docs_url=None, redoc_url=None, openapi_url=None)

app.include_router(authentication, prefix='/api/v1', tags=['autenticacao'])
app.include_router(hybrid_search, prefix='/api/v1', tags=['busca'])
app.include_router(book, prefix='/api/v1', tags=['livros'])

setup_docs(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:4200'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/health", tags=["health"])
async def healthcheck():
    return {"status": "ok", "mensagem": "API esta executando!"}
