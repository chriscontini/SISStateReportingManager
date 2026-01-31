"""Add roadmap and knowledge article tables for Sprint 5

Revision ID: 20260130_000004
Revises: 20260130_000003
Create Date: 2026-01-30

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260130_000004'
down_revision = '20260130_000003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create roadmaps table
    op.create_table(
        'roadmaps',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('state_id', sa.Integer(), sa.ForeignKey('states.id'), nullable=False, unique=True),

        # Roadmap metadata
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='draft'),

        # Timeline
        sa.Column('start_date', sa.String(20), nullable=True),
        sa.Column('end_date', sa.String(20), nullable=True),
        sa.Column('total_months', sa.Integer(), nullable=False, server_default='0'),

        # Resource estimates
        sa.Column('total_effort_hours', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('peak_fte', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_budget_estimate', sa.Integer(), nullable=True),

        # Source references
        sa.Column('gap_analysis_id', sa.Integer(), sa.ForeignKey('gap_analyses.id'), nullable=True),
        sa.Column('baseline_state', sa.String(2), nullable=False, server_default='NJ'),

        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_index('ix_roadmaps_state_id', 'roadmaps', ['state_id'])

    # Create roadmap_phases table
    op.create_table(
        'roadmap_phases',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('roadmap_id', sa.Integer(), sa.ForeignKey('roadmaps.id'), nullable=False),

        # Phase identification
        sa.Column('phase_number', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),

        # Timeline
        sa.Column('start_month', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('duration_months', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('end_month', sa.Integer(), nullable=False, server_default='1'),

        # Resources
        sa.Column('effort_hours', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('fte_required', sa.Float(), nullable=False, server_default='1.0'),

        # Status
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('progress_percent', sa.Integer(), nullable=False, server_default='0'),

        # Dependencies and deliverables
        sa.Column('dependencies', sa.String(100), nullable=True),
        sa.Column('deliverables', sa.Text(), nullable=True),
    )

    op.create_index('ix_roadmap_phases_roadmap_id', 'roadmap_phases', ['roadmap_id'])

    # Create roadmap_milestones table
    op.create_table(
        'roadmap_milestones',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('roadmap_id', sa.Integer(), sa.ForeignKey('roadmaps.id'), nullable=False),

        # Milestone details
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('milestone_type', sa.String(50), nullable=False, server_default='checkpoint'),

        # Timeline
        sa.Column('target_month', sa.Integer(), nullable=False),
        sa.Column('target_date', sa.String(20), nullable=True),

        # Status
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('completed_date', sa.String(20), nullable=True),

        # Associated phase
        sa.Column('phase_id', sa.Integer(), sa.ForeignKey('roadmap_phases.id'), nullable=True),
    )

    op.create_index('ix_roadmap_milestones_roadmap_id', 'roadmap_milestones', ['roadmap_id'])

    # Create knowledge_articles table
    op.create_table(
        'knowledge_articles',
        sa.Column('id', sa.Integer(), primary_key=True),

        # Article content
        sa.Column('title', sa.String(300), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),

        # Categorization
        sa.Column('state_id', sa.Integer(), sa.ForeignKey('states.id'), nullable=True),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('tags', sa.String(500), nullable=True),

        # Source attribution
        sa.Column('source_url', sa.String(500), nullable=True),
        sa.Column('source_name', sa.String(200), nullable=True),
        sa.Column('source_date', sa.String(20), nullable=True),

        # Metadata
        sa.Column('author', sa.String(100), nullable=True),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('view_count', sa.Integer(), nullable=False, server_default='0'),

        # Timestamps
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_index('ix_knowledge_articles_state_id', 'knowledge_articles', ['state_id'])
    op.create_index('ix_knowledge_articles_category', 'knowledge_articles', ['category'])


def downgrade() -> None:
    # Drop knowledge_articles
    op.drop_index('ix_knowledge_articles_category', table_name='knowledge_articles')
    op.drop_index('ix_knowledge_articles_state_id', table_name='knowledge_articles')
    op.drop_table('knowledge_articles')

    # Drop roadmap_milestones
    op.drop_index('ix_roadmap_milestones_roadmap_id', table_name='roadmap_milestones')
    op.drop_table('roadmap_milestones')

    # Drop roadmap_phases
    op.drop_index('ix_roadmap_phases_roadmap_id', table_name='roadmap_phases')
    op.drop_table('roadmap_phases')

    # Drop roadmaps
    op.drop_index('ix_roadmaps_state_id', table_name='roadmaps')
    op.drop_table('roadmaps')
