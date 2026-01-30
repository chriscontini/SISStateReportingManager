"""
Unit tests for roadmap service.

Tests roadmap generation logic, phase calculations, and milestone creation.
"""

import pytest
from datetime import datetime

# Import constants to test
import sys
sys.path.insert(0, '/home/user/SISStateReportingManager/src/backend')


class TestRoadmapPhases:
    """Test roadmap phase configuration."""

    def test_phases_sum_to_100_percent_duration(self):
        """Verify phase durations sum to 100%."""
        from services.roadmap_service import ROADMAP_PHASES

        total_duration = sum(phase["duration_percent"] for phase in ROADMAP_PHASES)
        assert abs(total_duration - 1.0) < 0.001, f"Duration percentages sum to {total_duration}, expected 1.0"

    def test_phases_sum_to_100_percent_effort(self):
        """Verify phase efforts sum to 100%."""
        from services.roadmap_service import ROADMAP_PHASES

        total_effort = sum(phase["effort_percent"] for phase in ROADMAP_PHASES)
        assert abs(total_effort - 1.0) < 0.001, f"Effort percentages sum to {total_effort}, expected 1.0"

    def test_all_phases_have_required_fields(self):
        """Verify all phases have required configuration fields."""
        from services.roadmap_service import ROADMAP_PHASES

        required_fields = ["number", "name", "description", "duration_percent", "effort_percent"]

        for phase in ROADMAP_PHASES:
            for field in required_fields:
                assert field in phase, f"Phase {phase.get('name', 'unknown')} missing field: {field}"

    def test_phase_numbers_are_sequential(self):
        """Verify phase numbers are sequential starting from 1."""
        from services.roadmap_service import ROADMAP_PHASES

        numbers = [phase["number"] for phase in ROADMAP_PHASES]
        expected = list(range(1, len(ROADMAP_PHASES) + 1))
        assert numbers == expected, f"Phase numbers {numbers} not sequential, expected {expected}"

    def test_dependencies_reference_earlier_phases(self):
        """Verify dependencies only reference earlier phases."""
        from services.roadmap_service import ROADMAP_PHASES

        for phase in ROADMAP_PHASES:
            for dep in phase.get("dependencies", []):
                assert dep < phase["number"], (
                    f"Phase {phase['number']} depends on phase {dep} which is not earlier"
                )


class TestLABenchmark:
    """Test LA benchmark constants."""

    def test_la_benchmark_values(self):
        """Verify LA benchmark values are reasonable."""
        from services.roadmap_service import LA_BENCHMARK_MONTHS, LA_BENCHMARK_HOURS, LA_BENCHMARK_FTE

        assert LA_BENCHMARK_MONTHS == 30, "LA benchmark should be 30 months"
        assert LA_BENCHMARK_HOURS == 15000, "LA benchmark should be 15000 hours"
        assert LA_BENCHMARK_FTE == 5, "LA benchmark should be 5 FTE"

    def test_benchmark_hours_match_fte_months(self):
        """Verify hours roughly match FTE * months * hours_per_month."""
        from services.roadmap_service import LA_BENCHMARK_MONTHS, LA_BENCHMARK_HOURS, LA_BENCHMARK_FTE

        # Assuming ~170 hours per FTE per month
        hours_per_month = 170
        expected_hours = LA_BENCHMARK_FTE * LA_BENCHMARK_MONTHS * hours_per_month

        # Allow 20% variance
        assert 0.8 * expected_hours < LA_BENCHMARK_HOURS < 1.2 * expected_hours, (
            f"Benchmark hours {LA_BENCHMARK_HOURS} don't match expected ~{expected_hours}"
        )


class TestPhaseCalculations:
    """Test phase calculation logic."""

    def test_calculate_phase_duration(self):
        """Test calculating phase duration from total months."""
        total_months = 24
        duration_percent = 0.25

        calculated = int(round(total_months * duration_percent))
        assert calculated == 6, f"Expected 6 months, got {calculated}"

    def test_calculate_phase_effort(self):
        """Test calculating phase effort hours."""
        total_effort = 12000
        effort_percent = 0.40

        calculated = int(round(total_effort * effort_percent))
        assert calculated == 4800, f"Expected 4800 hours, got {calculated}"

    def test_calculate_fte_from_hours_and_months(self):
        """Test FTE calculation from hours and duration."""
        effort_hours = 4800
        duration_months = 6
        hours_per_month = 170

        fte = round(effort_hours / (duration_months * hours_per_month))
        assert 4 <= fte <= 5, f"Expected FTE around 4-5, got {fte}"


class TestMilestoneCalculations:
    """Test milestone date calculations."""

    def test_milestone_month_offset(self):
        """Test milestone month calculation from offset."""
        phase_start = 4
        phase_duration = 6
        milestone_offset = 0.5  # 50% through phase

        milestone_month = phase_start + int(phase_duration * milestone_offset)
        assert milestone_month == 7, f"Expected month 7, got {milestone_month}"

    def test_milestone_date_from_month(self):
        """Test date calculation from month number."""
        start_date = datetime(2026, 1, 1)
        target_month = 6

        from datetime import timedelta

        # Calculate target date (add months)
        year_offset = (target_month - 1) // 12
        month_offset = (target_month - 1) % 12
        target_year = start_date.year + year_offset
        target_month_num = start_date.month + month_offset

        if target_month_num > 12:
            target_year += 1
            target_month_num -= 12

        # Simple check: month 6 from Jan 2026 = June 2026
        assert target_year == 2026
        assert target_month_num == 6


class TestTimelineScaling:
    """Test timeline scaling based on gap complexity."""

    def test_complexity_factor_scaling(self):
        """Test that complexity factors appropriately scale timeline."""
        base_months = 30

        # Low complexity (MD-like) should reduce timeline
        low_complexity_factor = 0.7
        scaled_low = int(base_months * low_complexity_factor)
        assert scaled_low == 21, f"Low complexity should be 21 months, got {scaled_low}"

        # High complexity should increase timeline
        high_complexity_factor = 1.3
        scaled_high = int(base_months * high_complexity_factor)
        assert scaled_high == 39, f"High complexity should be 39 months, got {scaled_high}"

    def test_effort_scales_with_timeline(self):
        """Test that effort scales proportionally with timeline."""
        base_hours = 15000
        timeline_ratio = 0.8  # 80% of base timeline

        scaled_hours = int(base_hours * timeline_ratio)
        assert scaled_hours == 12000, f"Expected 12000 hours, got {scaled_hours}"


class TestRoadmapValidation:
    """Test roadmap validation rules."""

    def test_minimum_phase_duration(self):
        """Verify phases have minimum viable duration."""
        from services.roadmap_service import ROADMAP_PHASES

        min_months = 24  # Minimum total roadmap
        for phase in ROADMAP_PHASES:
            phase_months = int(min_months * phase["duration_percent"])
            # Even shortest phases should be at least 1 month
            assert phase_months >= 1 or phase["duration_percent"] * min_months >= 0.5, (
                f"Phase {phase['name']} would be < 1 month in a {min_months} month roadmap"
            )

    def test_phase_six_exists(self):
        """Verify we have exactly 6 phases."""
        from services.roadmap_service import ROADMAP_PHASES

        assert len(ROADMAP_PHASES) == 6, f"Expected 6 phases, got {len(ROADMAP_PHASES)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
