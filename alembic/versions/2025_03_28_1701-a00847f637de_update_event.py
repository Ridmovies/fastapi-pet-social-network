"""update Event

Revision ID: a00847f637de
Revises: 974370dc617a
Create Date: 2025-03-28 17:01:57.791639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a00847f637de'
down_revision: Union[str, None] = '974370dc617a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'start_datetime')
    op.drop_column('event', 'end_datetime')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('end_datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('event', sa.Column('start_datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
