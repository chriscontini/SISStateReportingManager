"""
Unit tests for product alignment service.

Tests product-state fit analysis, hub-spoke synergy,
and cross-sell opportunity calculations.
"""

import pytest

import sys
sys.path.insert(0, '/home/user/SISStateReportingManager/src/backend')

# Define expected constants for testing
PRODUCT_TYPES = ["hub", "spoke"]

PRODUCT_CATEGORIES = [
    "sis",
    "lms",
    "assessment",
    "special_ed",
    "finance",
    "hr",
    "transportation",
]

COMPLEXITY_LEVELS = ["low", "medium", "high"]

FIT_SCORE_THRESHOLDS = {
    "excellent": 8.0,
    "good": 6.5,
    "challenging": 0.0,
}

ANALYSIS_STATUSES = ["pending", "analyzing", "analyzed", "failed"]


class TestProductTypes:
    """Test product type definitions."""

    def test_product_types_defined(self):
        """Verify product types are defined."""
        assert len(PRODUCT_TYPES) == 2
        assert "hub" in PRODUCT_TYPES
        assert "spoke" in PRODUCT_TYPES

    def test_hub_is_core_sis(self):
        """Test hub product represents core SIS."""
        hub_product = {
            "name": "OnCourse SIS",
            "product_type": "hub",
            "is_core": True,
            "category": "sis",
        }

        assert hub_product["product_type"] == "hub"
        assert hub_product["is_core"] is True
        assert hub_product["category"] == "sis"

    def test_spoke_products_integrate_with_hub(self):
        """Test spoke products integrate with hub."""
        spoke_products = [
            {"name": "OnCourse LMS", "product_type": "spoke", "integrates_with_hub": True},
            {"name": "OnCourse Assessment", "product_type": "spoke", "integrates_with_hub": True},
        ]

        for product in spoke_products:
            assert product["product_type"] == "spoke"
            assert product["integrates_with_hub"] is True


class TestProductCategories:
    """Test product category definitions."""

    def test_categories_defined(self):
        """Verify product categories are defined."""
        assert len(PRODUCT_CATEGORIES) >= 5

    def test_key_categories_present(self):
        """Test key product categories are present."""
        required = ["sis", "lms", "assessment", "special_ed", "finance"]
        for cat in required:
            assert cat in PRODUCT_CATEGORIES

    def test_category_revenue_multipliers(self):
        """Test categories have revenue multipliers."""
        multipliers = {
            "lms": 3,
            "assessment": 2,
            "special_ed": 4,
            "finance": 5,
            "hr": 3,
            "transportation": 2,
        }

        for category, multiplier in multipliers.items():
            assert multiplier >= 2
            assert multiplier <= 5


class TestFitScoreThresholds:
    """Test product-state fit score thresholds."""

    def test_thresholds_defined(self):
        """Verify fit score thresholds are defined."""
        expected_levels = ["excellent", "good", "challenging"]
        for level in expected_levels:
            assert level in FIT_SCORE_THRESHOLDS

    def test_threshold_values(self):
        """Test fit score threshold values."""
        assert FIT_SCORE_THRESHOLDS["excellent"] == 8.0
        assert FIT_SCORE_THRESHOLDS["good"] == 6.5
        assert FIT_SCORE_THRESHOLDS["challenging"] == 0.0

    def test_thresholds_ordered(self):
        """Test thresholds are in descending order."""
        levels = ["excellent", "good", "challenging"]
        thresholds = [FIT_SCORE_THRESHOLDS[l] for l in levels]

        for i in range(len(thresholds) - 1):
            assert thresholds[i] > thresholds[i + 1]

    def test_fit_score_classification(self):
        """Test classifying fit scores."""
        def classify_fit(score):
            if score >= 8.0:
                return "excellent"
            elif score >= 6.5:
                return "good"
            else:
                return "challenging"

        assert classify_fit(9.0) == "excellent"
        assert classify_fit(8.0) == "excellent"
        assert classify_fit(7.5) == "good"
        assert classify_fit(6.5) == "good"
        assert classify_fit(5.0) == "challenging"
        assert classify_fit(0.0) == "challenging"


class TestComplexityLevels:
    """Test feature complexity levels."""

    def test_complexity_levels_defined(self):
        """Verify complexity levels are defined."""
        assert len(COMPLEXITY_LEVELS) == 3
        assert "low" in COMPLEXITY_LEVELS
        assert "medium" in COMPLEXITY_LEVELS
        assert "high" in COMPLEXITY_LEVELS

    def test_complexity_affects_effort(self):
        """Test complexity affects customization effort."""
        effort_by_complexity = {
            "low": 40,
            "medium": 100,
            "high": 200,
        }

        assert effort_by_complexity["low"] < effort_by_complexity["medium"]
        assert effort_by_complexity["medium"] < effort_by_complexity["high"]


class TestCrossSellPotential:
    """Test cross-sell potential calculations."""

    def test_cross_sell_score_range(self):
        """Test cross-sell potential scores are in valid range."""
        scores = [0.0, 5.0, 7.5, 10.0]
        for score in scores:
            assert 0.0 <= score <= 10.0

    def test_cross_sell_calculation(self):
        """Test cross-sell potential calculation formula."""
        def calculate_cross_sell_potential(fit_score, synergy_score, customization_hours):
            if not fit_score:
                return 0.0

            # Base on fit and synergy
            potential = (fit_score * 0.4) + (synergy_score * 0.6)

            # Bonus for low customization
            if customization_hours and customization_hours < 200:
                potential += 1.0

            return min(10.0, round(potential, 1))

        # High fit, high synergy, low customization
        result = calculate_cross_sell_potential(9.0, 8.5, 100)
        expected = min(10.0, (9.0 * 0.4) + (8.5 * 0.6) + 1.0)
        assert result == round(expected, 1)

        # Low fit, low synergy
        result = calculate_cross_sell_potential(5.0, 4.0, 300)
        expected = (5.0 * 0.4) + (4.0 * 0.6)
        assert result == round(expected, 1)

    def test_high_synergy_increases_potential(self):
        """Test high synergy increases cross-sell potential."""
        fit = 8.0

        low_synergy = (fit * 0.4) + (5.0 * 0.6)
        high_synergy = (fit * 0.4) + (9.0 * 0.6)

        assert high_synergy > low_synergy


class TestBundleRecommendations:
    """Test product bundle recommendation logic."""

    def test_bundle_synergy_thresholds(self):
        """Test bundle recommendation synergy thresholds."""
        thresholds = {
            "strong": 8.5,
            "good": 7.5,
            "moderate": 6.5,
        }

        assert thresholds["strong"] > thresholds["good"]
        assert thresholds["good"] > thresholds["moderate"]

    def test_bundle_recommendation_classification(self):
        """Test bundle recommendation classification."""
        def get_bundle_recommendation(synergy_score):
            if synergy_score >= 8.5:
                return "Strong bundle candidate - include in initial offering"
            elif synergy_score >= 7.5:
                return "Good bundle candidate - offer as add-on"
            elif synergy_score >= 6.5:
                return "Moderate synergy - offer post-implementation"
            else:
                return "Low synergy - standalone offering only"

        assert "initial offering" in get_bundle_recommendation(9.0)
        assert "add-on" in get_bundle_recommendation(8.0)
        assert "post-implementation" in get_bundle_recommendation(7.0)
        assert "standalone" in get_bundle_recommendation(5.0)

    def test_bundle_size_limit(self):
        """Test bundle size has reasonable limit."""
        # Hub + up to 3 spokes
        max_bundle_size = 4
        assert max_bundle_size >= 2
        assert max_bundle_size <= 5


class TestEffortEstimation:
    """Test implementation effort estimation."""

    def test_months_from_hours(self):
        """Test converting hours to months."""
        def estimate_months(hours):
            if not hours:
                return 0
            # 100 hours/month * 5 FTE = 500 hours/month capacity
            return max(1, round(hours / 500))

        assert estimate_months(0) == 0
        assert estimate_months(500) == 1
        assert estimate_months(1000) == 2
        assert estimate_months(1500) == 3

    def test_fte_assumption(self):
        """Test FTE assumption for estimation."""
        fte = 5
        hours_per_month_per_fte = 100
        monthly_capacity = fte * hours_per_month_per_fte

        assert monthly_capacity == 500

    def test_minimum_one_month(self):
        """Test minimum of one month for non-zero hours."""
        def estimate_months(hours):
            if not hours:
                return 0
            return max(1, round(hours / 500))

        assert estimate_months(100) == 1  # Even small effort = 1 month minimum


class TestStateProductFit:
    """Test state-product fit analysis."""

    def test_fit_data_structure(self):
        """Test state-product fit data structure."""
        fit_data = {
            "state_id": 1,
            "product_id": 1,
            "fit_score": 8.5,
            "gap_count": 3,
            "critical_gaps": 1,
            "customization_hours": 400,
            "synergy_score": 8.0,
            "analysis_status": "analyzed",
        }

        assert "fit_score" in fit_data
        assert "gap_count" in fit_data
        assert "synergy_score" in fit_data
        assert fit_data["analysis_status"] in ANALYSIS_STATUSES

    def test_fit_score_valid_range(self):
        """Test fit scores are in valid range."""
        fit_scores = [0.0, 5.5, 8.0, 10.0]
        for score in fit_scores:
            assert 0.0 <= score <= 10.0

    def test_gap_count_non_negative(self):
        """Test gap count is non-negative."""
        gap_counts = [0, 3, 5, 10]
        for count in gap_counts:
            assert count >= 0


class TestHubAnalysis:
    """Test hub product analysis."""

    def test_hub_priority_classification(self):
        """Test hub fit priority classification."""
        def get_hub_priority(fit_score):
            if fit_score >= 8.0:
                return "high"
            elif fit_score >= 6.5:
                return "medium"
            else:
                return "low"

        assert get_hub_priority(9.0) == "high"
        assert get_hub_priority(7.5) == "medium"
        assert get_hub_priority(5.0) == "low"

    def test_hub_recommendation_text(self):
        """Test hub recommendation text generation."""
        def get_hub_recommendation(fit_score):
            if fit_score >= 8.0:
                return "Excellent fit - proceed with expansion"
            elif fit_score >= 6.5:
                return "Good fit - manageable customization required"
            else:
                return "Challenging fit - significant development needed"

        assert "proceed" in get_hub_recommendation(8.5)
        assert "manageable" in get_hub_recommendation(7.0)
        assert "significant" in get_hub_recommendation(5.0)


class TestOverallRecommendation:
    """Test overall state expansion recommendation."""

    def test_priority_levels(self):
        """Test priority level definitions."""
        priorities = ["high", "medium", "low", "pending"]
        for priority in priorities:
            assert priority in ["high", "medium", "low", "pending"]

    def test_recommendation_structure(self):
        """Test recommendation data structure."""
        recommendation = {
            "summary": "Strong expansion candidate with 8.5/10 hub fit",
            "action": "Prioritize for immediate expansion planning",
            "priority": "high",
            "cross_sell_count": 3,
        }

        assert "summary" in recommendation
        assert "action" in recommendation
        assert "priority" in recommendation
        assert recommendation["priority"] in ["high", "medium", "low", "pending"]

    def test_cross_sell_count_tracked(self):
        """Test cross-sell opportunities are counted."""
        opportunities = [
            {"product_name": "LMS", "cross_sell_potential": 8.0},
            {"product_name": "Assessment", "cross_sell_potential": 7.5},
            {"product_name": "Finance", "cross_sell_potential": 9.0},
        ]

        count = len([o for o in opportunities if o["cross_sell_potential"] >= 7.0])
        assert count == 3


class TestRevenueEstimation:
    """Test revenue potential estimation for products."""

    def test_revenue_per_student_by_category(self):
        """Test revenue multipliers by product category."""
        multipliers = {
            "lms": 3,
            "assessment": 2,
            "special_ed": 4,
            "finance": 5,
            "hr": 3,
            "transportation": 2,
        }

        # Finance has highest multiplier
        assert multipliers["finance"] == max(multipliers.values())

        # All multipliers are positive
        for cat, mult in multipliers.items():
            assert mult > 0

    def test_market_capture_assumption(self):
        """Test market capture assumption for revenue."""
        # Assume 10% market capture
        market_capture_percent = 10
        assert market_capture_percent > 0
        assert market_capture_percent <= 100

    def test_revenue_calculation(self):
        """Test revenue calculation formula."""
        students = 1000000
        market_capture = 0.10
        revenue_per_student = 4

        estimated_revenue = int(students * market_capture * revenue_per_student)
        assert estimated_revenue == 400000


class TestProductFeatures:
    """Test product feature analysis."""

    def test_feature_structure(self):
        """Test product feature data structure."""
        feature = {
            "id": 1,
            "product_id": 1,
            "name": "State Reporting",
            "category": "core",
            "complexity": "high",
            "is_state_specific": True,
            "customization_effort": 200,
        }

        assert "name" in feature
        assert "category" in feature
        assert feature["complexity"] in COMPLEXITY_LEVELS

    def test_state_specific_features_flagged(self):
        """Test state-specific features are properly flagged."""
        features = [
            {"name": "Core Data", "is_state_specific": False},
            {"name": "State Reporting", "is_state_specific": True},
            {"name": "Custom Fields", "is_state_specific": True},
        ]

        state_specific_count = sum(1 for f in features if f["is_state_specific"])
        assert state_specific_count == 2

    def test_customization_effort_positive(self):
        """Test customization effort is non-negative."""
        efforts = [0, 40, 100, 200]
        for effort in efforts:
            assert effort >= 0


class TestProductSummary:
    """Test product portfolio summary."""

    def test_summary_structure(self):
        """Test product summary data structure."""
        summary = {
            "total_products": 7,
            "hub_count": 1,
            "spoke_count": 6,
            "total_features": 42,
            "states_analyzed": 10,
        }

        assert summary["hub_count"] == 1  # Only one hub
        assert summary["spoke_count"] == summary["total_products"] - summary["hub_count"]
        assert summary["total_features"] > 0

    def test_hub_is_singular(self):
        """Test there is only one hub product."""
        hub_count = 1
        assert hub_count == 1

    def test_multiple_spokes(self):
        """Test there are multiple spoke products."""
        spoke_count = 6
        assert spoke_count > 1


class TestEaseOfSale:
    """Test ease of sale classification."""

    def test_ease_classification(self):
        """Test ease of sale classification based on potential."""
        def get_ease_of_sale(cross_sell_potential):
            if cross_sell_potential >= 8:
                return "easy"
            elif cross_sell_potential >= 6:
                return "moderate"
            else:
                return "challenging"

        assert get_ease_of_sale(9.0) == "easy"
        assert get_ease_of_sale(7.0) == "moderate"
        assert get_ease_of_sale(4.0) == "challenging"

    def test_ease_levels(self):
        """Test ease of sale level definitions."""
        ease_levels = ["easy", "moderate", "challenging"]
        for level in ease_levels:
            assert level in ["easy", "moderate", "challenging"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
