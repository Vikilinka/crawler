"""welcome

Revision ID: 72dda31f3e5d
Revises: 
Create Date: 2025-08-21 18:31:26.956651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '72dda31f3e5d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('create schema welcome')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('drop schema welcome')
