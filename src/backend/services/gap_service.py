"""
Gap analysis service for comparing target states against NJ/LA baselines.

Identifies capability gaps, estimates effort, and generates analysis reports.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import State, GapAnalysis, Gap, StateAnalysis
from ..baselines import (
    NJ_CAPABILITIES,
    LA_CAPABILITIES,
    FEATURE_CATEGORIES,
    get_capability_count,
    get_total_effort_hours,
    get_baseline_for_comparison,
    estimate_effort_from_la_benchmark,
)


# Effort multipliers by complexity
COMPLEXITY_MULTIPLIERS = {
    "low": 0.7,
    "medium": 1.0,
    "high": 1.5,
    "very_high": 2.0,
}

# Severity definitions
SEVERITY_THRESHOLDS = {
    "critical": 100,  # > 100 hours = critical
    "major": 50,      # 50-100 hours = major
    "minor": 0,       # < 50 hours = minor
}

# Category priorities for gap identification
CATEGORY_PRIORITIES = {
    "enrollment": 1,
    "attendance": 2,
    "grades": 3,
    "special_ed": 4,
    "assessments": 5,
    "staff": 6,
    "discipline": 7,
    "ell": 8,
    "cte": 9,
    "early_childhood": 10,
    "reporting": 1,  # Critical
    "integration": 2,  # Critical
    "certification": 1,  # Critical
}


class GapService:
    """Service for performing gap analysis between states and baselines."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_state_by_id(self, state_id: int) -> Optional[State]:
        """Get a state by ID."""
        result = await self.session.execute(
            select(State).where(State.id == state_id)
        )
        return result.scalar_one_or_none()

    async def get_state_by_abbrev(self, abbrev: str) -> Optional[State]:
        """Get a state by abbreviation."""
        result = await self.session.execute(
            select(State).where(State.abbreviation == abbrev.upper())
        )
        return result.scalar_one_or_none()

    async def get_state_analysis(self, state_id: int) -> Optional[StateAnalysis]:
        """Get existing state analysis if available."""
        result = await self.session.execute(
            select(StateAnalysis).where(StateAnalysis.state_id == state_id)
        )
        return result.scalar_one_or_none()

    async def get_existing_gap_analysis(self, state_id: int) -> Optional[GapAnalysis]:
        """Get existing gap analysis for a state."""
        result = await self.session.execute(
            select(GapAnalysis).where(GapAnalysis.state_id == state_id)
        )
        return result.scalar_one_or_none()

    def select_baseline(self, state: State) -> tuple[str, dict]:
        """
        Select the most appropriate baseline for comparison.

        LA baseline is preferred for county-based states (similar to parish model).
        NJ baseline is used for fragmented district models.
        """
        # Get state analysis if available for more context
        abbrev = state.abbreviation.upper()

        # States with county-based or consolidated district models
        # should use LA as baseline (similar to parish model)
        county_based_states = [
            "MD",  # 24 county LEAs
            "WV",  # County-based
            "NV",  # County-based
            "FL",  # County-based (67)
            "NC",  # County/city LEAs
            "VA",  # County/city divisions
            "DE",  # Small state, fewer districts
            "HI",  # Single statewide district
            "UT",  # Larger districts
        ]

        if abbrev in county_based_states:
            return "LA", LA_CAPABILITIES

        # Default to NJ baseline for fragmented district models
        return "NJ", NJ_CAPABILITIES

    def calculate_gap_severity(self, effort_hours: int) -> str:
        """Determine gap severity based on effort hours."""
        if effort_hours >= SEVERITY_THRESHOLDS["critical"]:
            return "critical"
        elif effort_hours >= SEVERITY_THRESHOLDS["major"]:
            return "major"
        return "minor"

    def estimate_gap_effort(
        self,
        base_hours: int,
        complexity: str,
        is_new: bool = True
    ) -> int:
        """
        Estimate effort hours for a gap.

        Args:
            base_hours: Base effort from baseline capability
            complexity: Complexity level (low, medium, high, very_high)
            is_new: Whether this is a new capability vs modification
        """
        multiplier = COMPLEXITY_MULTIPLIERS.get(complexity, 1.0)

        # New capabilities require full effort
        # Modifications may only need 60% of effort
        if not is_new:
            multiplier *= 0.6

        return int(base_hours * multiplier)

    def generate_state_specific_gaps(
        self,
        state_abbrev: str,
        baseline: dict
    ) -> list[dict]:
        """
        Generate state-specific gaps based on known requirements.

        This method contains hardcoded knowledge about specific state
        reporting systems (PIMS, PEIMS, MSDE, etc.)
        """
        gaps = []

        if state_abbrev == "PA":
            # Pennsylvania - PIMS (Pennsylvania Information Management System)
            gaps.extend([
                {
                    "code": "PA-PIMS-001",
                    "name": "PIMS File Format Adaptation",
                    "description": "Adapt data export to PIMS template format requirements",
                    "category": "reporting",
                    "complexity": "high",
                    "effort_hours": 150,
                },
                {
                    "code": "PA-PIMS-002",
                    "name": "PA Student Calendar Template",
                    "description": "Implement PA-specific student calendar template for PIMS",
                    "category": "enrollment",
                    "complexity": "medium",
                    "effort_hours": 80,
                },
                {
                    "code": "PA-PIMS-003",
                    "name": "PA Safe Schools Reporting",
                    "description": "Safe Schools Act reporting and incident categorization",
                    "category": "discipline",
                    "complexity": "high",
                    "effort_hours": 120,
                },
                {
                    "code": "PA-PIMS-004",
                    "name": "PA Keystone Exams",
                    "description": "Keystone end-of-course exam tracking and proficiency",
                    "category": "assessments",
                    "complexity": "high",
                    "effort_hours": 100,
                },
                {
                    "code": "PA-PIMS-005",
                    "name": "PA Act 158 Pathways",
                    "description": "Act 158 graduation pathway tracking",
                    "category": "grades",
                    "complexity": "high",
                    "effort_hours": 90,
                },
                {
                    "code": "PA-PIMS-006",
                    "name": "PA Title I Participation",
                    "description": "Title I program participation tracking",
                    "category": "enrollment",
                    "complexity": "medium",
                    "effort_hours": 60,
                },
                {
                    "code": "PA-PIMS-007",
                    "name": "PA PreID Labels",
                    "description": "Pre-ID label generation for state assessments",
                    "category": "assessments",
                    "complexity": "medium",
                    "effort_hours": 70,
                },
                {
                    "code": "PA-PIMS-008",
                    "name": "AUN Codes",
                    "description": "Administrative Unit Number (AUN) code mapping",
                    "category": "integration",
                    "complexity": "medium",
                    "effort_hours": 50,
                },
            ])

        elif state_abbrev == "TX":
            # Texas - PEIMS (Public Education Information Management System)
            gaps.extend([
                {
                    "code": "TX-PEIMS-001",
                    "name": "PEIMS XML Format",
                    "description": "PEIMS complex XML submission format with TEA schema",
                    "category": "reporting",
                    "complexity": "very_high",
                    "effort_hours": 250,
                },
                {
                    "code": "TX-PEIMS-002",
                    "name": "TSDS Integration",
                    "description": "Texas Student Data System (TSDS) portal integration",
                    "category": "integration",
                    "complexity": "very_high",
                    "effort_hours": 200,
                },
                {
                    "code": "TX-PEIMS-003",
                    "name": "TX Foundation Program",
                    "description": "Foundation High School Program and endorsement tracking",
                    "category": "grades",
                    "complexity": "high",
                    "effort_hours": 120,
                },
                {
                    "code": "TX-PEIMS-004",
                    "name": "TX STAAR Integration",
                    "description": "State of Texas Assessments of Academic Readiness data",
                    "category": "assessments",
                    "complexity": "high",
                    "effort_hours": 150,
                },
                {
                    "code": "TX-PEIMS-005",
                    "name": "TX UIL Eligibility",
                    "description": "UIL athletic eligibility tracking",
                    "category": "grades",
                    "complexity": "medium",
                    "effort_hours": 60,
                },
                {
                    "code": "TX-PEIMS-006",
                    "name": "TX Bilingual/ESL",
                    "description": "Texas bilingual and ESL program codes",
                    "category": "ell",
                    "complexity": "high",
                    "effort_hours": 100,
                },
                {
                    "code": "TX-PEIMS-007",
                    "name": "TX School Safety",
                    "description": "Texas school safety data collection",
                    "category": "discipline",
                    "complexity": "high",
                    "effort_hours": 110,
                },
                {
                    "code": "TX-PEIMS-008",
                    "name": "TX Special Ed Coding",
                    "description": "PEIMS special education service coding",
                    "category": "special_ed",
                    "complexity": "high",
                    "effort_hours": 130,
                },
                {
                    "code": "TX-PEIMS-009",
                    "name": "TX District Demographics",
                    "description": "Over 1,000 districts - massive demographic scope",
                    "category": "enrollment",
                    "complexity": "very_high",
                    "effort_hours": 180,
                },
                {
                    "code": "TX-PEIMS-010",
                    "name": "TEA Certification",
                    "description": "TEA vendor certification process",
                    "category": "certification",
                    "complexity": "very_high",
                    "effort_hours": 300,
                },
            ])

        elif state_abbrev == "MD":
            # Maryland - MSDE (Maryland State Department of Education)
            gaps.extend([
                {
                    "code": "MD-MSDE-001",
                    "name": "MSDE File Format",
                    "description": "MSDE data collection file format adaptation",
                    "category": "reporting",
                    "complexity": "high",
                    "effort_hours": 140,
                },
                {
                    "code": "MD-MSDE-002",
                    "name": "MD Bridge Plan",
                    "description": "Bridge Plan for Academic Validation tracking",
                    "category": "grades",
                    "complexity": "medium",
                    "effort_hours": 70,
                },
                {
                    "code": "MD-MSDE-003",
                    "name": "MD MCAP Assessments",
                    "description": "Maryland Comprehensive Assessment Program integration",
                    "category": "assessments",
                    "complexity": "high",
                    "effort_hours": 100,
                },
                {
                    "code": "MD-MSDE-004",
                    "name": "MD CTE Programs",
                    "description": "Maryland CTE program and pathway tracking",
                    "category": "cte",
                    "complexity": "medium",
                    "effort_hours": 80,
                },
                {
                    "code": "MD-MSDE-005",
                    "name": "MD Service Learning",
                    "description": "Service learning hours graduation requirement",
                    "category": "grades",
                    "complexity": "low",
                    "effort_hours": 40,
                },
                {
                    "code": "MD-MSDE-006",
                    "name": "MD County Codes",
                    "description": "24 LEA county code mapping",
                    "category": "integration",
                    "complexity": "low",
                    "effort_hours": 30,
                },
            ])

        return gaps

    def identify_baseline_gaps(
        self,
        target_abbrev: str,
        baseline: dict
    ) -> list[dict]:
        """
        Identify gaps between target state and baseline capabilities.

        Returns a list of gap dictionaries.
        """
        gaps = []
        gap_number = 1

        # Get state-specific gaps first
        state_specific = self.generate_state_specific_gaps(target_abbrev, baseline)
        gaps.extend(state_specific)

        # For each category, identify if target state might need modifications
        for category, capabilities in baseline.get("capabilities", {}).items():
            for cap in capabilities:
                # Most states will need adaptation of core capabilities
                # This is a simplified model - real analysis would need AI
                if category in ["reporting", "integration", "certification"]:
                    # Critical categories always need new development
                    gap_code = f"{target_abbrev}-GAP-{gap_number:03d}"
                    gaps.append({
                        "code": gap_code,
                        "name": f"{cap['name']} Adaptation",
                        "description": f"Adapt {cap['name']} for {target_abbrev} requirements",
                        "category": category,
                        "complexity": cap.get("complexity", "medium"),
                        "effort_hours": self.estimate_gap_effort(
                            cap.get("effort_hours", 50),
                            cap.get("complexity", "medium"),
                            is_new=False  # Adaptation, not new
                        ),
                        "baseline_feature": cap["name"],
                    })
                    gap_number += 1

        return gaps

    async def run_gap_analysis(
        self,
        state_id: int,
        force_baseline: Optional[str] = None
    ) -> GapAnalysis:
        """
        Run gap analysis for a state.

        Args:
            state_id: ID of the target state
            force_baseline: Optional baseline to force (NJ or LA)

        Returns:
            GapAnalysis object with results
        """
        state = await self.get_state_by_id(state_id)
        if not state:
            raise ValueError(f"State not found: {state_id}")

        # Check for existing analysis
        existing = await self.get_existing_gap_analysis(state_id)
        if existing:
            # Delete existing gaps and analysis
            for gap in existing.gaps:
                await self.session.delete(gap)
            await self.session.delete(existing)
            await self.session.flush()

        # Select baseline
        if force_baseline:
            baseline_abbrev = force_baseline.upper()
            baseline = NJ_CAPABILITIES if baseline_abbrev == "NJ" else LA_CAPABILITIES
        else:
            baseline_abbrev, baseline = self.select_baseline(state)

        # Identify gaps
        gaps = self.identify_baseline_gaps(state.abbreviation, baseline)
        state_specific = self.generate_state_specific_gaps(state.abbreviation, baseline)

        # Combine and deduplicate gaps
        all_gaps = gaps + state_specific
        seen_codes = set()
        unique_gaps = []
        for gap in all_gaps:
            if gap["code"] not in seen_codes:
                seen_codes.add(gap["code"])
                unique_gaps.append(gap)

        # Calculate totals
        total_effort = sum(g["effort_hours"] for g in unique_gaps)
        critical_count = sum(1 for g in unique_gaps if self.calculate_gap_severity(g["effort_hours"]) == "critical")
        major_count = sum(1 for g in unique_gaps if self.calculate_gap_severity(g["effort_hours"]) == "major")
        minor_count = sum(1 for g in unique_gaps if self.calculate_gap_severity(g["effort_hours"]) == "minor")

        # Calculate timeline based on LA benchmark
        # LA: 15,000 hours over 30 months with 5 FTE
        hours_per_month_per_fte = 160  # Standard work month
        assumed_fte = 5
        projected_months = max(12, int(total_effort / (hours_per_month_per_fte * assumed_fte)) + 6)  # +6 for buffer

        # Split effort into development, testing, certification
        dev_hours = int(total_effort * 0.6)
        testing_hours = int(total_effort * 0.25)
        cert_hours = int(total_effort * 0.15)

        # Create GapAnalysis
        gap_analysis = GapAnalysis(
            state_id=state_id,
            baseline_state=baseline_abbrev,
            analysis_status="completed",
            total_gaps=len(unique_gaps),
            critical_gaps=critical_count,
            major_gaps=major_count,
            minor_gaps=minor_count,
            total_effort_hours=total_effort,
            development_hours=dev_hours,
            testing_hours=testing_hours,
            certification_hours=cert_hours,
            projected_months=projected_months,
            executive_summary=self.generate_executive_summary(
                state, baseline_abbrev, unique_gaps, total_effort, projected_months
            ),
            recommendation=self.generate_recommendation(
                state, baseline_abbrev, total_effort, projected_months
            ),
            risk_assessment=self.generate_risk_assessment(
                state, unique_gaps, critical_count
            ),
        )

        self.session.add(gap_analysis)
        await self.session.flush()

        # Create Gap records
        for gap_data in unique_gaps:
            gap = Gap(
                gap_analysis_id=gap_analysis.id,
                gap_code=gap_data["code"],
                name=gap_data["name"],
                description=gap_data.get("description"),
                category=gap_data["category"],
                severity=self.calculate_gap_severity(gap_data["effort_hours"]),
                effort_hours=gap_data["effort_hours"],
                complexity=gap_data.get("complexity", "medium"),
                baseline_feature=gap_data.get("baseline_feature"),
                required_changes=gap_data.get("required_changes"),
                dependencies=gap_data.get("dependencies"),
                status="identified",
            )
            self.session.add(gap)

        await self.session.commit()
        return gap_analysis

    def generate_executive_summary(
        self,
        state: State,
        baseline: str,
        gaps: list[dict],
        total_effort: int,
        projected_months: int
    ) -> str:
        """Generate executive summary for gap analysis."""
        la_benchmark = LA_CAPABILITIES["expansion_metrics"]
        effort_ratio = total_effort / la_benchmark["total_development_hours"]

        return f"""Gap Analysis Summary for {state.name} ({state.abbreviation})

Baseline Used: {baseline} ({"Louisiana" if baseline == "LA" else "New Jersey"})

Total Gaps Identified: {len(gaps)}
- Critical: {sum(1 for g in gaps if self.calculate_gap_severity(g['effort_hours']) == 'critical')}
- Major: {sum(1 for g in gaps if self.calculate_gap_severity(g['effort_hours']) == 'major')}
- Minor: {sum(1 for g in gaps if self.calculate_gap_severity(g['effort_hours']) == 'minor')}

Effort Estimate: {total_effort:,} hours
Projected Timeline: {projected_months} months

Comparison to LA Benchmark:
- LA expansion took {la_benchmark['total_months']} months with {la_benchmark['total_development_hours']:,} hours
- This project represents {effort_ratio:.1%} of LA effort
- Team recommendation: {max(3, int(la_benchmark['team_size_fte'] * effort_ratio))} FTEs"""

    def generate_recommendation(
        self,
        state: State,
        baseline: str,
        total_effort: int,
        projected_months: int
    ) -> str:
        """Generate recommendation based on analysis."""
        if total_effort < 5000:
            priority = "HIGH PRIORITY"
            assessment = "This state represents a relatively low-effort expansion opportunity."
        elif total_effort < 10000:
            priority = "MEDIUM PRIORITY"
            assessment = "This state requires moderate development effort."
        else:
            priority = "LOWER PRIORITY"
            assessment = "This state requires significant development investment."

        return f"""{priority}: {state.name}

{assessment}

Using {baseline} as baseline provides the best starting point for adaptation.

Key Next Steps:
1. Review critical gaps in reporting and integration categories
2. Establish relationship with {state.abbreviation} DOE
3. Conduct detailed requirements gathering session
4. Create phased implementation roadmap

Estimated ROI Timeline: {projected_months + 12}-{projected_months + 24} months to positive ROI"""

    def generate_risk_assessment(
        self,
        state: State,
        gaps: list[dict],
        critical_count: int
    ) -> str:
        """Generate risk assessment for the expansion."""
        risks = []

        if critical_count > 5:
            risks.append("HIGH RISK: Multiple critical gaps require significant development")

        if any(g["category"] == "certification" for g in gaps):
            risks.append("MEDIUM RISK: State certification process required")

        integration_gaps = [g for g in gaps if g["category"] == "integration"]
        if len(integration_gaps) > 2:
            risks.append("MEDIUM RISK: Complex integration requirements")

        if state.abbreviation == "TX":
            risks.append("HIGH RISK: Largest state market - high complexity and competition")

        if not risks:
            risks.append("LOW RISK: Standard expansion complexity")

        return "\n".join(risks)

    async def get_gaps_for_analysis(self, gap_analysis_id: int) -> list[Gap]:
        """Get all gaps for a gap analysis."""
        result = await self.session.execute(
            select(Gap)
            .where(Gap.gap_analysis_id == gap_analysis_id)
            .order_by(Gap.severity, Gap.category)
        )
        return result.scalars().all()

    async def get_gaps_by_category(
        self,
        gap_analysis_id: int,
        category: str
    ) -> list[Gap]:
        """Get gaps filtered by category."""
        result = await self.session.execute(
            select(Gap)
            .where(Gap.gap_analysis_id == gap_analysis_id)
            .where(Gap.category == category)
            .order_by(Gap.severity)
        )
        return result.scalars().all()

    async def get_gaps_by_severity(
        self,
        gap_analysis_id: int,
        severity: str
    ) -> list[Gap]:
        """Get gaps filtered by severity."""
        result = await self.session.execute(
            select(Gap)
            .where(Gap.gap_analysis_id == gap_analysis_id)
            .where(Gap.severity == severity)
            .order_by(Gap.category)
        )
        return result.scalars().all()

    async def update_gap_status(
        self,
        gap_id: int,
        status: str
    ) -> Optional[Gap]:
        """Update the status of a gap."""
        result = await self.session.execute(
            select(Gap).where(Gap.id == gap_id)
        )
        gap = result.scalar_one_or_none()

        if gap:
            gap.status = status
            await self.session.commit()

        return gap
