"""
Database models for SISStateReportingManager.

SQLAlchemy ORM models for states, requirements, rankings, and related data.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, Float, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class State(Base):
    """
    US State model.

    Stores basic information about each state including DOE website
    and reporting system details.
    """
    __tablename__ = "states"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    abbreviation: Mapped[str] = mapped_column(String(2), nullable=False, unique=True)
    doe_website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    reporting_system_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    certification_required: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    requirements: Mapped[list["StateRequirement"]] = relationship(
        back_populates="state", cascade="all, delete-orphan"
    )
    nces_data: Mapped[Optional["NCESData"]] = relationship(
        back_populates="state", cascade="all, delete-orphan", uselist=False
    )
    scores: Mapped[list["StateScore"]] = relationship(
        back_populates="state", cascade="all, delete-orphan"
    )
    analysis: Mapped[Optional["StateAnalysis"]] = relationship(
        back_populates="state", cascade="all, delete-orphan", uselist=False
    )
    gap_analysis: Mapped[Optional["GapAnalysis"]] = relationship(
        back_populates="state", cascade="all, delete-orphan", uselist=False
    )
    roadmap: Mapped[Optional["Roadmap"]] = relationship(
        back_populates="state", cascade="all, delete-orphan", uselist=False
    )
    knowledge_articles: Mapped[list["KnowledgeArticle"]] = relationship(
        back_populates="state", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<State(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}')>"


class StateRequirement(Base):
    """
    State reporting requirement model.

    Stores individual data elements and requirements for state reporting.
    """
    __tablename__ = "state_requirements"

    id: Mapped[int] = mapped_column(primary_key=True)
    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"), nullable=False)

    requirement_name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    data_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    submission_format: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    submission_frequency: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    state: Mapped["State"] = relationship(back_populates="requirements")

    def __repr__(self) -> str:
        return f"<StateRequirement(id={self.id}, name='{self.requirement_name}')>"


class RankingFactor(Base):
    """
    Ranking factor configuration model.

    Stores the configurable factors used to rank states for expansion.
    """
    __tablename__ = "ranking_factors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    data_source: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    scores: Mapped[list["StateScore"]] = relationship(
        back_populates="factor", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<RankingFactor(id={self.id}, name='{self.name}', weight={self.weight})>"


class StateScore(Base):
    """
    State score model.

    Stores calculated scores for each state per ranking factor.
    """
    __tablename__ = "state_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"), nullable=False)
    factor_id: Mapped[int] = mapped_column(ForeignKey("ranking_factors.id"), nullable=False)

    score: Mapped[float] = mapped_column(Float, nullable=False)
    raw_value: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Tier classification (1, 2, or 3) based on total weighted score
    # Tier 1: > 70 (top candidates), Tier 2: 50-70 (potential), Tier 3: < 50 (low priority)
    tier: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Timestamps
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    state: Mapped["State"] = relationship(back_populates="scores")
    factor: Mapped["RankingFactor"] = relationship(back_populates="scores")

    def __repr__(self) -> str:
        return f"<StateScore(state_id={self.state_id}, factor_id={self.factor_id}, score={self.score})>"


class NCESData(Base):
    """
    NCES (National Center for Education Statistics) data model.

    Stores district and school statistics from NCES for market sizing.
    """
    __tablename__ = "nces_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"), nullable=False, unique=True)

    total_districts: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_schools: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_students: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    avg_district_size: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    data_year: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # District structure (county-based like LA, or fragmented like NJ)
    district_structure: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    state: Mapped["State"] = relationship(back_populates="nces_data")

    def __repr__(self) -> str:
        return f"<NCESData(state_id={self.state_id}, districts={self.total_districts})>"


class StateAnalysis(Base):
    """
    Deep state analysis model for Tier 2/3 analysis.

    Stores detailed AI-generated analysis including competitive intel,
    requirements deep-dive, and implementation insights.
    """
    __tablename__ = "state_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"), nullable=False, unique=True)

    # Analysis tier (2 or 3)
    analysis_tier: Mapped[int] = mapped_column(Integer, default=2, nullable=False)

    # Reporting system details
    reporting_system_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    submission_requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_elements_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Competitive intelligence
    major_competitors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    competitor_market_share: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    competitive_advantages: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Certification and compliance
    certification_process: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    compliance_requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estimated_certification_time: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Implementation insights
    key_challenges: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommended_approach: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estimated_development_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # AI analysis metadata
    ai_model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    analysis_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    state: Mapped["State"] = relationship(back_populates="analysis")

    def __repr__(self) -> str:
        return f"<StateAnalysis(state_id={self.state_id}, tier={self.analysis_tier})>"


class GapAnalysis(Base):
    """
    Gap analysis results for a state.

    Stores the overall gap analysis comparing a target state
    to NJ/LA baselines with effort estimates and projections.
    """
    __tablename__ = "gap_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"), nullable=False, unique=True)

    # Analysis configuration
    baseline_state: Mapped[str] = mapped_column(String(2), nullable=False)  # NJ or LA
    analysis_status: Mapped[str] = mapped_column(String(50), default="pending")

    # Gap counts
    total_gaps: Mapped[int] = mapped_column(Integer, default=0)
    critical_gaps: Mapped[int] = mapped_column(Integer, default=0)
    major_gaps: Mapped[int] = mapped_column(Integer, default=0)
    minor_gaps: Mapped[int] = mapped_column(Integer, default=0)

    # Effort estimates
    total_effort_hours: Mapped[int] = mapped_column(Integer, default=0)
    development_hours: Mapped[int] = mapped_column(Integer, default=0)
    testing_hours: Mapped[int] = mapped_column(Integer, default=0)
    certification_hours: Mapped[int] = mapped_column(Integer, default=0)

    # Timeline projections
    projected_months: Mapped[int] = mapped_column(Integer, default=0)
    projected_start_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    projected_end_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Summary
    executive_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommendation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    risk_assessment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    state: Mapped["State"] = relationship(back_populates="gap_analysis")
    gaps: Mapped[list["Gap"]] = relationship(
        back_populates="gap_analysis", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<GapAnalysis(state_id={self.state_id}, gaps={self.total_gaps})>"


class Gap(Base):
    """
    Individual gap between target state and baseline.

    Represents a specific requirement or capability that needs
    to be implemented for the target state.
    """
    __tablename__ = "gaps"

    id: Mapped[int] = mapped_column(primary_key=True)
    gap_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("gap_analyses.id"), nullable=False
    )

    # Gap identification
    gap_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Classification
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    # Categories: enrollment, attendance, grades, special_ed, assessments,
    # staff, finance, reporting, integration, certification
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    # Severity: critical, major, minor

    # Effort estimation
    effort_hours: Mapped[int] = mapped_column(Integer, default=0)
    complexity: Mapped[str] = mapped_column(String(20), default="medium")
    # Complexity: low, medium, high, very_high

    # Implementation details
    baseline_feature: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    required_changes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dependencies: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Status tracking
    status: Mapped[str] = mapped_column(String(50), default="identified")
    # Status: identified, in_progress, completed, deferred

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    gap_analysis: Mapped["GapAnalysis"] = relationship(back_populates="gaps")

    def __repr__(self) -> str:
        return f"<Gap(code={self.gap_code}, severity={self.severity})>"


class Roadmap(Base):
    """Implementation roadmap for a state expansion."""

    __tablename__ = "roadmaps"

    id: Mapped[int] = mapped_column(primary_key=True)
    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"), nullable=False, unique=True)

    # Roadmap metadata
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    # Status: draft, active, completed, on_hold

    # Timeline
    start_date: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    end_date: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    total_months: Mapped[int] = mapped_column(Integer, default=0)

    # Resource estimates
    total_effort_hours: Mapped[int] = mapped_column(Integer, default=0)
    peak_fte: Mapped[int] = mapped_column(Integer, default=0)
    total_budget_estimate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Source references
    gap_analysis_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("gap_analyses.id"), nullable=True
    )
    baseline_state: Mapped[str] = mapped_column(String(2), default="NJ")

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    state: Mapped["State"] = relationship(back_populates="roadmap")
    phases: Mapped[list["RoadmapPhase"]] = relationship(
        back_populates="roadmap", cascade="all, delete-orphan"
    )
    milestones: Mapped[list["RoadmapMilestone"]] = relationship(
        back_populates="roadmap", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Roadmap(state_id={self.state_id}, months={self.total_months})>"


class RoadmapPhase(Base):
    """A phase within an implementation roadmap."""

    __tablename__ = "roadmap_phases"

    id: Mapped[int] = mapped_column(primary_key=True)
    roadmap_id: Mapped[int] = mapped_column(ForeignKey("roadmaps.id"), nullable=False)

    # Phase identification
    phase_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timeline
    start_month: Mapped[int] = mapped_column(Integer, default=0)
    duration_months: Mapped[int] = mapped_column(Integer, default=1)
    end_month: Mapped[int] = mapped_column(Integer, default=1)

    # Resources
    effort_hours: Mapped[int] = mapped_column(Integer, default=0)
    fte_required: Mapped[float] = mapped_column(Float, default=1.0)

    # Status
    status: Mapped[str] = mapped_column(String(50), default="pending")
    # Status: pending, in_progress, completed
    progress_percent: Mapped[int] = mapped_column(Integer, default=0)

    # Dependencies (comma-separated phase numbers)
    dependencies: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Deliverables
    deliverables: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    roadmap: Mapped["Roadmap"] = relationship(back_populates="phases")

    def __repr__(self) -> str:
        return f"<RoadmapPhase(name={self.name}, months={self.duration_months})>"


class RoadmapMilestone(Base):
    """A milestone within an implementation roadmap."""

    __tablename__ = "roadmap_milestones"

    id: Mapped[int] = mapped_column(primary_key=True)
    roadmap_id: Mapped[int] = mapped_column(ForeignKey("roadmaps.id"), nullable=False)

    # Milestone details
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    milestone_type: Mapped[str] = mapped_column(String(50), default="checkpoint")
    # Types: checkpoint, deliverable, decision, external

    # Timeline
    target_month: Mapped[int] = mapped_column(Integer, nullable=False)
    target_date: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Status
    status: Mapped[str] = mapped_column(String(50), default="pending")
    # Status: pending, completed, missed, deferred
    completed_date: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Associated phase
    phase_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("roadmap_phases.id"), nullable=True
    )

    # Relationships
    roadmap: Mapped["Roadmap"] = relationship(back_populates="milestones")

    def __repr__(self) -> str:
        return f"<RoadmapMilestone(name={self.name}, month={self.target_month})>"


class KnowledgeArticle(Base):
    """Knowledge base article for state-specific documentation."""

    __tablename__ = "knowledge_articles"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Article content
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Categorization
    state_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("states.id"), nullable=True
    )
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    # Categories: reporting_requirements, certification, integration, best_practices, etc.
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    # Comma-separated tags

    # Source attribution
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    source_date: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Metadata
    author: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    state: Mapped[Optional["State"]] = relationship(back_populates="knowledge_articles")

    def __repr__(self) -> str:
        return f"<KnowledgeArticle(title={self.title[:30]})>"


class ChatSession(Base):
    """Chat session for AI assistant conversations."""

    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Session metadata
    title: Mapped[str] = mapped_column(String(200), default="New Chat")

    # Context filters for scoping knowledge retrieval
    state_filter: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at"
    )

    def __repr__(self) -> str:
        return f"<ChatSession(id={self.id}, title='{self.title[:30]}')>"


class ChatMessage(Base):
    """Individual message in a chat session."""

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("chat_sessions.id"), nullable=False)

    # Message content
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    # Role: user, assistant, system
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Citations/sources used (JSON array of article IDs)
    citations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Metadata
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    session: Mapped["ChatSession"] = relationship(back_populates="messages")

    def __repr__(self) -> str:
        return f"<ChatMessage(session_id={self.session_id}, role='{self.role}')>"


class KnowledgeEmbedding(Base):
    """Vector embeddings for knowledge articles for semantic search."""

    __tablename__ = "knowledge_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(
        ForeignKey("knowledge_articles.id"), nullable=False, unique=True
    )

    # Embedding vector (stored as JSON array since pgvector may not be available)
    # In production with pgvector, this would be: Vector(1536) for OpenAI embeddings
    embedding: Mapped[str] = mapped_column(Text, nullable=False)

    # Embedding metadata
    embedding_model: Mapped[str] = mapped_column(String(100), default="claude-3-haiku")
    embedding_dim: Mapped[int] = mapped_column(Integer, default=1024)

    # Content that was embedded (for cache invalidation)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<KnowledgeEmbedding(article_id={self.article_id})>"
