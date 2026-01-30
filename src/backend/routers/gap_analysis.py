"""
Gap Analysis API Router.

Endpoints for running gap analysis, retrieving results, and managing gaps.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.gap_service import GapService
from ..models import GapAnalysis, Gap


router = APIRouter(prefix="/api/gap-analysis", tags=["gap-analysis"])


# Pydantic response models
class GapResponse(BaseModel):
    id: int
    gap_code: str
    name: str
    description: Optional[str]
    category: str
    severity: str
    effort_hours: int
    complexity: str
    baseline_feature: Optional[str]
    required_changes: Optional[str]
    dependencies: Optional[str]
    status: str

    class Config:
        from_attributes = True


class GapAnalysisResponse(BaseModel):
    id: int
    state_id: int
    baseline_state: str
    analysis_status: str
    total_gaps: int
    critical_gaps: int
    major_gaps: int
    minor_gaps: int
    total_effort_hours: int
    development_hours: int
    testing_hours: int
    certification_hours: int
    projected_months: int
    projected_start_date: Optional[str]
    projected_end_date: Optional[str]
    executive_summary: Optional[str]
    recommendation: Optional[str]
    risk_assessment: Optional[str]
    gaps: list[GapResponse] = []

    class Config:
        from_attributes = True


class GapAnalysisSummary(BaseModel):
    id: int
    state_id: int
    state_name: str
    state_abbreviation: str
    baseline_state: str
    total_gaps: int
    critical_gaps: int
    total_effort_hours: int
    projected_months: int


class AnalyzeRequest(BaseModel):
    force_baseline: Optional[str] = None


class GapStatusUpdate(BaseModel):
    status: str


@router.post("/{state_id}/analyze", response_model=GapAnalysisResponse)
async def analyze_state(
    state_id: int,
    request: AnalyzeRequest = None,
    session: AsyncSession = Depends(get_db)
):
    """
    Run gap analysis for a state.

    Compares the target state against NJ or LA baseline and identifies gaps.
    """
    service = GapService(session)

    state = await service.get_state_by_id(state_id)
    if not state:
        raise HTTPException(status_code=404, detail="State not found")

    force_baseline = request.force_baseline if request else None

    try:
        analysis = await service.run_gap_analysis(state_id, force_baseline)

        # Fetch gaps for response
        gaps = await service.get_gaps_for_analysis(analysis.id)

        return GapAnalysisResponse(
            id=analysis.id,
            state_id=analysis.state_id,
            baseline_state=analysis.baseline_state,
            analysis_status=analysis.analysis_status,
            total_gaps=analysis.total_gaps,
            critical_gaps=analysis.critical_gaps,
            major_gaps=analysis.major_gaps,
            minor_gaps=analysis.minor_gaps,
            total_effort_hours=analysis.total_effort_hours,
            development_hours=analysis.development_hours,
            testing_hours=analysis.testing_hours,
            certification_hours=analysis.certification_hours,
            projected_months=analysis.projected_months,
            projected_start_date=analysis.projected_start_date,
            projected_end_date=analysis.projected_end_date,
            executive_summary=analysis.executive_summary,
            recommendation=analysis.recommendation,
            risk_assessment=analysis.risk_assessment,
            gaps=[GapResponse.model_validate(g) for g in gaps],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{state_id}", response_model=GapAnalysisResponse)
async def get_gap_analysis(
    state_id: int,
    session: AsyncSession = Depends(get_db)
):
    """
    Get existing gap analysis for a state.
    """
    service = GapService(session)

    analysis = await service.get_existing_gap_analysis(state_id)
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Gap analysis not found. Run POST /api/gap-analysis/{state_id}/analyze first."
        )

    gaps = await service.get_gaps_for_analysis(analysis.id)

    return GapAnalysisResponse(
        id=analysis.id,
        state_id=analysis.state_id,
        baseline_state=analysis.baseline_state,
        analysis_status=analysis.analysis_status,
        total_gaps=analysis.total_gaps,
        critical_gaps=analysis.critical_gaps,
        major_gaps=analysis.major_gaps,
        minor_gaps=analysis.minor_gaps,
        total_effort_hours=analysis.total_effort_hours,
        development_hours=analysis.development_hours,
        testing_hours=analysis.testing_hours,
        certification_hours=analysis.certification_hours,
        projected_months=analysis.projected_months,
        projected_start_date=analysis.projected_start_date,
        projected_end_date=analysis.projected_end_date,
        executive_summary=analysis.executive_summary,
        recommendation=analysis.recommendation,
        risk_assessment=analysis.risk_assessment,
        gaps=[GapResponse.model_validate(g) for g in gaps],
    )


@router.get("/{state_id}/gaps", response_model=list[GapResponse])
async def get_gaps(
    state_id: int,
    category: Optional[str] = Query(None, description="Filter by category"),
    severity: Optional[str] = Query(None, description="Filter by severity (critical, major, minor)"),
    session: AsyncSession = Depends(get_db)
):
    """
    Get gaps for a state's gap analysis with optional filtering.
    """
    service = GapService(session)

    analysis = await service.get_existing_gap_analysis(state_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Gap analysis not found")

    if category:
        gaps = await service.get_gaps_by_category(analysis.id, category)
    elif severity:
        gaps = await service.get_gaps_by_severity(analysis.id, severity)
    else:
        gaps = await service.get_gaps_for_analysis(analysis.id)

    return [GapResponse.model_validate(g) for g in gaps]


@router.patch("/gaps/{gap_id}/status", response_model=GapResponse)
async def update_gap_status(
    gap_id: int,
    update: GapStatusUpdate,
    session: AsyncSession = Depends(get_db)
):
    """
    Update the status of a specific gap.

    Valid statuses: identified, in_progress, completed, deferred
    """
    valid_statuses = ["identified", "in_progress", "completed", "deferred"]
    if update.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )

    service = GapService(session)
    gap = await service.update_gap_status(gap_id, update.status)

    if not gap:
        raise HTTPException(status_code=404, detail="Gap not found")

    return GapResponse.model_validate(gap)


@router.get("/", response_model=list[GapAnalysisSummary])
async def list_gap_analyses(
    session: AsyncSession = Depends(get_db)
):
    """
    List all gap analyses with summary information.
    """
    from sqlalchemy import select
    from ..models import GapAnalysis, State

    result = await session.execute(
        select(GapAnalysis, State)
        .join(State, GapAnalysis.state_id == State.id)
        .order_by(GapAnalysis.total_effort_hours)
    )

    analyses = result.all()

    return [
        GapAnalysisSummary(
            id=analysis.id,
            state_id=analysis.state_id,
            state_name=state.name,
            state_abbreviation=state.abbreviation,
            baseline_state=analysis.baseline_state,
            total_gaps=analysis.total_gaps,
            critical_gaps=analysis.critical_gaps,
            total_effort_hours=analysis.total_effort_hours,
            projected_months=analysis.projected_months,
        )
        for analysis, state in analyses
    ]


@router.get("/compare", response_model=list[GapAnalysisSummary])
async def compare_gap_analyses(
    ids: str = Query(..., description="Comma-separated state IDs to compare"),
    session: AsyncSession = Depends(get_db)
):
    """
    Compare gap analyses for multiple states.
    """
    from sqlalchemy import select
    from ..models import GapAnalysis, State

    state_ids = [int(id.strip()) for id in ids.split(",")]

    result = await session.execute(
        select(GapAnalysis, State)
        .join(State, GapAnalysis.state_id == State.id)
        .where(GapAnalysis.state_id.in_(state_ids))
        .order_by(GapAnalysis.total_effort_hours)
    )

    analyses = result.all()

    return [
        GapAnalysisSummary(
            id=analysis.id,
            state_id=analysis.state_id,
            state_name=state.name,
            state_abbreviation=state.abbreviation,
            baseline_state=analysis.baseline_state,
            total_gaps=analysis.total_gaps,
            critical_gaps=analysis.critical_gaps,
            total_effort_hours=analysis.total_effort_hours,
            projected_months=analysis.projected_months,
        )
        for analysis, state in analyses
    ]
