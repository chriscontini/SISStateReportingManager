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
