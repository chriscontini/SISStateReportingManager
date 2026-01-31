"""
Pydantic schemas for API request/response validation.

These schemas define the shape of data for API endpoints.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ============ State Schemas ============

class StateBase(BaseModel):
    """Base schema for State."""
    name: str
    abbreviation: str
    doe_website: Optional[str] = None
    reporting_system_name: Optional[str] = None
    certification_required: bool = False


class StateCreate(StateBase):
    """Schema for creating a State."""
    pass


class StateUpdate(BaseModel):
    """Schema for updating a State."""
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    doe_website: Optional[str] = None
    reporting_system_name: Optional[str] = None
    certification_required: Optional[bool] = None


class StateResponse(StateBase):
    """Schema for State response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class StateListResponse(BaseModel):
    """Schema for list of states."""
    states: list[StateResponse]
    total: int


# ============ StateRequirement Schemas ============

class StateRequirementBase(BaseModel):
    """Base schema for StateRequirement."""
    requirement_name: str
    description: Optional[str] = None
    category: Optional[str] = None
    data_type: Optional[str] = None
    submission_format: Optional[str] = None
    submission_frequency: Optional[str] = None


class StateRequirementCreate(StateRequirementBase):
    """Schema for creating a StateRequirement."""
    state_id: int


class StateRequirementResponse(StateRequirementBase):
    """Schema for StateRequirement response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    state_id: int
    created_at: datetime


# ============ RankingFactor Schemas ============

class RankingFactorBase(BaseModel):
    """Base schema for RankingFactor."""
    name: str
    description: Optional[str] = None
    weight: float = 1.0
    data_source: Optional[str] = None
    is_active: bool = True


class RankingFactorCreate(RankingFactorBase):
    """Schema for creating a RankingFactor."""
    pass


class RankingFactorResponse(RankingFactorBase):
    """Schema for RankingFactor response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ============ StateScore Schemas ============

class StateScoreBase(BaseModel):
    """Base schema for StateScore."""
    score: float
    raw_value: Optional[str] = None
    notes: Optional[str] = None


class StateScoreCreate(StateScoreBase):
    """Schema for creating a StateScore."""
    state_id: int
    factor_id: int


class StateScoreResponse(StateScoreBase):
    """Schema for StateScore response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    state_id: int
    factor_id: int
    calculated_at: datetime


# ============ NCESData Schemas ============

class NCESDataBase(BaseModel):
    """Base schema for NCESData."""
    total_districts: Optional[int] = None
    total_schools: Optional[int] = None
    total_students: Optional[int] = None
    avg_district_size: Optional[float] = None
    data_year: Optional[str] = None
    district_structure: Optional[str] = None


class NCESDataCreate(NCESDataBase):
    """Schema for creating NCESData."""
    state_id: int


class NCESDataResponse(NCESDataBase):
    """Schema for NCESData response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    state_id: int
    created_at: datetime
    updated_at: datetime


# ============ Ranking Response Schemas ============

class StateRankingResponse(BaseModel):
    """Schema for a ranked state."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    abbreviation: str
    total_score: float
    rank: int
    scores: list[StateScoreResponse] = []


class RankingsResponse(BaseModel):
    """Schema for rankings list."""
    rankings: list[StateRankingResponse]
    factors: list[RankingFactorResponse]


# ============ State Detail Response ============

class ScoreWithFactor(BaseModel):
    """Score with its associated factor details."""
    factor_name: str
    factor_weight: float
    score: float
    weighted_score: float
    notes: Optional[str] = None


class StateDetailResponse(BaseModel):
    """Comprehensive state detail including NCES data and scores."""
    model_config = ConfigDict(from_attributes=True)

    # Basic info
    id: int
    name: str
    abbreviation: str
    doe_website: Optional[str] = None
    reporting_system_name: Optional[str] = None
    certification_required: bool = False
    created_at: datetime
    updated_at: datetime

    # NCES data
    nces_data: Optional[NCESDataResponse] = None

    # Scoring
    total_score: float = 0.0
    rank: Optional[int] = None
    scores: list[ScoreWithFactor] = []

    # Requirements (if any)
    requirements: list[StateRequirementResponse] = []


# ============ State Analysis Schemas ============

class StateAnalysisResponse(BaseModel):
    """Schema for Tier 2/3 deep state analysis."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    state_id: int
    analysis_tier: int

    # Reporting system details
    reporting_system_details: Optional[str] = None
    submission_requirements: Optional[str] = None
    data_elements_summary: Optional[str] = None

    # Competitive intelligence
    major_competitors: Optional[str] = None
    competitor_market_share: Optional[str] = None
    competitive_advantages: Optional[str] = None

    # Certification and compliance
    certification_process: Optional[str] = None
    compliance_requirements: Optional[str] = None
    estimated_certification_time: Optional[str] = None

    # Implementation insights
    key_challenges: Optional[str] = None
    recommended_approach: Optional[str] = None
    estimated_development_months: Optional[int] = None

    # AI analysis metadata
    ai_model_used: Optional[str] = None
    analysis_confidence: Optional[float] = None

    # Timestamps
    created_at: datetime
    updated_at: datetime


# ============ State Comparison Schemas ============

class StateComparison(BaseModel):
    """Single state data for comparison."""
    id: int
    name: str
    abbreviation: str
    total_score: float
    nces_data: Optional[NCESDataResponse] = None
    scores: list[ScoreWithFactor] = []
    has_analysis: bool = False


class StateComparisonResponse(BaseModel):
    """Response for state comparison endpoint."""
    states: list[StateComparison]
