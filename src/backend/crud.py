"""
CRUD operations for database models.

Async database operations for all models.
"""

from typing import Optional, Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from . import models, schemas


# ============ State CRUD ============

async def get_states(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[models.State]:
    """Get all states with pagination."""
    result = await db.execute(
        select(models.State)
        .offset(skip)
        .limit(limit)
        .order_by(models.State.name)
    )
    return result.scalars().all()


async def get_state(db: AsyncSession, state_id: int) -> Optional[models.State]:
    """Get a single state by ID."""
    result = await db.execute(
        select(models.State)
        .where(models.State.id == state_id)
        .options(selectinload(models.State.requirements))
        .options(selectinload(models.State.nces_data))
        .options(selectinload(models.State.scores))
    )
    return result.scalar_one_or_none()


async def get_state_by_abbreviation(
    db: AsyncSession, abbreviation: str
) -> Optional[models.State]:
    """Get a state by abbreviation."""
    result = await db.execute(
        select(models.State).where(models.State.abbreviation == abbreviation.upper())
    )
    return result.scalar_one_or_none()


async def create_state(
    db: AsyncSession, state: schemas.StateCreate
) -> models.State:
    """Create a new state."""
    db_state = models.State(**state.model_dump())
    db.add(db_state)
    await db.flush()
    await db.refresh(db_state)
    return db_state


async def update_state(
    db: AsyncSession, state_id: int, state: schemas.StateUpdate
) -> Optional[models.State]:
    """Update an existing state."""
    db_state = await get_state(db, state_id)
    if db_state is None:
        return None

    update_data = state.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_state, field, value)

    await db.flush()
    await db.refresh(db_state)
    return db_state


async def delete_state(db: AsyncSession, state_id: int) -> bool:
    """Delete a state."""
    db_state = await get_state(db, state_id)
    if db_state is None:
        return False

    await db.delete(db_state)
    return True


async def get_states_count(db: AsyncSession) -> int:
    """Get total count of states."""
    result = await db.execute(select(func.count(models.State.id)))
    return result.scalar_one()


# ============ RankingFactor CRUD ============

async def get_ranking_factors(
    db: AsyncSession, active_only: bool = True
) -> Sequence[models.RankingFactor]:
    """Get all ranking factors."""
    query = select(models.RankingFactor)
    if active_only:
        query = query.where(models.RankingFactor.is_active == True)
    result = await db.execute(query.order_by(models.RankingFactor.weight.desc()))
    return result.scalars().all()


async def get_ranking_factor(
    db: AsyncSession, factor_id: int
) -> Optional[models.RankingFactor]:
    """Get a single ranking factor by ID."""
    result = await db.execute(
        select(models.RankingFactor).where(models.RankingFactor.id == factor_id)
    )
    return result.scalar_one_or_none()


async def create_ranking_factor(
    db: AsyncSession, factor: schemas.RankingFactorCreate
) -> models.RankingFactor:
    """Create a new ranking factor."""
    db_factor = models.RankingFactor(**factor.model_dump())
    db.add(db_factor)
    await db.flush()
    await db.refresh(db_factor)
    return db_factor


# ============ StateScore CRUD ============

async def get_state_scores(
    db: AsyncSession, state_id: int
) -> Sequence[models.StateScore]:
    """Get all scores for a state."""
    result = await db.execute(
        select(models.StateScore)
        .where(models.StateScore.state_id == state_id)
        .options(selectinload(models.StateScore.factor))
    )
    return result.scalars().all()


async def create_state_score(
    db: AsyncSession, score: schemas.StateScoreCreate
) -> models.StateScore:
    """Create a new state score."""
    db_score = models.StateScore(**score.model_dump())
    db.add(db_score)
    await db.flush()
    await db.refresh(db_score)
    return db_score


# ============ NCESData CRUD ============

async def get_nces_data(
    db: AsyncSession, state_id: int
) -> Optional[models.NCESData]:
    """Get NCES data for a state."""
    result = await db.execute(
        select(models.NCESData).where(models.NCESData.state_id == state_id)
    )
    return result.scalar_one_or_none()


async def create_or_update_nces_data(
    db: AsyncSession, nces_data: schemas.NCESDataCreate
) -> models.NCESData:
    """Create or update NCES data for a state."""
    existing = await get_nces_data(db, nces_data.state_id)

    if existing:
        update_data = nces_data.model_dump(exclude={"state_id"})
        for field, value in update_data.items():
            if value is not None:
                setattr(existing, field, value)
        await db.flush()
        await db.refresh(existing)
        return existing
    else:
        db_nces = models.NCESData(**nces_data.model_dump())
        db.add(db_nces)
        await db.flush()
        await db.refresh(db_nces)
        return db_nces
