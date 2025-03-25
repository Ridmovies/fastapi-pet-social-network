"""update Activity

Revision ID: 0db6b568ff97
Revises: 3c50a97250cf
Create Date: 2025-03-25 14:36:25.967180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0db6b568ff97'
down_revision: Union[str, None] = '3c50a97250cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bicycle', sa.Column('duration_sec', sa.Integer(), nullable=False))
    op.drop_column('bicycle', 'duration_min')
    op.add_column('run', sa.Column('duration_sec', sa.Integer(), nullable=False))
    op.drop_column('run', 'duration_min')
    op.add_column('walk', sa.Column('duration_sec', sa.Integer(), nullable=False))
    op.drop_column('walk', 'duration_min')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('walk', sa.Column('duration_min', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('walk', 'duration_sec')
    op.add_column('run', sa.Column('duration_min', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('run', 'duration_sec')
    op.add_column('bicycle', sa.Column('duration_min', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('bicycle', 'duration_sec')
    # ### end Alembic commands ###
