"""
States API router.

Endpoints for managing US states and their reporting requirements.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas
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
