from __future__ import annotations

import math
import unittest

from models.lumped_cell_thermal import (
    LumpedThermalSpec,
    simulate_lumped_temperature,
)


class LumpedCellThermalTests(unittest.TestCase):
    def test_zero_current_stays_at_ambient_equilibrium(self):
        result = simulate_lumped_temperature([0.0] * 120)
        self.assertTrue(all(value == 25.0 for value in result.temperature_c))
        self.assertEqual(result.energy_balance_error_j, 0.0)

    def test_constant_current_matches_discrete_solution(self):
        spec = LumpedThermalSpec()
        intervals = 600
        current_a = 75.0
        result = simulate_lumped_temperature([current_a] * intervals, spec)

        steady_rise_c = (
            current_a * current_a * spec.resistance_ohm
            / spec.heat_transfer_w_per_k
        )
        decay = 1.0 - (
            spec.heat_transfer_w_per_k
            * spec.time_step_s
            / spec.thermal_capacity_j_per_k
        )
        expected_c = spec.ambient_temperature_c + steady_rise_c * (
            1.0 - decay**intervals
        )
        self.assertAlmostEqual(result.temperature_c[-1], expected_c, places=10)
        self.assertGreater(result.temperature_c[-1], spec.ambient_temperature_c)
        self.assertLess(
            result.temperature_c[-1],
            spec.ambient_temperature_c + steady_rise_c,
        )

    def test_discrete_energy_balance_closes(self):
        profile = [80.0] * 300 + [0.0] * 300
        result = simulate_lumped_temperature(profile)
        self.assertLess(result.energy_balance_error_j, 1e-8)
        self.assertGreater(result.temperature_c[300], result.temperature_c[-1])

    def test_smaller_time_step_converges_for_constant_current(self):
        coarse = simulate_lumped_temperature([75.0] * 600)
        fine_spec = LumpedThermalSpec(time_step_s=0.5)
        fine = simulate_lumped_temperature([75.0] * 1200, fine_spec)
        self.assertLess(
            abs(coarse.temperature_c[-1] - fine.temperature_c[-1]),
            0.01,
        )

    def test_rejects_invalid_parameters(self):
        with self.assertRaisesRegex(ValueError, "mass_kg must be positive"):
            simulate_lumped_temperature([10.0], LumpedThermalSpec(mass_kg=0.0))
        with self.assertRaisesRegex(ValueError, "resistance_ohm"):
            simulate_lumped_temperature(
                [10.0],
                LumpedThermalSpec(resistance_ohm=-0.01),
            )

    def test_rejects_empty_or_nonfinite_current_profiles(self):
        with self.assertRaisesRegex(ValueError, "at least one interval"):
            simulate_lumped_temperature([])
        with self.assertRaisesRegex(ValueError, "current values must be finite"):
            simulate_lumped_temperature([math.nan])


if __name__ == "__main__":
    unittest.main()
