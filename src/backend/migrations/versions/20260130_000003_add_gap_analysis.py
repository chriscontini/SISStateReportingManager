"""Add gap_analyses and gaps tables for Sprint 4

Revision ID: 20260130_000003
Revises: 20260129_000002
Create Date: 2026-01-30

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260130_000003'
down_revision = '20260129_000002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create gap_analyses table
    op.create_table(
        'gap_analyses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('state_id', sa.Integer(), sa.ForeignKey('states.id'), nullable=False, unique=True),

        # Analysis configuration
        sa.Column('baseline_state', sa.String(2), nullable=False),  # NJ or LA
        sa.Column('analysis_status', sa.String(50), nullable=False, server_default='pending'),

        # Gap counts
        sa.Column('total_gaps', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('critical_gaps', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('major_gaps', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('minor_gaps', sa.Integer(), nullable=False, server_default='0'),

        # Effort estimates
        sa.Column('total_effort_hours', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('development_hours', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('testing_hours', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('certification_hours', sa.Integer(), nullable=False, server_default='0'),

        # Timeline projections
        sa.Column('projected_months', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('projected_start_date', sa.String(50), nullable=True),
        sa.Column('projected_end_date', sa.String(50), nullable=True),

        # Summary
        sa.Column('executive_summary', sa.Text(), nullable=True),
        sa.Column('recommendation', sa.Text(), nullable=True),
        sa.Column('risk_assessment', sa.Text(), nullable=True),

        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Create index on state_id
    op.create_index('ix_gap_analyses_state_id', 'gap_analyses', ['state_id'])

    # Create gaps table
    op.create_table(
        'gaps',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('gap_analysis_id', sa.Integer(), sa.ForeignKey('gap_analyses.id'), nullable=False),

        # Gap identification
        sa.Column('gap_code', sa.String(50), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),

        # Classification
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False),  # critical, major, minor

        # Effort estimation
        sa.Column('effort_hours', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('complexity', sa.String(20), nullable=False, server_default='medium'),

        # Implementation details
        sa.Column('baseline_feature', sa.String(200), nullable=True),
        sa.Column('required_changes', sa.Text(), nullable=True),
        sa.Column('dependencies', sa.Text(), nullable=True),

        # Status tracking
        sa.Column('status', sa.String(50), nullable=False, server_default='identified'),

        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    # Create indexes on gaps table
    op.create_index('ix_gaps_gap_analysis_id', 'gaps', ['gap_analysis_id'])
    op.create_index('ix_gaps_severity', 'gaps', ['severity'])
    op.create_index('ix_gaps_category', 'gaps', ['category'])


def downgrade() -> None:
    # Drop gaps table and indexes
    op.drop_index('ix_gaps_category', table_name='gaps')
    op.drop_index('ix_gaps_severity', table_name='gaps')
    op.drop_index('ix_gaps_gap_analysis_id', table_name='gaps')
    op.drop_table('gaps')

    # Drop gap_analyses table and index
    op.drop_index('ix_gap_analyses_state_id', table_name='gap_analyses')
    op.drop_table('gap_analyses')
