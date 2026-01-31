"""
Roadmap generation service for state expansion planning.

Generates implementation roadmaps based on gap analysis results,
using LA expansion as benchmark.
"""

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import State, GapAnalysis, Roadmap, RoadmapPhase, RoadmapMilestone


# Standard roadmap phases with baseline durations and effort percentages
ROADMAP_PHASES = [
    {
        "number": 1,
        "name": "Discovery & Planning",
        "description": "Requirements gathering, DOE relationship building, and detailed planning",
        "duration_percent": 0.10,
        "effort_percent": 0.05,
        "dependencies": [],
        "deliverables": [
            "Detailed requirements document",
            "DOE contact established",
            "Project charter approved",
            "Resource allocation plan",
        ],
        "milestones": [
            {"name": "Kickoff meeting completed", "month_offset": 0, "type": "checkpoint"},
            {"name": "Requirements gathering complete", "month_offset": 0.8, "type": "deliverable"},
        ],
    },
    {
        "number": 2,
        "name": "Development - Core",
        "description": "Core state reporting module development and data model adaptation",
        "duration_percent": 0.35,
        "effort_percent": 0.40,
        "dependencies": [1],
        "deliverables": [
            "State-specific data models",
            "Core submission file generation",
            "Validation rules implemented",
            "Unit tests passing",
        ],
        "milestones": [
            {"name": "Data model complete", "month_offset": 0.3, "type": "deliverable"},
            {"name": "Core submission working", "month_offset": 0.7, "type": "checkpoint"},
        ],
    },
    {
        "number": 3,
        "name": "Development - Integration",
        "description": "State DOE portal integration and API development",
        "duration_percent": 0.20,
        "effort_percent": 0.25,
        "dependencies": [2],
        "deliverables": [
            "DOE portal integration",
            "File submission automation",
            "Error handling and logging",
            "Integration tests passing",
        ],
        "milestones": [
            {"name": "Portal integration complete", "month_offset": 0.6, "type": "deliverable"},
            {"name": "End-to-end test successful", "month_offset": 0.9, "type": "checkpoint"},
        ],
    },
    {
        "number": 4,
        "name": "Testing & QA",
        "description": "Comprehensive testing, validation, and quality assurance",
        "duration_percent": 0.15,
        "effort_percent": 0.15,
        "dependencies": [3],
        "deliverables": [
            "Test plan executed",
            "All validation rules verified",
            "Performance testing complete",
            "Bug fixes resolved",
        ],
        "milestones": [
            {"name": "QA sign-off", "month_offset": 0.8, "type": "decision"},
        ],
    },
    {
        "number": 5,
        "name": "Certification",
        "description": "State DOE certification process and approval",
        "duration_percent": 0.10,
        "effort_percent": 0.10,
        "dependencies": [4],
        "deliverables": [
            "Certification application submitted",
            "DOE review meetings completed",
            "Certification approval received",
        ],
        "milestones": [
            {"name": "Certification submitted", "month_offset": 0.2, "type": "external"},
            {"name": "Certification approved", "month_offset": 0.9, "type": "external"},
        ],
    },
    {
        "number": 6,
        "name": "Pilot & Rollout",
        "description": "Pilot district deployment and full rollout preparation",
        "duration_percent": 0.10,
        "effort_percent": 0.05,
        "dependencies": [5],
        "deliverables": [
            "Pilot district deployed",
            "Training materials created",
            "Support documentation complete",
            "Go-live checklist verified",
        ],
        "milestones": [
            {"name": "Pilot go-live", "month_offset": 0.3, "type": "checkpoint"},
            {"name": "Full rollout ready", "month_offset": 0.9, "type": "decision"},
        ],
    },
]

# LA Benchmark data
LA_BENCHMARK = {
    "total_months": 30,
    "total_effort_hours": 15000,
    "team_size_fte": 5,
    "hours_per_month_per_fte": 160,
}


class RoadmapService:
    """Service for generating and managing implementation roadmaps."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_state_by_id(self, state_id: int) -> Optional[State]:
        """Get a state by ID."""
        result = await self.session.execute(
            select(State).where(State.id == state_id)
        )
        return result.scalar_one_or_none()

    async def get_gap_analysis(self, state_id: int) -> Optional[GapAnalysis]:
        """Get gap analysis for a state."""
        result = await self.session.execute(
            select(GapAnalysis).where(GapAnalysis.state_id == state_id)
        )
        return result.scalar_one_or_none()

    async def get_existing_roadmap(self, state_id: int) -> Optional[Roadmap]:
        """Get existing roadmap for a state."""
        result = await self.session.execute(
            select(Roadmap).where(Roadmap.state_id == state_id)
        )
        return result.scalar_one_or_none()

    def calculate_phase_durations(
        self,
        total_months: int,
        total_effort_hours: int
    ) -> list[dict]:
        """Calculate duration and effort for each phase."""
        phases = []

        cumulative_months = 0
        for phase_def in ROADMAP_PHASES:
            duration = max(1, int(total_months * phase_def["duration_percent"]))
            effort = int(total_effort_hours * phase_def["effort_percent"])

            # Calculate FTE required for this phase
            phase_hours = LA_BENCHMARK["hours_per_month_per_fte"] * duration
            fte_required = max(1.0, round(effort / phase_hours, 1)) if phase_hours > 0 else 1.0

            phases.append({
                "number": phase_def["number"],
                "name": phase_def["name"],
                "description": phase_def["description"],
                "start_month": cumulative_months,
                "duration_months": duration,
                "end_month": cumulative_months + duration,
                "effort_hours": effort,
                "fte_required": fte_required,
                "dependencies": ",".join(str(d) for d in phase_def["dependencies"]),
                "deliverables": "\n".join(f"• {d}" for d in phase_def["deliverables"]),
                "milestones": phase_def["milestones"],
            })

            cumulative_months += duration

        return phases

    def estimate_timeline_from_effort(self, total_effort_hours: int) -> dict:
        """
        Estimate timeline based on effort, using LA benchmark.

        Returns projected months and team size.
        """
        # LA ratio: 15000 hours = 30 months with 5 FTE
        # hours_per_month = 15000 / 30 = 500 hours/month
        la_hours_per_month = LA_BENCHMARK["total_effort_hours"] / LA_BENCHMARK["total_months"]

        # Estimate months assuming similar team capacity
        estimated_months = max(12, int(total_effort_hours / la_hours_per_month) + 3)

        # Estimate team size
        monthly_capacity = LA_BENCHMARK["hours_per_month_per_fte"]
        required_monthly_hours = total_effort_hours / estimated_months
        estimated_fte = max(3, int(required_monthly_hours / monthly_capacity) + 1)

        # Peak FTE (during development phases)
        peak_fte = int(estimated_fte * 1.5)

        return {
            "total_months": estimated_months,
            "average_fte": estimated_fte,
            "peak_fte": peak_fte,
            "la_comparison_ratio": total_effort_hours / LA_BENCHMARK["total_effort_hours"],
        }

    async def generate_roadmap(
        self,
        state_id: int,
        force_regenerate: bool = False
    ) -> Roadmap:
        """
        Generate an implementation roadmap for a state.

        Uses gap analysis data to estimate effort and timeline.
        """
        state = await self.get_state_by_id(state_id)
        if not state:
            raise ValueError(f"State not found: {state_id}")

        # Check for existing roadmap
        existing = await self.get_existing_roadmap(state_id)
        if existing and not force_regenerate:
            return existing
        elif existing:
            # Delete existing roadmap and related data
            for phase in existing.phases:
                await self.session.delete(phase)
            for milestone in existing.milestones:
                await self.session.delete(milestone)
            await self.session.delete(existing)
            await self.session.flush()

        # Get gap analysis for effort estimates
        gap_analysis = await self.get_gap_analysis(state_id)
        if not gap_analysis:
            raise ValueError(f"No gap analysis found for state {state_id}. Run gap analysis first.")

        # Calculate timeline from effort
        timeline = self.estimate_timeline_from_effort(gap_analysis.total_effort_hours)

        # Calculate start and end dates
        start_date = datetime.now()
        end_date = start_date + timedelta(days=timeline["total_months"] * 30)

        # Create roadmap
        roadmap = Roadmap(
            state_id=state_id,
            name=f"{state.name} State Expansion Roadmap",
            description=f"Implementation roadmap for {state.name} state reporting system, "
                       f"based on {gap_analysis.baseline_state} baseline.",
            status="draft",
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            total_months=timeline["total_months"],
            total_effort_hours=gap_analysis.total_effort_hours,
            peak_fte=timeline["peak_fte"],
            gap_analysis_id=gap_analysis.id,
            baseline_state=gap_analysis.baseline_state,
        )

        self.session.add(roadmap)
        await self.session.flush()

        # Calculate phase durations
        phases = self.calculate_phase_durations(
            timeline["total_months"],
            gap_analysis.total_effort_hours
        )

        # Create phases and milestones
        for phase_data in phases:
            phase = RoadmapPhase(
                roadmap_id=roadmap.id,
                phase_number=phase_data["number"],
                name=phase_data["name"],
                description=phase_data["description"],
                start_month=phase_data["start_month"],
                duration_months=phase_data["duration_months"],
                end_month=phase_data["end_month"],
                effort_hours=phase_data["effort_hours"],
                fte_required=phase_data["fte_required"],
                dependencies=phase_data["dependencies"],
                deliverables=phase_data["deliverables"],
                status="pending",
            )
            self.session.add(phase)
            await self.session.flush()

            # Create milestones for this phase
            for milestone_def in phase_data["milestones"]:
                target_month = phase_data["start_month"] + int(
                    phase_data["duration_months"] * milestone_def["month_offset"]
                )
                target_date = start_date + timedelta(days=target_month * 30)

                milestone = RoadmapMilestone(
                    roadmap_id=roadmap.id,
                    name=milestone_def["name"],
                    milestone_type=milestone_def["type"],
                    target_month=target_month,
                    target_date=target_date.strftime("%Y-%m-%d"),
                    phase_id=phase.id,
                    status="pending",
                )
                self.session.add(milestone)

        await self.session.commit()
        return roadmap

    async def get_roadmap_with_details(self, state_id: int) -> Optional[dict]:
        """Get roadmap with all phases and milestones."""
        roadmap = await self.get_existing_roadmap(state_id)
        if not roadmap:
            return None

        # Fetch phases
        phases_result = await self.session.execute(
            select(RoadmapPhase)
            .where(RoadmapPhase.roadmap_id == roadmap.id)
            .order_by(RoadmapPhase.phase_number)
        )
        phases = phases_result.scalars().all()

        # Fetch milestones
        milestones_result = await self.session.execute(
            select(RoadmapMilestone)
            .where(RoadmapMilestone.roadmap_id == roadmap.id)
            .order_by(RoadmapMilestone.target_month)
        )
        milestones = milestones_result.scalars().all()

        return {
            "roadmap": roadmap,
            "phases": phases,
            "milestones": milestones,
        }

    async def update_phase_status(
        self,
        phase_id: int,
        status: str,
        progress_percent: int = None
    ) -> Optional[RoadmapPhase]:
        """Update the status of a roadmap phase."""
        result = await self.session.execute(
            select(RoadmapPhase).where(RoadmapPhase.id == phase_id)
        )
        phase = result.scalar_one_or_none()

        if phase:
            phase.status = status
            if progress_percent is not None:
                phase.progress_percent = progress_percent
            await self.session.commit()

        return phase

    async def update_milestone_status(
        self,
        milestone_id: int,
        status: str
    ) -> Optional[RoadmapMilestone]:
        """Update the status of a milestone."""
        result = await self.session.execute(
            select(RoadmapMilestone).where(RoadmapMilestone.id == milestone_id)
        )
        milestone = result.scalar_one_or_none()

        if milestone:
            milestone.status = status
            if status == "completed":
                milestone.completed_date = datetime.now().strftime("%Y-%m-%d")
            await self.session.commit()

        return milestone

    def calculate_roadmap_progress(self, phases: list[RoadmapPhase]) -> dict:
        """Calculate overall roadmap progress from phases."""
        if not phases:
            return {"percent_complete": 0, "phases_completed": 0, "total_phases": 0}

        total_effort = sum(p.effort_hours for p in phases)
        completed_effort = sum(
            p.effort_hours * (p.progress_percent / 100)
            for p in phases
        )

        return {
            "percent_complete": int((completed_effort / total_effort) * 100) if total_effort > 0 else 0,
            "phases_completed": sum(1 for p in phases if p.status == "completed"),
            "total_phases": len(phases),
            "effort_completed": int(completed_effort),
            "effort_remaining": int(total_effort - completed_effort),
        }
