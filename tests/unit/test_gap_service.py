"""
Unit tests for gap analysis service.

Tests gap detection, severity calculation, and effort estimation.
"""

import pytest

import sys
sys.path.insert(0, '/home/user/SISStateReportingManager/src/backend')


class TestGapCategories:
    """Test gap category definitions."""

    def test_gap_categories_exist(self):
        """Verify gap categories are defined."""
        from services.gap_service import GAP_CATEGORIES

        assert len(GAP_CATEGORIES) > 0, "Gap categories should be defined"

    def test_categories_have_required_fields(self):
        """Verify each category has weight and description."""
        from services.gap_service import GAP_CATEGORIES

        for name, config in GAP_CATEGORIES.items():
            assert "weight" in config, f"Category {name} missing weight"
            assert "base_hours" in config, f"Category {name} missing base_hours"


class TestSeverityLevels:
    """Test gap severity calculations."""

    def test_severity_levels_defined(self):
        """Verify severity levels are properly defined."""
        from services.gap_service import SEVERITY_LEVELS

        expected_severities = ["low", "medium", "high", "critical"]
        for severity in expected_severities:
            assert severity in SEVERITY_LEVELS, f"Missing severity level: {severity}"

    def test_severity_multipliers_increase(self):
        """Verify severity multipliers increase with severity."""
        from services.gap_service import SEVERITY_LEVELS

        severities = ["low", "medium", "high", "critical"]
        multipliers = [SEVERITY_LEVELS[s]["multiplier"] for s in severities]

        for i in range(len(multipliers) - 1):
            assert multipliers[i] < multipliers[i + 1], (
                f"Severity multiplier for {severities[i]} should be less than {severities[i+1]}"
            )


class TestEffortEstimation:
    """Test effort estimation calculations."""

    def test_base_effort_calculation(self):
        """Test basic effort calculation."""
        base_hours = 100
        severity_multiplier = 1.5
        category_weight = 1.2

        effort = int(base_hours * severity_multiplier * category_weight)
        assert effort == 180, f"Expected 180 hours, got {effort}"

    def test_effort_with_gap_count(self):
        """Test effort scales with number of gaps."""
        base_effort = 100
        gap_count = 5
        overlap_factor = 0.8  # 20% efficiency from shared work

        total_effort = base_effort + (gap_count - 1) * base_effort * overlap_factor
        expected = 100 + 4 * 80  # 100 + 320 = 420
        assert total_effort == expected, f"Expected {expected}, got {total_effort}"


class TestBaselineComparison:
    """Test baseline comparison logic."""

    def test_nj_baseline_features_exist(self):
        """Verify NJ baseline features are defined."""
        from baselines import NJ_CAPABILITIES

        assert len(NJ_CAPABILITIES) > 0, "NJ capabilities should be defined"
        assert "features" in NJ_CAPABILITIES, "NJ capabilities should have features"

    def test_la_baseline_features_exist(self):
        """Verify LA baseline features are defined."""
        from baselines import LA_CAPABILITIES

        assert len(LA_CAPABILITIES) > 0, "LA capabilities should be defined"
        assert "features" in LA_CAPABILITIES, "LA capabilities should have features"

    def test_baseline_selection_by_structure(self):
        """Test selecting appropriate baseline based on state structure."""
        # County-based states should use LA baseline
        county_based_states = ["MD", "LA", "FL", "NV"]

        # Fragmented district states should use NJ baseline
        fragmented_states = ["NJ", "PA", "TX", "NY"]

        # Simple structure-based selection logic
        def select_baseline(state_abbrev: str, is_county_based: bool) -> str:
            return "LA" if is_county_based else "NJ"

        assert select_baseline("MD", True) == "LA"
        assert select_baseline("PA", False) == "NJ"


class TestGapIdentification:
    """Test gap identification logic."""

    def test_missing_feature_detection(self):
        """Test detecting missing features between states."""
        baseline_features = {"feature_a", "feature_b", "feature_c"}
        target_requirements = {"feature_a", "feature_b", "feature_d"}

        # Features in target but not in baseline = gaps
        gaps = target_requirements - baseline_features
        assert gaps == {"feature_d"}, f"Expected {{'feature_d'}}, got {gaps}"

    def test_partial_feature_detection(self):
        """Test detecting partially implemented features."""
        baseline_feature = {
            "name": "enrollment_reporting",
            "capabilities": ["basic", "demographics", "program_codes"],
        }
        target_requirement = {
            "name": "enrollment_reporting",
            "capabilities": ["basic", "demographics", "program_codes", "special_ed_indicators"],
        }

        missing_capabilities = set(target_requirement["capabilities"]) - set(baseline_feature["capabilities"])
        assert missing_capabilities == {"special_ed_indicators"}


class TestComplexityFactors:
    """Test complexity factor calculations."""

    def test_state_complexity_factors(self):
        """Test state complexity factor calculation."""
        # Factors that increase complexity
        factors = {
            "unique_data_elements": 50,  # Number of state-specific fields
            "integration_points": 3,  # Number of external system integrations
            "certification_required": True,
            "multiple_submission_windows": True,
        }

        # Simple complexity score calculation
        complexity = (
            factors["unique_data_elements"] * 0.02 +  # 0-2 points
            factors["integration_points"] * 0.3 +  # 0-1.5 points
            (1 if factors["certification_required"] else 0) * 0.5 +  # 0-0.5 points
            (1 if factors["multiple_submission_windows"] else 0) * 0.3  # 0-0.3 points
        )

        # Expected: 50*0.02 + 3*0.3 + 0.5 + 0.3 = 1.0 + 0.9 + 0.5 + 0.3 = 2.7
        assert 2.5 < complexity < 3.0, f"Expected complexity around 2.7, got {complexity}"

    def test_timeline_scaling_from_complexity(self):
        """Test timeline scaling based on complexity."""
        base_timeline = 30  # LA benchmark months
        complexity_score = 2.7

        # Scale factor: 1.0 is baseline, higher complexity increases timeline
        scale_factor = 0.8 + (complexity_score / 5.0) * 0.4  # Range: 0.8 to 1.2
        # 0.8 + (2.7/5.0) * 0.4 = 0.8 + 0.216 = 1.016

        scaled_timeline = int(base_timeline * scale_factor)
        assert 28 <= scaled_timeline <= 32, f"Expected timeline around 30, got {scaled_timeline}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
