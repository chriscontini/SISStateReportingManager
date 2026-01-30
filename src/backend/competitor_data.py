"""
Competitor seed data for SIS State Reporting Manager.

Contains information about major national and regional SIS competitors
with their known market presence across US states.
"""

# Major SIS Competitors
COMPETITORS = [
    # National Players
    {
        "name": "PowerSchool",
        "competitor_type": "national",
        "description": "Largest K-12 education software provider in North America. Offers comprehensive SIS, LMS, and state reporting solutions.",
        "headquarters": "Folsom, CA",
        "website": "https://www.powerschool.com",
        "founded_year": 1997,
        "employee_count": "3000+",
        "primary_product": "PowerSchool SIS",
        "has_state_reporting": True,
        "has_lms": True,
        "has_assessment": True,
        "strengths": [
            {"category": "features", "rating": 5, "description": "Most comprehensive feature set in market"},
            {"category": "state_reporting", "rating": 5, "description": "Supports all 50 states"},
            {"category": "integration", "rating": 4, "description": "Large partner ecosystem"},
            {"category": "support", "rating": 3, "description": "Large support team but mixed reviews"},
            {"category": "pricing", "rating": 2, "description": "Premium pricing, high TCO"},
            {"category": "ease_of_use", "rating": 3, "description": "Complex interface, steep learning curve"},
        ]
    },
    {
        "name": "Infinite Campus",
        "competitor_type": "national",
        "description": "Second largest SIS provider. Strong in midwest and western states with robust state reporting.",
        "headquarters": "Blaine, MN",
        "website": "https://www.infinitecampus.com",
        "founded_year": 1993,
        "employee_count": "1500+",
        "primary_product": "Infinite Campus SIS",
        "has_state_reporting": True,
        "has_lms": True,
        "has_assessment": False,
        "strengths": [
            {"category": "state_reporting", "rating": 5, "description": "Excellent state compliance tools"},
            {"category": "features", "rating": 4, "description": "Comprehensive K-12 functionality"},
            {"category": "support", "rating": 4, "description": "Strong customer support"},
            {"category": "ease_of_use", "rating": 3, "description": "Moderate complexity"},
            {"category": "pricing", "rating": 3, "description": "Mid-range pricing"},
            {"category": "integration", "rating": 3, "description": "Good but not as extensive as PowerSchool"},
        ]
    },
    {
        "name": "Tyler Technologies (Tyler SIS)",
        "competitor_type": "national",
        "description": "Public sector software company with growing K-12 presence through acquisitions.",
        "headquarters": "Plano, TX",
        "website": "https://www.tylertech.com",
        "founded_year": 1966,
        "employee_count": "6000+",
        "primary_product": "Tyler SIS",
        "has_state_reporting": True,
        "has_lms": False,
        "has_assessment": False,
        "strengths": [
            {"category": "integration", "rating": 5, "description": "Strong integration with government systems"},
            {"category": "support", "rating": 4, "description": "Enterprise-grade support"},
            {"category": "state_reporting", "rating": 4, "description": "Good state compliance"},
            {"category": "features", "rating": 3, "description": "Solid core functionality"},
            {"category": "pricing", "rating": 3, "description": "Enterprise pricing model"},
            {"category": "ease_of_use", "rating": 3, "description": "Government-style interface"},
        ]
    },
    {
        "name": "Skyward",
        "competitor_type": "national",
        "description": "Long-established SIS provider with strong presence in midwest and Texas.",
        "headquarters": "Stevens Point, WI",
        "website": "https://www.skyward.com",
        "founded_year": 1980,
        "employee_count": "800+",
        "primary_product": "Skyward SMS/Qmlativ",
        "has_state_reporting": True,
        "has_lms": False,
        "has_assessment": False,
        "strengths": [
            {"category": "support", "rating": 5, "description": "Exceptional customer support"},
            {"category": "ease_of_use", "rating": 4, "description": "User-friendly interface"},
            {"category": "state_reporting", "rating": 4, "description": "Strong Texas and midwest support"},
            {"category": "pricing", "rating": 4, "description": "Competitive pricing"},
            {"category": "features", "rating": 3, "description": "Good core features"},
            {"category": "integration", "rating": 3, "description": "Growing partner ecosystem"},
        ]
    },
    {
        "name": "Aeries Software",
        "competitor_type": "regional",
        "description": "California-focused SIS with dominant position in the state.",
        "headquarters": "Eagle, ID",
        "website": "https://www.aeries.com",
        "founded_year": 1995,
        "employee_count": "200+",
        "primary_product": "Aeries SIS",
        "has_state_reporting": True,
        "has_lms": False,
        "has_assessment": False,
        "strengths": [
            {"category": "state_reporting", "rating": 5, "description": "Best-in-class California CALPADS"},
            {"category": "support", "rating": 5, "description": "Excellent California-focused support"},
            {"category": "ease_of_use", "rating": 4, "description": "Clean, intuitive interface"},
            {"category": "pricing", "rating": 4, "description": "Competitive for California market"},
            {"category": "features", "rating": 3, "description": "California-specific features"},
            {"category": "integration", "rating": 3, "description": "California vendor ecosystem"},
        ]
    },
    {
        "name": "Follett (Aspen)",
        "competitor_type": "national",
        "description": "Education company with SIS offering through Aspen product line.",
        "headquarters": "McHenry, IL",
        "website": "https://www.follett.com",
        "founded_year": 1873,
        "employee_count": "5000+",
        "primary_product": "Aspen SIS",
        "has_state_reporting": True,
        "has_lms": False,
        "has_assessment": False,
        "strengths": [
            {"category": "integration", "rating": 4, "description": "Strong Follett ecosystem"},
            {"category": "features", "rating": 3, "description": "Solid core SIS"},
            {"category": "support", "rating": 3, "description": "Adequate support"},
            {"category": "pricing", "rating": 3, "description": "Bundle pricing with Follett products"},
            {"category": "state_reporting", "rating": 3, "description": "Covers major states"},
            {"category": "ease_of_use", "rating": 3, "description": "Standard interface"},
        ]
    },
    {
        "name": "Edupoint (Synergy)",
        "competitor_type": "regional",
        "description": "Growing regional player with strong presence in southwest states.",
        "headquarters": "Mesa, AZ",
        "website": "https://www.edupoint.com",
        "founded_year": 1984,
        "employee_count": "300+",
        "primary_product": "Synergy SIS",
        "has_state_reporting": True,
        "has_lms": True,
        "has_assessment": False,
        "strengths": [
            {"category": "state_reporting", "rating": 5, "description": "Excellent Arizona, California support"},
            {"category": "ease_of_use", "rating": 4, "description": "Modern, intuitive interface"},
            {"category": "support", "rating": 4, "description": "Responsive regional support"},
            {"category": "features", "rating": 4, "description": "Comprehensive feature set"},
            {"category": "pricing", "rating": 3, "description": "Mid-range pricing"},
            {"category": "integration", "rating": 3, "description": "Growing integrations"},
        ]
    },
    {
        "name": "LINQ (ERP)",
        "competitor_type": "regional",
        "description": "North Carolina-based provider with strong southeast presence.",
        "headquarters": "Wilmington, NC",
        "website": "https://www.linq.com",
        "founded_year": 1983,
        "employee_count": "400+",
        "primary_product": "LINQ ERP",
        "has_state_reporting": True,
        "has_lms": False,
        "has_assessment": False,
        "strengths": [
            {"category": "state_reporting", "rating": 5, "description": "Strong NC, SC compliance"},
            {"category": "support", "rating": 4, "description": "Excellent regional support"},
            {"category": "pricing", "rating": 4, "description": "Competitive southeast pricing"},
            {"category": "features", "rating": 3, "description": "ERP-focused feature set"},
            {"category": "ease_of_use", "rating": 3, "description": "Functional interface"},
            {"category": "integration", "rating": 3, "description": "Southeast vendor integrations"},
        ]
    },
    {
        "name": "Focus School Software",
        "competitor_type": "regional",
        "description": "Florida-based provider with growing multi-state presence.",
        "headquarters": "Jacksonville, FL",
        "website": "https://www.focusschoolsoftware.com",
        "founded_year": 2005,
        "employee_count": "150+",
        "primary_product": "Focus SIS",
        "has_state_reporting": True,
        "has_lms": True,
        "has_assessment": False,
        "strengths": [
            {"category": "state_reporting", "rating": 5, "description": "Excellent Florida compliance"},
            {"category": "ease_of_use", "rating": 5, "description": "Modern, cloud-native interface"},
            {"category": "pricing", "rating": 4, "description": "Competitive cloud pricing"},
            {"category": "support", "rating": 4, "description": "Responsive support team"},
            {"category": "features", "rating": 4, "description": "Modern feature set"},
            {"category": "integration", "rating": 3, "description": "Growing API ecosystem"},
        ]
    },
    {
        "name": "Illuminate Education",
        "competitor_type": "regional",
        "description": "Assessment-focused company with SIS and state reporting capabilities.",
        "headquarters": "Irvine, CA",
        "website": "https://www.illuminateed.com",
        "founded_year": 2009,
        "employee_count": "300+",
        "primary_product": "Illuminate DnA",
        "has_state_reporting": True,
        "has_lms": False,
        "has_assessment": True,
        "strengths": [
            {"category": "features", "rating": 5, "description": "Best-in-class assessment tools"},
            {"category": "state_reporting", "rating": 4, "description": "Good California compliance"},
            {"category": "ease_of_use", "rating": 4, "description": "Clean data interface"},
            {"category": "pricing", "rating": 3, "description": "Assessment bundle pricing"},
            {"category": "support", "rating": 3, "description": "Growing support team"},
            {"category": "integration", "rating": 4, "description": "Strong data integrations"},
        ]
    },
]

# State-specific competitor presence data
# Format: {state_abbrev: [{competitor_name, presence_level, market_share_percent, notes}]}
STATE_COMPETITORS = {
    "AL": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 20},
        {"name": "Tyler Technologies (Tyler SIS)", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "AK": [
        {"name": "PowerSchool", "presence_level": "dominant", "market_share_percent": 50},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "AZ": [
        {"name": "Edupoint (Synergy)", "presence_level": "dominant", "market_share_percent": 45},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 25},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "AR": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Skyward", "presence_level": "moderate", "market_share_percent": 20},
        {"name": "Tyler Technologies (Tyler SIS)", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "CA": [
        {"name": "Aeries Software", "presence_level": "dominant", "market_share_percent": 40},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 25},
        {"name": "Illuminate Education", "presence_level": "moderate", "market_share_percent": 10},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 10},
    ],
    "CO": [
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 35},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 30},
        {"name": "Skyward", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "CT": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Follett (Aspen)", "presence_level": "moderate", "market_share_percent": 20},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "DE": [
        {"name": "PowerSchool", "presence_level": "dominant", "market_share_percent": 50},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 20},
    ],
    "FL": [
        {"name": "Focus School Software", "presence_level": "strong", "market_share_percent": 30},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 25},
        {"name": "Skyward", "presence_level": "moderate", "market_share_percent": 15},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 10},
    ],
    "GA": [
        {"name": "Infinite Campus", "presence_level": "dominant", "market_share_percent": 45},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 25},
        {"name": "Tyler Technologies (Tyler SIS)", "presence_level": "moderate", "market_share_percent": 10},
    ],
    "HI": [
        {"name": "Infinite Campus", "presence_level": "dominant", "market_share_percent": 60},
        {"name": "PowerSchool", "presence_level": "moderate", "market_share_percent": 20},
    ],
    "ID": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 30},
    ],
    "IL": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 30},
        {"name": "Skyward", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "IN": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 30},
        {"name": "Skyward", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "IA": [
        {"name": "Infinite Campus", "presence_level": "dominant", "market_share_percent": 50},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 25},
    ],
    "KS": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Skyward", "presence_level": "moderate", "market_share_percent": 25},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "KY": [
        {"name": "Infinite Campus", "presence_level": "dominant", "market_share_percent": 55},
        {"name": "PowerSchool", "presence_level": "moderate", "market_share_percent": 20},
    ],
    "LA": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
        {"name": "Tyler Technologies (Tyler SIS)", "presence_level": "moderate", "market_share_percent": 20},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "ME": [
        {"name": "PowerSchool", "presence_level": "dominant", "market_share_percent": 50},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 20},
    ],
    "MD": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 30},
    ],
    "MA": [
        {"name": "Follett (Aspen)", "presence_level": "strong", "market_share_percent": 35},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 30},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "MI": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
        {"name": "Skyward", "presence_level": "strong", "market_share_percent": 30},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "MN": [
        {"name": "Infinite Campus", "presence_level": "dominant", "market_share_percent": 55},
        {"name": "PowerSchool", "presence_level": "moderate", "market_share_percent": 20},
        {"name": "Skyward", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "MS": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "MO": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
        {"name": "Tyler Technologies (Tyler SIS)", "presence_level": "strong", "market_share_percent": 25},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 20},
    ],
    "MT": [
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 40},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
    ],
    "NE": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 30},
    ],
    "NV": [
        {"name": "Infinite Campus", "presence_level": "dominant", "market_share_percent": 60},
        {"name": "PowerSchool", "presence_level": "moderate", "market_share_percent": 20},
    ],
    "NH": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 45},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "NJ": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
        {"name": "Follett (Aspen)", "presence_level": "moderate", "market_share_percent": 20},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "NM": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "NY": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 30},
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 25},
        {"name": "Follett (Aspen)", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "NC": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
        {"name": "LINQ (ERP)", "presence_level": "strong", "market_share_percent": 30},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "ND": [
        {"name": "PowerSchool", "presence_level": "dominant", "market_share_percent": 50},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "OH": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 30},
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 30},
        {"name": "Skyward", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "OK": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Tyler Technologies (Tyler SIS)", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "OR": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 30},
    ],
    "PA": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
        {"name": "Skyward", "presence_level": "moderate", "market_share_percent": 20},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 20},
    ],
    "RI": [
        {"name": "PowerSchool", "presence_level": "dominant", "market_share_percent": 55},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 20},
    ],
    "SC": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "LINQ (ERP)", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "SD": [
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 40},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 35},
    ],
    "TN": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "TX": [
        {"name": "Skyward", "presence_level": "strong", "market_share_percent": 30},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 25},
        {"name": "Tyler Technologies (Tyler SIS)", "presence_level": "moderate", "market_share_percent": 15},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 10},
    ],
    "UT": [
        {"name": "Infinite Campus", "presence_level": "dominant", "market_share_percent": 55},
        {"name": "PowerSchool", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "VT": [
        {"name": "PowerSchool", "presence_level": "dominant", "market_share_percent": 55},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 20},
    ],
    "VA": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 40},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "WA": [
        {"name": "Skyward", "presence_level": "strong", "market_share_percent": 35},
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 30},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "WV": [
        {"name": "PowerSchool", "presence_level": "dominant", "market_share_percent": 50},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 25},
    ],
    "WI": [
        {"name": "Skyward", "presence_level": "dominant", "market_share_percent": 45},
        {"name": "Infinite Campus", "presence_level": "strong", "market_share_percent": 25},
        {"name": "PowerSchool", "presence_level": "moderate", "market_share_percent": 15},
    ],
    "WY": [
        {"name": "PowerSchool", "presence_level": "strong", "market_share_percent": 45},
        {"name": "Infinite Campus", "presence_level": "moderate", "market_share_percent": 30},
    ],
}


async def seed_competitors(db):
    """Seed competitor data into database."""
    from models import Competitor, CompetitorStrength, StateCompetitor, State
    from sqlalchemy import select

    # First, create competitors
    competitor_map = {}

    for comp_data in COMPETITORS:
        # Check if competitor exists
        result = await db.execute(
            select(Competitor).where(Competitor.name == comp_data["name"])
        )
        competitor = result.scalar_one_or_none()

        if not competitor:
            # Create competitor
            competitor = Competitor(
                name=comp_data["name"],
                description=comp_data.get("description"),
                competitor_type=comp_data["competitor_type"],
                headquarters=comp_data.get("headquarters"),
                website=comp_data.get("website"),
                founded_year=comp_data.get("founded_year"),
                employee_count=comp_data.get("employee_count"),
                primary_product=comp_data.get("primary_product"),
                has_state_reporting=comp_data.get("has_state_reporting", True),
                has_lms=comp_data.get("has_lms", False),
                has_assessment=comp_data.get("has_assessment", False),
            )
            db.add(competitor)
            await db.flush()

            # Add strengths
            for strength_data in comp_data.get("strengths", []):
                strength = CompetitorStrength(
                    competitor_id=competitor.id,
                    category=strength_data["category"],
                    rating=strength_data["rating"],
                    description=strength_data.get("description"),
                    is_strength=strength_data["rating"] >= 4,
                )
                db.add(strength)

        competitor_map[comp_data["name"]] = competitor.id

    await db.commit()

    # Refresh competitor map after commit
    for comp_data in COMPETITORS:
        result = await db.execute(
            select(Competitor).where(Competitor.name == comp_data["name"])
        )
        competitor = result.scalar_one()
        competitor_map[comp_data["name"]] = competitor.id

    # Now add state presence data
    for state_abbrev, competitors in STATE_COMPETITORS.items():
        # Get state
        result = await db.execute(
            select(State).where(State.abbreviation == state_abbrev)
        )
        state = result.scalar_one_or_none()

        if not state:
            continue

        for comp_presence in competitors:
            competitor_id = competitor_map.get(comp_presence["name"])
            if not competitor_id:
                continue

            # Check if presence record exists
            result = await db.execute(
                select(StateCompetitor).where(
                    StateCompetitor.state_id == state.id,
                    StateCompetitor.competitor_id == competitor_id
                )
            )
            existing = result.scalar_one_or_none()

            if not existing:
                presence = StateCompetitor(
                    state_id=state.id,
                    competitor_id=competitor_id,
                    presence_level=comp_presence.get("presence_level", "moderate"),
                    market_share_percent=comp_presence.get("market_share_percent"),
                    data_confidence="estimated",
                )
                db.add(presence)

    await db.commit()

    # Update competitor total_states counts
    for name, comp_id in competitor_map.items():
        result = await db.execute(
            select(StateCompetitor).where(StateCompetitor.competitor_id == comp_id)
        )
        presence_count = len(result.scalars().all())

        result = await db.execute(
            select(Competitor).where(Competitor.id == comp_id)
        )
        competitor = result.scalar_one()
        competitor.total_states = presence_count

    await db.commit()

    return len(competitor_map)
