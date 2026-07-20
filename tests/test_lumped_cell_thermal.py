from __future__ import annotations

import contextlib
import csv
import io
import math
import tempfile
import unittest
from pathlib import Path

from models.lumped_cell_thermal import (
    LumpedThermalSpec,
    load_current_profile,
    main,
    simulate_lumped_temperature,
    write_simulation_csv,
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
            current_a * current_a * spec.resistance_ohm / spec.heat_transfer_w_per_k
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

    def test_loads_uniform_csv_current_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.csv"
            path.write_text(
                "time_s,current_a\n0,0\n60,75\n120,-50\n",
                encoding="utf-8",
            )
            profile = load_current_profile(path)
        self.assertEqual(profile.time_s, (0.0, 60.0, 120.0))
        self.assertEqual(profile.current_a, (0.0, 75.0, -50.0))
        self.assertIsNone(profile.ambient_temperature_c)
        self.assertEqual(profile.time_step_s, 60.0)

    def test_loads_profile_with_interval_ambient_temperature(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.csv"
            path.write_text(
                "time_s,current_a,ambient_temperature_c\n"
                "0,0,25\n60,75,30\n120,-50,35\n",
                encoding="utf-8",
            )
            profile = load_current_profile(path)
        self.assertEqual(profile.current_a, (0.0, 75.0, -50.0))
        self.assertEqual(profile.ambient_temperature_c, (25.0, 30.0, 35.0))

    def test_interval_ambient_changes_heat_rejection_and_temperature(self):
        constant = simulate_lumped_temperature([0.0, 0.0])
        warming = simulate_lumped_temperature(
            [0.0, 0.0],
            ambient_temperatures_c=[35.0, 35.0],
        )
        self.assertEqual(constant.temperature_c[-1], 25.0)
        self.assertGreater(warming.temperature_c[-1], 25.0)
        self.assertTrue(all(value < 0.0 for value in warming.heat_rejection_w))
        self.assertLess(warming.energy_balance_error_j, 1e-8)

    def test_rejects_invalid_ambient_profile(self):
        with self.assertRaisesRegex(ValueError, "one value per current interval"):
            simulate_lumped_temperature([10.0, 20.0], ambient_temperatures_c=[25.0])
        with self.assertRaisesRegex(ValueError, "temperature values must be finite"):
            simulate_lumped_temperature([10.0], ambient_temperatures_c=[math.nan])

    def test_rejects_invalid_csv_header_and_time_grid(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.csv"
            path.write_text("time,current\n0,0\n1,10\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "header must be exactly"):
                load_current_profile(path)
            path.write_text(
                "time_s,current_a\n0,0\n1,10\n2.5,20\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "uniform time step"):
                load_current_profile(path)

    def test_writes_interval_level_energy_records(self):
        result = simulate_lumped_temperature([50.0, 0.0])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "result.csv"
            write_simulation_csv(path, result)
            with path.open("r", encoding="utf-8", newline="") as output_file:
                rows = list(csv.DictReader(output_file))
        self.assertEqual(len(rows), 2)
        self.assertEqual(float(rows[0]["current_a"]), 50.0)
        self.assertEqual(float(rows[0]["ambient_temperature_c"]), 25.0)
        self.assertAlmostEqual(
            sum(float(row["net_heat_j"]) for row in rows),
            result.integrated_net_heat_j,
        )

    def test_cli_runs_profile_and_exports_results(self):
        with tempfile.TemporaryDirectory() as directory:
            profile_path = Path(directory) / "profile.csv"
            output_path = Path(directory) / "result.csv"
            profile_path.write_text(
                "time_s,current_a\n0,0\n60,75\n120,75\n",
                encoding="utf-8",
            )
            standard_output = io.StringIO()
            with contextlib.redirect_stdout(standard_output):
                exit_code = main(
                    [
                        "--profile-csv",
                        str(profile_path),
                        "--output-csv",
                        str(output_path),
                    ]
                )
            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.is_file())
            self.assertIn("Intervals: 3", standard_output.getvalue())
            self.assertIn("Duration: 180.000 s", standard_output.getvalue())

    def test_cli_uses_profile_ambient_in_export(self):
        with tempfile.TemporaryDirectory() as directory:
            profile_path = Path(directory) / "profile.csv"
            output_path = Path(directory) / "result.csv"
            profile_path.write_text(
                "time_s,current_a,ambient_temperature_c\n0,0,25\n1,0,35\n",
                encoding="utf-8",
            )
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(
                    main(
                        [
                            "--profile-csv",
                            str(profile_path),
                            "--output-csv",
                            str(output_path),
                        ]
                    ),
                    0,
                )
            with output_path.open("r", encoding="utf-8", newline="") as output_file:
                rows = list(csv.DictReader(output_file))
        self.assertEqual(float(rows[1]["ambient_temperature_c"]), 35.0)
        self.assertEqual(float(rows[1]["heat_rejection_w"]), -12.0)

    def test_profile_mode_rejects_constant_current_options(self):
        with tempfile.TemporaryDirectory() as directory:
            profile_path = Path(directory) / "profile.csv"
            profile_path.write_text(
                "time_s,current_a\n0,0\n1,10\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "cannot be combined"):
                main(["--profile-csv", str(profile_path), "--current-a", "50"])

    def test_profile_ambient_rejects_constant_ambient_override(self):
        with tempfile.TemporaryDirectory() as directory:
            profile_path = Path(directory) / "profile.csv"
            profile_path.write_text(
                "time_s,current_a,ambient_temperature_c\n0,0,25\n1,10,30\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "cannot be combined"):
                main(
                    [
                        "--profile-csv",
                        str(profile_path),
                        "--ambient-temperature-c",
                        "20",
                    ]
                )


if __name__ == "__main__":
    unittest.main()
