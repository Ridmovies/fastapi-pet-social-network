"""update Message

Revision ID: 03151afcce40
Revises: e7d6b52d270d
Create Date: 2025-03-21 17:18:21.359859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03151afcce40'
down_revision: Union[str, None] = 'e7d6b52d270d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('read', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'read')
    # ### end Alembic commands ###
