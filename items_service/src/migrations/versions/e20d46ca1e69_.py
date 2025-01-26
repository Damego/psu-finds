"""empty message

Revision ID: e20d46ca1e69
Revises: fada1187f62a
Create Date: 2025-01-26 22:44:33.417929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e20d46ca1e69'
down_revision: Union[str, None] = 'fada1187f62a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('image_url', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'image_url')
    # ### end Alembic commands ###
