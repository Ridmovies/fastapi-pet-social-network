"""update Event

Revision ID: 178552f09103
Revises: ca9d42ae1075
Create Date: 2025-03-31 11:23:51.135687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '178552f09103'
down_revision: Union[str, None] = 'ca9d42ae1075'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('event_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'event', ['event_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'event_id')
    # ### end Alembic commands ###
