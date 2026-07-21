from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Sequence


ABSOLUTE_ZERO_C = -273.15
STEFAN_BOLTZMANN_W_PER_M2_K4 = 5.670374419e-8


class IntegrationMethod(str, Enum):
    EXPLICIT_EULER = "explicit-euler"
    EXACT_LINEAR = "exact-linear"
    RK4 = "rk4"


@dataclass(frozen=True)
class LumpedThermalSpec:
    """Parameters for a one-node cell thermal model."""

    mass_kg: float = 1.05
    specific_heat_j_per_kg_k: float = 1000.0
    resistance_ohm: float = 0.004
    resistance_temperature_coefficient_per_k: float = 0.0
    resistance_reference_temperature_c: float = 25.0
    entropic_coefficient_v_per_k: float = 0.0
    heat_transfer_w_per_k: float = 1.2
    emissivity: float = 0.0
    radiating_area_m2: float = 0.0
    ambient_temperature_c: float = 25.0
    radiative_surroundings_temperature_c: float | None = None
    initial_temperature_c: float = 25.0
    time_step_s: float = 1.0
    rk4_max_step_s: float = 1.0
    integration_method: IntegrationMethod | str = IntegrationMethod.EXPLICIT_EULER

    @property
    def thermal_capacity_j_per_k(self) -> float:
        return self.mass_kg * self.specific_heat_j_per_kg_k

    @property
    def radiation_coefficient_w_per_k4(self) -> float:
        """Return epsilon * sigma * area for diffuse-gray surface radiation."""

        return self.emissivity * STEFAN_BOLTZMANN_W_PER_M2_K4 * self.radiating_area_m2

    def validate(self) -> None:
        integration_method = self.resolved_integration_method()
        finite_values = {
            "mass_kg": self.mass_kg,
            "specific_heat_j_per_kg_k": self.specific_heat_j_per_kg_k,
            "resistance_ohm": self.resistance_ohm,
            "resistance_temperature_coefficient_per_k": (
                self.resistance_temperature_coefficient_per_k
            ),
            "resistance_reference_temperature_c": (
                self.resistance_reference_temperature_c
            ),
            "entropic_coefficient_v_per_k": self.entropic_coefficient_v_per_k,
            "heat_transfer_w_per_k": self.heat_transfer_w_per_k,
            "emissivity": self.emissivity,
            "radiating_area_m2": self.radiating_area_m2,
            "ambient_temperature_c": self.ambient_temperature_c,
            "initial_temperature_c": self.initial_temperature_c,
            "time_step_s": self.time_step_s,
            "rk4_max_step_s": self.rk4_max_step_s,
        }
        for name, value in finite_values.items():
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")

        if self.mass_kg <= 0.0:
            raise ValueError("mass_kg must be positive")
        if self.specific_heat_j_per_kg_k <= 0.0:
            raise ValueError("specific_heat_j_per_kg_k must be positive")
        if self.resistance_ohm < 0.0:
            raise ValueError("resistance_ohm must be nonnegative")
        if self.heat_transfer_w_per_k < 0.0:
            raise ValueError("heat_transfer_w_per_k must be nonnegative")
        if not 0.0 <= self.emissivity <= 1.0:
            raise ValueError("emissivity must be between zero and one")
        if self.radiating_area_m2 < 0.0:
            raise ValueError("radiating_area_m2 must be nonnegative")
        if (self.emissivity == 0.0) != (self.radiating_area_m2 == 0.0):
            raise ValueError(
                "emissivity and radiating_area_m2 must both be zero or both positive"
            )
        if self.time_step_s <= 0.0:
            raise ValueError("time_step_s must be positive")
        if self.rk4_max_step_s <= 0.0:
            raise ValueError("rk4_max_step_s must be positive")
        _temperature_k(self.ambient_temperature_c, "ambient_temperature_c")
        if self.radiative_surroundings_temperature_c is not None:
            _temperature_k(
                self.radiative_surroundings_temperature_c,
                "radiative_surroundings_temperature_c",
            )
        _temperature_k(self.initial_temperature_c, "initial_temperature_c")
        _temperature_k(
            self.resistance_reference_temperature_c,
            "resistance_reference_temperature_c",
        )
        self.resistance_at_temperature(self.initial_temperature_c)
        if self.radiation_coefficient_w_per_k4 > 0.0:
            if integration_method is IntegrationMethod.EXACT_LINEAR:
                raise ValueError(
                    "exact-linear integration does not support nonlinear radiation; "
                    "use rk4"
                )
            if integration_method is not IntegrationMethod.RK4:
                raise ValueError("nonlinear radiation requires rk4 integration")

    def resolved_integration_method(self) -> IntegrationMethod:
        """Return the configured integration method as a validated enum."""

        try:
            return IntegrationMethod(self.integration_method)
        except ValueError as error:
            choices = ", ".join(method.value for method in IntegrationMethod)
            raise ValueError(f"integration_method must be one of: {choices}") from error

    def resistance_at_temperature(self, temperature_c: float) -> float:
        """Evaluate the configured linear resistance-temperature relation."""

        _temperature_k(temperature_c, "temperature_c")
        resistance_factor = 1.0 + (
            self.resistance_temperature_coefficient_per_k
            * (temperature_c - self.resistance_reference_temperature_c)
        )
        resistance_ohm = self.resistance_ohm * resistance_factor
        if resistance_ohm < 0.0:
            raise ValueError("temperature-dependent resistance must remain nonnegative")
        return resistance_ohm

    def reversible_heat_w(
        self,
        current_a: float,
        temperature_c: float,
        entropic_coefficient_v_per_k: float | None = None,
    ) -> float:
        """Return reversible heat for the positive-discharge convention."""

        coefficient = (
            self.entropic_coefficient_v_per_k
            if entropic_coefficient_v_per_k is None
            else entropic_coefficient_v_per_k
        )
        if not math.isfinite(current_a):
            raise ValueError("current_a must be finite")
        if not math.isfinite(coefficient):
            raise ValueError("entropic_coefficient_v_per_k must be finite")
        temperature_k = _temperature_k(temperature_c, "temperature_c")
        return -current_a * temperature_k * coefficient

    def radiative_heat_rejection_w(
        self,
        temperature_c: float,
        surroundings_temperature_c: float,
    ) -> float:
        """Return net diffuse-gray radiation from the cell to its surroundings."""

        temperature_k = _temperature_k(temperature_c, "temperature_c")
        surroundings_k = _temperature_k(
            surroundings_temperature_c,
            "surroundings_temperature_c",
        )
        if self.radiation_coefficient_w_per_k4 == 0.0:
            return 0.0
        try:
            heat_w = self.radiation_coefficient_w_per_k4 * (
                temperature_k**4 - surroundings_k**4
            )
        except OverflowError as error:
            raise ValueError("radiative heat calculation overflowed") from error
        if not math.isfinite(heat_w):
            raise ValueError("radiative heat calculation must remain finite")
        return heat_w


@dataclass(frozen=True)
class ThermalSimulation:
    """Discrete temperatures and interval-level heat flows."""

    time_s: tuple[float, ...]
    temperature_c: tuple[float, ...]
    current_a: tuple[float, ...]
    ambient_temperature_c: tuple[float, ...]
    radiative_surroundings_temperature_c: tuple[float, ...]
    heat_transfer_w_per_k: tuple[float, ...]
    resistance_ohm: tuple[float, ...]
    entropic_coefficient_v_per_k: tuple[float, ...]
    irreversible_heat_w: tuple[float, ...]
    reversible_heat_w: tuple[float, ...]
    heat_generation_w: tuple[float, ...]
    convective_heat_rejection_w: tuple[float, ...]
    radiative_heat_rejection_w: tuple[float, ...]
    heat_rejection_w: tuple[float, ...]
    interval_net_heat_j: tuple[float, ...]
    interval_duration_s: tuple[float, ...]
    thermal_capacity_j_per_k: float
    emissivity: float
    radiating_area_m2: float
    rk4_max_step_s: float
    integration_method: IntegrationMethod

    @property
    def peak_temperature_c(self) -> float:
        return max(self.temperature_c)

    @property
    def stored_energy_change_j(self) -> float:
        return self.thermal_capacity_j_per_k * (
            self.temperature_c[-1] - self.temperature_c[0]
        )

    @property
    def integrated_net_heat_j(self) -> float:
        return sum(self.interval_net_heat_j)

    @property
    def energy_balance_error_j(self) -> float:
        return abs(self.stored_energy_change_j - self.integrated_net_heat_j)

    @property
    def duration_s(self) -> float:
        return sum(self.interval_duration_s)

    @property
    def time_step_s(self) -> float | None:
        """Return the common interval duration, or None for a variable grid."""

        first_duration = self.interval_duration_s[0]
        if all(
            math.isclose(
                duration,
                first_duration,
                rel_tol=1e-12,
                abs_tol=1e-12,
            )
            for duration in self.interval_duration_s[1:]
        ):
            return first_duration
        return None


@dataclass(frozen=True)
class CurrentProfile:
    """Piecewise-constant electrical and thermal boundary conditions."""

    time_s: tuple[float, ...]
    current_a: tuple[float, ...]
    ambient_temperature_c: tuple[float, ...] | None
    radiative_surroundings_temperature_c: tuple[float, ...] | None
    entropic_coefficient_v_per_k: tuple[float, ...] | None
    heat_transfer_w_per_k: tuple[float, ...] | None
    interval_duration_s: tuple[float, ...]

    @property
    def time_step_s(self) -> float | None:
        """Return the common interval duration, or None for a variable grid."""

        first_duration = self.interval_duration_s[0]
        if all(
            math.isclose(
                duration,
                first_duration,
                rel_tol=1e-12,
                abs_tol=1e-12,
            )
            for duration in self.interval_duration_s[1:]
        ):
            return first_duration
        return None


@dataclass(frozen=True)
class HeatRates:
    """Start-of-step heat rates for one thermal state and boundary condition."""

    resistance_ohm: float
    irreversible_w: float
    reversible_w: float
    generation_w: float
    convective_rejection_w: float
    radiative_rejection_w: float
    total_rejection_w: float
    net_w: float


def _temperature_k(temperature_c: float, context: str) -> float:
    if not math.isfinite(temperature_c):
        raise ValueError(f"{context} must be finite")
    if temperature_c <= ABSOLUTE_ZERO_C:
        raise ValueError(f"{context} must be above absolute zero")
    return temperature_c - ABSOLUTE_ZERO_C


def _heat_rates(
    spec: LumpedThermalSpec,
    temperature_c: float,
    current_a: float,
    ambient_temperature_c: float,
    radiative_surroundings_temperature_c: float,
    entropic_coefficient_v_per_k: float,
    heat_transfer_w_per_k: float,
) -> HeatRates:
    resistance_ohm = spec.resistance_at_temperature(temperature_c)
    irreversible_w = current_a * current_a * resistance_ohm
    reversible_w = spec.reversible_heat_w(
        current_a,
        temperature_c,
        entropic_coefficient_v_per_k,
    )
    generation_w = irreversible_w + reversible_w
    convective_rejection_w = heat_transfer_w_per_k * (
        temperature_c - ambient_temperature_c
    )
    radiative_rejection_w = spec.radiative_heat_rejection_w(
        temperature_c,
        radiative_surroundings_temperature_c,
    )
    total_rejection_w = convective_rejection_w + radiative_rejection_w
    return HeatRates(
        resistance_ohm=resistance_ohm,
        irreversible_w=irreversible_w,
        reversible_w=reversible_w,
        generation_w=generation_w,
        convective_rejection_w=convective_rejection_w,
        radiative_rejection_w=radiative_rejection_w,
        total_rejection_w=total_rejection_w,
        net_w=generation_w - total_rejection_w,
    )


def _rk4_temperature_change_c(
    spec: LumpedThermalSpec,
    start_temperature_c: float,
    current_a: float,
    ambient_temperature_c: float,
    radiative_surroundings_temperature_c: float,
    entropic_coefficient_v_per_k: float,
    heat_transfer_w_per_k: float,
    interval_duration_s: float,
) -> float:
    """Integrate one constant-boundary interval with bounded RK4 substeps."""

    substeps = max(1, math.ceil(interval_duration_s / spec.rk4_max_step_s))
    step_s = interval_duration_s / substeps
    temperature_c = start_temperature_c

    def derivative(value_c: float) -> float:
        rates = _heat_rates(
            spec,
            value_c,
            current_a,
            ambient_temperature_c,
            radiative_surroundings_temperature_c,
            entropic_coefficient_v_per_k,
            heat_transfer_w_per_k,
        )
        return rates.net_w / spec.thermal_capacity_j_per_k

    for _ in range(substeps):
        k1 = derivative(temperature_c)
        k2 = derivative(temperature_c + 0.5 * step_s * k1)
        k3 = derivative(temperature_c + 0.5 * step_s * k2)
        k4 = derivative(temperature_c + step_s * k3)
        temperature_c += step_s * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        if not math.isfinite(temperature_c):
            raise ValueError("rk4 integration produced a non-finite temperature")
        _temperature_k(temperature_c, "rk4 integrated temperature")

    return temperature_c - start_temperature_c


def load_current_profile(path: Path) -> CurrentProfile:
    """Load piecewise-constant electrical and thermal profile intervals."""

    with path.open("r", encoding="utf-8", newline="") as profile_file:
        reader = csv.DictReader(profile_file)
        required_headers = ["time_s", "current_a"]
        optional_headers = [
            "duration_s",
            "ambient_temperature_c",
            "radiative_surroundings_temperature_c",
            "entropic_coefficient_v_per_k",
            "heat_transfer_w_per_k",
        ]
        fieldnames = reader.fieldnames or []
        selected_optional_headers = [
            header for header in optional_headers if header in fieldnames[2:]
        ]
        if (
            fieldnames[:2] != required_headers
            or fieldnames[2:] != selected_optional_headers
        ):
            raise ValueError(
                "profile CSV header must be exactly time_s,current_a followed by "
                "any of duration_s,ambient_temperature_c,"
                "radiative_surroundings_temperature_c,"
                "entropic_coefficient_v_per_k,heat_transfer_w_per_k in that order"
            )
        has_ambient = "ambient_temperature_c" in fieldnames
        has_radiative_surroundings = (
            "radiative_surroundings_temperature_c" in fieldnames
        )
        has_duration = "duration_s" in fieldnames
        has_entropic_coefficient = "entropic_coefficient_v_per_k" in fieldnames
        has_heat_transfer = "heat_transfer_w_per_k" in fieldnames
        rows = list(reader)

    if not rows:
        raise ValueError("profile CSV must contain at least one interval")
    if not has_duration and len(rows) < 2:
        raise ValueError("profile CSV must contain at least two intervals")

    times: list[float] = []
    currents: list[float] = []
    durations: list[float] = []
    ambient_temperatures: list[float] = []
    radiative_surroundings_temperatures: list[float] = []
    entropic_coefficients: list[float] = []
    heat_transfers: list[float] = []
    for line_number, row in enumerate(rows, start=2):
        try:
            time_s = float(row["time_s"])
            current_a = float(row["current_a"])
            duration_s = float(row["duration_s"]) if has_duration else None
            ambient_temperature_c = (
                float(row["ambient_temperature_c"]) if has_ambient else None
            )
            radiative_surroundings_temperature_c = (
                float(row["radiative_surroundings_temperature_c"])
                if has_radiative_surroundings
                else None
            )
            entropic_coefficient_v_per_k = (
                float(row["entropic_coefficient_v_per_k"])
                if has_entropic_coefficient
                else None
            )
            heat_transfer_w_per_k = (
                float(row["heat_transfer_w_per_k"]) if has_heat_transfer else None
            )
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"profile CSV line {line_number} must contain numeric values"
            ) from error
        values = [time_s, current_a]
        if duration_s is not None:
            values.append(duration_s)
        if ambient_temperature_c is not None:
            values.append(ambient_temperature_c)
        if radiative_surroundings_temperature_c is not None:
            values.append(radiative_surroundings_temperature_c)
        if entropic_coefficient_v_per_k is not None:
            values.append(entropic_coefficient_v_per_k)
        if heat_transfer_w_per_k is not None:
            values.append(heat_transfer_w_per_k)
        if None in row or any(not math.isfinite(value) for value in values):
            raise ValueError(f"profile CSV line {line_number} must be finite")
        if duration_s is not None and duration_s <= 0.0:
            raise ValueError(
                f"profile CSV line {line_number} duration_s must be positive"
            )
        if heat_transfer_w_per_k is not None and heat_transfer_w_per_k < 0.0:
            raise ValueError(
                f"profile CSV line {line_number} heat_transfer_w_per_k "
                "must be nonnegative"
            )
        times.append(time_s)
        currents.append(current_a)
        if duration_s is not None:
            durations.append(duration_s)
        if ambient_temperature_c is not None:
            _temperature_k(
                ambient_temperature_c,
                f"profile CSV line {line_number} ambient_temperature_c",
            )
            ambient_temperatures.append(ambient_temperature_c)
        if radiative_surroundings_temperature_c is not None:
            _temperature_k(
                radiative_surroundings_temperature_c,
                f"profile CSV line {line_number} "
                "radiative_surroundings_temperature_c",
            )
            radiative_surroundings_temperatures.append(
                radiative_surroundings_temperature_c
            )
        if entropic_coefficient_v_per_k is not None:
            entropic_coefficients.append(entropic_coefficient_v_per_k)
        if heat_transfer_w_per_k is not None:
            heat_transfers.append(heat_transfer_w_per_k)

    if not math.isclose(times[0], 0.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("profile CSV time_s must start at zero")
    if has_duration:
        for index, (previous_start, previous_duration, current_start) in enumerate(
            zip(times, durations, times[1:], strict=False), start=3
        ):
            expected_start = previous_start + previous_duration
            if not math.isclose(
                current_start,
                expected_start,
                rel_tol=1e-9,
                abs_tol=1e-12,
            ):
                raise ValueError(
                    f"profile CSV line {index} time_s must equal the previous "
                    "interval end"
                )
    else:
        time_step_s = times[1] - times[0]
        if time_step_s <= 0.0:
            raise ValueError("profile CSV timestamps must be strictly increasing")
        for index, (previous, current) in enumerate(
            zip(times, times[1:], strict=False), start=3
        ):
            step = current - previous
            if step <= 0.0:
                raise ValueError(
                    f"profile CSV line {index} timestamp must be strictly increasing"
                )
            if not math.isclose(
                step,
                time_step_s,
                rel_tol=1e-9,
                abs_tol=1e-12,
            ):
                raise ValueError("profile CSV timestamps must use a uniform time step")
        durations = [time_step_s] * len(times)

    return CurrentProfile(
        time_s=tuple(times),
        current_a=tuple(currents),
        ambient_temperature_c=(tuple(ambient_temperatures) if has_ambient else None),
        radiative_surroundings_temperature_c=(
            tuple(radiative_surroundings_temperatures)
            if has_radiative_surroundings
            else None
        ),
        entropic_coefficient_v_per_k=(
            tuple(entropic_coefficients) if has_entropic_coefficient else None
        ),
        heat_transfer_w_per_k=(tuple(heat_transfers) if has_heat_transfer else None),
        interval_duration_s=tuple(durations),
    )


def simulate_lumped_temperature(
    currents_a: Sequence[float],
    spec: LumpedThermalSpec = LumpedThermalSpec(),
    ambient_temperatures_c: Sequence[float] | None = None,
    radiative_surroundings_temperatures_c: Sequence[float] | None = None,
    interval_durations_s: Sequence[float] | None = None,
    entropic_coefficients_v_per_k: Sequence[float] | None = None,
    heat_transfers_w_per_k: Sequence[float] | None = None,
) -> ThermalSimulation:
    """Integrate a one-node thermal balance over piecewise-constant intervals."""

    spec.validate()
    integration_method = spec.resolved_integration_method()
    currents = tuple(float(current) for current in currents_a)
    if not currents:
        raise ValueError("currents_a must contain at least one interval")
    if any(not math.isfinite(current) for current in currents):
        raise ValueError("all current values must be finite")

    if interval_durations_s is None:
        interval_durations = (spec.time_step_s,) * len(currents)
    else:
        interval_durations = tuple(float(value) for value in interval_durations_s)
        if len(interval_durations) != len(currents):
            raise ValueError(
                "interval_durations_s must contain one value per current interval"
            )
        if any(not math.isfinite(value) for value in interval_durations):
            raise ValueError("all interval duration values must be finite")
        if any(value <= 0.0 for value in interval_durations):
            raise ValueError("all interval duration values must be positive")

    if ambient_temperatures_c is None:
        ambient_temperatures = (spec.ambient_temperature_c,) * len(currents)
    else:
        ambient_temperatures = tuple(
            float(temperature) for temperature in ambient_temperatures_c
        )
        if len(ambient_temperatures) != len(currents):
            raise ValueError(
                "ambient_temperatures_c must contain one value per current interval"
            )
        if any(not math.isfinite(value) for value in ambient_temperatures):
            raise ValueError("all ambient temperature values must be finite")
        for value in ambient_temperatures:
            _temperature_k(value, "ambient temperature values")

    if radiative_surroundings_temperatures_c is None:
        if spec.radiative_surroundings_temperature_c is None:
            radiative_surroundings_temperatures = ambient_temperatures
        else:
            radiative_surroundings_temperatures = (
                spec.radiative_surroundings_temperature_c,
            ) * len(currents)
    else:
        radiative_surroundings_temperatures = tuple(
            float(temperature)
            for temperature in radiative_surroundings_temperatures_c
        )
        if len(radiative_surroundings_temperatures) != len(currents):
            raise ValueError(
                "radiative_surroundings_temperatures_c must contain one value "
                "per current interval"
            )
        if any(
            not math.isfinite(value)
            for value in radiative_surroundings_temperatures
        ):
            raise ValueError(
                "all radiative surroundings temperature values must be finite"
            )
        for value in radiative_surroundings_temperatures:
            _temperature_k(value, "radiative surroundings temperature values")

    if entropic_coefficients_v_per_k is None:
        entropic_coefficients = (spec.entropic_coefficient_v_per_k,) * len(currents)
    else:
        entropic_coefficients = tuple(
            float(value) for value in entropic_coefficients_v_per_k
        )
        if len(entropic_coefficients) != len(currents):
            raise ValueError(
                "entropic_coefficients_v_per_k must contain one value per "
                "current interval"
            )
        if any(not math.isfinite(value) for value in entropic_coefficients):
            raise ValueError("all entropic coefficient values must be finite")

    if heat_transfers_w_per_k is None:
        heat_transfers = (spec.heat_transfer_w_per_k,) * len(currents)
    else:
        heat_transfers = tuple(float(value) for value in heat_transfers_w_per_k)
        if len(heat_transfers) != len(currents):
            raise ValueError(
                "heat_transfers_w_per_k must contain one value per current interval"
            )
        if any(not math.isfinite(value) for value in heat_transfers):
            raise ValueError("all heat transfer values must be finite")
        if any(value < 0.0 for value in heat_transfers):
            raise ValueError("all heat transfer values must be nonnegative")

    temperatures = [spec.initial_temperature_c]
    irreversible_heat: list[float] = []
    reversible_heat: list[float] = []
    generated_heat: list[float] = []
    convective_rejected_heat: list[float] = []
    radiative_rejected_heat: list[float] = []
    rejected_heat: list[float] = []
    interval_net_heat: list[float] = []
    interval_resistance: list[float] = []
    interval_entropic_coefficient: list[float] = []

    for (
        current,
        ambient_temperature_c,
        radiative_surroundings_temperature_c,
        interval_duration_s,
        entropic_coefficient_v_per_k,
        heat_transfer_w_per_k,
    ) in zip(
        currents,
        ambient_temperatures,
        radiative_surroundings_temperatures,
        interval_durations,
        entropic_coefficients,
        heat_transfers,
        strict=True,
    ):
        temperature = temperatures[-1]
        rates = _heat_rates(
            spec,
            temperature,
            current,
            ambient_temperature_c,
            radiative_surroundings_temperature_c,
            entropic_coefficient_v_per_k,
            heat_transfer_w_per_k,
        )
        if integration_method is IntegrationMethod.EXPLICIT_EULER:
            temperature_change_c = (
                rates.net_w * interval_duration_s / spec.thermal_capacity_j_per_k
            )
        elif integration_method is IntegrationMethod.EXACT_LINEAR:
            thermal_feedback_w_per_k = (
                current
                * current
                * spec.resistance_ohm
                * spec.resistance_temperature_coefficient_per_k
                - current * entropic_coefficient_v_per_k
                - heat_transfer_w_per_k
            )
            if thermal_feedback_w_per_k == 0.0:
                temperature_change_c = (
                    rates.net_w * interval_duration_s / spec.thermal_capacity_j_per_k
                )
            else:
                exponent = (
                    thermal_feedback_w_per_k
                    * interval_duration_s
                    / spec.thermal_capacity_j_per_k
                )
                try:
                    temperature_change_c = (
                        rates.net_w * math.expm1(exponent) / thermal_feedback_w_per_k
                    )
                except OverflowError as error:
                    raise ValueError(
                        "exact integration produced a non-finite temperature"
                    ) from error
        else:
            temperature_change_c = _rk4_temperature_change_c(
                spec,
                temperature,
                current,
                ambient_temperature_c,
                radiative_surroundings_temperature_c,
                entropic_coefficient_v_per_k,
                heat_transfer_w_per_k,
                interval_duration_s,
            )

        next_temperature_c = temperature + temperature_change_c
        if not math.isfinite(next_temperature_c):
            raise ValueError("integration produced a non-finite temperature")
        _temperature_k(next_temperature_c, "integrated temperature")
        spec.resistance_at_temperature(next_temperature_c)

        interval_resistance.append(rates.resistance_ohm)
        interval_entropic_coefficient.append(entropic_coefficient_v_per_k)
        irreversible_heat.append(rates.irreversible_w)
        reversible_heat.append(rates.reversible_w)
        generated_heat.append(rates.generation_w)
        convective_rejected_heat.append(rates.convective_rejection_w)
        radiative_rejected_heat.append(rates.radiative_rejection_w)
        rejected_heat.append(rates.total_rejection_w)
        interval_net_heat.append(temperature_change_c * spec.thermal_capacity_j_per_k)
        temperatures.append(next_temperature_c)

    times = [0.0]
    for duration_s in interval_durations:
        times.append(times[-1] + duration_s)
    return ThermalSimulation(
        time_s=tuple(times),
        temperature_c=tuple(temperatures),
        current_a=currents,
        ambient_temperature_c=ambient_temperatures,
        radiative_surroundings_temperature_c=(
            radiative_surroundings_temperatures
        ),
        heat_transfer_w_per_k=heat_transfers,
        resistance_ohm=tuple(interval_resistance),
        entropic_coefficient_v_per_k=tuple(interval_entropic_coefficient),
        irreversible_heat_w=tuple(irreversible_heat),
        reversible_heat_w=tuple(reversible_heat),
        heat_generation_w=tuple(generated_heat),
        convective_heat_rejection_w=tuple(convective_rejected_heat),
        radiative_heat_rejection_w=tuple(radiative_rejected_heat),
        heat_rejection_w=tuple(rejected_heat),
        interval_net_heat_j=tuple(interval_net_heat),
        interval_duration_s=interval_durations,
        thermal_capacity_j_per_k=spec.thermal_capacity_j_per_k,
        emissivity=spec.emissivity,
        radiating_area_m2=spec.radiating_area_m2,
        rk4_max_step_s=spec.rk4_max_step_s,
        integration_method=integration_method,
    )


def write_simulation_csv(path: Path, result: ThermalSimulation) -> None:
    """Write one auditable result row per simulated current interval."""

    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "interval_start_s",
        "interval_end_s",
        "duration_s",
        "current_a",
        "ambient_temperature_c",
        "radiative_surroundings_temperature_c",
        "heat_transfer_w_per_k",
        "emissivity",
        "radiating_area_m2",
        "resistance_ohm",
        "entropic_coefficient_v_per_k",
        "start_temperature_c",
        "end_temperature_c",
        "irreversible_heat_w",
        "reversible_heat_w",
        "heat_generation_w",
        "convective_heat_rejection_w",
        "radiative_heat_rejection_w",
        "heat_rejection_w",
        "net_heat_j",
    ]
    with path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for index, current_a in enumerate(result.current_a):
            generated_w = result.heat_generation_w[index]
            rejected_w = result.heat_rejection_w[index]
            values = {
                "interval_start_s": result.time_s[index],
                "interval_end_s": result.time_s[index + 1],
                "duration_s": result.interval_duration_s[index],
                "current_a": current_a,
                "ambient_temperature_c": result.ambient_temperature_c[index],
                "radiative_surroundings_temperature_c": (
                    result.radiative_surroundings_temperature_c[index]
                ),
                "heat_transfer_w_per_k": result.heat_transfer_w_per_k[index],
                "emissivity": result.emissivity,
                "radiating_area_m2": result.radiating_area_m2,
                "resistance_ohm": result.resistance_ohm[index],
                "entropic_coefficient_v_per_k": (
                    result.entropic_coefficient_v_per_k[index]
                ),
                "start_temperature_c": result.temperature_c[index],
                "end_temperature_c": result.temperature_c[index + 1],
                "irreversible_heat_w": result.irreversible_heat_w[index],
                "reversible_heat_w": result.reversible_heat_w[index],
                "heat_generation_w": generated_w,
                "convective_heat_rejection_w": (
                    result.convective_heat_rejection_w[index]
                ),
                "radiative_heat_rejection_w": (
                    result.radiative_heat_rejection_w[index]
                ),
                "heat_rejection_w": rejected_w,
                "net_heat_j": result.interval_net_heat_j[index],
            }
            writer.writerow(
                {name: format(value, ".12g") for name, value in values.items()}
            )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a constant-current or CSV-profile cell thermal calculation."
    )
    parser.add_argument("--profile-csv", type=Path)
    parser.add_argument("--output-csv", type=Path)
    parser.add_argument("--current-a", type=float)
    parser.add_argument("--duration-s", type=float)
    parser.add_argument("--time-step-s", type=float)
    parser.add_argument("--resistance-ohm", type=float, default=0.004)
    parser.add_argument(
        "--resistance-temperature-coefficient-per-k",
        type=float,
        default=0.0,
    )
    parser.add_argument(
        "--resistance-reference-temperature-c",
        type=float,
        default=25.0,
    )
    parser.add_argument("--entropic-coefficient-v-per-k", type=float)
    parser.add_argument("--heat-transfer-w-per-k", type=float)
    parser.add_argument("--emissivity", type=float, default=0.0)
    parser.add_argument("--radiating-area-m2", type=float, default=0.0)
    parser.add_argument("--ambient-temperature-c", type=float)
    parser.add_argument("--radiative-surroundings-temperature-c", type=float)
    parser.add_argument("--initial-temperature-c", type=float, default=25.0)
    parser.add_argument("--mass-kg", type=float, default=1.05)
    parser.add_argument("--specific-heat-j-per-kg-k", type=float, default=1000.0)
    parser.add_argument("--rk4-max-step-s", type=float, default=1.0)
    parser.add_argument(
        "--integration-method",
        choices=tuple(method.value for method in IntegrationMethod),
        default=IntegrationMethod.EXPLICIT_EULER.value,
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    ambient_temperatures_c = None
    radiative_surroundings_temperatures_c = None
    interval_durations_s = None
    entropic_coefficients_v_per_k = None
    heat_transfers_w_per_k = None
    if args.profile_csv:
        conflicting = [
            name
            for name in ("current_a", "duration_s", "time_step_s")
            if getattr(args, name) is not None
        ]
        if conflicting:
            options = ", ".join(f"--{name.replace('_', '-')}" for name in conflicting)
            raise ValueError(f"--profile-csv cannot be combined with {options}")
        profile = load_current_profile(args.profile_csv)
        if (
            profile.ambient_temperature_c is not None
            and args.ambient_temperature_c is not None
        ):
            raise ValueError(
                "--ambient-temperature-c cannot be combined with a profile "
                "that contains ambient_temperature_c"
            )
        if (
            profile.entropic_coefficient_v_per_k is not None
            and args.entropic_coefficient_v_per_k is not None
        ):
            raise ValueError(
                "--entropic-coefficient-v-per-k cannot be combined with a "
                "profile that contains entropic_coefficient_v_per_k"
            )
        if (
            profile.radiative_surroundings_temperature_c is not None
            and args.radiative_surroundings_temperature_c is not None
        ):
            raise ValueError(
                "--radiative-surroundings-temperature-c cannot be combined "
                "with a profile that contains "
                "radiative_surroundings_temperature_c"
            )
        if (
            profile.heat_transfer_w_per_k is not None
            and args.heat_transfer_w_per_k is not None
        ):
            raise ValueError(
                "--heat-transfer-w-per-k cannot be combined with a profile "
                "that contains heat_transfer_w_per_k"
            )
        currents = profile.current_a
        ambient_temperatures_c = profile.ambient_temperature_c
        radiative_surroundings_temperatures_c = (
            profile.radiative_surroundings_temperature_c
        )
        interval_durations_s = profile.interval_duration_s
        entropic_coefficients_v_per_k = profile.entropic_coefficient_v_per_k
        heat_transfers_w_per_k = profile.heat_transfer_w_per_k
        time_step_s = profile.time_step_s or profile.interval_duration_s[0]
    else:
        current_a = 75.0 if args.current_a is None else args.current_a
        duration_s = 600.0 if args.duration_s is None else args.duration_s
        time_step_s = 1.0 if args.time_step_s is None else args.time_step_s
        if duration_s <= 0.0:
            raise ValueError("duration_s must be positive")
        if time_step_s <= 0.0:
            raise ValueError("time_step_s must be positive")

        intervals = round(duration_s / time_step_s)
        if intervals < 1 or not math.isclose(
            intervals * time_step_s,
            duration_s,
            rel_tol=0.0,
            abs_tol=1e-9,
        ):
            raise ValueError("duration_s must be an integer multiple of time_step_s")
        currents = (current_a,) * intervals

    ambient_temperature_c = (
        25.0 if args.ambient_temperature_c is None else args.ambient_temperature_c
    )
    spec = LumpedThermalSpec(
        mass_kg=args.mass_kg,
        specific_heat_j_per_kg_k=args.specific_heat_j_per_kg_k,
        resistance_ohm=args.resistance_ohm,
        resistance_temperature_coefficient_per_k=(
            args.resistance_temperature_coefficient_per_k
        ),
        resistance_reference_temperature_c=(args.resistance_reference_temperature_c),
        entropic_coefficient_v_per_k=(
            0.0
            if args.entropic_coefficient_v_per_k is None
            else args.entropic_coefficient_v_per_k
        ),
        heat_transfer_w_per_k=(
            1.2 if args.heat_transfer_w_per_k is None else args.heat_transfer_w_per_k
        ),
        emissivity=args.emissivity,
        radiating_area_m2=args.radiating_area_m2,
        ambient_temperature_c=ambient_temperature_c,
        radiative_surroundings_temperature_c=(
            args.radiative_surroundings_temperature_c
        ),
        initial_temperature_c=args.initial_temperature_c,
        time_step_s=time_step_s,
        rk4_max_step_s=args.rk4_max_step_s,
        integration_method=args.integration_method,
    )
    result = simulate_lumped_temperature(
        currents,
        spec,
        ambient_temperatures_c=ambient_temperatures_c,
        radiative_surroundings_temperatures_c=(
            radiative_surroundings_temperatures_c
        ),
        interval_durations_s=interval_durations_s,
        entropic_coefficients_v_per_k=entropic_coefficients_v_per_k,
        heat_transfers_w_per_k=heat_transfers_w_per_k,
    )

    if args.output_csv:
        write_simulation_csv(args.output_csv, result)

    print(f"Intervals: {len(currents)}")
    print(f"Duration: {result.duration_s:.3f} s")
    print(f"Integration method: {result.integration_method.value}")
    print(f"Final temperature: {result.temperature_c[-1]:.3f} degC")
    print(f"Peak temperature: {result.peak_temperature_c:.3f} degC")
    print(
        "Resistance range: "
        f"{min(result.resistance_ohm):.6f} to "
        f"{max(result.resistance_ohm):.6f} ohm"
    )
    print(
        "Heat-transfer range: "
        f"{min(result.heat_transfer_w_per_k):.6g} to "
        f"{max(result.heat_transfer_w_per_k):.6g} W/K"
    )
    print(f"Radiation coefficient: {spec.radiation_coefficient_w_per_k4:.12g} W/K^4")
    print(
        "Radiative-surroundings temperature range: "
        f"{min(result.radiative_surroundings_temperature_c):.6g} to "
        f"{max(result.radiative_surroundings_temperature_c):.6g} degC"
    )
    print(
        "Entropic coefficient range: "
        f"{min(result.entropic_coefficient_v_per_k):.6g} to "
        f"{max(result.entropic_coefficient_v_per_k):.6g} V/K"
    )
    print(
        "Reversible heat range: "
        f"{min(result.reversible_heat_w):.6f} to "
        f"{max(result.reversible_heat_w):.6f} W"
    )
    print(
        "Total heat-source range: "
        f"{min(result.heat_generation_w):.6f} to "
        f"{max(result.heat_generation_w):.6f} W"
    )
    print(
        "Convective heat-rejection range: "
        f"{min(result.convective_heat_rejection_w):.6f} to "
        f"{max(result.convective_heat_rejection_w):.6f} W"
    )
    print(
        "Radiative heat-rejection range: "
        f"{min(result.radiative_heat_rejection_w):.6f} to "
        f"{max(result.radiative_heat_rejection_w):.6f} W"
    )
    if result.integration_method is IntegrationMethod.RK4:
        print(f"RK4 maximum internal step: {result.rk4_max_step_s:.6g} s")
    print(f"Stored thermal energy: {result.stored_energy_change_j:.3f} J")
    print(f"Integrated net heat: {result.integrated_net_heat_j:.3f} J")
    print(f"Energy-balance error: {result.energy_balance_error_j:.6e} J")
    if args.output_csv:
        print(f"Interval results: {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
