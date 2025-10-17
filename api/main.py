from fastapi import FastAPI
from routers import book, hybrid_search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='BIBLIOTECA')

app.include_router(hybrid_search, prefix='/api/v1',
                   tags=['busca e conversacao'])
app.include_router(book, prefix='/api/v1', tags=['livros'])

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
