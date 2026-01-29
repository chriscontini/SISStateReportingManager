"""Add tier to state_scores and create state_analyses table

Revision ID: 20260129_000002
Revises: 20260129_000001
Create Date: 2026-01-29

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260129_000002'
down_revision = '20260129_000001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add tier column to state_scores
    op.add_column('state_scores', sa.Column('tier', sa.Integer(), nullable=True))

    # Create state_analyses table
    op.create_table(
        'state_analyses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('state_id', sa.Integer(), sa.ForeignKey('states.id'), nullable=False, unique=True),
        sa.Column('analysis_tier', sa.Integer(), nullable=False, default=2),

        # Reporting system details
        sa.Column('reporting_system_details', sa.Text(), nullable=True),
        sa.Column('submission_requirements', sa.Text(), nullable=True),
        sa.Column('data_elements_summary', sa.Text(), nullable=True),

        # Competitive intelligence
        sa.Column('major_competitors', sa.Text(), nullable=True),
        sa.Column('competitor_market_share', sa.Text(), nullable=True),
        sa.Column('competitive_advantages', sa.Text(), nullable=True),

        # Certification and compliance
        sa.Column('certification_process', sa.Text(), nullable=True),
        sa.Column('compliance_requirements', sa.Text(), nullable=True),
        sa.Column('estimated_certification_time', sa.String(100), nullable=True),

        # Implementation insights
        sa.Column('key_challenges', sa.Text(), nullable=True),
        sa.Column('recommended_approach', sa.Text(), nullable=True),
        sa.Column('estimated_development_months', sa.Integer(), nullable=True),

        # AI analysis metadata
        sa.Column('ai_model_used', sa.String(100), nullable=True),
        sa.Column('analysis_confidence', sa.Float(), nullable=True),

        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Create index on state_id
    op.create_index('ix_state_analyses_state_id', 'state_analyses', ['state_id'])


def downgrade() -> None:
    # Drop state_analyses table
    op.drop_index('ix_state_analyses_state_id', table_name='state_analyses')
    op.drop_table('state_analyses')

    # Remove tier column from state_scores
    op.drop_column('state_scores', 'tier')
