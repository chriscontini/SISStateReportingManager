"""
States API router.

Endpoints for managing US states and their reporting requirements.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(prefix="/api/states", tags=["states"])


@router.get("", response_model=schemas.StateListResponse)
async def list_states(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get all states with pagination."""
    states = await crud.get_states(db, skip=skip, limit=limit)
    total = await crud.get_states_count(db)
    return schemas.StateListResponse(
        states=[schemas.StateResponse.model_validate(s) for s in states],
        total=total,
    )


@router.get("/{state_id}", response_model=schemas.StateResponse)
async def get_state(
    state_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a single state by ID."""
    state = await crud.get_state(db, state_id)
    if state is None:
        raise HTTPException(status_code=404, detail="State not found")
    return schemas.StateResponse.model_validate(state)


@router.get("/abbreviation/{abbreviation}", response_model=schemas.StateResponse)
async def get_state_by_abbreviation(
    abbreviation: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a state by its abbreviation (e.g., 'NJ', 'TX')."""
    state = await crud.get_state_by_abbreviation(db, abbreviation)
    if state is None:
        raise HTTPException(status_code=404, detail="State not found")
    return schemas.StateResponse.model_validate(state)


@router.post("", response_model=schemas.StateResponse, status_code=201)
async def create_state(
    state: schemas.StateCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new state."""
    # Check if abbreviation already exists
    existing = await crud.get_state_by_abbreviation(db, state.abbreviation)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"State with abbreviation '{state.abbreviation}' already exists",
        )

    db_state = await crud.create_state(db, state)
    return schemas.StateResponse.model_validate(db_state)


@router.patch("/{state_id}", response_model=schemas.StateResponse)
async def update_state(
    state_id: int,
    state: schemas.StateUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing state."""
    db_state = await crud.update_state(db, state_id, state)
    if db_state is None:
        raise HTTPException(status_code=404, detail="State not found")
    return schemas.StateResponse.model_validate(db_state)


@router.delete("/{state_id}", status_code=204)
async def delete_state(
    state_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete a state."""
    success = await crud.delete_state(db, state_id)
    if not success:
        raise HTTPException(status_code=404, detail="State not found")


@router.get("/{state_id}/detail", response_model=schemas.StateDetailResponse)
async def get_state_detail(
    state_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get comprehensive state details including NCES data and all scores.

    Returns:
    - Basic state info (name, abbreviation, DOE website)
    - NCES data (districts, schools, students)
    - All ranking factor scores with weights
    - Total weighted score and rank
    - Any stored requirements
    """
    # Get the state
    state = await crud.get_state(db, state_id)
    if state is None:
        raise HTTPException(status_code=404, detail="State not found")

    # Get NCES data
    nces_result = await db.execute(
        select(models.NCESData).where(models.NCESData.state_id == state_id)
    )
    nces_data = nces_result.scalar_one_or_none()

    # Get all scores with their factors
    scores_result = await db.execute(
        select(models.StateScore, models.RankingFactor)
        .join(models.RankingFactor)
        .where(models.StateScore.state_id == state_id)
    )
    score_rows = scores_result.all()

    # Build score list with factor info
    scores_with_factors = []
    total_score = 0.0

    for score, factor in score_rows:
        weighted = score.score * factor.weight
        total_score += weighted
        scores_with_factors.append(schemas.ScoreWithFactor(
            factor_name=factor.name,
            factor_weight=factor.weight,
            score=score.score,
            weighted_score=weighted,
            notes=score.notes,
        ))

    # Get requirements
    reqs_result = await db.execute(
        select(models.StateRequirement).where(
            models.StateRequirement.state_id == state_id
        )
    )
    requirements = reqs_result.scalars().all()

    # Calculate rank (position among all states)
    rank = await _calculate_state_rank(db, state_id, total_score)

    return schemas.StateDetailResponse(
        id=state.id,
        name=state.name,
        abbreviation=state.abbreviation,
        doe_website=state.doe_website,
        reporting_system_name=getattr(state, 'reporting_system_name', None),
        certification_required=getattr(state, 'certification_required', False),
        created_at=state.created_at,
        updated_at=state.updated_at,
        nces_data=schemas.NCESDataResponse.model_validate(nces_data) if nces_data else None,
        total_score=total_score,
        rank=rank,
        scores=scores_with_factors,
        requirements=[schemas.StateRequirementResponse.model_validate(r) for r in requirements],
    )


async def _calculate_state_rank(
    db: AsyncSession,
    state_id: int,
    state_total_score: float,
) -> int:
    """Calculate the rank of a state based on its total score."""
    # Count how many states have a higher score
    factors = await crud.get_ranking_factors(db, active_only=True)
    result = await db.execute(select(models.State))
    all_states = result.scalars().all()

    higher_count = 0
    for s in all_states:
        if s.id == state_id:
            continue
        scores = await crud.get_state_scores(db, s.id)
        scores_dict = {sc.factor_id: sc for sc in scores}
        total = sum(
            scores_dict[f.id].score * f.weight
            for f in factors
            if f.id in scores_dict
        )
        if total > state_total_score:
            higher_count += 1

    return higher_count + 1


@router.get("/{state_id}/analysis", response_model=schemas.StateAnalysisResponse)
async def get_state_analysis(
    state_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get Tier 2/3 deep analysis for a state.

    Returns detailed analysis including:
    - Reporting system details
    - Competitive intelligence
    - Certification requirements
    - Implementation recommendations
    """
    # Verify state exists
    state = await crud.get_state(db, state_id)
    if state is None:
        raise HTTPException(status_code=404, detail="State not found")

    # Get analysis
    result = await db.execute(
        select(models.StateAnalysis).where(models.StateAnalysis.state_id == state_id)
    )
    analysis = result.scalar_one_or_none()

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail=f"No analysis available for {state.name}. Run Tier 2 analysis first."
        )

    return schemas.StateAnalysisResponse.model_validate(analysis)


@router.get("/compare", response_model=schemas.StateComparisonResponse)
async def compare_states(
    ids: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Compare multiple states side-by-side.

    Args:
        ids: Comma-separated state IDs (e.g., "1,2,3")

    Returns comparison data for all requested states.
    """
    try:
        state_ids = [int(id.strip()) for id in ids.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid state IDs format")

    if len(state_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 states required for comparison")

    if len(state_ids) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 states can be compared")

    comparisons = []

    for state_id in state_ids:
        state = await crud.get_state(db, state_id)
        if state is None:
            raise HTTPException(status_code=404, detail=f"State with ID {state_id} not found")

        # Get NCES data
        nces_result = await db.execute(
            select(models.NCESData).where(models.NCESData.state_id == state_id)
        )
        nces_data = nces_result.scalar_one_or_none()

        # Get scores
        scores_result = await db.execute(
            select(models.StateScore, models.RankingFactor)
            .join(models.RankingFactor)
            .where(models.StateScore.state_id == state_id)
        )
        score_rows = scores_result.all()

        scores_with_factors = []
        total_score = 0.0

        for score, factor in score_rows:
            weighted = score.score * factor.weight
            total_score += weighted
            scores_with_factors.append(schemas.ScoreWithFactor(
                factor_name=factor.name,
                factor_weight=factor.weight,
                score=score.score,
                weighted_score=weighted,
                notes=score.notes,
            ))

        # Check for analysis
        analysis_result = await db.execute(
            select(models.StateAnalysis).where(models.StateAnalysis.state_id == state_id)
        )
        has_analysis = analysis_result.scalar_one_or_none() is not None

        comparisons.append(schemas.StateComparison(
            id=state.id,
            name=state.name,
            abbreviation=state.abbreviation,
            total_score=total_score,
            nces_data=schemas.NCESDataResponse.model_validate(nces_data) if nces_data else None,
            scores=scores_with_factors,
            has_analysis=has_analysis,
        ))

    return schemas.StateComparisonResponse(states=comparisons)
