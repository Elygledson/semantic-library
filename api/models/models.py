from pytz import timezone
from datetime import datetime
from sqlalchemy.orm import deferred
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Text,
    Column,
    DateTime,
    Integer,
    String,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    name = Column("nome", String(100), index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = deferred(Column("senha", String, nullable=False))
    created_at = Column("criado_em", DateTime, nullable=False, index=True,
                        default=lambda: datetime.now(timezone('America/Sao_Paulo')))
    updated_at = Column("atualizado_em", DateTime, nullable=False,
                        default=lambda: datetime.now(timezone('America/Sao_Paulo')))
    deleted_at = Column("deletado_em", DateTime, nullable=True)


class Book(Base):
    __tablename__ = 'livros'

    id = Column(Integer, primary_key=True)
    author = Column("autor", String(100), nullable=False)
    title = Column("titulo", String(100), nullable=False)
    summary = Column("resumo", Text(), nullable=False)
    embedding = Column("embedding", Vector(), nullable=False, index=True)
    created_at = Column("criado_em", DateTime, nullable=False, index=True,
                        default=lambda: datetime.now(timezone('America/Sao_Paulo')))
    updated_at = Column("atualizado_em", DateTime, nullable=False,
                        default=lambda: datetime.now(timezone('America/Sao_Paulo')))
    deleted_at = Column("deletado_em", DateTime, nullable=True)
