"""
Seed roadmaps for target states (MD and PA).

This script generates implementation roadmaps for the primary target states
using the roadmap service based on gap analysis data.
"""

import asyncio
from sqlalchemy import select

from .database import get_engine, get_session_maker
from .models import State, Roadmap, RoadmapPhase
from .services.roadmap_service import RoadmapService


# Target states for roadmap generation
TARGET_STATES = ["MD", "PA"]


async def seed_roadmaps():
    """Generate roadmaps for target states."""
    engine = get_engine()
    SessionLocal = get_session_maker(engine)

    async with SessionLocal() as session:
        service = RoadmapService(session)

        print("=" * 60)
        print("GENERATING ROADMAPS FOR TARGET STATES")
        print("=" * 60)

        for abbrev in TARGET_STATES:
            print(f"\n{'=' * 60}")
            print(f"Generating roadmap for {abbrev}...")
            print("=" * 60)

            # Get state
            result = await session.execute(
                select(State).where(State.abbreviation == abbrev)
            )
            state = result.scalar_one_or_none()

            if not state:
                print(f"  WARNING: State {abbrev} not found in database. Skipping.")
                continue

            print(f"  State ID: {state.id}")
            print(f"  State Name: {state.name}")

            try:
                # Generate roadmap
                roadmap = await service.generate_roadmap(state.id, force_regenerate=True)

                # Get details
                details = await service.get_roadmap_with_details(state.id)

                print(f"\n  ROADMAP GENERATED:")
                print(f"  - Name: {roadmap.name}")
                print(f"  - Total Months: {roadmap.total_months}")
                print(f"  - Total Effort: {roadmap.total_effort_hours:,} hours")
                print(f"  - Peak FTE: {roadmap.peak_fte}")
                print(f"  - Baseline: {roadmap.baseline_state}")
                print(f"  - Start Date: {roadmap.start_date}")
                print(f"  - End Date: {roadmap.end_date}")

                print(f"\n  PHASES:")
                for phase in details["phases"]:
                    print(f"    {phase.phase_number}. {phase.name}")
                    print(f"       Duration: {phase.duration_months} months "
                          f"(Month {phase.start_month}-{phase.end_month})")
                    print(f"       Effort: {phase.effort_hours:,} hours, "
                          f"{phase.fte_required} FTE")

                print(f"\n  MILESTONES: {len(details['milestones'])}")
                for milestone in details["milestones"][:5]:  # Show first 5
                    print(f"    - {milestone.name} (Month {milestone.target_month})")
                if len(details["milestones"]) > 5:
                    print(f"    ... and {len(details['milestones']) - 5} more")

            except Exception as e:
                print(f"  ERROR: Failed to generate roadmap - {e}")

        print("\n" + "=" * 60)
        print("ROADMAP GENERATION COMPLETE")
        print("=" * 60)

        # Summary
        result = await session.execute(
            select(Roadmap, State)
            .join(State)
            .where(State.abbreviation.in_(TARGET_STATES))
            .order_by(Roadmap.total_months)
        )
        roadmaps = result.all()

        print("\n  SUMMARY (sorted by timeline):")
        print("-" * 60)
        for roadmap, state in roadmaps:
            print(f"  {state.abbreviation}: {roadmap.total_months} months, "
                  f"{roadmap.total_effort_hours:,} hours, "
                  f"Peak {roadmap.peak_fte} FTE")

        # Recommendation
        if roadmaps:
            shortest = roadmaps[0]
            print("\n  RECOMMENDATION:")
            print(f"  {shortest[1].name} ({shortest[1].abbreviation}) has the shortest "
                  f"timeline at {shortest[0].total_months} months")


async def get_roadmap_summary():
    """Get a summary of all roadmaps."""
    engine = get_engine()
    SessionLocal = get_session_maker(engine)

    async with SessionLocal() as session:
        result = await session.execute(
            select(Roadmap, State)
            .join(State)
            .order_by(Roadmap.total_months)
        )
        roadmaps = result.all()

        print("\nROADMAP SUMMARY")
        print("=" * 80)
        print(f"{'State':<20} {'Months':<10} {'Effort (h)':<12} "
              f"{'Peak FTE':<10} {'Status':<10}")
        print("-" * 80)

        for roadmap, state in roadmaps:
            print(f"{state.name:<20} {roadmap.total_months:<10} "
                  f"{roadmap.total_effort_hours:<12,} "
                  f"{roadmap.peak_fte:<10} {roadmap.status:<10}")

        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(seed_roadmaps())
