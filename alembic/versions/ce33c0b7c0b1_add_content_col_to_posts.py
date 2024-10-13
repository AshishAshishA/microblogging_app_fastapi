"""add content col to posts

Revision ID: ce33c0b7c0b1
Revises: 812643f9a6c5
Create Date: 2024-10-13 23:28:40.735153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce33c0b7c0b1'
down_revision: Union[str, None] = '812643f9a6c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
