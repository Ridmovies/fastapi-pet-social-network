"""change Event

Revision ID: 8d7fa11ebfca
Revises: 6f0154f187a4
Create Date: 2025-04-14 13:41:03.446580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d7fa11ebfca'
down_revision: Union[str, None] = '6f0154f187a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'required_equipment')
    op.drop_column('event', 'skill_level')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('skill_level', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('event', sa.Column('required_equipment', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
