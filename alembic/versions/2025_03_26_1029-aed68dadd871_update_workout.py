"""update Workout

Revision ID: aed68dadd871
Revises: 9d1d312fac1e
Create Date: 2025-03-26 10:29:42.899500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aed68dadd871'
down_revision: Union[str, None] = '9d1d312fac1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workout', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('workout', 'title')
    # ### end Alembic commands ###
