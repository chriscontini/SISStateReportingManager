"""
Seed data for all 50 US states.

Includes state names, abbreviations, and Department of Education URLs.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from .models import State, RankingFactor


# All 50 US states with DOE websites
STATES_DATA = [
    {"name": "Alabama", "abbreviation": "AL", "doe_website": "https://www.alsde.edu/"},
    {"name": "Alaska", "abbreviation": "AK", "doe_website": "https://education.alaska.gov/"},
    {"name": "Arizona", "abbreviation": "AZ", "doe_website": "https://www.azed.gov/"},
    {"name": "Arkansas", "abbreviation": "AR", "doe_website": "https://dese.ade.arkansas.gov/"},
    {"name": "California", "abbreviation": "CA", "doe_website": "https://www.cde.ca.gov/"},
    {"name": "Colorado", "abbreviation": "CO", "doe_website": "https://www.cde.state.co.us/"},
    {"name": "Connecticut", "abbreviation": "CT", "doe_website": "https://portal.ct.gov/sde"},
    {"name": "Delaware", "abbreviation": "DE", "doe_website": "https://www.doe.k12.de.us/"},
    {"name": "Florida", "abbreviation": "FL", "doe_website": "https://www.fldoe.org/"},
    {"name": "Georgia", "abbreviation": "GA", "doe_website": "https://www.gadoe.org/"},
    {"name": "Hawaii", "abbreviation": "HI", "doe_website": "https://www.hawaiipublicschools.org/"},
    {"name": "Idaho", "abbreviation": "ID", "doe_website": "https://www.sde.idaho.gov/"},
    {"name": "Illinois", "abbreviation": "IL", "doe_website": "https://www.isbe.net/"},
    {"name": "Indiana", "abbreviation": "IN", "doe_website": "https://www.in.gov/doe/"},
    {"name": "Iowa", "abbreviation": "IA", "doe_website": "https://educateiowa.gov/"},
    {"name": "Kansas", "abbreviation": "KS", "doe_website": "https://www.ksde.org/"},
    {"name": "Kentucky", "abbreviation": "KY", "doe_website": "https://education.ky.gov/"},
    {"name": "Louisiana", "abbreviation": "LA", "doe_website": "https://www.louisianabelieves.com/"},
    {"name": "Maine", "abbreviation": "ME", "doe_website": "https://www.maine.gov/doe/"},
    {"name": "Maryland", "abbreviation": "MD", "doe_website": "https://www.marylandpublicschools.org/"},
    {"name": "Massachusetts", "abbreviation": "MA", "doe_website": "https://www.doe.mass.edu/"},
    {"name": "Michigan", "abbreviation": "MI", "doe_website": "https://www.michigan.gov/mde"},
    {"name": "Minnesota", "abbreviation": "MN", "doe_website": "https://education.mn.gov/"},
    {"name": "Mississippi", "abbreviation": "MS", "doe_website": "https://www.mdek12.org/"},
    {"name": "Missouri", "abbreviation": "MO", "doe_website": "https://dese.mo.gov/"},
    {"name": "Montana", "abbreviation": "MT", "doe_website": "https://opi.mt.gov/"},
    {"name": "Nebraska", "abbreviation": "NE", "doe_website": "https://www.education.ne.gov/"},
    {"name": "Nevada", "abbreviation": "NV", "doe_website": "https://doe.nv.gov/"},
    {"name": "New Hampshire", "abbreviation": "NH", "doe_website": "https://www.education.nh.gov/"},
    {"name": "New Jersey", "abbreviation": "NJ", "doe_website": "https://www.nj.gov/education/"},
    {"name": "New Mexico", "abbreviation": "NM", "doe_website": "https://webnew.ped.state.nm.us/"},
    {"name": "New York", "abbreviation": "NY", "doe_website": "https://www.nysed.gov/"},
    {"name": "North Carolina", "abbreviation": "NC", "doe_website": "https://www.dpi.nc.gov/"},
    {"name": "North Dakota", "abbreviation": "ND", "doe_website": "https://www.nd.gov/dpi/"},
    {"name": "Ohio", "abbreviation": "OH", "doe_website": "https://education.ohio.gov/"},
    {"name": "Oklahoma", "abbreviation": "OK", "doe_website": "https://sde.ok.gov/"},
    {"name": "Oregon", "abbreviation": "OR", "doe_website": "https://www.oregon.gov/ode/"},
    {"name": "Pennsylvania", "abbreviation": "PA", "doe_website": "https://www.education.pa.gov/"},
    {"name": "Rhode Island", "abbreviation": "RI", "doe_website": "https://www.ride.ri.gov/"},
    {"name": "South Carolina", "abbreviation": "SC", "doe_website": "https://ed.sc.gov/"},
    {"name": "South Dakota", "abbreviation": "SD", "doe_website": "https://doe.sd.gov/"},
    {"name": "Tennessee", "abbreviation": "TN", "doe_website": "https://www.tn.gov/education.html"},
    {"name": "Texas", "abbreviation": "TX", "doe_website": "https://tea.texas.gov/"},
    {"name": "Utah", "abbreviation": "UT", "doe_website": "https://www.schools.utah.gov/"},
    {"name": "Vermont", "abbreviation": "VT", "doe_website": "https://education.vermont.gov/"},
    {"name": "Virginia", "abbreviation": "VA", "doe_website": "https://www.doe.virginia.gov/"},
    {"name": "Washington", "abbreviation": "WA", "doe_website": "https://www.k12.wa.us/"},
    {"name": "West Virginia", "abbreviation": "WV", "doe_website": "https://wvde.us/"},
    {"name": "Wisconsin", "abbreviation": "WI", "doe_website": "https://dpi.wi.gov/"},
    {"name": "Wyoming", "abbreviation": "WY", "doe_website": "https://edu.wyoming.gov/"},
]

# Default ranking factors based on PRD
DEFAULT_RANKING_FACTORS = [
    {
        "name": "Development Effort",
        "description": "Amount of work to build state reporting/validation",
        "weight": 3.0,
        "data_source": "DOE documentation analysis",
        "is_active": True,
    },
    {
        "name": "District Structure",
        "description": "Parish/county model (like LA) vs fragmented districts (like NJ)",
        "weight": 2.5,
        "data_source": "NCES data",
        "is_active": True,
    },
    {
        "name": "Average District Size",
        "description": "Larger districts = higher ARPU potential",
        "weight": 2.5,
        "data_source": "NCES data",
        "is_active": True,
    },
    {
        "name": "Technical Fit",
        "description": "How closely existing NJ/LA code matches state requirements",
        "weight": 2.0,
        "data_source": "DOE documentation",
        "is_active": True,
    },
    {
        "name": "Certification Complexity",
        "description": "Formal vendor certification vs. open market",
        "weight": 1.5,
        "data_source": "DOE documentation",
        "is_active": True,
    },
    {
        "name": "Competitive Landscape",
        "description": "Density of national/regional competitors",
        "weight": 1.5,
        "data_source": "Market research",
        "is_active": True,
    },
    {
        "name": "Market Opportunity",
        "description": "Total addressable market; growth potential",
        "weight": 1.5,
        "data_source": "NCES data",
        "is_active": True,
    },
    {
        "name": "Regulatory Complexity",
        "description": "Compliance burden beyond core reporting",
        "weight": 1.0,
        "data_source": "DOE documentation",
        "is_active": True,
    },
    {
        "name": "Geographic Proximity",
        "description": "Ease of support and relationship building",
        "weight": 0.5,
        "data_source": "Geography",
        "is_active": True,
    },
]


async def seed_states(db: AsyncSession) -> int:
    """
    Seed the database with all 50 US states.

    Returns the number of states created.
    """
    created = 0
    for state_data in STATES_DATA:
        # Check if state already exists
        from sqlalchemy import select
        result = await db.execute(
            select(State).where(State.abbreviation == state_data["abbreviation"])
        )
        existing = result.scalar_one_or_none()

        if not existing:
            state = State(**state_data)
            db.add(state)
            created += 1

    await db.commit()
    return created


async def seed_ranking_factors(db: AsyncSession) -> int:
    """
    Seed the database with default ranking factors.

    Returns the number of factors created.
    """
    created = 0
    for factor_data in DEFAULT_RANKING_FACTORS:
        # Check if factor already exists
        from sqlalchemy import select
        result = await db.execute(
            select(RankingFactor).where(RankingFactor.name == factor_data["name"])
        )
        existing = result.scalar_one_or_none()

        if not existing:
            factor = RankingFactor(**factor_data)
            db.add(factor)
            created += 1

    await db.commit()
    return created


async def seed_all(db: AsyncSession) -> dict:
    """
    Seed all initial data.

    Returns a summary of what was created.
    """
    states_created = await seed_states(db)
    factors_created = await seed_ranking_factors(db)

    return {
        "states_created": states_created,
        "ranking_factors_created": factors_created,
    }
