"""
Claude API service for AI-powered state analysis.

Provides async methods for analyzing state reporting complexity,
development effort estimation, and technical fit scoring.
"""

import asyncio
import logging
from typing import Optional
from datetime import datetime, timedelta

import anthropic
from anthropic import AsyncAnthropic

from ..config import settings

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter for API calls."""

    def __init__(self, max_calls: int = 10, period_seconds: int = 60):
        self.max_calls = max_calls
        self.period_seconds = period_seconds
        self.calls: list[datetime] = []

    async def acquire(self):
        """Wait if necessary to stay within rate limits."""
        now = datetime.now()
        # Remove old calls outside the window
        self.calls = [
            t for t in self.calls
            if now - t < timedelta(seconds=self.period_seconds)
        ]

        if len(self.calls) >= self.max_calls:
            # Wait until oldest call expires
            oldest = self.calls[0]
            wait_time = (oldest + timedelta(seconds=self.period_seconds) - now).total_seconds()
            if wait_time > 0:
                logger.info(f"Rate limit reached, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
                # Recursively check again
                await self.acquire()
                return

        self.calls.append(now)


class ClaudeService:
    """
    Service for interacting with Claude API for state analysis.

    Provides methods for:
    - Analyzing state reporting complexity
    - Estimating development effort
    - Evaluating technical fit with existing capabilities
    - Researching competitive landscape
    """

    def __init__(self):
        self.client: Optional[AsyncAnthropic] = None
        self.rate_limiter = RateLimiter(max_calls=10, period_seconds=60)
        self._cache: dict[str, tuple[str, datetime]] = {}
        self._cache_ttl = timedelta(hours=24)

    def _get_client(self) -> AsyncAnthropic:
        """Get or create the Anthropic client."""
        if self.client is None:
            if not settings.claude_api_key:
                raise ValueError("CLAUDE_API_KEY not configured")
            self.client = AsyncAnthropic(api_key=settings.claude_api_key)
        return self.client

    def _get_cached(self, cache_key: str) -> Optional[str]:
        """Get cached response if still valid."""
        if cache_key in self._cache:
            response, timestamp = self._cache[cache_key]
            if datetime.now() - timestamp < self._cache_ttl:
                logger.debug(f"Cache hit for {cache_key}")
                return response
            else:
                del self._cache[cache_key]
        return None

    def _set_cached(self, cache_key: str, response: str):
        """Cache a response."""
        self._cache[cache_key] = (response, datetime.now())

    async def _call_claude(
        self,
        prompt: str,
        system_prompt: str,
        cache_key: Optional[str] = None,
        max_tokens: int = 1024,
    ) -> str:
        """
        Make a call to Claude API with rate limiting and caching.

        Args:
            prompt: The user prompt
            system_prompt: System instructions
            cache_key: Optional key for caching response
            max_tokens: Maximum tokens in response

        Returns:
            Claude's response text
        """
        # Check cache first
        if cache_key:
            cached = self._get_cached(cache_key)
            if cached:
                return cached

        # Apply rate limiting
        await self.rate_limiter.acquire()

        try:
            client = self._get_client()
            response = await client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )

            result = response.content[0].text

            # Cache the response
            if cache_key:
                self._set_cached(cache_key, result)

            return result

        except anthropic.APIError as e:
            logger.error(f"Claude API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling Claude: {e}")
            raise

    async def analyze_state_complexity(
        self,
        state_name: str,
        doe_website: str,
    ) -> dict:
        """
        Analyze the complexity of a state's reporting requirements.

        Returns a dict with:
        - complexity_score: 1-10 (10 = most complex)
        - analysis: Text explanation
        - key_factors: List of complexity factors
        """
        system_prompt = """You are an expert in K-12 state education reporting requirements.
        Analyze state Department of Education reporting complexity and provide structured assessments.
        Be concise and data-driven in your analysis."""

        prompt = f"""Analyze the reporting requirements complexity for {state_name}.
        DOE Website: {doe_website}

        Based on your knowledge of this state's K-12 reporting requirements, assess:
        1. Number and complexity of required data submissions
        2. Submission format requirements (XML, CSV, APIs, proprietary)
        3. Validation rule complexity
        4. Reporting calendar frequency
        5. Historical requirement changes (stability)

        Respond in this exact format:
        COMPLEXITY_SCORE: [1-10, where 10 is most complex]
        KEY_FACTORS:
        - [factor 1]
        - [factor 2]
        - [factor 3]
        ANALYSIS: [2-3 sentence summary]"""

        cache_key = f"complexity_{state_name}"

        try:
            response = await self._call_claude(prompt, system_prompt, cache_key)
            return self._parse_complexity_response(response)
        except Exception as e:
            logger.error(f"Failed to analyze complexity for {state_name}: {e}")
            return {
                "complexity_score": 5,
                "analysis": "Analysis unavailable",
                "key_factors": [],
                "error": str(e),
            }

    def _parse_complexity_response(self, response: str) -> dict:
        """Parse the structured complexity response."""
        result = {
            "complexity_score": 5,
            "analysis": "",
            "key_factors": [],
        }

        lines = response.strip().split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if line.startswith("COMPLEXITY_SCORE:"):
                try:
                    score = int(line.split(":")[1].strip().split()[0])
                    result["complexity_score"] = max(1, min(10, score))
                except (ValueError, IndexError):
                    pass
            elif line.startswith("KEY_FACTORS:"):
                current_section = "factors"
            elif line.startswith("ANALYSIS:"):
                current_section = "analysis"
                analysis_text = line.replace("ANALYSIS:", "").strip()
                if analysis_text:
                    result["analysis"] = analysis_text
            elif line.startswith("- ") and current_section == "factors":
                result["key_factors"].append(line[2:])
            elif current_section == "analysis" and line:
                result["analysis"] += " " + line

        return result

    async def estimate_development_effort(
        self,
        state_name: str,
        doe_website: str,
        baseline_states: list[str],
    ) -> dict:
        """
        Estimate development effort to support a new state.

        Args:
            state_name: Target state
            doe_website: State DOE website
            baseline_states: List of currently supported states (e.g., ["NJ", "LA"])

        Returns dict with:
        - effort_score: 1-10 (10 = lowest effort / easiest)
        - estimated_months: Rough timeline estimate
        - analysis: Text explanation
        """
        system_prompt = """You are an expert in SIS (Student Information System) development.
        You help assess development effort for supporting new state reporting requirements.
        Consider existing capabilities and reuse potential."""

        prompt = f"""Estimate the development effort to add state reporting support for {state_name}.
        DOE Website: {doe_website}
        Currently Supported States: {', '.join(baseline_states)}

        Consider:
        1. Similarity to existing supported states
        2. Data format requirements
        3. Integration complexity
        4. Validation rule implementation
        5. Testing and certification needs

        Respond in this exact format:
        EFFORT_SCORE: [1-10, where 10 means LOWEST effort / easiest to implement]
        ESTIMATED_MONTHS: [number]
        REUSE_POTENTIAL: [HIGH/MEDIUM/LOW]
        ANALYSIS: [2-3 sentence summary]"""

        cache_key = f"effort_{state_name}"

        try:
            response = await self._call_claude(prompt, system_prompt, cache_key)
            return self._parse_effort_response(response)
        except Exception as e:
            logger.error(f"Failed to estimate effort for {state_name}: {e}")
            return {
                "effort_score": 5,
                "estimated_months": 12,
                "reuse_potential": "MEDIUM",
                "analysis": "Analysis unavailable",
                "error": str(e),
            }

    def _parse_effort_response(self, response: str) -> dict:
        """Parse the structured effort response."""
        result = {
            "effort_score": 5,
            "estimated_months": 12,
            "reuse_potential": "MEDIUM",
            "analysis": "",
        }

        lines = response.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("EFFORT_SCORE:"):
                try:
                    score = int(line.split(":")[1].strip().split()[0])
                    result["effort_score"] = max(1, min(10, score))
                except (ValueError, IndexError):
                    pass
            elif line.startswith("ESTIMATED_MONTHS:"):
                try:
                    months = int(line.split(":")[1].strip().split()[0])
                    result["estimated_months"] = months
                except (ValueError, IndexError):
                    pass
            elif line.startswith("REUSE_POTENTIAL:"):
                potential = line.split(":")[1].strip().upper()
                if potential in ["HIGH", "MEDIUM", "LOW"]:
                    result["reuse_potential"] = potential
            elif line.startswith("ANALYSIS:"):
                result["analysis"] = line.replace("ANALYSIS:", "").strip()

        return result

    async def evaluate_technical_fit(
        self,
        state_name: str,
        doe_website: str,
        nj_capabilities: dict,
        la_capabilities: dict,
    ) -> dict:
        """
        Evaluate how well existing NJ/LA capabilities match a target state.

        Returns dict with:
        - fit_score: 1-10 (10 = best fit)
        - nj_similarity: Percentage similarity to NJ
        - la_similarity: Percentage similarity to LA
        - analysis: Text explanation
        """
        system_prompt = """You are an expert in K-12 state reporting requirements.
        Compare state requirements and assess technical compatibility."""

        # Summarize capabilities for prompt
        nj_summary = ", ".join(nj_capabilities.get("key_features", [])[:5])
        la_summary = ", ".join(la_capabilities.get("key_features", [])[:5])

        prompt = f"""Evaluate how well existing SIS capabilities would fit {state_name}'s requirements.
        DOE Website: {doe_website}

        Current NJ Capabilities: {nj_summary}
        Current LA Capabilities: {la_summary}

        Assess:
        1. Data element overlap with NJ requirements
        2. Data element overlap with LA requirements
        3. Submission format compatibility
        4. Process workflow similarity

        Respond in this exact format:
        FIT_SCORE: [1-10, where 10 means best technical fit]
        NJ_SIMILARITY: [percentage, e.g., 75%]
        LA_SIMILARITY: [percentage, e.g., 60%]
        ANALYSIS: [2-3 sentence summary]"""

        cache_key = f"fit_{state_name}"

        try:
            response = await self._call_claude(prompt, system_prompt, cache_key)
            return self._parse_fit_response(response)
        except Exception as e:
            logger.error(f"Failed to evaluate fit for {state_name}: {e}")
            return {
                "fit_score": 5,
                "nj_similarity": 50,
                "la_similarity": 50,
                "analysis": "Analysis unavailable",
                "error": str(e),
            }

    def _parse_fit_response(self, response: str) -> dict:
        """Parse the structured fit response."""
        result = {
            "fit_score": 5,
            "nj_similarity": 50,
            "la_similarity": 50,
            "analysis": "",
        }

        lines = response.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("FIT_SCORE:"):
                try:
                    score = int(line.split(":")[1].strip().split()[0])
                    result["fit_score"] = max(1, min(10, score))
                except (ValueError, IndexError):
                    pass
            elif line.startswith("NJ_SIMILARITY:"):
                try:
                    pct = line.split(":")[1].strip().replace("%", "").split()[0]
                    result["nj_similarity"] = int(pct)
                except (ValueError, IndexError):
                    pass
            elif line.startswith("LA_SIMILARITY:"):
                try:
                    pct = line.split(":")[1].strip().replace("%", "").split()[0]
                    result["la_similarity"] = int(pct)
                except (ValueError, IndexError):
                    pass
            elif line.startswith("ANALYSIS:"):
                result["analysis"] = line.replace("ANALYSIS:", "").strip()

        return result

    async def analyze_competitive_landscape(
        self,
        state_name: str,
    ) -> dict:
        """
        Analyze the SIS competitive landscape in a state.

        Returns dict with:
        - competition_score: 1-10 (10 = least competition)
        - major_competitors: List of major SIS vendors in state
        - market_saturation: HIGH/MEDIUM/LOW
        - analysis: Text explanation
        """
        system_prompt = """You are an expert in the K-12 education technology market.
        Analyze SIS (Student Information System) vendor competition in US states."""

        prompt = f"""Analyze the SIS competitive landscape in {state_name}.

        Identify:
        1. Major SIS vendors with significant presence
        2. Any statewide contracts or preferred vendors
        3. Market saturation level
        4. Opportunities for new entrants

        Consider vendors like: PowerSchool, Infinite Campus, Tyler Technologies,
        Skyward, Aeries, Synergy, Eschool Solutions, and regional vendors.

        Respond in this exact format:
        COMPETITION_SCORE: [1-10, where 10 means LEAST competition / best opportunity]
        MARKET_SATURATION: [HIGH/MEDIUM/LOW]
        MAJOR_COMPETITORS:
        - [competitor 1]
        - [competitor 2]
        ANALYSIS: [2-3 sentence summary]"""

        cache_key = f"competition_{state_name}"

        try:
            response = await self._call_claude(prompt, system_prompt, cache_key)
            return self._parse_competition_response(response)
        except Exception as e:
            logger.error(f"Failed to analyze competition for {state_name}: {e}")
            return {
                "competition_score": 5,
                "market_saturation": "MEDIUM",
                "major_competitors": [],
                "analysis": "Analysis unavailable",
                "error": str(e),
            }

    def _parse_competition_response(self, response: str) -> dict:
        """Parse the structured competition response."""
        result = {
            "competition_score": 5,
            "market_saturation": "MEDIUM",
            "major_competitors": [],
            "analysis": "",
        }

        lines = response.strip().split("\n")
        current_section = None

        for line in lines:
            line = line.strip()
            if line.startswith("COMPETITION_SCORE:"):
                try:
                    score = int(line.split(":")[1].strip().split()[0])
                    result["competition_score"] = max(1, min(10, score))
                except (ValueError, IndexError):
                    pass
            elif line.startswith("MARKET_SATURATION:"):
                saturation = line.split(":")[1].strip().upper()
                if saturation in ["HIGH", "MEDIUM", "LOW"]:
                    result["market_saturation"] = saturation
            elif line.startswith("MAJOR_COMPETITORS:"):
                current_section = "competitors"
            elif line.startswith("ANALYSIS:"):
                current_section = "analysis"
                result["analysis"] = line.replace("ANALYSIS:", "").strip()
            elif line.startswith("- ") and current_section == "competitors":
                result["major_competitors"].append(line[2:])

        return result


# Singleton instance
claude_service = ClaudeService()
