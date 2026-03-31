"""persona

Revision ID: 63ede865f432
Revises: 72dda31f3e5d
Create Date: 2026-01-17 09:15:07.312934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '63ede865f432'
down_revision: Union[str, Sequence[str], None] = '72dda31f3e5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('create schema persona')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('drop schema persona')
