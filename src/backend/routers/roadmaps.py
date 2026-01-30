"""
Roadmap API Router.

Endpoints for generating, retrieving, and managing implementation roadmaps.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..services.roadmap_service import RoadmapService
from ..models import Roadmap, RoadmapPhase, RoadmapMilestone


router = APIRouter(prefix="/api/roadmaps", tags=["roadmaps"])


# Pydantic response models
class MilestoneResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    milestone_type: str
    target_month: int
    target_date: Optional[str]
    status: str
    completed_date: Optional[str]
    phase_id: Optional[int]

    class Config:
        from_attributes = True


class PhaseResponse(BaseModel):
    id: int
    phase_number: int
    name: str
    description: Optional[str]
    start_month: int
    duration_months: int
    end_month: int
    effort_hours: int
    fte_required: float
    status: str
    progress_percent: int
    dependencies: Optional[str]
    deliverables: Optional[str]

    class Config:
        from_attributes = True


class RoadmapResponse(BaseModel):
    id: int
    state_id: int
    name: str
    description: Optional[str]
    status: str
    start_date: Optional[str]
    end_date: Optional[str]
    total_months: int
    total_effort_hours: int
    peak_fte: int
    total_budget_estimate: Optional[int]
    baseline_state: str
    gap_analysis_id: Optional[int]
    phases: list[PhaseResponse] = []
    milestones: list[MilestoneResponse] = []

    class Config:
        from_attributes = True


class RoadmapSummary(BaseModel):
    id: int
    state_id: int
    state_name: str
    state_abbreviation: str
    name: str
    status: str
    total_months: int
    total_effort_hours: int
    progress_percent: int


class GenerateRequest(BaseModel):
    force_regenerate: bool = False


class PhaseStatusUpdate(BaseModel):
    status: str
    progress_percent: Optional[int] = None


class MilestoneStatusUpdate(BaseModel):
    status: str


@router.post("/{state_id}/generate", response_model=RoadmapResponse)
async def generate_roadmap(
    state_id: int,
    request: GenerateRequest = None,
    session: AsyncSession = Depends(get_session)
):
    """
    Generate an implementation roadmap for a state.

    Requires gap analysis to be completed first.
    """
    service = RoadmapService(session)

    force = request.force_regenerate if request else False

    try:
        roadmap = await service.generate_roadmap(state_id, force_regenerate=force)

        # Get full details
        details = await service.get_roadmap_with_details(state_id)

        return RoadmapResponse(
            id=roadmap.id,
            state_id=roadmap.state_id,
            name=roadmap.name,
            description=roadmap.description,
            status=roadmap.status,
            start_date=roadmap.start_date,
            end_date=roadmap.end_date,
            total_months=roadmap.total_months,
            total_effort_hours=roadmap.total_effort_hours,
            peak_fte=roadmap.peak_fte,
            total_budget_estimate=roadmap.total_budget_estimate,
            baseline_state=roadmap.baseline_state,
            gap_analysis_id=roadmap.gap_analysis_id,
            phases=[PhaseResponse.model_validate(p) for p in details["phases"]],
            milestones=[MilestoneResponse.model_validate(m) for m in details["milestones"]],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{state_id}", response_model=RoadmapResponse)
async def get_roadmap(
    state_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get existing roadmap for a state.
    """
    service = RoadmapService(session)

    details = await service.get_roadmap_with_details(state_id)
    if not details:
        raise HTTPException(
            status_code=404,
            detail="Roadmap not found. Use POST /api/roadmaps/{state_id}/generate first."
        )

    roadmap = details["roadmap"]

    return RoadmapResponse(
        id=roadmap.id,
        state_id=roadmap.state_id,
        name=roadmap.name,
        description=roadmap.description,
        status=roadmap.status,
        start_date=roadmap.start_date,
        end_date=roadmap.end_date,
        total_months=roadmap.total_months,
        total_effort_hours=roadmap.total_effort_hours,
        peak_fte=roadmap.peak_fte,
        total_budget_estimate=roadmap.total_budget_estimate,
        baseline_state=roadmap.baseline_state,
        gap_analysis_id=roadmap.gap_analysis_id,
        phases=[PhaseResponse.model_validate(p) for p in details["phases"]],
        milestones=[MilestoneResponse.model_validate(m) for m in details["milestones"]],
    )


@router.get("/{state_id}/phases", response_model=list[PhaseResponse])
async def get_roadmap_phases(
    state_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get all phases for a state's roadmap.
    """
    service = RoadmapService(session)

    details = await service.get_roadmap_with_details(state_id)
    if not details:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    return [PhaseResponse.model_validate(p) for p in details["phases"]]


@router.patch("/phases/{phase_id}/status", response_model=PhaseResponse)
async def update_phase_status(
    phase_id: int,
    update: PhaseStatusUpdate,
    session: AsyncSession = Depends(get_session)
):
    """
    Update the status of a roadmap phase.

    Valid statuses: pending, in_progress, completed
    """
    valid_statuses = ["pending", "in_progress", "completed"]
    if update.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )

    service = RoadmapService(session)
    phase = await service.update_phase_status(
        phase_id,
        update.status,
        update.progress_percent
    )

    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")

    return PhaseResponse.model_validate(phase)


@router.patch("/milestones/{milestone_id}/status", response_model=MilestoneResponse)
async def update_milestone_status(
    milestone_id: int,
    update: MilestoneStatusUpdate,
    session: AsyncSession = Depends(get_session)
):
    """
    Update the status of a milestone.

    Valid statuses: pending, completed, missed, deferred
    """
    valid_statuses = ["pending", "completed", "missed", "deferred"]
    if update.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )

    service = RoadmapService(session)
    milestone = await service.update_milestone_status(milestone_id, update.status)

    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    return MilestoneResponse.model_validate(milestone)


@router.get("/", response_model=list[RoadmapSummary])
async def list_roadmaps(
    session: AsyncSession = Depends(get_session)
):
    """
    List all roadmaps with summary information.
    """
    from sqlalchemy import select
    from ..models import Roadmap, State, RoadmapPhase

    result = await session.execute(
        select(Roadmap, State)
        .join(State, Roadmap.state_id == State.id)
        .order_by(Roadmap.total_effort_hours)
    )

    roadmaps = result.all()
    summaries = []

    for roadmap, state in roadmaps:
        # Get phases to calculate progress
        phases_result = await session.execute(
            select(RoadmapPhase).where(RoadmapPhase.roadmap_id == roadmap.id)
        )
        phases = phases_result.scalars().all()

        service = RoadmapService(session)
        progress = service.calculate_roadmap_progress(phases)

        summaries.append(RoadmapSummary(
            id=roadmap.id,
            state_id=roadmap.state_id,
            state_name=state.name,
            state_abbreviation=state.abbreviation,
            name=roadmap.name,
            status=roadmap.status,
            total_months=roadmap.total_months,
            total_effort_hours=roadmap.total_effort_hours,
            progress_percent=progress["percent_complete"],
        ))

    return summaries


@router.get("/compare", response_model=list[RoadmapResponse])
async def compare_roadmaps(
    ids: str = Query(..., description="Comma-separated state IDs to compare"),
    session: AsyncSession = Depends(get_session)
):
    """
    Compare roadmaps for multiple states.
    """
    state_ids = [int(id.strip()) for id in ids.split(",")]

    service = RoadmapService(session)
    roadmaps = []

    for state_id in state_ids:
        details = await service.get_roadmap_with_details(state_id)
        if details:
            roadmap = details["roadmap"]
            roadmaps.append(RoadmapResponse(
                id=roadmap.id,
                state_id=roadmap.state_id,
                name=roadmap.name,
                description=roadmap.description,
                status=roadmap.status,
                start_date=roadmap.start_date,
                end_date=roadmap.end_date,
                total_months=roadmap.total_months,
                total_effort_hours=roadmap.total_effort_hours,
                peak_fte=roadmap.peak_fte,
                total_budget_estimate=roadmap.total_budget_estimate,
                baseline_state=roadmap.baseline_state,
                gap_analysis_id=roadmap.gap_analysis_id,
                phases=[PhaseResponse.model_validate(p) for p in details["phases"]],
                milestones=[MilestoneResponse.model_validate(m) for m in details["milestones"]],
            ))

    return roadmaps
