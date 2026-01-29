"""
Rankings API router.

Endpoints for state rankings and ranking factors.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(prefix="/api/rankings", tags=["rankings"])


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
