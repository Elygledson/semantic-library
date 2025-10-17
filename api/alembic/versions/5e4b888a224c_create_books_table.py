"""create books table

Revision ID: 5e4b888a224c
Revises: 8093420abd9f
Create Date: 2025-09-29 16:10:06.407568

"""

from alembic import op
import sqlalchemy as sa

from typing import Sequence, Union
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '5e4b888a224c'
down_revision: Union[str, Sequence[str], None] = '8093420abd9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'livros',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('titulo', sa.String(100), nullable=False),
        sa.Column('autor', sa.String(100), nullable=False),
        sa.Column('resumo', sa.Text(), nullable=False),
        sa.Column('data_publicacao', sa.Date(), nullable=False),
        sa.Column('embedding', Vector(1536), nullable=False),
        sa.Column('criado_em', sa.DateTime(), nullable=False,
                  server_default=sa.func.now()),
        sa.Column('atualizado_em', sa.DateTime(),
                  nullable=False, server_default=sa.func.now()),
    )

    op.create_index('idx_livros_criado_em',
                    'livros', ['criado_em'])

    op.execute("""
    CREATE INDEX idx_livros_resumo_fulltext
    ON livros
    USING GIN (to_tsvector('portuguese', resumo));
    """)

    op.execute("""
    CREATE INDEX idx_livros_hnsw 
    ON livros 
    USING hnsw (embedding vector_cosine_ops) 
    WITH (m = 16, ef_construction = 200);
    """)


def downgrade() -> None:
    op.execute(
        "DROP INDEX IF EXISTS idx_livros_resumo_fulltext;")
    op.execute("DROP INDEX IF EXISTS idx_livros_hnsw;")

    op.drop_index('idx_livros_criado_em',
                  table_name='livros')

    op.drop_table('livros')
