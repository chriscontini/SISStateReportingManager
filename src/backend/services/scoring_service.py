"""
Scoring service for state ranking calculations.

Implements all ranking factors:
1. Development Effort (weight 3.0) - PRIMARY
2. District Structure (weight 2.5)
3. Average District Size (weight 2.5)
4. Technical Fit (weight 2.0)
5. Certification Complexity (weight 1.5)
6. Competitive Landscape (weight 1.5)
7. Market Opportunity (weight 1.5)
8. Regulatory Complexity (weight 1.0)
9. Geographic Proximity (weight 0.5)
"""

import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import State, StateScore, RankingFactor, NCESData
from ..nces_data import NCES_DATA
from .claude_service import claude_service

logger = logging.getLogger(__name__)


# Geographic coordinates for proximity calculation (approximate state centers)
STATE_COORDINATES = {
    "AL": (32.7, -86.7), "AK": (64.0, -153.0), "AZ": (34.2, -111.6),
    "AR": (34.7, -92.3), "CA": (37.2, -119.4), "CO": (39.0, -105.5),
    "CT": (41.6, -72.7), "DE": (39.0, -75.5), "FL": (28.6, -82.4),
    "GA": (32.6, -83.4), "HI": (20.8, -156.3), "ID": (44.4, -114.6),
    "IL": (40.0, -89.2), "IN": (39.9, -86.3), "IA": (42.0, -93.5),
    "KS": (38.5, -98.4), "KY": (37.8, -85.7), "LA": (31.0, -92.0),
    "ME": (45.3, -69.0), "MD": (39.0, -76.7), "MA": (42.2, -71.5),
    "MI": (44.3, -85.4), "MN": (46.3, -94.2), "MS": (32.7, -89.7),
    "MO": (38.4, -92.5), "MT": (47.0, -109.6), "NE": (41.5, -99.8),
    "NV": (39.5, -116.9), "NH": (43.6, -71.5), "NJ": (40.2, -74.7),
    "NM": (34.5, -106.0), "NY": (42.9, -75.5), "NC": (35.5, -79.8),
    "ND": (47.4, -100.3), "OH": (40.4, -82.8), "OK": (35.6, -97.5),
    "OR": (44.0, -120.5), "PA": (40.9, -77.8), "RI": (41.7, -71.5),
    "SC": (33.9, -80.9), "SD": (44.4, -100.2), "TN": (35.8, -86.3),
    "TX": (31.5, -99.3), "UT": (39.3, -111.7), "VT": (44.0, -72.7),
    "VA": (37.5, -78.8), "WA": (47.4, -120.5), "WV": (38.9, -80.5),
    "WI": (44.6, -89.7), "WY": (43.0, -107.6),
}

# NJ coordinates (HQ location)
NJ_COORDS = STATE_COORDINATES["NJ"]


class ScoringService:
    """
    Service for calculating state ranking scores.

    All scores are normalized to 0-10 scale where:
    - Higher score = more favorable for expansion
    """

    def __init__(self):
        self._nces_cache: dict[str, dict] = {}
        self._load_nces_cache()

    def _load_nces_cache(self):
        """Load NCES data into memory cache."""
        for entry in NCES_DATA:
            self._nces_cache[entry["abbreviation"]] = entry

    def _get_nces_data(self, abbreviation: str) -> Optional[dict]:
        """Get NCES data for a state."""
        return self._nces_cache.get(abbreviation)

    async def save_score(
        self,
        db: AsyncSession,
        state_id: int,
        factor_name: str,
        score: float,
        notes: Optional[str] = None,
    ) -> StateScore:
        """
        Save a score for a state and factor.

        Creates or updates the score record.
        """
        # Get the factor by name
        result = await db.execute(
            select(RankingFactor).where(RankingFactor.name == factor_name)
        )
        factor = result.scalar_one_or_none()

        if not factor:
            raise ValueError(f"Unknown ranking factor: {factor_name}")

        # Check for existing score
        result = await db.execute(
            select(StateScore).where(
                StateScore.state_id == state_id,
                StateScore.factor_id == factor.id,
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.score = score
            existing.notes = notes
            existing.calculated_at = datetime.utcnow()
            return existing
        else:
            new_score = StateScore(
                state_id=state_id,
                factor_id=factor.id,
                score=score,
                notes=notes,
            )
            db.add(new_score)
            return new_score

    # =========================================================================
    # SCORING METHODS (each returns 0-10 score)
    # =========================================================================

    def district_structure_score(self, abbreviation: str) -> float:
        """
        Score based on district structure (county-based vs fragmented).

        County-based models (fewer, larger districts) score higher because:
        - Fewer implementations needed
        - Higher ARPU per district
        - Simpler support model

        Score 0-10:
        - 10: < 50 districts (Hawaii, Maryland, Nevada)
        - 7-9: 50-150 districts (Florida, Utah, West Virginia)
        - 5-6: 150-300 districts (most states)
        - 3-4: 300-500 districts
        - 1-2: > 500 districts (Texas, California, New Jersey)
        """
        nces = self._get_nces_data(abbreviation)
        if not nces:
            return 5.0

        districts = nces["total_districts"]

        if districts <= 25:
            return 10.0
        elif districts <= 50:
            return 9.0
        elif districts <= 100:
            return 8.0
        elif districts <= 150:
            return 7.0
        elif districts <= 200:
            return 6.0
        elif districts <= 300:
            return 5.0
        elif districts <= 400:
            return 4.0
        elif districts <= 500:
            return 3.0
        elif districts <= 700:
            return 2.0
        else:
            return 1.0

    def avg_district_size_score(self, abbreviation: str) -> float:
        """
        Score based on average district size (students per district).

        Larger districts = higher ARPU potential.

        Score 0-10:
        - 10: > 30K students/district
        - 8-9: 20-30K students/district
        - 6-7: 10-20K students/district
        - 4-5: 5-10K students/district
        - 2-3: 2-5K students/district
        - 1: < 2K students/district
        """
        nces = self._get_nces_data(abbreviation)
        if not nces:
            return 5.0

        avg_size = nces["total_students"] / nces["total_districts"]

        if avg_size >= 40000:
            return 10.0
        elif avg_size >= 30000:
            return 9.0
        elif avg_size >= 20000:
            return 8.0
        elif avg_size >= 15000:
            return 7.0
        elif avg_size >= 10000:
            return 6.0
        elif avg_size >= 7500:
            return 5.0
        elif avg_size >= 5000:
            return 4.0
        elif avg_size >= 3000:
            return 3.0
        elif avg_size >= 2000:
            return 2.0
        else:
            return 1.0

    def market_opportunity_score(self, abbreviation: str) -> float:
        """
        Score based on total market size (students and districts).

        Larger markets = more revenue potential.

        Score 0-10 based on total students:
        - 10: > 3M students (California, Texas)
        - 8-9: 2-3M students
        - 6-7: 1-2M students
        - 4-5: 500K-1M students
        - 2-3: 200K-500K students
        - 1: < 200K students
        """
        nces = self._get_nces_data(abbreviation)
        if not nces:
            return 5.0

        students = nces["total_students"]

        if students >= 4000000:
            return 10.0
        elif students >= 3000000:
            return 9.0
        elif students >= 2000000:
            return 8.0
        elif students >= 1500000:
            return 7.0
        elif students >= 1000000:
            return 6.0
        elif students >= 750000:
            return 5.0
        elif students >= 500000:
            return 4.0
        elif students >= 300000:
            return 3.0
        elif students >= 150000:
            return 2.0
        else:
            return 1.0

    def geographic_proximity_score(self, abbreviation: str) -> float:
        """
        Score based on distance from NJ (company HQ).

        Closer states = easier support and relationship building.

        Score 0-10:
        - 10: Adjacent to NJ (PA, NY, DE)
        - 8-9: Northeast region
        - 6-7: Mid-Atlantic / Southeast
        - 4-5: Midwest
        - 2-3: South / Mountain
        - 1: West Coast / Alaska / Hawaii
        """
        coords = STATE_COORDINATES.get(abbreviation)
        if not coords:
            return 5.0

        # Calculate distance from NJ
        lat_diff = abs(coords[0] - NJ_COORDS[0])
        lon_diff = abs(coords[1] - NJ_COORDS[1])
        distance = (lat_diff ** 2 + lon_diff ** 2) ** 0.5

        # Convert to score (closer = higher)
        if distance <= 2:  # Adjacent states
            return 10.0
        elif distance <= 5:  # Northeast
            return 8.0
        elif distance <= 8:  # Mid-Atlantic
            return 7.0
        elif distance <= 12:  # Southeast / Great Lakes
            return 6.0
        elif distance <= 18:  # Midwest
            return 5.0
        elif distance <= 25:  # South / Plains
            return 4.0
        elif distance <= 35:  # Mountain
            return 3.0
        elif distance <= 50:  # West Coast
            return 2.0
        else:  # Alaska, Hawaii
            return 1.0

    def certification_complexity_score(self, abbreviation: str) -> float:
        """
        Score based on state vendor certification requirements.

        Open market = higher score (easier entry)
        Formal certification = lower score (barrier to entry)

        Based on known state certification requirements.
        """
        # States with known formal certification requirements
        formal_certification = {
            "TX": 4.0,  # TEA certification process
            "CA": 4.0,  # CDE approval process
            "NY": 5.0,  # NYSED data standards
            "FL": 5.0,  # FLDOE approval
            "GA": 3.0,  # Statewide contract (PowerSchool)
            "NC": 6.0,  # DPI approval
            "VA": 6.0,  # VDOE standards
            "PA": 7.0,  # PDE guidelines
            "OH": 6.0,  # ODE EMIS certification
            "MI": 6.0,  # CEPI certification
            "IL": 6.0,  # ISBE approval
        }

        # States with easier/open market entry
        open_market = {
            "NJ": 8.0,  # Already certified
            "LA": 8.0,  # Already certified
            "MD": 7.0,  # County-based, relationships matter
            "WV": 8.0,  # Smaller state, easier entry
            "DE": 8.0,  # Small state
            "RI": 8.0,  # Small state
            "VT": 8.0,  # Small state
            "NH": 8.0,  # Small state
            "ME": 7.0,  # Regional
        }

        if abbreviation in formal_certification:
            return formal_certification[abbreviation]
        elif abbreviation in open_market:
            return open_market[abbreviation]
        else:
            return 6.0  # Default moderate

    async def development_effort_score(
        self,
        state_name: str,
        abbreviation: str,
        doe_website: str,
    ) -> tuple[float, str]:
        """
        Score based on estimated development effort (AI-powered).

        This is the PRIMARY ranking factor.
        Lower effort = higher score.

        Returns: (score, analysis_notes)
        """
        try:
            result = await claude_service.estimate_development_effort(
                state_name=state_name,
                doe_website=doe_website,
                baseline_states=["NJ", "LA"],
            )
            # Claude returns effort_score where 10 = lowest effort
            return result["effort_score"], result.get("analysis", "")
        except Exception as e:
            logger.error(f"AI development effort scoring failed for {abbreviation}: {e}")
            # Fallback to heuristic based on district structure
            struct_score = self.district_structure_score(abbreviation)
            return struct_score, "Fallback: Based on district structure"

    async def technical_fit_score(
        self,
        state_name: str,
        abbreviation: str,
        doe_website: str,
        nj_capabilities: dict,
        la_capabilities: dict,
    ) -> tuple[float, str]:
        """
        Score based on technical fit with existing NJ/LA capabilities (AI-powered).

        Higher fit = higher score.

        Returns: (score, analysis_notes)
        """
        try:
            result = await claude_service.evaluate_technical_fit(
                state_name=state_name,
                doe_website=doe_website,
                nj_capabilities=nj_capabilities,
                la_capabilities=la_capabilities,
            )
            return result["fit_score"], result.get("analysis", "")
        except Exception as e:
            logger.error(f"AI technical fit scoring failed for {abbreviation}: {e}")
            # Fallback: states geographically close often have similar requirements
            prox_score = self.geographic_proximity_score(abbreviation)
            return prox_score, "Fallback: Based on geographic proximity"

    async def competitive_landscape_score(
        self,
        state_name: str,
        abbreviation: str,
    ) -> tuple[float, str]:
        """
        Score based on competitive landscape (AI-powered).

        Less competition = higher score.

        Returns: (score, analysis_notes)
        """
        try:
            result = await claude_service.analyze_competitive_landscape(
                state_name=state_name,
            )
            competitors = ", ".join(result.get("major_competitors", [])[:3])
            notes = f"{result.get('analysis', '')} Competitors: {competitors}"
            return result["competition_score"], notes
        except Exception as e:
            logger.error(f"AI competitive scoring failed for {abbreviation}: {e}")
            # Fallback: larger states typically have more competition
            market_score = self.market_opportunity_score(abbreviation)
            # Inverse relationship: bigger market = more competition
            competition_score = max(1, 10 - market_score + 3)
            return competition_score, "Fallback: Inverse of market size"

    def regulatory_complexity_score(self, abbreviation: str) -> float:
        """
        Score based on regulatory complexity beyond core reporting.

        Simpler regulatory environment = higher score.

        Considers:
        - Data privacy laws (FERPA + state additions)
        - Special reporting requirements
        - Audit requirements
        """
        # States with additional regulatory complexity
        complex_regulatory = {
            "CA": 3.0,  # CCPA, extensive privacy laws
            "NY": 4.0,  # Additional privacy requirements
            "IL": 4.0,  # BIPA, student privacy act
            "TX": 5.0,  # TPEA, additional requirements
            "CO": 5.0,  # CPA privacy law
            "VA": 5.0,  # VCDPA privacy law
            "CT": 5.0,  # CTDPA privacy law
        }

        # States with simpler regulatory environment
        simpler_regulatory = {
            "NJ": 7.0,  # Known environment
            "LA": 7.0,  # Known environment
            "WV": 8.0,  # Simpler requirements
            "WY": 8.0,  # Minimal additional regulations
            "SD": 8.0,  # Business-friendly
            "ND": 8.0,  # Simpler environment
        }

        if abbreviation in complex_regulatory:
            return complex_regulatory[abbreviation]
        elif abbreviation in simpler_regulatory:
            return simpler_regulatory[abbreviation]
        else:
            return 6.0  # Default moderate

    # =========================================================================
    # MAIN CALCULATION METHOD
    # =========================================================================

    async def calculate_all_scores(
        self,
        db: AsyncSession,
        nj_capabilities: dict,
        la_capabilities: dict,
        use_ai: bool = True,
    ) -> dict:
        """
        Calculate all scores for all states.

        Args:
            db: Database session
            nj_capabilities: NJ capability baseline
            la_capabilities: LA capability baseline
            use_ai: Whether to use AI-powered scoring (slower but more accurate)

        Returns:
            Summary of calculation results
        """
        # Get all states
        result = await db.execute(select(State))
        states = result.scalars().all()

        calculated = 0
        errors = []

        for state in states:
            try:
                await self._calculate_state_scores(
                    db=db,
                    state=state,
                    nj_capabilities=nj_capabilities,
                    la_capabilities=la_capabilities,
                    use_ai=use_ai,
                )
                calculated += 1
            except Exception as e:
                logger.error(f"Error calculating scores for {state.abbreviation}: {e}")
                errors.append({"state": state.abbreviation, "error": str(e)})

        await db.commit()

        return {
            "states_calculated": calculated,
            "errors": errors,
            "ai_enabled": use_ai,
        }

    async def _calculate_state_scores(
        self,
        db: AsyncSession,
        state: State,
        nj_capabilities: dict,
        la_capabilities: dict,
        use_ai: bool,
    ):
        """Calculate all factor scores for a single state."""
        abbr = state.abbreviation
        doe_website = state.doe_website or ""

        # 1. District Structure (non-AI)
        struct_score = self.district_structure_score(abbr)
        await self.save_score(db, state.id, "District Structure", struct_score)

        # 2. Average District Size (non-AI)
        size_score = self.avg_district_size_score(abbr)
        await self.save_score(db, state.id, "Average District Size", size_score)

        # 3. Market Opportunity (non-AI)
        market_score = self.market_opportunity_score(abbr)
        await self.save_score(db, state.id, "Market Opportunity", market_score)

        # 4. Geographic Proximity (non-AI)
        prox_score = self.geographic_proximity_score(abbr)
        await self.save_score(db, state.id, "Geographic Proximity", prox_score)

        # 5. Certification Complexity (non-AI)
        cert_score = self.certification_complexity_score(abbr)
        await self.save_score(db, state.id, "Certification Complexity", cert_score)

        # 6. Regulatory Complexity (non-AI)
        reg_score = self.regulatory_complexity_score(abbr)
        await self.save_score(db, state.id, "Regulatory Complexity", reg_score)

        if use_ai:
            # 7. Development Effort (AI-powered) - PRIMARY
            effort_score, effort_notes = await self.development_effort_score(
                state.name, abbr, doe_website
            )
            await self.save_score(
                db, state.id, "Development Effort", effort_score, effort_notes
            )

            # 8. Technical Fit (AI-powered)
            fit_score, fit_notes = await self.technical_fit_score(
                state.name, abbr, doe_website, nj_capabilities, la_capabilities
            )
            await self.save_score(db, state.id, "Technical Fit", fit_score, fit_notes)

            # 9. Competitive Landscape (AI-powered)
            comp_score, comp_notes = await self.competitive_landscape_score(
                state.name, abbr
            )
            await self.save_score(
                db, state.id, "Competitive Landscape", comp_score, comp_notes
            )
        else:
            # Fallback scores without AI
            await self.save_score(db, state.id, "Development Effort", struct_score)
            await self.save_score(db, state.id, "Technical Fit", prox_score)
            await self.save_score(db, state.id, "Competitive Landscape", 5.0)


# Singleton instance
scoring_service = ScoringService()
