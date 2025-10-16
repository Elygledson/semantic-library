"""adding extensions

Revision ID: d4e4453de9e4
Revises: 58c6fb6d3407
Create Date: 2025-09-29 16:04:42.230977

"""

from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'd4e4453de9e4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    op.execute('CREATE EXTENSION IF NOT EXISTS unaccent')


def downgrade() -> None:
    pass
