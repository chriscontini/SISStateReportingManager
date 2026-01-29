"""
Rankings API router.

Endpoints for state rankings and ranking factors.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel

from .. import crud, schemas, models
from ..database import get_db
from ..services import scoring_service
from ..baselines import NJ_CAPABILITIES, LA_CAPABILITIES

router = APIRouter(prefix="/api/rankings", tags=["rankings"])


class CalculateRequest(BaseModel):
    """Request body for score calculation."""
    use_ai: bool = False  # AI scoring is slower but more accurate


class CalculateResponse(BaseModel):
    """Response from score calculation."""
    status: str
    message: str
    states_calculated: int = 0
    errors: list[dict] = []


class FactorWeightUpdate(BaseModel):
    """Request body for updating factor weight."""
    weight: float


@router.get("", response_model=schemas.RankingsResponse)
async def get_rankings(
    db: AsyncSession = Depends(get_db),
):
    """
    Get ranked list of all states.

    States are ranked by their total weighted score across all active factors.
    """
    # Get all active ranking factors
    factors = await crud.get_ranking_factors(db, active_only=True)

    # Get all states with their scores
    result = await db.execute(
        select(models.State)
        .options(
            # Load scores eagerly
        )
        .order_by(models.State.name)
    )
    states = result.scalars().all()

    # Calculate total scores for each state
    rankings = []
    for state in states:
        # Get scores for this state
        scores = await crud.get_state_scores(db, state.id)
        scores_dict = {s.factor_id: s for s in scores}

        # Calculate weighted total
        total_score = 0.0
        score_responses = []

        for factor in factors:
            if factor.id in scores_dict:
                score = scores_dict[factor.id]
                total_score += score.score * factor.weight
                score_responses.append(
                    schemas.StateScoreResponse.model_validate(score)
                )

        rankings.append({
            "id": state.id,
            "name": state.name,
            "abbreviation": state.abbreviation,
            "total_score": total_score,
            "rank": 0,  # Will be set after sorting
            "scores": score_responses,
        })

    # Sort by total score descending and assign ranks
    rankings.sort(key=lambda x: x["total_score"], reverse=True)
    for i, ranking in enumerate(rankings, 1):
        ranking["rank"] = i

    return schemas.RankingsResponse(
        rankings=[schemas.StateRankingResponse(**r) for r in rankings],
        factors=[schemas.RankingFactorResponse.model_validate(f) for f in factors],
    )


@router.get("/factors", response_model=list[schemas.RankingFactorResponse])
async def get_ranking_factors(
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """Get all ranking factors."""
    factors = await crud.get_ranking_factors(db, active_only=active_only)
    return [schemas.RankingFactorResponse.model_validate(f) for f in factors]


@router.post("/factors", response_model=schemas.RankingFactorResponse, status_code=201)
async def create_ranking_factor(
    factor: schemas.RankingFactorCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new ranking factor."""
    db_factor = await crud.create_ranking_factor(db, factor)
    return schemas.RankingFactorResponse.model_validate(db_factor)


@router.get("/factors/{factor_id}", response_model=schemas.RankingFactorResponse)
async def get_ranking_factor(
    factor_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a single ranking factor by ID."""
    factor = await crud.get_ranking_factor(db, factor_id)
    if factor is None:
        raise HTTPException(status_code=404, detail="Ranking factor not found")
    return schemas.RankingFactorResponse.model_validate(factor)


@router.patch("/factors/{factor_id}", response_model=schemas.RankingFactorResponse)
async def update_ranking_factor_weight(
    factor_id: int,
    update: FactorWeightUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update a ranking factor's weight.

    Weight must be a positive number. Common weights:
    - 3.0: Primary factor (Development Effort)
    - 2.5: High importance (District Structure, Avg District Size)
    - 2.0: Medium-high (Technical Fit)
    - 1.5: Medium (Certification, Competition, Market)
    - 1.0: Lower (Regulatory)
    - 0.5: Minor (Geographic Proximity)
    """
    if update.weight <= 0:
        raise HTTPException(
            status_code=400,
            detail="Weight must be a positive number"
        )

    factor = await crud.get_ranking_factor(db, factor_id)
    if factor is None:
        raise HTTPException(status_code=404, detail="Ranking factor not found")

    # Update the weight
    factor.weight = update.weight
    await db.commit()
    await db.refresh(factor)

    return schemas.RankingFactorResponse.model_validate(factor)


@router.post("/calculate", response_model=CalculateResponse)
async def calculate_scores(
    request: CalculateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Calculate scores for all states.

    This endpoint triggers the scoring service to calculate scores
    for all ranking factors across all states.

    Args:
        use_ai: If True, uses AI-powered scoring for Development Effort,
               Technical Fit, and Competitive Landscape. This is slower
               but more accurate. Default False uses heuristic fallbacks.

    Note: AI scoring requires CLAUDE_API_KEY to be configured and
          may take several minutes for all 50 states.
    """
    try:
        result = await scoring_service.calculate_all_scores(
            db=db,
            nj_capabilities=NJ_CAPABILITIES,
            la_capabilities=LA_CAPABILITIES,
            use_ai=request.use_ai,
        )

        return CalculateResponse(
            status="completed",
            message=f"Calculated scores for {result['states_calculated']} states",
            states_calculated=result["states_calculated"],
            errors=result.get("errors", []),
        )

    except Exception as e:
        return CalculateResponse(
            status="error",
            message=f"Score calculation failed: {str(e)}",
            errors=[{"error": str(e)}],
        )
