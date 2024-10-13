"""add user tqble

Revision ID: a4708bfb6d4a
Revises: ce33c0b7c0b1
Create Date: 2024-10-13 23:46:36.459733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4708bfb6d4a'
down_revision: Union[str, None] = 'ce33c0b7c0b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
