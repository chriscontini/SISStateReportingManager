"""
Products API endpoints.

Provides endpoints for product data, product-state fit analysis,
and cross-sell opportunities.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from services.product_service import (
    get_products,
    get_product_by_id,
    get_hub_product,
    get_state_products,
    analyze_product_alignment,
    get_cross_sell_opportunities,
    get_product_summary,
)

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("")
async def list_products(db: AsyncSession = Depends(get_db)):
    """Get all products with their features."""
    products = await get_products(db)
    return {
        "products": products,
        "total": len(products),
        "hub_count": sum(1 for p in products if p["product_type"] == "hub"),
        "spoke_count": sum(1 for p in products if p["product_type"] == "spoke"),
    }


@router.get("/summary")
async def product_summary(db: AsyncSession = Depends(get_db)):
    """Get product portfolio summary."""
    summary = await get_product_summary(db)
    return summary


@router.get("/hub")
async def hub_product(db: AsyncSession = Depends(get_db)):
    """Get the hub (core SIS) product."""
    product = await get_hub_product(db)

    if not product:
        raise HTTPException(status_code=404, detail="Hub product not found")

    return product


@router.get("/cross-sell")
async def cross_sell_opportunities(
    state_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get cross-sell opportunities for a state."""
    result = await get_cross_sell_opportunities(db, state_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@router.get("/{product_id}")
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed product information."""
    product = await get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.get("/state/{state_id}")
async def state_products(
    state_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all products with fit data for a specific state."""
    result = await get_state_products(db, state_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@router.get("/state/{state_id}/alignment")
async def state_product_alignment(
    state_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive product alignment analysis for a state."""
    result = await analyze_product_alignment(db, state_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result
