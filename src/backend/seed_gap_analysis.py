"""
Seed gap analysis data for target states (PA, TX, MD).

This script runs gap analysis for the three preliminary target states
using the gap detection service.
"""

import asyncio
from sqlalchemy import select

from .database import get_engine, get_session_maker
from .models import State, GapAnalysis
from .services.gap_service import GapService


# Target states for gap analysis
TARGET_STATES = ["PA", "TX", "MD"]


async def seed_gap_analysis():
    """Run gap analysis for target states."""
    engine = get_engine()
    SessionLocal = get_session_maker(engine)

    async with SessionLocal() as session:
        service = GapService(session)

        print("=" * 60)
        print("RUNNING GAP ANALYSIS FOR TARGET STATES")
        print("=" * 60)

        for abbrev in TARGET_STATES:
            print(f"\n{'=' * 60}")
            print(f"Analyzing {abbrev}...")
            print("=" * 60)

            # Get state
            result = await session.execute(
                select(State).where(State.abbreviation == abbrev)
            )
            state = result.scalar_one_or_none()

            if not state:
                print(f"  WARNING: State {abbrev} not found in database. Skipping.")
                continue

            # Determine baseline
            if abbrev == "MD":
                force_baseline = "LA"  # MD uses LA baseline (county model)
            else:
                force_baseline = "NJ"  # PA and TX use NJ baseline

            print(f"  State ID: {state.id}")
            print(f"  State Name: {state.name}")
            print(f"  Using Baseline: {force_baseline}")

            try:
                # Run analysis
                analysis = await service.run_gap_analysis(
                    state.id,
                    force_baseline=force_baseline
                )

                print(f"\n  RESULTS:")
                print(f"  - Total Gaps: {analysis.total_gaps}")
                print(f"  - Critical Gaps: {analysis.critical_gaps}")
                print(f"  - Major Gaps: {analysis.major_gaps}")
                print(f"  - Minor Gaps: {analysis.minor_gaps}")
                print(f"  - Total Effort: {analysis.total_effort_hours:,} hours")
                print(f"  - Projected Timeline: {analysis.projected_months} months")
                print(f"  - Analysis Status: {analysis.analysis_status}")

                # Get gaps summary
                gaps = await service.get_gaps_for_analysis(analysis.id)

                print(f"\n  GAPS BY CATEGORY:")
                category_counts = {}
                for gap in gaps:
                    cat = gap.category
                    if cat not in category_counts:
                        category_counts[cat] = 0
                    category_counts[cat] += 1

                for cat, count in sorted(category_counts.items()):
                    print(f"    - {cat}: {count}")

            except Exception as e:
                print(f"  ERROR: Failed to run analysis - {e}")

        print("\n" + "=" * 60)
        print("GAP ANALYSIS COMPLETE")
        print("=" * 60)

        # Summary
        result = await session.execute(
            select(GapAnalysis, State)
            .join(State)
            .where(State.abbreviation.in_(TARGET_STATES))
            .order_by(GapAnalysis.total_effort_hours)
        )
        analyses = result.all()

        print("\n  SUMMARY (sorted by effort):")
        print("-" * 60)
        for analysis, state in analyses:
            print(f"  {state.abbreviation}: {analysis.total_effort_hours:,} hours "
                  f"({analysis.projected_months} months) - "
                  f"{analysis.total_gaps} gaps ({analysis.critical_gaps} critical)")

        # Recommendation
        if analyses:
            lowest_effort = analyses[0]
            print("\n  RECOMMENDATION:")
            print(f"  {lowest_effort[1].name} ({lowest_effort[1].abbreviation}) has the "
                  f"lowest effort estimate at {lowest_effort[0].total_effort_hours:,} hours")


async def get_gap_analysis_summary():
    """Get a summary of all gap analyses."""
    engine = get_engine()
    SessionLocal = get_session_maker(engine)

    async with SessionLocal() as session:
        result = await session.execute(
            select(GapAnalysis, State)
            .join(State)
            .order_by(GapAnalysis.total_effort_hours)
        )
        analyses = result.all()

        print("\nGAP ANALYSIS SUMMARY")
        print("=" * 80)
        print(f"{'State':<20} {'Baseline':<10} {'Gaps':<8} {'Critical':<10} "
              f"{'Effort (h)':<12} {'Months':<8}")
        print("-" * 80)

        for analysis, state in analyses:
            print(f"{state.name:<20} {analysis.baseline_state:<10} "
                  f"{analysis.total_gaps:<8} {analysis.critical_gaps:<10} "
                  f"{analysis.total_effort_hours:<12,} {analysis.projected_months:<8}")

        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(seed_gap_analysis())
