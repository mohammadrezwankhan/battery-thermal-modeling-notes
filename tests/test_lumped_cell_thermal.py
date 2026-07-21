from __future__ import annotations

import contextlib
import csv
import io
import math
import tempfile
import unittest
from pathlib import Path

from models.lumped_cell_thermal import (
    IntegrationMethod,
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
        self.assertEqual(result.time_step_s, 1.0)
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

    def test_exact_linear_matches_constant_current_analytic_solution(self):
        spec = LumpedThermalSpec(
            time_step_s=600.0,
            integration_method=IntegrationMethod.EXACT_LINEAR,
        )
        current_a = 75.0
        result = simulate_lumped_temperature([current_a], spec)

        steady_rise_c = (
            current_a * current_a * spec.resistance_ohm / spec.heat_transfer_w_per_k
        )
        expected_c = spec.ambient_temperature_c + steady_rise_c * (
            1.0
            - math.exp(
                -spec.heat_transfer_w_per_k
                * spec.time_step_s
                / spec.thermal_capacity_j_per_k
            )
        )
        self.assertAlmostEqual(result.temperature_c[-1], expected_c, places=12)
        self.assertIs(result.integration_method, IntegrationMethod.EXACT_LINEAR)
        self.assertLess(result.energy_balance_error_j, 1e-9)

    def test_exact_linear_matches_temperature_feedback_solution(self):
        spec = LumpedThermalSpec(
            mass_kg=1.0,
            specific_heat_j_per_kg_k=1000.0,
            resistance_ohm=0.01,
            resistance_temperature_coefficient_per_k=0.02,
            resistance_reference_temperature_c=25.0,
            heat_transfer_w_per_k=0.0,
            initial_temperature_c=25.0,
            time_step_s=100.0,
            integration_method="exact-linear",
        )
        result = simulate_lumped_temperature([100.0], spec)
        expected_rise_c = math.expm1(0.2) / 0.02

        self.assertAlmostEqual(
            result.temperature_c[-1],
            spec.initial_temperature_c + expected_rise_c,
            places=12,
        )
        self.assertGreater(
            result.interval_net_heat_j[0],
            result.heat_generation_w[0] * spec.time_step_s,
        )

    def test_exact_linear_handles_zero_net_feedback_slope(self):
        spec = LumpedThermalSpec(
            mass_kg=1.0,
            specific_heat_j_per_kg_k=1000.0,
            resistance_ohm=0.01,
            resistance_temperature_coefficient_per_k=0.01,
            resistance_reference_temperature_c=25.0,
            heat_transfer_w_per_k=1.0,
            ambient_temperature_c=25.0,
            initial_temperature_c=25.0,
            time_step_s=100.0,
            integration_method=IntegrationMethod.EXACT_LINEAR,
        )
        result = simulate_lumped_temperature([100.0], spec)
        self.assertAlmostEqual(result.temperature_c[-1], 35.0, places=12)
        self.assertAlmostEqual(result.interval_net_heat_j[0], 10_000.0, places=9)

    def test_exact_linear_handles_entropy_cancelling_cooling_slope(self):
        spec = LumpedThermalSpec(
            mass_kg=1.0,
            specific_heat_j_per_kg_k=1000.0,
            resistance_ohm=0.01,
            entropic_coefficient_v_per_k=-0.01,
            heat_transfer_w_per_k=1.0,
            ambient_temperature_c=25.0,
            initial_temperature_c=25.0,
            time_step_s=100.0,
            integration_method=IntegrationMethod.EXACT_LINEAR,
        )
        result = simulate_lumped_temperature([100.0], spec)
        self.assertAlmostEqual(result.temperature_c[-1], 64.815, places=12)
        self.assertAlmostEqual(result.interval_net_heat_j[0], 39_815.0, places=9)

    def test_discrete_energy_balance_closes(self):
        profile = [80.0] * 300 + [0.0] * 300
        result = simulate_lumped_temperature(profile)
        self.assertLess(result.energy_balance_error_j, 1e-8)
        self.assertGreater(result.temperature_c[300], result.temperature_c[-1])

    def test_default_resistance_trace_remains_constant(self):
        result = simulate_lumped_temperature([75.0] * 120)
        self.assertEqual(result.resistance_ohm, (0.004,) * 120)
        self.assertTrue(
            all(
                math.isclose(heat_w, 75.0**2 * 0.004)
                for heat_w in result.heat_generation_w
            )
        )

    def test_default_entropic_term_preserves_irreversible_only_behavior(self):
        result = simulate_lumped_temperature([75.0, -75.0])
        self.assertEqual(result.entropic_coefficient_v_per_k, (0.0, 0.0))
        self.assertEqual(result.reversible_heat_w, (0.0, 0.0))
        self.assertEqual(result.irreversible_heat_w, result.heat_generation_w)

    def test_reversible_heat_changes_sign_with_current_direction(self):
        spec = LumpedThermalSpec(
            entropic_coefficient_v_per_k=0.0001,
            heat_transfer_w_per_k=0.0,
        )
        discharge = simulate_lumped_temperature([100.0], spec)
        charge = simulate_lumped_temperature([-100.0], spec)
        expected_magnitude_w = 100.0 * (25.0 + 273.15) * 0.0001

        self.assertAlmostEqual(
            discharge.reversible_heat_w[0],
            -expected_magnitude_w,
            places=12,
        )
        self.assertAlmostEqual(
            charge.reversible_heat_w[0],
            expected_magnitude_w,
            places=12,
        )
        self.assertEqual(discharge.irreversible_heat_w[0], 40.0)
        self.assertAlmostEqual(
            discharge.heat_generation_w[0],
            40.0 - expected_magnitude_w,
            places=12,
        )
        self.assertLess(discharge.temperature_c[-1], charge.temperature_c[-1])

    def test_exact_linear_matches_combined_thermal_feedback_solution(self):
        spec = LumpedThermalSpec(
            mass_kg=1.0,
            specific_heat_j_per_kg_k=1000.0,
            resistance_ohm=0.01,
            resistance_temperature_coefficient_per_k=0.01,
            entropic_coefficient_v_per_k=0.0002,
            heat_transfer_w_per_k=1.0,
            ambient_temperature_c=20.0,
            initial_temperature_c=30.0,
            time_step_s=600.0,
            integration_method=IntegrationMethod.EXACT_LINEAR,
        )
        current_a = 50.0
        result = simulate_lumped_temperature([current_a], spec)
        feedback_w_per_k = (
            current_a**2
            * spec.resistance_ohm
            * spec.resistance_temperature_coefficient_per_k
            - current_a * spec.entropic_coefficient_v_per_k
            - spec.heat_transfer_w_per_k
        )
        start_net_heat_w = result.heat_generation_w[0] - result.heat_rejection_w[0]
        expected_change_c = (
            start_net_heat_w
            * math.expm1(
                feedback_w_per_k * spec.time_step_s / spec.thermal_capacity_j_per_k
            )
            / feedback_w_per_k
        )
        self.assertAlmostEqual(
            result.temperature_c[-1],
            spec.initial_temperature_c + expected_change_c,
            places=12,
        )
        self.assertLess(result.energy_balance_error_j, 1e-9)

    def test_interval_entropic_coefficients_override_constant_spec_value(self):
        result = simulate_lumped_temperature(
            [80.0, -80.0],
            LumpedThermalSpec(entropic_coefficient_v_per_k=0.5),
            entropic_coefficients_v_per_k=[0.0001, -0.0002],
        )
        self.assertEqual(
            result.entropic_coefficient_v_per_k,
            (0.0001, -0.0002),
        )
        self.assertLess(result.reversible_heat_w[0], 0.0)
        self.assertLess(result.reversible_heat_w[1], 0.0)

    def test_temperature_feedback_matches_closed_form_discrete_solution(self):
        spec = LumpedThermalSpec(
            mass_kg=1.0,
            specific_heat_j_per_kg_k=1000.0,
            resistance_ohm=0.01,
            resistance_temperature_coefficient_per_k=0.02,
            resistance_reference_temperature_c=25.0,
            heat_transfer_w_per_k=0.0,
            ambient_temperature_c=25.0,
            initial_temperature_c=25.0,
            time_step_s=1.0,
        )
        current_a = 100.0
        intervals = 100
        result = simulate_lumped_temperature([current_a] * intervals, spec)
        base_step_c = (
            current_a**2
            * spec.resistance_ohm
            * spec.time_step_s
            / spec.thermal_capacity_j_per_k
        )
        recurrence_factor = (
            1.0 + base_step_c * spec.resistance_temperature_coefficient_per_k
        )
        expected_rise_c = (
            base_step_c
            * (recurrence_factor**intervals - 1.0)
            / (recurrence_factor - 1.0)
        )
        self.assertAlmostEqual(
            result.temperature_c[-1],
            spec.initial_temperature_c + expected_rise_c,
            places=10,
        )
        self.assertEqual(result.resistance_ohm[0], spec.resistance_ohm)
        self.assertGreater(result.resistance_ohm[-1], result.resistance_ohm[0])
        self.assertLess(result.energy_balance_error_j, 1e-8)

    def test_positive_temperature_coefficient_increases_peak_temperature(self):
        constant = simulate_lumped_temperature([100.0] * 600)
        feedback = simulate_lumped_temperature(
            [100.0] * 600,
            LumpedThermalSpec(
                resistance_temperature_coefficient_per_k=0.01,
            ),
        )
        self.assertGreater(feedback.peak_temperature_c, constant.peak_temperature_c)
        self.assertGreater(
            feedback.heat_generation_w[-1],
            constant.heat_generation_w[-1],
        )

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
        with self.assertRaisesRegex(ValueError, "coefficient_per_k must be finite"):
            simulate_lumped_temperature(
                [10.0],
                LumpedThermalSpec(
                    resistance_temperature_coefficient_per_k=math.nan,
                ),
            )
        with self.assertRaisesRegex(ValueError, "must remain nonnegative"):
            simulate_lumped_temperature(
                [10.0],
                LumpedThermalSpec(
                    initial_temperature_c=40.0,
                    resistance_temperature_coefficient_per_k=-0.10,
                ),
            )
        with self.assertRaisesRegex(ValueError, "integration_method must be one of"):
            simulate_lumped_temperature(
                [10.0],
                LumpedThermalSpec(integration_method="runge-kutta"),
            )
        with self.assertRaisesRegex(ValueError, "entropic_coefficient.*finite"):
            simulate_lumped_temperature(
                [10.0],
                LumpedThermalSpec(entropic_coefficient_v_per_k=math.nan),
            )
        with self.assertRaisesRegex(ValueError, "above absolute zero"):
            simulate_lumped_temperature(
                [10.0],
                LumpedThermalSpec(initial_temperature_c=-273.15),
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
        self.assertIsNone(profile.entropic_coefficient_v_per_k)
        self.assertEqual(profile.time_step_s, 60.0)
        self.assertEqual(profile.interval_duration_s, (60.0, 60.0, 60.0))

    def test_loads_explicit_nonuniform_interval_durations(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.csv"
            path.write_text(
                "time_s,current_a,duration_s,ambient_temperature_c\n"
                "0,0,30,25\n"
                "30,75,90,30\n"
                "120,-50,15,35\n",
                encoding="utf-8",
            )
            profile = load_current_profile(path)
        self.assertEqual(profile.time_s, (0.0, 30.0, 120.0))
        self.assertEqual(profile.interval_duration_s, (30.0, 90.0, 15.0))
        self.assertEqual(profile.current_a, (0.0, 75.0, -50.0))
        self.assertEqual(profile.ambient_temperature_c, (25.0, 30.0, 35.0))
        self.assertIsNone(profile.time_step_s)

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

    def test_loads_profile_with_interval_entropic_coefficients(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.csv"
            path.write_text(
                "time_s,current_a,duration_s,ambient_temperature_c,"
                "entropic_coefficient_v_per_k\n"
                "0,0,30,25,0.0001\n"
                "30,75,90,30,-0.0002\n",
                encoding="utf-8",
            )
            profile = load_current_profile(path)
        self.assertEqual(profile.interval_duration_s, (30.0, 90.0))
        self.assertEqual(profile.ambient_temperature_c, (25.0, 30.0))
        self.assertEqual(
            profile.entropic_coefficient_v_per_k,
            (0.0001, -0.0002),
        )

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

    def test_variable_duration_exact_solution_matches_total_elapsed_time(self):
        spec = LumpedThermalSpec(
            integration_method=IntegrationMethod.EXACT_LINEAR,
        )
        variable = simulate_lumped_temperature(
            [75.0, 75.0, 75.0],
            spec,
            interval_durations_s=[10.0, 20.0, 30.0],
        )
        reference = simulate_lumped_temperature(
            [75.0],
            spec,
            interval_durations_s=[60.0],
        )
        self.assertEqual(variable.time_s, (0.0, 10.0, 30.0, 60.0))
        self.assertEqual(variable.interval_duration_s, (10.0, 20.0, 30.0))
        self.assertIsNone(variable.time_step_s)
        self.assertEqual(variable.duration_s, 60.0)
        self.assertAlmostEqual(
            variable.temperature_c[-1],
            reference.temperature_c[-1],
            places=12,
        )
        self.assertLess(variable.energy_balance_error_j, 1e-9)

    def test_rejects_invalid_ambient_profile(self):
        with self.assertRaisesRegex(ValueError, "one value per current interval"):
            simulate_lumped_temperature([10.0, 20.0], ambient_temperatures_c=[25.0])
        with self.assertRaisesRegex(ValueError, "temperature values must be finite"):
            simulate_lumped_temperature([10.0], ambient_temperatures_c=[math.nan])

    def test_rejects_invalid_interval_duration_profile(self):
        with self.assertRaisesRegex(ValueError, "one value per current interval"):
            simulate_lumped_temperature(
                [10.0, 20.0],
                interval_durations_s=[1.0],
            )
        with self.assertRaisesRegex(ValueError, "duration values must be finite"):
            simulate_lumped_temperature([10.0], interval_durations_s=[math.nan])
        with self.assertRaisesRegex(ValueError, "duration values must be positive"):
            simulate_lumped_temperature([10.0], interval_durations_s=[0.0])

    def test_rejects_invalid_entropic_coefficient_profile(self):
        with self.assertRaisesRegex(ValueError, "one value per current interval"):
            simulate_lumped_temperature(
                [10.0, 20.0],
                entropic_coefficients_v_per_k=[0.0001],
            )
        with self.assertRaisesRegex(ValueError, "coefficient values must be finite"):
            simulate_lumped_temperature(
                [10.0],
                entropic_coefficients_v_per_k=[math.nan],
            )

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

    def test_rejects_invalid_explicit_duration_schedule(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "profile.csv"
            path.write_text(
                "time_s,current_a,duration_s\n0,0,0\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duration_s must be positive"):
                load_current_profile(path)
            path.write_text(
                "time_s,current_a,duration_s\n0,0,30\n40,10,20\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "previous interval end"):
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
        self.assertEqual(float(rows[0]["duration_s"]), 1.0)
        self.assertEqual(float(rows[0]["ambient_temperature_c"]), 25.0)
        self.assertEqual(float(rows[0]["resistance_ohm"]), 0.004)
        self.assertEqual(float(rows[0]["entropic_coefficient_v_per_k"]), 0.0)
        self.assertEqual(float(rows[0]["reversible_heat_w"]), 0.0)
        self.assertEqual(
            float(rows[0]["irreversible_heat_w"]),
            float(rows[0]["heat_generation_w"]),
        )
        self.assertAlmostEqual(
            sum(float(row["net_heat_j"]) for row in rows),
            result.integrated_net_heat_j,
        )

    def test_exact_linear_export_uses_integrated_interval_heat(self):
        result = simulate_lumped_temperature(
            [100.0],
            LumpedThermalSpec(
                time_step_s=120.0,
                resistance_temperature_coefficient_per_k=0.02,
                integration_method=IntegrationMethod.EXACT_LINEAR,
            ),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.csv"
            write_simulation_csv(path, result)
            with path.open("r", encoding="utf-8", newline="") as output_file:
                row = next(csv.DictReader(output_file))
        self.assertAlmostEqual(
            float(row["net_heat_j"]),
            result.interval_net_heat_j[0],
            places=7,
        )
        self.assertAlmostEqual(
            result.integrated_net_heat_j,
            result.stored_energy_change_j,
            places=9,
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

    def test_cli_runs_nonuniform_profile_and_exports_true_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            profile_path = Path(directory) / "profile.csv"
            output_path = Path(directory) / "result.csv"
            profile_path.write_text(
                "time_s,current_a,duration_s\n0,0,10\n10,75,20\n30,0,45\n",
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
                        "--integration-method",
                        "exact-linear",
                    ]
                )
            with output_path.open("r", encoding="utf-8", newline="") as output_file:
                rows = list(csv.DictReader(output_file))
        self.assertEqual(exit_code, 0)
        self.assertIn("Duration: 75.000 s", standard_output.getvalue())
        self.assertEqual(
            [
                (
                    float(row["interval_start_s"]),
                    float(row["interval_end_s"]),
                    float(row["duration_s"]),
                )
                for row in rows
            ],
            [(0.0, 10.0, 10.0), (10.0, 30.0, 20.0), (30.0, 75.0, 45.0)],
        )

    def test_cli_reports_temperature_dependent_resistance_range(self):
        standard_output = io.StringIO()
        with contextlib.redirect_stdout(standard_output):
            exit_code = main(
                [
                    "--current-a",
                    "100",
                    "--duration-s",
                    "120",
                    "--resistance-temperature-coefficient-per-k",
                    "0.01",
                ]
            )
        self.assertEqual(exit_code, 0)
        output = standard_output.getvalue()
        self.assertIn("Resistance range: 0.004000 to ", output)
        upper_resistance = float(
            output.split("Resistance range: 0.004000 to ", 1)[1].split(" ", 1)[0]
        )
        self.assertGreater(upper_resistance, 0.004)

    def test_cli_applies_constant_entropic_coefficient(self):
        standard_output = io.StringIO()
        with contextlib.redirect_stdout(standard_output):
            exit_code = main(
                [
                    "--current-a",
                    "100",
                    "--duration-s",
                    "1",
                    "--entropic-coefficient-v-per-k",
                    "0.0001",
                ]
            )
        self.assertEqual(exit_code, 0)
        output = standard_output.getvalue()
        self.assertIn("Entropic coefficient range: 0.0001 to 0.0001 V/K", output)
        self.assertIn("Reversible heat range: -2.981500 to -2.981500 W", output)

    def test_cli_runs_entropic_profile_and_exports_heat_components(self):
        with tempfile.TemporaryDirectory() as directory:
            profile_path = Path(directory) / "profile.csv"
            output_path = Path(directory) / "result.csv"
            profile_path.write_text(
                "time_s,current_a,duration_s,entropic_coefficient_v_per_k\n"
                "0,80,60,0.0001\n"
                "60,-80,60,0.0001\n",
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
                        "--integration-method",
                        "exact-linear",
                    ]
                )
            with output_path.open("r", encoding="utf-8", newline="") as output_file:
                rows = list(csv.DictReader(output_file))
        self.assertEqual(exit_code, 0)
        self.assertIn(
            "Entropic coefficient range: 0.0001 to 0.0001 V/K",
            standard_output.getvalue(),
        )
        self.assertIn("Reversible heat range: -", standard_output.getvalue())
        self.assertLess(float(rows[0]["reversible_heat_w"]), 0.0)
        self.assertGreater(float(rows[1]["reversible_heat_w"]), 0.0)
        for row in rows:
            self.assertAlmostEqual(
                float(row["heat_generation_w"]),
                float(row["irreversible_heat_w"]) + float(row["reversible_heat_w"]),
                places=9,
            )

    def test_cli_reports_exact_linear_integration(self):
        standard_output = io.StringIO()
        with contextlib.redirect_stdout(standard_output):
            exit_code = main(
                [
                    "--current-a",
                    "75",
                    "--duration-s",
                    "600",
                    "--time-step-s",
                    "600",
                    "--integration-method",
                    "exact-linear",
                ]
            )
        self.assertEqual(exit_code, 0)
        output = standard_output.getvalue()
        self.assertIn("Integration method: exact-linear", output)
        energy_error_j = float(
            output.split("Energy-balance error: ", 1)[1].split(" ", 1)[0]
        )
        self.assertLess(energy_error_j, 1e-9)

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

    def test_profile_entropic_coefficient_rejects_constant_override(self):
        with tempfile.TemporaryDirectory() as directory:
            profile_path = Path(directory) / "profile.csv"
            profile_path.write_text(
                "time_s,current_a,entropic_coefficient_v_per_k\n"
                "0,0,0.0001\n1,10,0.0001\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "cannot be combined"):
                main(
                    [
                        "--profile-csv",
                        str(profile_path),
                        "--entropic-coefficient-v-per-k",
                        "0.0002",
                    ]
                )


if __name__ == "__main__":
    unittest.main()
