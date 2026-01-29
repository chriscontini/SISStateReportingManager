"""
Tier 2/3 Deep Analysis Service.

Performs comprehensive AI-powered analysis of target states including:
- Reporting system details and requirements
- Competitive intelligence
- Certification process analysis
- Implementation recommendations
"""

import json
from typing import Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import State, StateAnalysis
from services.claude_service import ClaudeService


class AnalysisService:
    """Service for performing deep Tier 2/3 state analysis."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.claude = ClaudeService()

    async def get_state_analysis(self, state_id: int) -> Optional[StateAnalysis]:
        """Get existing analysis for a state."""
        result = await self.db.execute(
            select(StateAnalysis).where(StateAnalysis.state_id == state_id)
        )
        return result.scalar_one_or_none()

    async def analyze_state_deep(
        self,
        state_id: int,
        tier: int = 2,
        use_ai: bool = True
    ) -> StateAnalysis:
        """
        Perform deep Tier 2 or Tier 3 analysis on a state.

        Args:
            state_id: ID of state to analyze
            tier: Analysis tier (2 or 3)
            use_ai: Whether to use Claude for AI analysis

        Returns:
            StateAnalysis object with results
        """
        # Get state info
        state = await self.db.get(State, state_id)
        if not state:
            raise ValueError(f"State with id {state_id} not found")

        # Check for existing analysis
        existing = await self.get_state_analysis(state_id)

        if use_ai:
            analysis_data = await self._perform_ai_analysis(state, tier)
        else:
            analysis_data = self._get_default_analysis(state, tier)

        if existing:
            # Update existing analysis
            for key, value in analysis_data.items():
                setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            analysis = existing
        else:
            # Create new analysis
            analysis = StateAnalysis(
                state_id=state_id,
                **analysis_data
            )
            self.db.add(analysis)

        await self.db.commit()
        await self.db.refresh(analysis)
        return analysis

    async def _perform_ai_analysis(self, state: State, tier: int) -> dict:
        """Perform AI-powered deep analysis using Claude."""

        # Analyze reporting system
        reporting_prompt = f"""Analyze the state reporting requirements for {state.name} ({state.abbreviation}).

Provide detailed information about:
1. The name and structure of the state's student information reporting system
2. Main data submission portals and formats
3. Key reporting windows and deadlines
4. Major data elements required (attendance, enrollment, demographics, etc.)

Focus on K-12 public school reporting requirements. Be specific and factual."""

        reporting_result = await self.claude.analyze_state_complexity(
            state.name,
            state.doe_website or ""
        )

        # Analyze competitive landscape
        competitive_prompt = f"""Analyze the SIS (Student Information System) competitive landscape in {state.name}.

Identify:
1. Major SIS vendors currently serving {state.name} schools
2. Approximate market share for each major vendor
3. Key competitive advantages and disadvantages
4. Entry barriers for new vendors

Focus on vendors serving K-12 public schools."""

        competitive_result = await self.claude.analyze_competitive_landscape(state.name)

        # Analyze certification requirements
        certification_info = await self._analyze_certification(state)

        return {
            "analysis_tier": tier,
            "reporting_system_details": reporting_result.get("details", ""),
            "submission_requirements": reporting_result.get("submission_info", ""),
            "data_elements_summary": reporting_result.get("data_elements", ""),
            "major_competitors": competitive_result.get("competitors", ""),
            "competitor_market_share": competitive_result.get("market_share", ""),
            "competitive_advantages": competitive_result.get("advantages", ""),
            "certification_process": certification_info.get("process", ""),
            "compliance_requirements": certification_info.get("compliance", ""),
            "estimated_certification_time": certification_info.get("timeline", ""),
            "key_challenges": await self._identify_challenges(state),
            "recommended_approach": await self._get_recommendations(state),
            "estimated_development_months": self._estimate_development_time(state, tier),
            "ai_model_used": "claude-3-sonnet",
            "analysis_confidence": 0.75,
        }

    def _get_default_analysis(self, state: State, tier: int) -> dict:
        """Get default analysis data without AI."""
        return {
            "analysis_tier": tier,
            "reporting_system_details": f"State reporting system for {state.name}. Manual research required.",
            "submission_requirements": "Research state DOE website for submission requirements.",
            "data_elements_summary": "Standard K-12 data elements (enrollment, attendance, demographics).",
            "major_competitors": "PowerSchool, Infinite Campus, Tyler Technologies (typical national competitors)",
            "competitor_market_share": "Market share data requires research.",
            "competitive_advantages": "To be determined based on market research.",
            "certification_process": "Check state DOE for vendor certification requirements.",
            "compliance_requirements": "FERPA compliance required. State-specific requirements TBD.",
            "estimated_certification_time": "6-12 months typical",
            "key_challenges": "Integration complexity, state-specific requirements, competitive landscape.",
            "recommended_approach": "Phased implementation starting with core reporting modules.",
            "estimated_development_months": 18 if tier == 2 else 24,
            "ai_model_used": None,
            "analysis_confidence": 0.5,
        }

    async def _analyze_certification(self, state: State) -> dict:
        """Analyze certification requirements for a state."""
        # Known certification requirements by state
        certification_data = {
            "PA": {
                "process": "Pennsylvania requires SIS vendors to be approved through PDE vendor certification process.",
                "compliance": "Must comply with PIMS data collection standards and FERPA requirements.",
                "timeline": "6-9 months"
            },
            "TX": {
                "process": "Texas requires PEIMS certification through TEA. Vendors must pass PEIMS data validation tests.",
                "compliance": "Must comply with TSDS (Texas Student Data System) standards and TEA requirements.",
                "timeline": "9-12 months"
            },
            "MD": {
                "process": "Maryland vendor approval through MSDE. Less formal certification process.",
                "compliance": "Must comply with Maryland student data privacy laws and MSDE reporting standards.",
                "timeline": "3-6 months"
            },
            "NJ": {
                "process": "New Jersey has open market - no formal vendor certification required.",
                "compliance": "Must comply with NJ SMART reporting standards and state privacy laws.",
                "timeline": "N/A - open market"
            },
            "LA": {
                "process": "Louisiana vendor approval through LDOE. Parish-level procurement.",
                "compliance": "Must comply with Louisiana student data privacy laws and SIS reporting requirements.",
                "timeline": "3-6 months"
            },
        }

        if state.abbreviation in certification_data:
            return certification_data[state.abbreviation]

        return {
            "process": f"Certification requirements for {state.name} require research.",
            "compliance": "Standard FERPA compliance required. State-specific requirements TBD.",
            "timeline": "6-12 months (estimated)"
        }

    async def _identify_challenges(self, state: State) -> str:
        """Identify key implementation challenges for a state."""
        challenges = []

        # Known state-specific challenges
        state_challenges = {
            "PA": ["Complex PIMS reporting requirements", "Large number of districts (500+)", "Established PowerSchool presence"],
            "TX": ["Very large market with complex PEIMS requirements", "TEA certification is rigorous", "Strong existing vendor relationships"],
            "MD": ["County-based model requires LEA-level relationships", "MSDE reporting complexity", "Montgomery County is major single customer"],
            "NJ": ["Highly fragmented (600+ districts)", "Established OnCourse presence (use as model)", "Competitive market"],
            "LA": ["Parish-based model (64 parishes)", "Established OnCourse presence", "Hurricane-prone region requires resilience"],
        }

        if state.abbreviation in state_challenges:
            challenges = state_challenges[state.abbreviation]
        else:
            challenges = [
                f"State-specific reporting requirements for {state.name}",
                "Competitive landscape analysis needed",
                "Certification and approval process",
            ]

        return "; ".join(challenges)

    async def _get_recommendations(self, state: State) -> str:
        """Get implementation recommendations for a state."""
        recommendations = {
            "PA": "Focus on PIMS compliance first. Target mid-size districts. Leverage NJ experience for similar Northeast requirements.",
            "TX": "Phased approach starting with smaller districts. Build PEIMS expertise. Consider partnership with established TX vendor.",
            "MD": "County-based model aligns well with LA experience. Target 2-3 counties initially. Emphasize 6x ARPU potential like LA.",
            "NJ": "Existing market - focus on retention and upselling additional modules.",
            "LA": "Existing market - use as reference case for other parish/county-based states.",
        }

        if state.abbreviation in recommendations:
            return recommendations[state.abbreviation]

        return f"Phased implementation approach for {state.name}. Start with core reporting modules and expand based on customer feedback."

    def _estimate_development_time(self, state: State, tier: int) -> int:
        """Estimate development time in months."""
        # Base estimates by complexity
        base_months = {
            "PA": 18,
            "TX": 24,
            "MD": 12,
            "NJ": 0,  # Already implemented
            "LA": 0,  # Already implemented
        }

        if state.abbreviation in base_months:
            return base_months[state.abbreviation]

        # Default estimate based on tier
        return 18 if tier == 2 else 24
