"""
NCES (National Center for Education Statistics) data for all 50 US states.

Data sourced from NCES Common Core of Data (CCD) - 2022-2023 school year.
https://nces.ed.gov/ccd/

This data is used for ranking calculations:
- Market opportunity (total students, districts)
- Average district size (students / districts)
- District structure analysis
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import State, NCESData


# NCES data for all 50 states (2022-2023 school year)
# Sources: NCES CCD Public School District Data
NCES_DATA = [
    # State, Districts, Schools, Students
    {"abbreviation": "AL", "total_districts": 143, "total_schools": 1509, "total_students": 744637},
    {"abbreviation": "AK", "total_districts": 54, "total_schools": 507, "total_students": 129390},
    {"abbreviation": "AZ", "total_districts": 237, "total_schools": 2414, "total_students": 1134378},
    {"abbreviation": "AR", "total_districts": 262, "total_schools": 1088, "total_students": 493447},
    {"abbreviation": "CA", "total_districts": 1037, "total_schools": 10523, "total_students": 5892240},
    {"abbreviation": "CO", "total_districts": 183, "total_schools": 1956, "total_students": 883199},
    {"abbreviation": "CT", "total_districts": 169, "total_schools": 1010, "total_students": 530612},
    {"abbreviation": "DE", "total_districts": 19, "total_schools": 228, "total_students": 139069},
    {"abbreviation": "FL", "total_districts": 74, "total_schools": 4337, "total_students": 2851995},
    {"abbreviation": "GA", "total_districts": 181, "total_schools": 2323, "total_students": 1765623},
    {"abbreviation": "HI", "total_districts": 1, "total_schools": 294, "total_students": 180837},
    {"abbreviation": "ID", "total_districts": 149, "total_schools": 789, "total_students": 322610},
    {"abbreviation": "IL", "total_districts": 852, "total_schools": 4187, "total_students": 1908647},
    {"abbreviation": "IN", "total_districts": 403, "total_schools": 1934, "total_students": 1043037},
    {"abbreviation": "IA", "total_districts": 327, "total_schools": 1321, "total_students": 516807},
    {"abbreviation": "KS", "total_districts": 286, "total_schools": 1314, "total_students": 498691},
    {"abbreviation": "KY", "total_districts": 173, "total_schools": 1517, "total_students": 680136},
    {"abbreviation": "LA", "total_districts": 69, "total_schools": 1416, "total_students": 684563},  # Parish model
    {"abbreviation": "ME", "total_districts": 197, "total_schools": 596, "total_students": 180036},
    {"abbreviation": "MD", "total_districts": 24, "total_schools": 1454, "total_students": 889445},  # County-based
    {"abbreviation": "MA", "total_districts": 295, "total_schools": 1861, "total_students": 953369},
    {"abbreviation": "MI", "total_districts": 539, "total_schools": 3503, "total_students": 1454079},
    {"abbreviation": "MN", "total_districts": 333, "total_schools": 2510, "total_students": 881566},
    {"abbreviation": "MS", "total_districts": 144, "total_schools": 925, "total_students": 445107},
    {"abbreviation": "MO", "total_districts": 518, "total_schools": 2383, "total_students": 902003},
    {"abbreviation": "MT", "total_districts": 411, "total_schools": 826, "total_students": 152896},
    {"abbreviation": "NE", "total_districts": 244, "total_schools": 1078, "total_students": 331351},
    {"abbreviation": "NV", "total_districts": 17, "total_schools": 736, "total_students": 496938},
    {"abbreviation": "NH", "total_districts": 161, "total_schools": 478, "total_students": 176871},
    {"abbreviation": "NJ", "total_districts": 599, "total_schools": 2610, "total_students": 1410581},  # Fragmented
    {"abbreviation": "NM", "total_districts": 89, "total_schools": 881, "total_students": 323070},
    {"abbreviation": "NY", "total_districts": 731, "total_schools": 4719, "total_students": 2611011},
    {"abbreviation": "NC", "total_districts": 115, "total_schools": 2680, "total_students": 1546615},
    {"abbreviation": "ND", "total_districts": 173, "total_schools": 510, "total_students": 117227},
    {"abbreviation": "OH", "total_districts": 610, "total_schools": 3561, "total_students": 1688642},
    {"abbreviation": "OK", "total_districts": 513, "total_schools": 1792, "total_students": 700779},
    {"abbreviation": "OR", "total_districts": 197, "total_schools": 1256, "total_students": 573157},
    {"abbreviation": "PA", "total_districts": 500, "total_schools": 3012, "total_students": 1729093},
    {"abbreviation": "RI", "total_districts": 36, "total_schools": 306, "total_students": 144732},
    {"abbreviation": "SC", "total_districts": 81, "total_schools": 1271, "total_students": 790024},
    {"abbreviation": "SD", "total_districts": 149, "total_schools": 711, "total_students": 144864},
    {"abbreviation": "TN", "total_districts": 147, "total_schools": 1859, "total_students": 999693},
    {"abbreviation": "TX", "total_districts": 1024, "total_schools": 9039, "total_students": 5427680},
    {"abbreviation": "UT", "total_districts": 41, "total_schools": 1088, "total_students": 692767},
    {"abbreviation": "VT", "total_districts": 282, "total_schools": 311, "total_students": 88904},
    {"abbreviation": "VA", "total_districts": 132, "total_schools": 2133, "total_students": 1288956},
    {"abbreviation": "WA", "total_districts": 295, "total_schools": 2469, "total_students": 1094020},
    {"abbreviation": "WV", "total_districts": 55, "total_schools": 663, "total_students": 252372},
    {"abbreviation": "WI", "total_districts": 421, "total_schools": 2254, "total_students": 865450},
    {"abbreviation": "WY", "total_districts": 48, "total_schools": 368, "total_students": 94867},
]

DATA_YEAR = 2023


async def seed_nces_data(db: AsyncSession) -> int:
    """
    Seed the database with NCES data for all 50 states.

    Returns the number of records created/updated.
    """
    updated = 0

    for nces_entry in NCES_DATA:
        # Find the state by abbreviation
        result = await db.execute(
            select(State).where(State.abbreviation == nces_entry["abbreviation"])
        )
        state = result.scalar_one_or_none()

        if not state:
            continue

        # Check if NCES data already exists for this state and year
        result = await db.execute(
            select(NCESData).where(
                NCESData.state_id == state.id,
                NCESData.data_year == DATA_YEAR
            )
        )
        existing = result.scalar_one_or_none()

        # Calculate average district size
        avg_size = nces_entry["total_students"] / nces_entry["total_districts"]

        if existing:
            # Update existing record
            existing.total_districts = nces_entry["total_districts"]
            existing.total_schools = nces_entry["total_schools"]
            existing.total_students = nces_entry["total_students"]
            existing.avg_district_size = avg_size
        else:
            # Create new record
            nces_record = NCESData(
                state_id=state.id,
                total_districts=nces_entry["total_districts"],
                total_schools=nces_entry["total_schools"],
                total_students=nces_entry["total_students"],
                avg_district_size=avg_size,
                data_year=DATA_YEAR,
            )
            db.add(nces_record)

        updated += 1

    await db.commit()
    return updated


# Notable observations for ranking algorithm:
#
# COUNTY-BASED MODELS (fewer, larger districts - favorable for ARPU):
# - Maryland (MD): 24 districts, ~37K students/district
# - Nevada (NV): 17 districts, ~29K students/district
# - Florida (FL): 74 districts, ~38K students/district
# - Louisiana (LA): 69 parishes, ~10K students/district (current client)
# - Hawaii (HI): 1 district (statewide)
#
# FRAGMENTED MODELS (many small districts - harder to scale):
# - New Jersey (NJ): 599 districts, ~2.4K students/district (current client)
# - Texas (TX): 1024 districts, ~5.3K students/district
# - California (CA): 1037 districts, ~5.7K students/district
# - Illinois (IL): 852 districts, ~2.2K students/district
#
# LARGE MARKETS (by total students):
# 1. California: 5.9M students
# 2. Texas: 5.4M students
# 3. Florida: 2.9M students
# 4. New York: 2.6M students
# 5. Illinois: 1.9M students
