"""
Product seed data for OnCourse Systems product portfolio.

Contains Hub (Core SIS) and Spoke (Complementary) products with features
and state fit analysis data.
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# OnCourse Product Portfolio
PRODUCTS = [
    # Hub Product - Core SIS
    {
        "name": "OnCourse SIS",
        "product_type": "hub",
        "category": "sis",
        "description": "Comprehensive Student Information System serving as the central hub for all student data management, state reporting, and district operations.",
        "is_core": True,
        "launch_year": 2005,
        "total_states": 2,  # NJ and LA currently
        "total_districts": 650,
        "integration_complexity": "low",
        "pricing_tier": "standard",
        "features": [
            {"name": "Student Demographics", "category": "core", "complexity": "low", "customization_effort": 20},
            {"name": "Enrollment Management", "category": "core", "complexity": "medium", "customization_effort": 40},
            {"name": "Attendance Tracking", "category": "core", "complexity": "medium", "customization_effort": 60},
            {"name": "Grade Management", "category": "core", "complexity": "medium", "customization_effort": 40},
            {"name": "Scheduling", "category": "core", "complexity": "high", "customization_effort": 80},
            {"name": "State Reporting Engine", "category": "reporting", "complexity": "high", "customization_effort": 200, "is_state_specific": True},
            {"name": "CEDS Compliance", "category": "compliance", "complexity": "medium", "customization_effort": 40},
            {"name": "Ed-Fi Integration", "category": "integration", "complexity": "medium", "customization_effort": 60},
            {"name": "Parent Portal", "category": "core", "complexity": "low", "customization_effort": 20},
            {"name": "Student Portal", "category": "core", "complexity": "low", "customization_effort": 20},
            {"name": "Custom Reports Builder", "category": "analytics", "complexity": "medium", "customization_effort": 30},
            {"name": "Data Validation Rules", "category": "compliance", "complexity": "high", "customization_effort": 100, "is_state_specific": True},
            {"name": "Transcript Management", "category": "core", "complexity": "medium", "customization_effort": 50},
            {"name": "Health Records", "category": "core", "complexity": "low", "customization_effort": 30},
            {"name": "Discipline Tracking", "category": "core", "complexity": "low", "customization_effort": 25},
        ],
    },
    # Spoke Products
    {
        "name": "OnCourse LMS",
        "product_type": "spoke",
        "category": "lms",
        "description": "Learning Management System for course content delivery, assignments, and online learning experiences.",
        "is_core": False,
        "launch_year": 2018,
        "total_states": 2,
        "total_districts": 200,
        "integration_complexity": "low",
        "pricing_tier": "standard",
        "features": [
            {"name": "Course Management", "category": "core", "complexity": "medium", "customization_effort": 20},
            {"name": "Assignment Submission", "category": "core", "complexity": "low", "customization_effort": 10},
            {"name": "Discussion Forums", "category": "core", "complexity": "low", "customization_effort": 10},
            {"name": "Video Conferencing", "category": "core", "complexity": "medium", "customization_effort": 20},
            {"name": "Gradebook Sync", "category": "integration", "complexity": "low", "customization_effort": 15},
            {"name": "Content Library", "category": "core", "complexity": "low", "customization_effort": 10},
        ],
    },
    {
        "name": "OnCourse Assessment",
        "product_type": "spoke",
        "category": "assessment",
        "description": "Assessment platform for creating, delivering, and analyzing formative and summative assessments.",
        "is_core": False,
        "launch_year": 2019,
        "total_states": 2,
        "total_districts": 150,
        "integration_complexity": "low",
        "pricing_tier": "standard",
        "features": [
            {"name": "Test Builder", "category": "core", "complexity": "medium", "customization_effort": 30},
            {"name": "Item Banks", "category": "core", "complexity": "medium", "customization_effort": 25},
            {"name": "Online Testing", "category": "core", "complexity": "medium", "customization_effort": 30},
            {"name": "Standards Alignment", "category": "compliance", "complexity": "high", "customization_effort": 60, "is_state_specific": True},
            {"name": "Performance Analytics", "category": "analytics", "complexity": "medium", "customization_effort": 25},
            {"name": "Score Import/Export", "category": "integration", "complexity": "low", "customization_effort": 15},
        ],
    },
    {
        "name": "OnCourse Special Ed",
        "product_type": "spoke",
        "category": "special_ed",
        "description": "Special Education management system for IEP tracking, compliance, and progress monitoring.",
        "is_core": False,
        "launch_year": 2015,
        "total_states": 2,
        "total_districts": 300,
        "integration_complexity": "medium",
        "pricing_tier": "premium",
        "features": [
            {"name": "IEP Management", "category": "core", "complexity": "high", "customization_effort": 80, "is_state_specific": True},
            {"name": "504 Plans", "category": "core", "complexity": "medium", "customization_effort": 40},
            {"name": "Progress Monitoring", "category": "core", "complexity": "medium", "customization_effort": 30},
            {"name": "Compliance Reporting", "category": "compliance", "complexity": "high", "customization_effort": 100, "is_state_specific": True},
            {"name": "Meeting Scheduler", "category": "core", "complexity": "low", "customization_effort": 15},
            {"name": "Document Generation", "category": "automation", "complexity": "medium", "customization_effort": 40, "is_state_specific": True},
            {"name": "IDEA Compliance", "category": "compliance", "complexity": "high", "customization_effort": 60},
        ],
    },
    {
        "name": "OnCourse Finance",
        "product_type": "spoke",
        "category": "finance",
        "description": "Financial management system for budgeting, accounting, and financial reporting.",
        "is_core": False,
        "launch_year": 2012,
        "total_states": 2,
        "total_districts": 250,
        "integration_complexity": "medium",
        "pricing_tier": "premium",
        "features": [
            {"name": "Budget Management", "category": "core", "complexity": "high", "customization_effort": 50},
            {"name": "General Ledger", "category": "core", "complexity": "high", "customization_effort": 60},
            {"name": "Accounts Payable", "category": "core", "complexity": "medium", "customization_effort": 40},
            {"name": "Accounts Receivable", "category": "core", "complexity": "medium", "customization_effort": 40},
            {"name": "Grant Tracking", "category": "core", "complexity": "medium", "customization_effort": 35},
            {"name": "State Financial Reporting", "category": "reporting", "complexity": "high", "customization_effort": 80, "is_state_specific": True},
            {"name": "Audit Trail", "category": "compliance", "complexity": "medium", "customization_effort": 25},
        ],
    },
    {
        "name": "OnCourse HR",
        "product_type": "spoke",
        "category": "hr",
        "description": "Human Resources management for staff records, certifications, and personnel operations.",
        "is_core": False,
        "launch_year": 2014,
        "total_states": 2,
        "total_districts": 200,
        "integration_complexity": "medium",
        "pricing_tier": "standard",
        "features": [
            {"name": "Staff Records", "category": "core", "complexity": "medium", "customization_effort": 30},
            {"name": "Certification Tracking", "category": "compliance", "complexity": "high", "customization_effort": 60, "is_state_specific": True},
            {"name": "Position Management", "category": "core", "complexity": "medium", "customization_effort": 35},
            {"name": "Absence Tracking", "category": "core", "complexity": "low", "customization_effort": 20},
            {"name": "Professional Development", "category": "core", "complexity": "medium", "customization_effort": 30},
            {"name": "Staff Reporting", "category": "reporting", "complexity": "high", "customization_effort": 70, "is_state_specific": True},
        ],
    },
    {
        "name": "OnCourse Transportation",
        "product_type": "spoke",
        "category": "transportation",
        "description": "Transportation management for routing, bus tracking, and transportation reporting.",
        "is_core": False,
        "launch_year": 2017,
        "total_states": 1,
        "total_districts": 100,
        "integration_complexity": "low",
        "pricing_tier": "entry",
        "features": [
            {"name": "Route Planning", "category": "core", "complexity": "high", "customization_effort": 40},
            {"name": "Bus Tracking", "category": "core", "complexity": "medium", "customization_effort": 30},
            {"name": "Stop Management", "category": "core", "complexity": "low", "customization_effort": 20},
            {"name": "Driver Management", "category": "core", "complexity": "low", "customization_effort": 15},
            {"name": "Transportation Reports", "category": "reporting", "complexity": "medium", "customization_effort": 35, "is_state_specific": True},
        ],
    },
]


# State product fit data for target states
STATE_PRODUCT_FITS = {
    # Maryland - High fit due to county-based model like LA
    "MD": {
        "OnCourse SIS": {"fit_score": 8.5, "gap_count": 12, "critical_gaps": 2, "customization_hours": 800, "synergy_score": 9.0},
        "OnCourse LMS": {"fit_score": 9.0, "gap_count": 3, "critical_gaps": 0, "customization_hours": 100, "synergy_score": 8.5},
        "OnCourse Assessment": {"fit_score": 7.5, "gap_count": 5, "critical_gaps": 1, "customization_hours": 200, "synergy_score": 8.0},
        "OnCourse Special Ed": {"fit_score": 7.0, "gap_count": 8, "critical_gaps": 2, "customization_hours": 400, "synergy_score": 8.5},
        "OnCourse Finance": {"fit_score": 6.5, "gap_count": 10, "critical_gaps": 2, "customization_hours": 350, "synergy_score": 7.5},
        "OnCourse HR": {"fit_score": 7.5, "gap_count": 6, "critical_gaps": 1, "customization_hours": 250, "synergy_score": 8.0},
        "OnCourse Transportation": {"fit_score": 8.0, "gap_count": 4, "critical_gaps": 0, "customization_hours": 150, "synergy_score": 7.0},
    },
    # Pennsylvania - Good fit, similar to NJ
    "PA": {
        "OnCourse SIS": {"fit_score": 8.0, "gap_count": 15, "critical_gaps": 3, "customization_hours": 1000, "synergy_score": 8.5},
        "OnCourse LMS": {"fit_score": 9.0, "gap_count": 2, "critical_gaps": 0, "customization_hours": 80, "synergy_score": 8.5},
        "OnCourse Assessment": {"fit_score": 7.0, "gap_count": 7, "critical_gaps": 2, "customization_hours": 300, "synergy_score": 7.5},
        "OnCourse Special Ed": {"fit_score": 7.5, "gap_count": 6, "critical_gaps": 1, "customization_hours": 350, "synergy_score": 8.5},
        "OnCourse Finance": {"fit_score": 7.0, "gap_count": 8, "critical_gaps": 1, "customization_hours": 300, "synergy_score": 7.5},
        "OnCourse HR": {"fit_score": 8.0, "gap_count": 5, "critical_gaps": 1, "customization_hours": 200, "synergy_score": 8.0},
        "OnCourse Transportation": {"fit_score": 7.5, "gap_count": 5, "critical_gaps": 1, "customization_hours": 180, "synergy_score": 7.0},
    },
    # Texas - Large market, complex requirements
    "TX": {
        "OnCourse SIS": {"fit_score": 6.5, "gap_count": 25, "critical_gaps": 5, "customization_hours": 2000, "synergy_score": 9.0},
        "OnCourse LMS": {"fit_score": 8.5, "gap_count": 4, "critical_gaps": 0, "customization_hours": 120, "synergy_score": 8.0},
        "OnCourse Assessment": {"fit_score": 6.0, "gap_count": 12, "critical_gaps": 3, "customization_hours": 500, "synergy_score": 7.5},
        "OnCourse Special Ed": {"fit_score": 6.5, "gap_count": 10, "critical_gaps": 3, "customization_hours": 600, "synergy_score": 8.0},
        "OnCourse Finance": {"fit_score": 6.0, "gap_count": 15, "critical_gaps": 3, "customization_hours": 550, "synergy_score": 7.0},
        "OnCourse HR": {"fit_score": 7.0, "gap_count": 8, "critical_gaps": 2, "customization_hours": 350, "synergy_score": 7.5},
        "OnCourse Transportation": {"fit_score": 7.0, "gap_count": 7, "critical_gaps": 1, "customization_hours": 250, "synergy_score": 7.0},
    },
    # Florida - County-based, good opportunity
    "FL": {
        "OnCourse SIS": {"fit_score": 7.5, "gap_count": 18, "critical_gaps": 3, "customization_hours": 1200, "synergy_score": 8.5},
        "OnCourse LMS": {"fit_score": 8.5, "gap_count": 3, "critical_gaps": 0, "customization_hours": 100, "synergy_score": 8.0},
        "OnCourse Assessment": {"fit_score": 7.0, "gap_count": 8, "critical_gaps": 2, "customization_hours": 350, "synergy_score": 7.5},
        "OnCourse Special Ed": {"fit_score": 7.0, "gap_count": 9, "critical_gaps": 2, "customization_hours": 450, "synergy_score": 8.0},
        "OnCourse Finance": {"fit_score": 6.5, "gap_count": 12, "critical_gaps": 2, "customization_hours": 400, "synergy_score": 7.0},
        "OnCourse HR": {"fit_score": 7.5, "gap_count": 6, "critical_gaps": 1, "customization_hours": 280, "synergy_score": 7.5},
        "OnCourse Transportation": {"fit_score": 8.0, "gap_count": 4, "critical_gaps": 0, "customization_hours": 160, "synergy_score": 7.5},
    },
    # New York - Large, complex market
    "NY": {
        "OnCourse SIS": {"fit_score": 7.0, "gap_count": 20, "critical_gaps": 4, "customization_hours": 1500, "synergy_score": 8.5},
        "OnCourse LMS": {"fit_score": 8.5, "gap_count": 4, "critical_gaps": 0, "customization_hours": 110, "synergy_score": 8.0},
        "OnCourse Assessment": {"fit_score": 6.5, "gap_count": 10, "critical_gaps": 2, "customization_hours": 400, "synergy_score": 7.5},
        "OnCourse Special Ed": {"fit_score": 7.0, "gap_count": 8, "critical_gaps": 2, "customization_hours": 500, "synergy_score": 8.5},
        "OnCourse Finance": {"fit_score": 6.5, "gap_count": 11, "critical_gaps": 2, "customization_hours": 380, "synergy_score": 7.0},
        "OnCourse HR": {"fit_score": 7.5, "gap_count": 7, "critical_gaps": 1, "customization_hours": 300, "synergy_score": 8.0},
        "OnCourse Transportation": {"fit_score": 7.5, "gap_count": 5, "critical_gaps": 1, "customization_hours": 200, "synergy_score": 7.0},
    },
    # Delaware - Small, adjacent to NJ
    "DE": {
        "OnCourse SIS": {"fit_score": 8.5, "gap_count": 10, "critical_gaps": 1, "customization_hours": 600, "synergy_score": 8.5},
        "OnCourse LMS": {"fit_score": 9.0, "gap_count": 2, "critical_gaps": 0, "customization_hours": 70, "synergy_score": 8.5},
        "OnCourse Assessment": {"fit_score": 8.0, "gap_count": 4, "critical_gaps": 0, "customization_hours": 150, "synergy_score": 8.0},
        "OnCourse Special Ed": {"fit_score": 8.0, "gap_count": 5, "critical_gaps": 1, "customization_hours": 250, "synergy_score": 8.5},
        "OnCourse Finance": {"fit_score": 7.5, "gap_count": 6, "critical_gaps": 1, "customization_hours": 220, "synergy_score": 7.5},
        "OnCourse HR": {"fit_score": 8.0, "gap_count": 4, "critical_gaps": 0, "customization_hours": 180, "synergy_score": 8.0},
        "OnCourse Transportation": {"fit_score": 8.5, "gap_count": 3, "critical_gaps": 0, "customization_hours": 100, "synergy_score": 7.5},
    },
    # Connecticut - New England, moderate complexity
    "CT": {
        "OnCourse SIS": {"fit_score": 7.5, "gap_count": 14, "critical_gaps": 2, "customization_hours": 900, "synergy_score": 8.0},
        "OnCourse LMS": {"fit_score": 9.0, "gap_count": 2, "critical_gaps": 0, "customization_hours": 80, "synergy_score": 8.5},
        "OnCourse Assessment": {"fit_score": 7.5, "gap_count": 6, "critical_gaps": 1, "customization_hours": 250, "synergy_score": 7.5},
        "OnCourse Special Ed": {"fit_score": 7.5, "gap_count": 6, "critical_gaps": 1, "customization_hours": 320, "synergy_score": 8.5},
        "OnCourse Finance": {"fit_score": 7.0, "gap_count": 8, "critical_gaps": 1, "customization_hours": 280, "synergy_score": 7.5},
        "OnCourse HR": {"fit_score": 8.0, "gap_count": 5, "critical_gaps": 1, "customization_hours": 200, "synergy_score": 8.0},
        "OnCourse Transportation": {"fit_score": 7.5, "gap_count": 5, "critical_gaps": 0, "customization_hours": 170, "synergy_score": 7.0},
    },
    # Virginia - Growing market
    "VA": {
        "OnCourse SIS": {"fit_score": 7.5, "gap_count": 16, "critical_gaps": 3, "customization_hours": 1100, "synergy_score": 8.5},
        "OnCourse LMS": {"fit_score": 8.5, "gap_count": 3, "critical_gaps": 0, "customization_hours": 90, "synergy_score": 8.0},
        "OnCourse Assessment": {"fit_score": 7.0, "gap_count": 7, "critical_gaps": 1, "customization_hours": 280, "synergy_score": 7.5},
        "OnCourse Special Ed": {"fit_score": 7.0, "gap_count": 8, "critical_gaps": 2, "customization_hours": 400, "synergy_score": 8.0},
        "OnCourse Finance": {"fit_score": 6.5, "gap_count": 10, "critical_gaps": 2, "customization_hours": 350, "synergy_score": 7.0},
        "OnCourse HR": {"fit_score": 7.5, "gap_count": 6, "critical_gaps": 1, "customization_hours": 260, "synergy_score": 7.5},
        "OnCourse Transportation": {"fit_score": 7.5, "gap_count": 5, "critical_gaps": 1, "customization_hours": 190, "synergy_score": 7.0},
    },
    # Georgia - County-based
    "GA": {
        "OnCourse SIS": {"fit_score": 7.5, "gap_count": 17, "critical_gaps": 3, "customization_hours": 1150, "synergy_score": 8.5},
        "OnCourse LMS": {"fit_score": 8.5, "gap_count": 4, "critical_gaps": 0, "customization_hours": 100, "synergy_score": 8.0},
        "OnCourse Assessment": {"fit_score": 7.0, "gap_count": 8, "critical_gaps": 2, "customization_hours": 320, "synergy_score": 7.5},
        "OnCourse Special Ed": {"fit_score": 7.0, "gap_count": 9, "critical_gaps": 2, "customization_hours": 420, "synergy_score": 8.0},
        "OnCourse Finance": {"fit_score": 6.5, "gap_count": 11, "critical_gaps": 2, "customization_hours": 380, "synergy_score": 7.0},
        "OnCourse HR": {"fit_score": 7.0, "gap_count": 7, "critical_gaps": 1, "customization_hours": 280, "synergy_score": 7.5},
        "OnCourse Transportation": {"fit_score": 7.5, "gap_count": 5, "critical_gaps": 1, "customization_hours": 180, "synergy_score": 7.0},
    },
    # North Carolina - Growing market
    "NC": {
        "OnCourse SIS": {"fit_score": 7.0, "gap_count": 18, "critical_gaps": 3, "customization_hours": 1200, "synergy_score": 8.0},
        "OnCourse LMS": {"fit_score": 8.5, "gap_count": 3, "critical_gaps": 0, "customization_hours": 95, "synergy_score": 8.0},
        "OnCourse Assessment": {"fit_score": 6.5, "gap_count": 9, "critical_gaps": 2, "customization_hours": 350, "synergy_score": 7.0},
        "OnCourse Special Ed": {"fit_score": 7.0, "gap_count": 8, "critical_gaps": 2, "customization_hours": 400, "synergy_score": 8.0},
        "OnCourse Finance": {"fit_score": 6.5, "gap_count": 10, "critical_gaps": 2, "customization_hours": 360, "synergy_score": 7.0},
        "OnCourse HR": {"fit_score": 7.0, "gap_count": 7, "critical_gaps": 1, "customization_hours": 270, "synergy_score": 7.5},
        "OnCourse Transportation": {"fit_score": 7.0, "gap_count": 6, "critical_gaps": 1, "customization_hours": 200, "synergy_score": 7.0},
    },
}


async def seed_products(db: AsyncSession) -> None:
    """Seed products and features into the database."""
    from models import Product, ProductFeature, State, StateProductFit

    for product_data in PRODUCTS:
        # Check if product already exists
        result = await db.execute(
            select(Product).where(Product.name == product_data["name"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            continue

        # Create product
        features_data = product_data.pop("features", [])

        product = Product(**product_data)
        db.add(product)
        await db.flush()

        # Add features
        for feature_data in features_data:
            feature = ProductFeature(
                product_id=product.id,
                **feature_data
            )
            db.add(feature)

    await db.commit()

    # Seed state product fits
    await seed_state_product_fits(db)


async def seed_state_product_fits(db: AsyncSession) -> None:
    """Seed state product fit data."""
    from models import Product, State, StateProductFit

    for state_abbrev, products_fit in STATE_PRODUCT_FITS.items():
        # Get state
        state_result = await db.execute(
            select(State).where(State.abbreviation == state_abbrev)
        )
        state = state_result.scalar_one_or_none()

        if not state:
            continue

        for product_name, fit_data in products_fit.items():
            # Get product
            product_result = await db.execute(
                select(Product).where(Product.name == product_name)
            )
            product = product_result.scalar_one_or_none()

            if not product:
                continue

            # Check if fit already exists
            existing_result = await db.execute(
                select(StateProductFit).where(
                    StateProductFit.state_id == state.id,
                    StateProductFit.product_id == product.id
                )
            )
            existing = existing_result.scalar_one_or_none()

            if existing:
                continue

            # Create fit record
            fit = StateProductFit(
                state_id=state.id,
                product_id=product.id,
                fit_score=fit_data["fit_score"],
                gap_count=fit_data["gap_count"],
                critical_gaps=fit_data["critical_gaps"],
                customization_hours=fit_data["customization_hours"],
                synergy_score=fit_data["synergy_score"],
                analysis_status="analyzed",
            )
            db.add(fit)

    await db.commit()
