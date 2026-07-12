# Battery Thermal Validation Checklist

Use this checklist before publishing or sharing thermal modeling results.

| Check | Evidence Required | Status |
|---|---|---|
| Geometry stated | Cell/module/pack dimensions and simplifications | Not started |
| Material properties stated | Conductivity, density, heat capacity, and source | Not started |
| Boundary conditions stated | Ambient, convection coefficient, flow assumptions | Not started |
| Duty cycle stated | Current, power, or mission profile | Not started |
| Time step/solver stated | Numerical setup sufficient for reproducibility | Not started |
| Validation reference included | Test data, datasheet comparison, or literature benchmark | Not started |
| Limits stated | Known simplifications and confidence limits | Not started |

## Units and Sign Conventions

| Check | Evidence Required | Status |
|---|---|---|
| Temperature units stated | Celsius or Kelvin used consistently across plots, tables, and equations | Not started |
| Current sign convention stated | Charge/discharge sign convention documented before heat-generation equations | Not started |
| Heat rate units stated | Heat generation reported in W, W/cell, W/module, or W/kg with scaling basis | Not started |
| Thermal property units stated | Conductivity, density, heat capacity, and convection coefficients include units | Not started |
| Operating range stated | SOC, C-rate, temperature, and ambient range included with assumptions | Not started |

## Thermal Boundary Conditions

| Check | Evidence Required | Status |
|---|---|---|
| Ambient condition stated | Ambient temperature, enclosure condition, and initial temperature | Not started |
| Cooling condition stated | Natural convection, forced air, liquid cooling, or fixed-temperature boundary | Not started |
| Heat-transfer coefficient stated | Value, units, and source or calibration basis | Not started |
| Contact assumptions stated | Thermal interface, contact resistance, or lumped simplification documented | Not started |
| Edge cases stated | High/low ambient, derating condition, or worst-case pulse profile identified | Not started |

## Minimum Result Package

- Temperature plot with axis labels and units.
- Peak temperature summary.
- Temperature gradient summary.
- Assumption table.
- Validation or benchmark statement.
