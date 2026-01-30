"""
Product Alignment Service.

Provides analysis of product-state fit, hub-spoke synergy,
and cross-sell opportunities for state expansion planning.
"""

from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import State, Product, ProductFeature, StateProductFit


async def get_products(db: AsyncSession) -> list[dict]:
    """Get all products with their features."""
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.features))
        .order_by(Product.product_type.desc(), Product.name)  # Hub first, then spokes
    )
    products = result.scalars().all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "product_type": p.product_type,
            "category": p.category,
            "is_core": p.is_core,
            "launch_year": p.launch_year,
            "total_states": p.total_states,
            "total_districts": p.total_districts,
            "integration_complexity": p.integration_complexity,
            "pricing_tier": p.pricing_tier,
            "feature_count": len(p.features),
            "features": [
                {
                    "id": f.id,
                    "name": f.name,
                    "category": f.category,
                    "complexity": f.complexity,
                    "is_state_specific": f.is_state_specific,
                }
                for f in p.features
            ],
        }
        for p in products
    ]


async def get_product_by_id(db: AsyncSession, product_id: int) -> Optional[dict]:
    """Get a single product by ID with full details."""
    result = await db.execute(
        select(Product)
        .options(
            selectinload(Product.features),
            selectinload(Product.state_fits).selectinload(StateProductFit.state)
        )
        .where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        return None

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "product_type": product.product_type,
        "category": product.category,
        "is_core": product.is_core,
        "launch_year": product.launch_year,
        "total_states": product.total_states,
        "total_districts": product.total_districts,
        "integration_complexity": product.integration_complexity,
        "pricing_tier": product.pricing_tier,
        "features": [
            {
                "id": f.id,
                "name": f.name,
                "description": f.description,
                "category": f.category,
                "complexity": f.complexity,
                "is_state_specific": f.is_state_specific,
                "customization_effort": f.customization_effort,
            }
            for f in product.features
        ],
        "state_fits": [
            {
                "state_id": sf.state_id,
                "state_name": sf.state.name if sf.state else None,
                "state_abbrev": sf.state.abbreviation if sf.state else None,
                "fit_score": sf.fit_score,
                "gap_count": sf.gap_count,
                "synergy_score": sf.synergy_score,
            }
            for sf in sorted(product.state_fits, key=lambda x: x.fit_score, reverse=True)
        ],
    }


async def get_hub_product(db: AsyncSession) -> Optional[dict]:
    """Get the hub (core SIS) product."""
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.features))
        .where(Product.product_type == "hub")
    )
    product = result.scalar_one_or_none()

    if not product:
        return None

    return await get_product_by_id(db, product.id)


async def get_state_products(db: AsyncSession, state_id: int) -> dict:
    """Get all products with fit data for a specific state."""
    # Get state info
    state_result = await db.execute(
        select(State).where(State.id == state_id)
    )
    state = state_result.scalar_one_or_none()

    if not state:
        return {"error": "State not found"}

    # Get all products
    products_result = await db.execute(
        select(Product).options(selectinload(Product.features))
    )
    all_products = products_result.scalars().all()

    # Get fit data for this state
    fits_result = await db.execute(
        select(StateProductFit)
        .where(StateProductFit.state_id == state_id)
    )
    fits = {f.product_id: f for f in fits_result.scalars().all()}

    products_data = []
    hub_product = None
    spoke_products = []

    for product in all_products:
        fit = fits.get(product.id)

        product_data = {
            "id": product.id,
            "name": product.name,
            "product_type": product.product_type,
            "category": product.category,
            "description": product.description,
            "fit_score": fit.fit_score if fit else None,
            "gap_count": fit.gap_count if fit else None,
            "critical_gaps": fit.critical_gaps if fit else None,
            "customization_hours": fit.customization_hours if fit else None,
            "synergy_score": fit.synergy_score if fit else None,
            "analysis_status": fit.analysis_status if fit else "pending",
            "feature_count": len(product.features),
            "state_specific_features": sum(1 for f in product.features if f.is_state_specific),
        }

        if product.product_type == "hub":
            hub_product = product_data
        else:
            spoke_products.append(product_data)

        products_data.append(product_data)

    # Sort spoke products by fit score
    spoke_products.sort(key=lambda x: x["fit_score"] or 0, reverse=True)

    # Calculate overall metrics
    avg_fit = sum(p["fit_score"] or 0 for p in products_data) / len(products_data) if products_data else 0
    total_customization = sum(p["customization_hours"] or 0 for p in products_data)

    return {
        "state_id": state_id,
        "state_name": state.name,
        "state_abbrev": state.abbreviation,
        "hub_product": hub_product,
        "spoke_products": spoke_products,
        "all_products": products_data,
        "metrics": {
            "average_fit_score": round(avg_fit, 1),
            "total_customization_hours": total_customization,
            "products_analyzed": sum(1 for p in products_data if p["analysis_status"] == "analyzed"),
            "products_pending": sum(1 for p in products_data if p["analysis_status"] == "pending"),
        },
    }


async def analyze_product_alignment(db: AsyncSession, state_id: int) -> dict:
    """Perform comprehensive product alignment analysis for a state."""
    state_data = await get_state_products(db, state_id)

    if "error" in state_data:
        return state_data

    hub = state_data["hub_product"]
    spokes = state_data["spoke_products"]

    # Analyze hub fit
    hub_analysis = None
    if hub and hub["fit_score"]:
        hub_fit = hub["fit_score"]
        if hub_fit >= 8.0:
            hub_recommendation = "Excellent fit - proceed with expansion"
            hub_priority = "high"
        elif hub_fit >= 6.5:
            hub_recommendation = "Good fit - manageable customization required"
            hub_priority = "medium"
        else:
            hub_recommendation = "Challenging fit - significant development needed"
            hub_priority = "low"

        hub_analysis = {
            "fit_score": hub_fit,
            "recommendation": hub_recommendation,
            "priority": hub_priority,
            "customization_hours": hub["customization_hours"],
            "critical_gaps": hub["critical_gaps"],
            "estimated_months": _estimate_months(hub["customization_hours"]),
        }

    # Analyze spoke opportunities
    spoke_opportunities = []
    for spoke in spokes:
        if spoke["fit_score"] and spoke["fit_score"] >= 7.0:
            opportunity = {
                "product_name": spoke["name"],
                "category": spoke["category"],
                "fit_score": spoke["fit_score"],
                "synergy_score": spoke["synergy_score"],
                "customization_hours": spoke["customization_hours"],
                "cross_sell_potential": _calculate_cross_sell_potential(spoke),
                "bundle_recommendation": _get_bundle_recommendation(spoke, hub),
            }
            spoke_opportunities.append(opportunity)

    spoke_opportunities.sort(key=lambda x: x["cross_sell_potential"], reverse=True)

    # Calculate bundle value
    bundle_analysis = _analyze_bundle_value(hub, spokes)

    return {
        **state_data,
        "analysis": {
            "hub_analysis": hub_analysis,
            "spoke_opportunities": spoke_opportunities,
            "bundle_analysis": bundle_analysis,
            "overall_recommendation": _get_overall_recommendation(hub_analysis, spoke_opportunities),
        },
    }


def _estimate_months(hours: int) -> int:
    """Estimate months based on hours (100 productive hours/month, 5 FTE)."""
    if not hours:
        return 0
    # 100 hours/month * 5 FTE = 500 hours/month capacity
    return max(1, round(hours / 500))


def _calculate_cross_sell_potential(spoke: dict) -> float:
    """Calculate cross-sell potential score (0-10)."""
    if not spoke["fit_score"]:
        return 0.0

    # Base on fit and synergy
    fit = spoke["fit_score"]
    synergy = spoke["synergy_score"] or 5.0

    # Higher fit and synergy = higher cross-sell potential
    potential = (fit * 0.4) + (synergy * 0.6)

    # Bonus for low customization
    if spoke["customization_hours"] and spoke["customization_hours"] < 200:
        potential += 1.0

    return min(10.0, round(potential, 1))


def _get_bundle_recommendation(spoke: dict, hub: dict) -> str:
    """Get bundle recommendation for a spoke product."""
    if not spoke["fit_score"] or not hub:
        return "Not recommended"

    synergy = spoke["synergy_score"] or 0

    if synergy >= 8.5:
        return "Strong bundle candidate - include in initial offering"
    elif synergy >= 7.5:
        return "Good bundle candidate - offer as add-on"
    elif synergy >= 6.5:
        return "Moderate synergy - offer post-implementation"
    else:
        return "Low synergy - standalone offering only"


def _analyze_bundle_value(hub: dict, spokes: list) -> dict:
    """Analyze the value of bundling products."""
    if not hub or not hub["fit_score"]:
        return {"recommendation": "Hub analysis required first"}

    # Find high-synergy spokes
    bundle_candidates = [s for s in spokes if s["synergy_score"] and s["synergy_score"] >= 7.5]

    # Calculate bundle metrics
    total_hours = hub["customization_hours"] or 0
    for spoke in bundle_candidates[:3]:  # Top 3 spokes
        total_hours += spoke["customization_hours"] or 0

    # Estimate bundle discount (typically 15-25% for bundles)
    bundle_discount = 20 if len(bundle_candidates) >= 2 else 15

    return {
        "recommended_bundle_size": min(len(bundle_candidates) + 1, 4),  # Hub + up to 3 spokes
        "bundle_candidates": [s["name"] for s in bundle_candidates[:3]],
        "estimated_bundle_discount": f"{bundle_discount}%",
        "total_implementation_hours": total_hours,
        "implementation_months": _estimate_months(total_hours),
        "value_proposition": _get_bundle_value_proposition(hub, bundle_candidates),
    }


def _get_bundle_value_proposition(hub: dict, spokes: list) -> str:
    """Generate value proposition for the bundle."""
    if not spokes:
        return "Core SIS implementation with future expansion options"

    spoke_names = [s["name"].replace("OnCourse ", "") for s in spokes[:3]]
    spoke_list = ", ".join(spoke_names[:-1]) + f" and {spoke_names[-1]}" if len(spoke_names) > 1 else spoke_names[0]

    return f"Comprehensive solution including Core SIS, {spoke_list} with integrated data flow and unified support"


def _get_overall_recommendation(hub_analysis: dict, opportunities: list) -> dict:
    """Generate overall state expansion recommendation."""
    if not hub_analysis:
        return {
            "summary": "Analysis pending",
            "action": "Complete hub product analysis first",
            "priority": "pending",
        }

    priority = hub_analysis["priority"]
    fit = hub_analysis["fit_score"]

    if priority == "high":
        return {
            "summary": f"Strong expansion candidate with {fit}/10 hub fit",
            "action": "Prioritize for immediate expansion planning",
            "priority": "high",
            "cross_sell_count": len(opportunities),
        }
    elif priority == "medium":
        return {
            "summary": f"Viable expansion candidate with {fit}/10 hub fit",
            "action": "Include in expansion roadmap with adequate preparation",
            "priority": "medium",
            "cross_sell_count": len(opportunities),
        }
    else:
        return {
            "summary": f"Challenging expansion with {fit}/10 hub fit",
            "action": "Consider only after easier markets are addressed",
            "priority": "low",
            "cross_sell_count": len(opportunities),
        }


async def get_cross_sell_opportunities(db: AsyncSession, state_id: int) -> dict:
    """Get cross-sell opportunities for a state."""
    state_data = await get_state_products(db, state_id)

    if "error" in state_data:
        return state_data

    opportunities = []

    for spoke in state_data["spoke_products"]:
        if not spoke["fit_score"]:
            continue

        potential = _calculate_cross_sell_potential(spoke)

        # Estimate revenue (rough: $2-5 per student based on product)
        revenue_multiplier = {
            "lms": 3,
            "assessment": 2,
            "special_ed": 4,
            "finance": 5,
            "hr": 3,
            "transportation": 2,
        }.get(spoke["category"], 2)

        # Get state student count for revenue estimate
        state_result = await db.execute(
            select(State).where(State.id == state_id)
        )
        state = state_result.scalar_one_or_none()
        students = state.total_students if state else 100000

        # Assume 10% market capture
        estimated_revenue = int(students * 0.10 * revenue_multiplier)

        opportunities.append({
            "product_id": spoke["id"],
            "product_name": spoke["name"],
            "category": spoke["category"],
            "fit_score": spoke["fit_score"],
            "cross_sell_potential": potential,
            "synergy_score": spoke["synergy_score"],
            "customization_hours": spoke["customization_hours"],
            "estimated_annual_revenue": estimated_revenue,
            "ease_of_sale": "easy" if potential >= 8 else "moderate" if potential >= 6 else "challenging",
        })

    # Sort by cross-sell potential
    opportunities.sort(key=lambda x: x["cross_sell_potential"], reverse=True)

    return {
        "state_id": state_id,
        "state_name": state_data["state_name"],
        "opportunities": opportunities,
        "total_revenue_potential": sum(o["estimated_annual_revenue"] for o in opportunities),
        "top_opportunity": opportunities[0] if opportunities else None,
    }


async def get_product_summary(db: AsyncSession) -> dict:
    """Get summary of product portfolio."""
    # Count products by type
    result = await db.execute(
        select(Product.product_type, func.count(Product.id))
        .group_by(Product.product_type)
    )
    type_counts = {row[0]: row[1] for row in result.fetchall()}

    # Get total features
    features_result = await db.execute(select(func.count(ProductFeature.id)))
    total_features = features_result.scalar() or 0

    # Get states with product fits
    fits_result = await db.execute(
        select(func.count(func.distinct(StateProductFit.state_id)))
    )
    states_analyzed = fits_result.scalar() or 0

    # Get average fit scores by product
    avg_fits = await db.execute(
        select(Product.name, func.avg(StateProductFit.fit_score))
        .join(StateProductFit, Product.id == StateProductFit.product_id)
        .group_by(Product.id, Product.name)
    )
    product_avg_fits = [
        {"product": row[0], "avg_fit": round(row[1], 1) if row[1] else None}
        for row in avg_fits.fetchall()
    ]

    return {
        "total_products": sum(type_counts.values()),
        "hub_count": type_counts.get("hub", 0),
        "spoke_count": type_counts.get("spoke", 0),
        "total_features": total_features,
        "states_analyzed": states_analyzed,
        "product_fit_averages": product_avg_fits,
    }
