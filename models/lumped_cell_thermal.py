from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class LumpedThermalSpec:
    """Parameters for a one-node cell thermal model."""

    mass_kg: float = 1.05
    specific_heat_j_per_kg_k: float = 1000.0
    resistance_ohm: float = 0.004
    heat_transfer_w_per_k: float = 1.2
    ambient_temperature_c: float = 25.0
    initial_temperature_c: float = 25.0
    time_step_s: float = 1.0

    @property
    def thermal_capacity_j_per_k(self) -> float:
        return self.mass_kg * self.specific_heat_j_per_kg_k

    def validate(self) -> None:
        finite_values = {
            "mass_kg": self.mass_kg,
            "specific_heat_j_per_kg_k": self.specific_heat_j_per_kg_k,
            "resistance_ohm": self.resistance_ohm,
            "heat_transfer_w_per_k": self.heat_transfer_w_per_k,
            "ambient_temperature_c": self.ambient_temperature_c,
            "initial_temperature_c": self.initial_temperature_c,
            "time_step_s": self.time_step_s,
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
        if self.time_step_s <= 0.0:
            raise ValueError("time_step_s must be positive")


@dataclass(frozen=True)
class ThermalSimulation:
    """Discrete temperatures and interval-level heat flows."""

    time_s: tuple[float, ...]
    temperature_c: tuple[float, ...]
    current_a: tuple[float, ...]
    heat_generation_w: tuple[float, ...]
    heat_rejection_w: tuple[float, ...]
    thermal_capacity_j_per_k: float
    time_step_s: float

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
        return sum(
            (generated - rejected) * self.time_step_s
            for generated, rejected in zip(
                self.heat_generation_w,
                self.heat_rejection_w,
                strict=True,
            )
        )

    @property
    def energy_balance_error_j(self) -> float:
        return abs(self.stored_energy_change_j - self.integrated_net_heat_j)


def simulate_lumped_temperature(
    currents_a: Sequence[float],
    spec: LumpedThermalSpec = LumpedThermalSpec(),
) -> ThermalSimulation:
    """Integrate a one-node thermal balance with explicit Euler steps."""

    spec.validate()
    currents = tuple(float(current) for current in currents_a)
    if not currents:
        raise ValueError("currents_a must contain at least one interval")
    if any(not math.isfinite(current) for current in currents):
        raise ValueError("all current values must be finite")

    temperatures = [spec.initial_temperature_c]
    generated_heat: list[float] = []
    rejected_heat: list[float] = []

    for current in currents:
        temperature = temperatures[-1]
        generation_w = current * current * spec.resistance_ohm
        rejection_w = spec.heat_transfer_w_per_k * (
            temperature - spec.ambient_temperature_c
        )
        temperature_change_c = (
            (generation_w - rejection_w)
            * spec.time_step_s
            / spec.thermal_capacity_j_per_k
        )

        generated_heat.append(generation_w)
        rejected_heat.append(rejection_w)
        temperatures.append(temperature + temperature_change_c)

    times = tuple(index * spec.time_step_s for index in range(len(currents) + 1))
    return ThermalSimulation(
        time_s=times,
        temperature_c=tuple(temperatures),
        current_a=currents,
        heat_generation_w=tuple(generated_heat),
        heat_rejection_w=tuple(rejected_heat),
        thermal_capacity_j_per_k=spec.thermal_capacity_j_per_k,
        time_step_s=spec.time_step_s,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a constant-current lumped cell thermal calculation."
    )
    parser.add_argument("--current-a", type=float, default=75.0)
    parser.add_argument("--duration-s", type=float, default=600.0)
    parser.add_argument("--time-step-s", type=float, default=1.0)
    parser.add_argument("--resistance-ohm", type=float, default=0.004)
    parser.add_argument("--heat-transfer-w-per-k", type=float, default=1.2)
    parser.add_argument("--ambient-temperature-c", type=float, default=25.0)
    parser.add_argument("--initial-temperature-c", type=float, default=25.0)
    parser.add_argument("--mass-kg", type=float, default=1.05)
    parser.add_argument("--specific-heat-j-per-kg-k", type=float, default=1000.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.duration_s <= 0.0:
        raise ValueError("duration_s must be positive")
    if args.time_step_s <= 0.0:
        raise ValueError("time_step_s must be positive")

    intervals = round(args.duration_s / args.time_step_s)
    if intervals < 1 or not math.isclose(
        intervals * args.time_step_s,
        args.duration_s,
        rel_tol=0.0,
        abs_tol=1e-9,
    ):
        raise ValueError("duration_s must be an integer multiple of time_step_s")

    spec = LumpedThermalSpec(
        mass_kg=args.mass_kg,
        specific_heat_j_per_kg_k=args.specific_heat_j_per_kg_k,
        resistance_ohm=args.resistance_ohm,
        heat_transfer_w_per_k=args.heat_transfer_w_per_k,
        ambient_temperature_c=args.ambient_temperature_c,
        initial_temperature_c=args.initial_temperature_c,
        time_step_s=args.time_step_s,
    )
    result = simulate_lumped_temperature([args.current_a] * intervals, spec)

    print(f"Intervals: {intervals}")
    print(f"Final temperature: {result.temperature_c[-1]:.3f} degC")
    print(f"Peak temperature: {result.peak_temperature_c:.3f} degC")
    print(f"Stored thermal energy: {result.stored_energy_change_j:.3f} J")
    print(f"Integrated net heat: {result.integrated_net_heat_j:.3f} J")
    print(f"Energy-balance error: {result.energy_balance_error_j:.6e} J")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
