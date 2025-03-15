"""community

Revision ID: e74bbb0f7d83
Revises: c2cacbbdb6d5
Create Date: 2025-03-15 17:03:58.740108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e74bbb0f7d83'
down_revision: Union[str, None] = 'c2cacbbdb6d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('community',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_community_id'), 'community', ['id'], unique=False)
    op.create_index(op.f('ix_community_name'), 'community', ['name'], unique=False)
    op.create_table('community_member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('community_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['community_id'], ['community.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_community_member_id'), 'community_member', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_community_member_id'), table_name='community_member')
    op.drop_table('community_member')
    op.drop_index(op.f('ix_community_name'), table_name='community')
    op.drop_index(op.f('ix_community_id'), table_name='community')
    op.drop_table('community')
    # ### end Alembic commands ###
