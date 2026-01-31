"""Initial schema for State, StateRequirement, RankingFactor, StateScore, NCESData

Revision ID: 20260129_000001
Revises:
Create Date: 2026-01-29

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260129_000001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create states table
    op.create_table(
        'states',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('abbreviation', sa.String(length=2), nullable=False),
        sa.Column('doe_website', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('abbreviation'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_states_abbreviation'), 'states', ['abbreviation'], unique=True)
    op.create_index(op.f('ix_states_name'), 'states', ['name'], unique=True)

    # Create ranking_factors table
    op.create_table(
        'ranking_factors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('weight', sa.Float(), nullable=False),
        sa.Column('data_source', sa.String(length=200), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_ranking_factors_name'), 'ranking_factors', ['name'], unique=True)

    # Create state_requirements table
    op.create_table(
        'state_requirements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('state_id', sa.Integer(), nullable=False),
        sa.Column('requirement_name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('data_type', sa.String(length=50), nullable=True),
        sa.Column('submission_format', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['state_id'], ['states.id'], ondelete='CASCADE')
    )
    op.create_index(op.f('ix_state_requirements_state_id'), 'state_requirements', ['state_id'], unique=False)

    # Create state_scores table
    op.create_table(
        'state_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('state_id', sa.Integer(), nullable=False),
        sa.Column('factor_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('calculated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['state_id'], ['states.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['factor_id'], ['ranking_factors.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('state_id', 'factor_id', name='unique_state_factor_score')
    )
    op.create_index(op.f('ix_state_scores_state_id'), 'state_scores', ['state_id'], unique=False)
    op.create_index(op.f('ix_state_scores_factor_id'), 'state_scores', ['factor_id'], unique=False)

    # Create nces_data table
    op.create_table(
        'nces_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('state_id', sa.Integer(), nullable=False),
        sa.Column('total_districts', sa.Integer(), nullable=True),
        sa.Column('total_schools', sa.Integer(), nullable=True),
        sa.Column('total_students', sa.Integer(), nullable=True),
        sa.Column('avg_district_size', sa.Float(), nullable=True),
        sa.Column('data_year', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['state_id'], ['states.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('state_id', 'data_year', name='unique_state_year_nces')
    )
    op.create_index(op.f('ix_nces_data_state_id'), 'nces_data', ['state_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_nces_data_state_id'), table_name='nces_data')
    op.drop_table('nces_data')

    op.drop_index(op.f('ix_state_scores_factor_id'), table_name='state_scores')
    op.drop_index(op.f('ix_state_scores_state_id'), table_name='state_scores')
    op.drop_table('state_scores')

    op.drop_index(op.f('ix_state_requirements_state_id'), table_name='state_requirements')
    op.drop_table('state_requirements')

    op.drop_index(op.f('ix_ranking_factors_name'), table_name='ranking_factors')
    op.drop_table('ranking_factors')

    op.drop_index(op.f('ix_states_name'), table_name='states')
    op.drop_index(op.f('ix_states_abbreviation'), table_name='states')
    op.drop_table('states')
