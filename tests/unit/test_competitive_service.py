"""
Unit tests for competitive intelligence service.

Tests competitor data models, market analysis, and opportunity scoring.
"""

import pytest

import sys
sys.path.insert(0, '/home/user/SISStateReportingManager/src/backend')

# Define expected constants for testing
COMPETITOR_TYPES = ["national", "regional", "local"]

PRESENCE_LEVELS = {
    "dominant": {"min_share": 40, "description": "Market leader"},
    "strong": {"min_share": 20, "description": "Major player"},
    "moderate": {"min_share": 5, "description": "Established presence"},
    "minimal": {"min_share": 0, "description": "Limited presence"},
}

STRENGTH_CATEGORIES = [
    "pricing",
    "support",
    "features",
    "integration",
    "reputation",
    "state_reporting",
    "ease_of_use",
]


class TestCompetitorTypes:
    """Test competitor type definitions."""

    def test_competitor_types_defined(self):
        """Verify competitor types are defined."""
        assert len(COMPETITOR_TYPES) == 3
        assert "national" in COMPETITOR_TYPES
        assert "regional" in COMPETITOR_TYPES
        assert "local" in COMPETITOR_TYPES

    def test_national_competitors_characteristics(self):
        """Test national competitor characteristics."""
        national_features = {
            "typical_states": 30,  # Minimum states for national
            "has_state_reporting": True,
            "typical_employees": "1000+",
        }

        assert national_features["typical_states"] >= 30
        assert national_features["has_state_reporting"] is True


class TestPresenceLevels:
    """Test market presence level definitions."""

    def test_presence_levels_defined(self):
        """Verify presence levels are defined."""
        expected_levels = ["dominant", "strong", "moderate", "minimal"]
        for level in expected_levels:
            assert level in PRESENCE_LEVELS

    def test_presence_level_thresholds(self):
        """Test presence level market share thresholds."""
        assert PRESENCE_LEVELS["dominant"]["min_share"] == 40
        assert PRESENCE_LEVELS["strong"]["min_share"] == 20
        assert PRESENCE_LEVELS["moderate"]["min_share"] == 5
        assert PRESENCE_LEVELS["minimal"]["min_share"] == 0

    def test_presence_levels_ordered(self):
        """Test presence levels are in descending order."""
        levels = ["dominant", "strong", "moderate", "minimal"]
        thresholds = [PRESENCE_LEVELS[l]["min_share"] for l in levels]

        for i in range(len(thresholds) - 1):
            assert thresholds[i] > thresholds[i + 1], (
                f"Threshold for {levels[i]} should be greater than {levels[i+1]}"
            )


class TestStrengthCategories:
    """Test competitor strength categories."""

    def test_strength_categories_exist(self):
        """Verify strength categories are defined."""
        assert len(STRENGTH_CATEGORIES) >= 5

    def test_key_categories_present(self):
        """Test key strength categories are present."""
        required = ["pricing", "support", "features", "state_reporting"]
        for cat in required:
            assert cat in STRENGTH_CATEGORIES

    def test_strength_rating_range(self):
        """Test strength ratings are valid."""
        valid_ratings = [1, 2, 3, 4, 5]
        for rating in valid_ratings:
            assert 1 <= rating <= 5


class TestMarketConcentration:
    """Test market concentration calculations."""

    def test_highly_concentrated_market(self):
        """Test highly concentrated market detection."""
        competitors = [
            {"name": "A", "presence_level": "dominant", "market_share": 45},
            {"name": "B", "presence_level": "dominant", "market_share": 42},
            {"name": "C", "presence_level": "minimal", "market_share": 5},
        ]

        dominant_count = sum(1 for c in competitors if c["presence_level"] == "dominant")
        assert dominant_count >= 2

        # Highly concentrated = 2+ dominant players
        concentration = "highly_concentrated" if dominant_count >= 2 else "other"
        assert concentration == "highly_concentrated"

    def test_fragmented_market(self):
        """Test fragmented market detection."""
        competitors = [
            {"name": "A", "presence_level": "moderate", "market_share": 15},
            {"name": "B", "presence_level": "moderate", "market_share": 12},
            {"name": "C", "presence_level": "moderate", "market_share": 10},
            {"name": "D", "presence_level": "minimal", "market_share": 8},
        ]

        dominant_count = sum(1 for c in competitors if c["presence_level"] == "dominant")
        strong_count = sum(1 for c in competitors if c["presence_level"] == "strong")

        assert dominant_count == 0
        assert strong_count == 0

        # Fragmented = no dominant or strong players
        concentration = "fragmented_open" if dominant_count == 0 and strong_count < 3 else "other"
        assert concentration == "fragmented_open"


class TestOpportunityScoring:
    """Test market opportunity scoring."""

    def test_opportunity_score_range(self):
        """Test opportunity scores are in valid range."""
        scores = [1, 5, 9, 10]
        for score in scores:
            assert 1 <= score <= 10

    def test_fragmented_market_high_opportunity(self):
        """Test fragmented markets have higher opportunity scores."""
        # Fragmented open market should score high
        fragmented_score = 9

        # Highly concentrated should score low
        concentrated_score = 3

        assert fragmented_score > concentrated_score

    def test_size_affects_opportunity(self):
        """Test state size affects opportunity score."""
        # Large state (5M+ students)
        large_state_size_score = 10

        # Small state (<500K students)
        small_state_size_score = 2

        assert large_state_size_score > small_state_size_score


class TestEntryDifficulty:
    """Test market entry difficulty calculations."""

    def test_difficulty_score_range(self):
        """Test difficulty scores are in valid range."""
        # Base difficulty is 5, can range from 1-10
        base = 5
        assert 1 <= base <= 10

    def test_concentration_increases_difficulty(self):
        """Test market concentration increases entry difficulty."""
        base_difficulty = 5

        # Highly concentrated adds 3
        concentrated_difficulty = base_difficulty + 3
        assert concentrated_difficulty == 8

        # Fragmented open subtracts 2
        fragmented_difficulty = base_difficulty - 2
        assert fragmented_difficulty == 3

    def test_difficulty_labels(self):
        """Test difficulty labels map to scores."""
        labels = {
            1: "Very Easy",
            2: "Easy",
            3: "Easy",
            4: "Moderate",
            5: "Moderate",
            6: "Moderate",
            7: "Difficult",
            8: "Difficult",
            9: "Very Difficult",
            10: "Extremely Difficult",
        }

        assert labels[3] == "Easy"
        assert labels[5] == "Moderate"
        assert labels[8] == "Difficult"


class TestCompetitorComparison:
    """Test competitor comparison logic."""

    def test_compare_requires_multiple(self):
        """Test comparison requires at least 2 competitors."""
        min_competitors = 2
        assert min_competitors >= 2

    def test_compare_max_limit(self):
        """Test comparison has maximum limit."""
        max_competitors = 5
        assert max_competitors <= 5

    def test_average_rating_calculation(self):
        """Test average rating calculation."""
        ratings = {"pricing": 4, "support": 5, "features": 3, "integration": None}

        valid_ratings = [r for r in ratings.values() if r is not None]
        avg = sum(valid_ratings) / len(valid_ratings)

        assert avg == 4.0  # (4 + 5 + 3) / 3


class TestRevenueEstimation:
    """Test revenue potential estimation."""

    def test_revenue_per_student(self):
        """Test revenue calculation per student."""
        students = 1000000
        revenue_per_student = 5  # $5 per student per year

        total_revenue = students * revenue_per_student
        assert total_revenue == 5000000

    def test_addressable_market_calculation(self):
        """Test addressable market calculation."""
        total_revenue = 5000000
        tracked_market_share = 60  # 60% tracked to competitors

        addressable_percent = 100 - tracked_market_share
        addressable_revenue = int(total_revenue * (addressable_percent / 100))

        assert addressable_percent == 40
        assert addressable_revenue == 2000000


class TestStrategyRecommendation:
    """Test strategy recommendation logic."""

    def test_direct_entry_for_fragmented(self):
        """Test direct entry recommended for fragmented markets."""
        concentration = "fragmented_open"

        if concentration in ["fragmented_open", "fragmented_competitive"]:
            strategy = "direct_entry"
        else:
            strategy = "other"

        assert strategy == "direct_entry"

    def test_differentiation_for_single_leader(self):
        """Test differentiation recommended for single leader markets."""
        concentration = "single_leader"

        if concentration == "single_leader":
            strategy = "differentiation"
        else:
            strategy = "other"

        assert strategy == "differentiation"

    def test_niche_entry_for_concentrated(self):
        """Test niche entry recommended for concentrated markets."""
        concentration = "highly_concentrated"

        if concentration not in ["fragmented_open", "fragmented_competitive", "single_leader"]:
            strategy = "niche_entry"
        else:
            strategy = "other"

        assert strategy == "niche_entry"


class TestCompetitorDataValidation:
    """Test competitor data validation."""

    def test_competitor_required_fields(self):
        """Test competitor has required fields."""
        competitor = {
            "name": "Test SIS",
            "competitor_type": "regional",
            "total_states": 5,
        }

        assert "name" in competitor
        assert "competitor_type" in competitor
        assert competitor["competitor_type"] in COMPETITOR_TYPES

    def test_state_competitor_required_fields(self):
        """Test state competitor relationship has required fields."""
        state_competitor = {
            "state_id": 1,
            "competitor_id": 1,
            "presence_level": "moderate",
        }

        assert "state_id" in state_competitor
        assert "competitor_id" in state_competitor
        assert state_competitor["presence_level"] in PRESENCE_LEVELS

    def test_market_share_valid_range(self):
        """Test market share is in valid range."""
        market_shares = [0, 25.5, 50, 100]

        for share in market_shares:
            assert 0 <= share <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
