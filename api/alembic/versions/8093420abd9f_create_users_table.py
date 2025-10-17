"""create users table

Revision ID: 8093420abd9f
Revises: d4e4453de9e4
Create Date: 2025-09-29 16:08:18.730817

"""

from alembic import op
import sqlalchemy as sa
from typing import Sequence, Union
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = '8093420abd9f'
down_revision: Union[str, Sequence[str], None] = 'd4e4453de9e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('nome', sa.String(100), nullable=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('senha', sa.String(), nullable=False),
        sa.Column('criado_em', sa.DateTime(), nullable=False,
                  server_default=sa.func.now()),
        sa.Column('atualizado_em', sa.DateTime(),
                  nullable=False, server_default=sa.func.now()),
    )

    op.create_index('idx_usuarios_nome', 'usuarios', ['nome'])
    op.create_index('idx_usuarios_criado_em', 'usuarios', ['criado_em'])

    users_table = table(
        'usuarios',
        column('nome', sa.String),
        column('email', sa.String),
        column('senha', sa.String),
    )

    op.bulk_insert(
        users_table,
        [{
            'nome': 'admin',
            'email': 'admin@teste.com',
            'senha': "$2b$12$9P7uGuun1qwfwsUONOmq5uUzDYLkrNDY32jSDLnZcDH8dntrc8Nqm",
        }]
    )


def downgrade() -> None:
    op.drop_index('idx_usuarios_nome', table_name='usuarios')
    op.drop_index('idx_usuarios_criado_em', table_name='usuarios')
    op.drop_table('usuarios')
