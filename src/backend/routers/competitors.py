"""
Competitor API endpoints.

Provides endpoints for competitor data, competitive analysis,
and market opportunity assessment.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from database import get_db
from services.competitive_service import (
    get_competitors,
    get_competitor_by_id,
    get_state_competitors,
    analyze_competitive_landscape,
    calculate_market_opportunity,
    compare_competitors,
    get_competitive_summary,
)

router = APIRouter(prefix="/api/competitors", tags=["competitors"])


@router.get("")
async def list_competitors(db: AsyncSession = Depends(get_db)):
    """Get all competitors with their strengths."""
    competitors = await get_competitors(db)
    return {
        "competitors": competitors,
        "total": len(competitors),
    }


@router.get("/summary")
async def competitive_summary(db: AsyncSession = Depends(get_db)):
    """Get overall competitive landscape summary."""
    summary = await get_competitive_summary(db)
    return summary


@router.get("/compare")
async def compare_competitors_endpoint(
    ids: str = Query(..., description="Comma-separated competitor IDs"),
    db: AsyncSession = Depends(get_db)
):
    """Compare multiple competitors side by side."""
    try:
        competitor_ids = [int(id.strip()) for id in ids.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid competitor IDs format")

    if len(competitor_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 competitors required for comparison")

    if len(competitor_ids) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 competitors can be compared at once")

    comparison = await compare_competitors(db, competitor_ids)

    if "error" in comparison:
        raise HTTPException(status_code=404, detail=comparison["error"])

    return comparison


@router.get("/{competitor_id}")
async def get_competitor(
    competitor_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed competitor information."""
    competitor = await get_competitor_by_id(db, competitor_id)

    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    return competitor


@router.get("/state/{state_id}")
async def state_competitors(
    state_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all competitors present in a specific state."""
    result = await get_state_competitors(db, state_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@router.get("/state/{state_id}/analysis")
async def state_competitive_analysis(
    state_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get deep competitive analysis for a state."""
    result = await analyze_competitive_landscape(db, state_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@router.get("/state/{state_id}/opportunity")
async def state_market_opportunity(
    state_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Calculate market opportunity score for a state."""
    result = await calculate_market_opportunity(db, state_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result
