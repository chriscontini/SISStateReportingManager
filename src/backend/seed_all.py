"""
Master seeding script for SISStateReportingManager.

Runs all seeders in the correct dependency order:
1. States and ranking factors (seed_data.py)
2. NCES data (nces_data.py)
3. State analysis (seed_analysis.py)
4. Gap analysis (seed_gap_analysis.py)
5. Roadmaps (seed_roadmaps.py)
6. Knowledge articles (seed_knowledge.py)

Usage:
    python -m src.backend.seed_all

    Or with options:
    python -m src.backend.seed_all --skip-analysis --skip-roadmaps
"""

import asyncio
import argparse
import sys
from datetime import datetime

from sqlalchemy import select, func

from .database import get_engine, get_session_maker
from .models import State, RankingFactor, StateScore, StateAnalysis, GapAnalysis, Roadmap, KnowledgeArticle


async def check_database_connection():
    """Verify database connection works."""
    print("\n" + "=" * 60)
    print("CHECKING DATABASE CONNECTION")
    print("=" * 60)

    try:
        engine = get_engine()
        SessionLocal = get_session_maker(engine)

        async with SessionLocal() as session:
            result = await session.execute(select(func.count()).select_from(State))
            count = result.scalar()
            print(f"Database connected. Found {count} existing states.")
            return True
    except Exception as e:
        print(f"ERROR: Database connection failed: {e}")
        return False


async def seed_states_and_factors():
    """Seed states and ranking factors."""
    print("\n" + "=" * 60)
    print("STEP 1: SEEDING STATES AND RANKING FACTORS")
    print("=" * 60)

    from .seed_data import seed_states

    engine = get_engine()
    SessionLocal = get_session_maker(engine)

    async with SessionLocal() as session:
        # Check if states already exist
        result = await session.execute(select(func.count()).select_from(State))
        count = result.scalar()

        if count >= 50:
            print(f"States already seeded ({count} states). Skipping.")
            return True

        print("Seeding 50 US states...")
        await seed_states(session)
        print("States seeded successfully.")
        return True


async def seed_nces_data():
    """Seed NCES (National Center for Education Statistics) data."""
    print("\n" + "=" * 60)
    print("STEP 2: SEEDING NCES DATA")
    print("=" * 60)

    try:
        from .nces_data import seed_nces_data as do_seed_nces

        engine = get_engine()
        SessionLocal = get_session_maker(engine)

        async with SessionLocal() as session:
            # Check if NCES data already exists
            result = await session.execute(
                select(State).where(State.total_students > 0).limit(1)
            )
            existing = result.scalar_one_or_none()

            if existing:
                print("NCES data already seeded. Skipping.")
                return True

            print("Seeding NCES data for all states...")
            await do_seed_nces(session)
            print("NCES data seeded successfully.")
            return True
    except ImportError:
        print("NCES data module not found. Skipping.")
        return True
    except Exception as e:
        print(f"Warning: Could not seed NCES data: {e}")
        return True


async def seed_state_analysis():
    """Seed state analysis for top states."""
    print("\n" + "=" * 60)
    print("STEP 3: SEEDING STATE ANALYSIS")
    print("=" * 60)

    try:
        from .seed_analysis import seed_tier2_analysis

        engine = get_engine()
        SessionLocal = get_session_maker(engine)

        async with SessionLocal() as session:
            # Check if analysis already exists
            result = await session.execute(select(func.count()).select_from(StateAnalysis))
            count = result.scalar()

            if count > 0:
                print(f"State analysis already seeded ({count} analyses). Skipping.")
                return True

            print("Seeding state analysis for PA, TX, MD...")
            await seed_tier2_analysis()
            print("State analysis seeded successfully.")
            return True
    except ImportError:
        print("State analysis module not found. Skipping.")
        return True
    except Exception as e:
        print(f"Warning: Could not seed state analysis: {e}")
        return True


async def seed_gap_analysis():
    """Seed gap analysis for target states."""
    print("\n" + "=" * 60)
    print("STEP 4: SEEDING GAP ANALYSIS")
    print("=" * 60)

    try:
        from .seed_gap_analysis import seed_gap_analysis as do_seed_gaps

        engine = get_engine()
        SessionLocal = get_session_maker(engine)

        async with SessionLocal() as session:
            # Check if gaps already exist
            result = await session.execute(select(func.count()).select_from(GapAnalysis))
            count = result.scalar()

            if count > 0:
                print(f"Gap analysis already seeded ({count} analyses). Skipping.")
                return True

            print("Seeding gap analysis for PA, TX, MD...")
            await do_seed_gaps()
            print("Gap analysis seeded successfully.")
            return True
    except ImportError:
        print("Gap analysis module not found. Skipping.")
        return True
    except Exception as e:
        print(f"Warning: Could not seed gap analysis: {e}")
        return True


async def seed_roadmaps():
    """Seed roadmaps for target states."""
    print("\n" + "=" * 60)
    print("STEP 5: SEEDING ROADMAPS")
    print("=" * 60)

    try:
        from .seed_roadmaps import seed_roadmaps as do_seed_roadmaps

        engine = get_engine()
        SessionLocal = get_session_maker(engine)

        async with SessionLocal() as session:
            # Check if roadmaps already exist
            result = await session.execute(select(func.count()).select_from(Roadmap))
            count = result.scalar()

            if count > 0:
                print(f"Roadmaps already seeded ({count} roadmaps). Skipping.")
                return True

            print("Seeding roadmaps for MD, PA...")
            await do_seed_roadmaps()
            print("Roadmaps seeded successfully.")
            return True
    except ImportError:
        print("Roadmaps module not found. Skipping.")
        return True
    except Exception as e:
        print(f"Warning: Could not seed roadmaps: {e}")
        return True


async def seed_knowledge():
    """Seed knowledge articles for target states."""
    print("\n" + "=" * 60)
    print("STEP 6: SEEDING KNOWLEDGE ARTICLES")
    print("=" * 60)

    try:
        from .seed_knowledge import seed_knowledge_articles

        engine = get_engine()
        SessionLocal = get_session_maker(engine)

        async with SessionLocal() as session:
            # Check if articles already exist
            result = await session.execute(select(func.count()).select_from(KnowledgeArticle))
            count = result.scalar()

            if count > 0:
                print(f"Knowledge articles already seeded ({count} articles). Skipping.")
                return True

            print("Seeding knowledge articles for PA, TX, MD...")
            await seed_knowledge_articles()
            print("Knowledge articles seeded successfully.")
            return True
    except ImportError:
        print("Knowledge module not found. Skipping.")
        return True
    except Exception as e:
        print(f"Warning: Could not seed knowledge articles: {e}")
        return True


async def print_summary():
    """Print summary of seeded data."""
    print("\n" + "=" * 60)
    print("SEEDING SUMMARY")
    print("=" * 60)

    engine = get_engine()
    SessionLocal = get_session_maker(engine)

    async with SessionLocal() as session:
        # Count all entities
        states = (await session.execute(select(func.count()).select_from(State))).scalar()
        factors = (await session.execute(select(func.count()).select_from(RankingFactor))).scalar()
        scores = (await session.execute(select(func.count()).select_from(StateScore))).scalar()
        analyses = (await session.execute(select(func.count()).select_from(StateAnalysis))).scalar()
        gaps = (await session.execute(select(func.count()).select_from(GapAnalysis))).scalar()
        roadmaps = (await session.execute(select(func.count()).select_from(Roadmap))).scalar()
        articles = (await session.execute(select(func.count()).select_from(KnowledgeArticle))).scalar()

        print(f"""
Database Contents:
------------------
States:             {states}
Ranking Factors:    {factors}
State Scores:       {scores}
State Analyses:     {analyses}
Gap Analyses:       {gaps}
Roadmaps:           {roadmaps}
Knowledge Articles: {articles}

Seeding completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")


async def main(
    skip_nces: bool = False,
    skip_analysis: bool = False,
    skip_gaps: bool = False,
    skip_roadmaps: bool = False,
    skip_knowledge: bool = False,
):
    """Run all seeders in order."""
    print("\n" + "=" * 60)
    print("SISStateReportingManager - Database Seeding")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check database connection
    if not await check_database_connection():
        print("\nERROR: Cannot proceed without database connection.")
        sys.exit(1)

    # Run seeders in order
    await seed_states_and_factors()

    if not skip_nces:
        await seed_nces_data()
    else:
        print("\nSkipping NCES data (--skip-nces)")

    if not skip_analysis:
        await seed_state_analysis()
    else:
        print("\nSkipping state analysis (--skip-analysis)")

    if not skip_gaps:
        await seed_gap_analysis()
    else:
        print("\nSkipping gap analysis (--skip-gaps)")

    if not skip_roadmaps:
        await seed_roadmaps()
    else:
        print("\nSkipping roadmaps (--skip-roadmaps)")

    if not skip_knowledge:
        await seed_knowledge()
    else:
        print("\nSkipping knowledge articles (--skip-knowledge)")

    # Print summary
    await print_summary()

    print("=" * 60)
    print("SEEDING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed SISStateReportingManager database")
    parser.add_argument("--skip-nces", action="store_true", help="Skip NCES data seeding")
    parser.add_argument("--skip-analysis", action="store_true", help="Skip state analysis seeding")
    parser.add_argument("--skip-gaps", action="store_true", help="Skip gap analysis seeding")
    parser.add_argument("--skip-roadmaps", action="store_true", help="Skip roadmaps seeding")
    parser.add_argument("--skip-knowledge", action="store_true", help="Skip knowledge articles seeding")

    args = parser.parse_args()

    asyncio.run(main(
        skip_nces=args.skip_nces,
        skip_analysis=args.skip_analysis,
        skip_gaps=args.skip_gaps,
        skip_roadmaps=args.skip_roadmaps,
        skip_knowledge=args.skip_knowledge,
    ))
