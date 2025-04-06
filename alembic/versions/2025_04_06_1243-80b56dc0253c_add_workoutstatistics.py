"""add WorkoutStatistics

Revision ID: 80b56dc0253c
Revises: 
Create Date: 2025-04-06 12:43:27.806158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80b56dc0253c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.LargeBinary(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('achievement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
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
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('start_datetime', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('end_datetime', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('max_participants', sa.Integer(), nullable=True),
    sa.Column('is_private', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('required_equipment', sa.String(), nullable=True),
    sa.Column('skill_level', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_title'), 'event', ['title'], unique=False)
    op.create_table('gym_workout',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('equipment', sa.Enum('ANY', 'NONE', 'BARBELL', 'DUMBBELLS', 'RESISTANCE_BANDS', 'BENCH', 'KETTLEBELLS', 'WEIGHT_PLATES', 'GYMNASTIC_BALL', 'EZ_BAR', 'PULL_UP_BAR', 'MACHINES', name='equipment'), nullable=False),
    sa.Column('difficulty', sa.Enum('ALL', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', name='difficultylevel'), nullable=False),
    sa.Column('workout_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('read', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('receiver_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_to_user',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('following_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['following_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'following_id')
    )
    op.create_table('workout',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('type', sa.Enum('RUN', 'BICYCLE', 'WALK', name='workouttype'), nullable=False),
    sa.Column('map', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workout_statistics',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('total_workouts', sa.Integer(), nullable=False),
    sa.Column('total_distance_km', sa.Float(), nullable=False),
    sa.Column('total_duration_sec', sa.Integer(), nullable=False),
    sa.Column('runs_count', sa.Integer(), nullable=False),
    sa.Column('runs_distance', sa.Float(), nullable=False),
    sa.Column('bicycles_count', sa.Integer(), nullable=False),
    sa.Column('bicycles_distance', sa.Float(), nullable=False),
    sa.Column('walks_count', sa.Integer(), nullable=False),
    sa.Column('walks_distance', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('bicycle',
    sa.Column('max_speed_kmh', sa.Float(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.Column('distance_km', sa.Float(), nullable=False),
    sa.Column('duration_sec', sa.Integer(), nullable=False),
    sa.Column('avg_speed_kmh', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['workout_id'], ['workout.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('community_chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('community_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['community_id'], ['community.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_community_chat_id'), 'community_chat', ['id'], unique=False)
    op.create_table('community_member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('community_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['community_id'], ['community.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_community_member_id'), 'community_member', ['id'], unique=False)
    op.create_table('event_participation',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('joined_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'event_id')
    )
    op.create_table('exercise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('muscle_group', sa.Enum('BACK', 'TRICEPS', 'CHEST', 'SHOULDERS', 'CORE', 'BICEPS', 'FOREARM', 'THIGHS', 'GLUTES', 'CALVES', 'FULL_BODY', name='musclegroup'), nullable=False),
    sa.Column('gym_workout_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['gym_workout_id'], ['gym_workout.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('community_id', sa.Integer(), nullable=False),
    sa.Column('image_path', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['community_id'], ['community.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('run',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.Column('distance_km', sa.Float(), nullable=False),
    sa.Column('duration_sec', sa.Integer(), nullable=False),
    sa.Column('avg_speed_kmh', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['workout_id'], ['workout.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('walk',
    sa.Column('avg_heart_rate_bpm', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.Column('distance_km', sa.Float(), nullable=False),
    sa.Column('duration_sec', sa.Integer(), nullable=False),
    sa.Column('avg_speed_kmh', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['workout_id'], ['workout.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.CheckConstraint('post_id IS NOT NULL OR event_id IS NOT NULL', name='check_comment_has_post_or_event'),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('community_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['community_chat.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_community_message_id'), 'community_message', ['id'], unique=False)
    op.create_table('exercise_set',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reps', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('like')
    op.drop_table('exercise_set')
    op.drop_index(op.f('ix_community_message_id'), table_name='community_message')
    op.drop_table('community_message')
    op.drop_table('comment')
    op.drop_table('walk')
    op.drop_table('run')
    op.drop_table('post')
    op.drop_table('exercise')
    op.drop_table('event_participation')
    op.drop_index(op.f('ix_community_member_id'), table_name='community_member')
    op.drop_table('community_member')
    op.drop_index(op.f('ix_community_chat_id'), table_name='community_chat')
    op.drop_table('community_chat')
    op.drop_table('bicycle')
    op.drop_table('workout_statistics')
    op.drop_table('workout')
    op.drop_table('user_to_user')
    op.drop_table('profile')
    op.drop_table('message')
    op.drop_table('gym_workout')
    op.drop_index(op.f('ix_event_title'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_community_name'), table_name='community')
    op.drop_index(op.f('ix_community_id'), table_name='community')
    op.drop_table('community')
    op.drop_table('achievement')
    op.drop_table('user')
    # ### end Alembic commands ###
