"""
Competitive Intelligence Service.

Provides analysis of competitive landscape, market opportunity assessment,
and competitor comparisons for state expansion planning.
"""

from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import State, Competitor, StateCompetitor, CompetitorStrength


async def get_competitors(db: AsyncSession) -> list[dict]:
    """Get all competitors with their strengths."""
    result = await db.execute(
        select(Competitor)
        .options(selectinload(Competitor.strengths))
        .order_by(Competitor.name)
    )
    competitors = result.scalars().all()

    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "competitor_type": c.competitor_type,
            "headquarters": c.headquarters,
            "website": c.website,
            "founded_year": c.founded_year,
            "employee_count": c.employee_count,
            "total_states": c.total_states,
            "total_districts": c.total_districts,
            "total_students": c.total_students,
            "primary_product": c.primary_product,
            "has_state_reporting": c.has_state_reporting,
            "has_lms": c.has_lms,
            "has_assessment": c.has_assessment,
            "strengths": [
                {
                    "category": s.category,
                    "rating": s.rating,
                    "description": s.description,
                    "is_strength": s.is_strength,
                }
                for s in c.strengths
            ],
        }
        for c in competitors
    ]


async def get_competitor_by_id(db: AsyncSession, competitor_id: int) -> Optional[dict]:
    """Get a single competitor by ID with full details."""
    result = await db.execute(
        select(Competitor)
        .options(
            selectinload(Competitor.strengths),
            selectinload(Competitor.state_presence).selectinload(StateCompetitor.state)
        )
        .where(Competitor.id == competitor_id)
    )
    competitor = result.scalar_one_or_none()

    if not competitor:
        return None

    return {
        "id": competitor.id,
        "name": competitor.name,
        "description": competitor.description,
        "competitor_type": competitor.competitor_type,
        "headquarters": competitor.headquarters,
        "website": competitor.website,
        "founded_year": competitor.founded_year,
        "employee_count": competitor.employee_count,
        "total_states": competitor.total_states,
        "total_districts": competitor.total_districts,
        "total_students": competitor.total_students,
        "primary_product": competitor.primary_product,
        "has_state_reporting": competitor.has_state_reporting,
        "has_lms": competitor.has_lms,
        "has_assessment": competitor.has_assessment,
        "strengths": [
            {
                "category": s.category,
                "rating": s.rating,
                "description": s.description,
                "is_strength": s.is_strength,
            }
            for s in competitor.strengths
        ],
        "state_presence": [
            {
                "state_id": sp.state_id,
                "state_name": sp.state.name if sp.state else None,
                "state_abbrev": sp.state.abbreviation if sp.state else None,
                "presence_level": sp.presence_level,
                "market_share_percent": sp.market_share_percent,
                "district_count": sp.district_count,
                "is_certified": sp.is_certified,
            }
            for sp in competitor.state_presence
        ],
    }


async def get_state_competitors(db: AsyncSession, state_id: int) -> dict:
    """Get all competitors present in a specific state with market data."""
    # Get state info
    state_result = await db.execute(
        select(State).where(State.id == state_id)
    )
    state = state_result.scalar_one_or_none()

    if not state:
        return {"error": "State not found"}

    # Get competitors in state
    result = await db.execute(
        select(StateCompetitor)
        .options(
            selectinload(StateCompetitor.competitor).selectinload(Competitor.strengths)
        )
        .where(StateCompetitor.state_id == state_id)
        .order_by(StateCompetitor.market_share_percent.desc().nullslast())
    )
    state_competitors = result.scalars().all()

    competitors_data = []
    total_market_share = 0.0

    for sc in state_competitors:
        comp = sc.competitor
        if sc.market_share_percent:
            total_market_share += sc.market_share_percent

        competitors_data.append({
            "id": comp.id,
            "name": comp.name,
            "competitor_type": comp.competitor_type,
            "presence_level": sc.presence_level,
            "market_share_percent": sc.market_share_percent,
            "district_count": sc.district_count,
            "estimated_annual_revenue": sc.estimated_annual_revenue,
            "is_certified": sc.is_certified,
            "data_confidence": sc.data_confidence,
            "primary_product": comp.primary_product,
            "has_state_reporting": comp.has_state_reporting,
            "strengths": [
                {
                    "category": s.category,
                    "rating": s.rating,
                    "is_strength": s.is_strength,
                }
                for s in comp.strengths
                if s.is_strength
            ][:3],  # Top 3 strengths only
        })

    # Calculate market metrics
    dominant_count = sum(1 for c in competitors_data if c["presence_level"] == "dominant")
    strong_count = sum(1 for c in competitors_data if c["presence_level"] == "strong")

    # Market concentration assessment
    if dominant_count >= 2:
        concentration = "highly_concentrated"
        opportunity_score = 3
    elif dominant_count == 1 and strong_count >= 2:
        concentration = "moderately_concentrated"
        opportunity_score = 5
    elif dominant_count == 1:
        concentration = "single_leader"
        opportunity_score = 6
    elif strong_count >= 3:
        concentration = "fragmented_competitive"
        opportunity_score = 7
    else:
        concentration = "fragmented_open"
        opportunity_score = 9

    return {
        "state_id": state_id,
        "state_name": state.name,
        "state_abbrev": state.abbreviation,
        "total_competitors": len(competitors_data),
        "total_market_share_tracked": round(total_market_share, 1),
        "market_concentration": concentration,
        "opportunity_score": opportunity_score,
        "competitors": competitors_data,
    }


async def analyze_competitive_landscape(db: AsyncSession, state_id: int) -> dict:
    """Perform deep competitive analysis for a state."""
    state_data = await get_state_competitors(db, state_id)

    if "error" in state_data:
        return state_data

    competitors = state_data["competitors"]

    # Identify key threats and opportunities
    threats = []
    opportunities = []

    for comp in competitors:
        if comp["presence_level"] == "dominant":
            threats.append({
                "competitor": comp["name"],
                "threat_level": "high",
                "reason": f"Dominant market position with {comp['market_share_percent'] or 'significant'}% market share",
            })
        elif comp["presence_level"] == "strong":
            # Could be threat or opportunity
            if comp.get("strengths"):
                strength_categories = [s["category"] for s in comp["strengths"]]
                if "pricing" in strength_categories:
                    threats.append({
                        "competitor": comp["name"],
                        "threat_level": "medium",
                        "reason": "Strong presence with competitive pricing advantage",
                    })
                elif "state_reporting" in strength_categories:
                    threats.append({
                        "competitor": comp["name"],
                        "threat_level": "medium",
                        "reason": "Strong state reporting capabilities",
                    })

    # Calculate opportunity areas
    total_tracked = state_data["total_market_share_tracked"]
    untracked_market = 100 - total_tracked if total_tracked < 100 else 0

    if untracked_market > 20:
        opportunities.append({
            "type": "market_gap",
            "description": f"Approximately {untracked_market:.0f}% of market not dominated by major vendors",
            "potential": "high",
        })

    if state_data["market_concentration"] in ["fragmented_open", "fragmented_competitive"]:
        opportunities.append({
            "type": "fragmented_market",
            "description": "No single dominant vendor - easier market entry",
            "potential": "high",
        })

    # Check for regional vendor dominance (opportunity for national features)
    regional_dominant = [c for c in competitors if c["competitor_type"] == "regional" and c["presence_level"] in ["dominant", "strong"]]
    if regional_dominant:
        opportunities.append({
            "type": "regional_displacement",
            "description": f"Regional vendors ({', '.join(c['name'] for c in regional_dominant)}) may lack features of national solutions",
            "potential": "medium",
        })

    # Competitive advantages to highlight
    advantages_to_leverage = []

    # Check what competitors lack
    has_assessment = [c for c in competitors if c.get("has_state_reporting")]
    if len(has_assessment) < len(competitors) * 0.5:
        advantages_to_leverage.append("Strong state reporting automation")

    return {
        **state_data,
        "analysis": {
            "threats": threats,
            "opportunities": opportunities,
            "advantages_to_leverage": advantages_to_leverage,
            "entry_difficulty": _calculate_entry_difficulty(state_data),
            "recommended_strategy": _recommend_strategy(state_data, threats, opportunities),
        }
    }


def _calculate_entry_difficulty(state_data: dict) -> dict:
    """Calculate market entry difficulty score."""
    score = 5  # Base difficulty

    concentration = state_data["market_concentration"]
    if concentration == "highly_concentrated":
        score += 3
    elif concentration == "moderately_concentrated":
        score += 2
    elif concentration == "single_leader":
        score += 1
    elif concentration == "fragmented_open":
        score -= 2

    # Number of competitors
    num_competitors = state_data["total_competitors"]
    if num_competitors > 6:
        score += 1
    elif num_competitors < 3:
        score -= 1

    # Cap score
    score = max(1, min(10, score))

    difficulty_labels = {
        1: "Very Easy",
        2: "Easy",
        3: "Easy",
        4: "Moderate",
        5: "Moderate",
        6: "Moderate",
        7: "Difficult",
        8: "Difficult",
        9: "Very Difficult",
        10: "Extremely Difficult",
    }

    return {
        "score": score,
        "label": difficulty_labels[score],
        "factors": [
            f"Market concentration: {concentration.replace('_', ' ').title()}",
            f"Number of competitors: {num_competitors}",
        ]
    }


def _recommend_strategy(state_data: dict, threats: list, opportunities: list) -> dict:
    """Generate recommended market entry strategy."""
    concentration = state_data["market_concentration"]

    if concentration in ["fragmented_open", "fragmented_competitive"]:
        strategy = "direct_entry"
        description = "Market conditions favorable for direct entry. Focus on demonstrating superior capabilities and building district relationships."
        tactics = [
            "Target mid-size districts underserved by regional vendors",
            "Emphasize state reporting automation and accuracy",
            "Competitive pricing to win initial reference customers",
            "Partner with local implementation consultants",
        ]
    elif concentration == "single_leader":
        strategy = "differentiation"
        description = "Single dominant vendor creates opportunity to differentiate on underserved needs."
        tactics = [
            "Identify pain points with dominant vendor",
            "Target districts frustrated with current solution",
            "Offer superior customer service and support",
            "Focus on specific feature advantages",
        ]
    else:
        strategy = "niche_entry"
        description = "Concentrated market requires focused niche strategy to establish foothold."
        tactics = [
            "Target specific district types (charter, small rural, etc.)",
            "Build reference customers before broader push",
            "Consider partnership with complementary vendors",
            "Focus on long-term relationship building",
        ]

    return {
        "strategy": strategy,
        "description": description,
        "tactics": tactics,
    }


async def calculate_market_opportunity(db: AsyncSession, state_id: int) -> dict:
    """Calculate overall market opportunity score for a state."""
    state_result = await db.execute(
        select(State).where(State.id == state_id)
    )
    state = state_result.scalar_one_or_none()

    if not state:
        return {"error": "State not found"}

    competitive_data = await get_state_competitors(db, state_id)

    # Base opportunity from state size
    total_students = state.total_students or 0
    total_districts = state.total_districts or 0

    # Size score (1-10)
    if total_students > 5000000:
        size_score = 10
    elif total_students > 2000000:
        size_score = 8
    elif total_students > 1000000:
        size_score = 6
    elif total_students > 500000:
        size_score = 4
    else:
        size_score = 2

    # Competition score (from competitive analysis)
    competition_score = competitive_data.get("opportunity_score", 5)

    # District structure score
    avg_district_size = total_students / total_districts if total_districts > 0 else 0
    if avg_district_size > 20000:  # Large districts = higher ARPU
        structure_score = 9
    elif avg_district_size > 10000:
        structure_score = 7
    elif avg_district_size > 5000:
        structure_score = 5
    else:
        structure_score = 3

    # Calculate weighted total
    weights = {
        "size": 0.3,
        "competition": 0.4,
        "structure": 0.3,
    }

    total_score = (
        size_score * weights["size"] +
        competition_score * weights["competition"] +
        structure_score * weights["structure"]
    )

    # Revenue potential estimate (rough)
    # Assuming $5 per student per year average
    potential_revenue = total_students * 5

    # Addressable market (based on competition)
    addressable_percent = 100 - competitive_data.get("total_market_share_tracked", 50)
    addressable_revenue = int(potential_revenue * (addressable_percent / 100))

    return {
        "state_id": state_id,
        "state_name": state.name,
        "state_abbrev": state.abbreviation,
        "total_score": round(total_score, 1),
        "score_breakdown": {
            "size_score": size_score,
            "competition_score": competition_score,
            "structure_score": structure_score,
        },
        "market_size": {
            "total_students": total_students,
            "total_districts": total_districts,
            "avg_district_size": int(avg_district_size),
        },
        "revenue_potential": {
            "total_market": potential_revenue,
            "addressable_market": addressable_revenue,
            "addressable_percent": round(addressable_percent, 1),
        },
        "recommendation": _get_opportunity_recommendation(total_score),
    }


def _get_opportunity_recommendation(score: float) -> str:
    """Get recommendation based on opportunity score."""
    if score >= 8:
        return "High Priority - Strong market opportunity with favorable conditions"
    elif score >= 6:
        return "Medium Priority - Good opportunity with some competitive challenges"
    elif score >= 4:
        return "Lower Priority - Moderate opportunity, significant effort required"
    else:
        return "Not Recommended - Limited opportunity or high barriers to entry"


async def compare_competitors(db: AsyncSession, competitor_ids: list[int]) -> dict:
    """Compare multiple competitors side by side."""
    result = await db.execute(
        select(Competitor)
        .options(selectinload(Competitor.strengths))
        .where(Competitor.id.in_(competitor_ids))
    )
    competitors = result.scalars().all()

    if not competitors:
        return {"error": "No competitors found"}

    comparison = {
        "competitors": [],
        "categories": [],
    }

    # Collect all strength categories
    all_categories = set()
    for comp in competitors:
        for strength in comp.strengths:
            all_categories.add(strength.category)

    comparison["categories"] = sorted(list(all_categories))

    for comp in competitors:
        # Build category ratings dict
        category_ratings = {}
        for cat in all_categories:
            matching = [s for s in comp.strengths if s.category == cat]
            if matching:
                category_ratings[cat] = matching[0].rating
            else:
                category_ratings[cat] = None

        comparison["competitors"].append({
            "id": comp.id,
            "name": comp.name,
            "type": comp.competitor_type,
            "total_states": comp.total_states,
            "total_students": comp.total_students,
            "primary_product": comp.primary_product,
            "category_ratings": category_ratings,
            "avg_rating": sum(r for r in category_ratings.values() if r) / len([r for r in category_ratings.values() if r]) if any(category_ratings.values()) else 0,
        })

    return comparison


async def get_competitive_summary(db: AsyncSession) -> dict:
    """Get summary of competitive landscape across all states."""
    # Count competitors by type
    type_counts = await db.execute(
        select(Competitor.competitor_type, func.count(Competitor.id))
        .group_by(Competitor.competitor_type)
    )
    type_data = {row[0]: row[1] for row in type_counts.fetchall()}

    # Get total competitors
    total_result = await db.execute(select(func.count(Competitor.id)))
    total_competitors = total_result.scalar() or 0

    # Get states with most competitors
    state_competitor_counts = await db.execute(
        select(State.name, State.abbreviation, func.count(StateCompetitor.id).label("count"))
        .join(StateCompetitor, State.id == StateCompetitor.state_id)
        .group_by(State.id, State.name, State.abbreviation)
        .order_by(func.count(StateCompetitor.id).desc())
        .limit(10)
    )
    top_competitive_states = [
        {"state": row[0], "abbrev": row[1], "competitor_count": row[2]}
        for row in state_competitor_counts.fetchall()
    ]

    # Get least competitive states
    least_competitive = await db.execute(
        select(State.name, State.abbreviation, func.count(StateCompetitor.id).label("count"))
        .join(StateCompetitor, State.id == StateCompetitor.state_id)
        .group_by(State.id, State.name, State.abbreviation)
        .order_by(func.count(StateCompetitor.id).asc())
        .limit(10)
    )
    least_competitive_states = [
        {"state": row[0], "abbrev": row[1], "competitor_count": row[2]}
        for row in least_competitive.fetchall()
    ]

    return {
        "total_competitors": total_competitors,
        "by_type": type_data,
        "most_competitive_states": top_competitive_states,
        "least_competitive_states": least_competitive_states,
    }
