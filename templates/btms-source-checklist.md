# BTMS Source Checklist

Use this checklist when evaluating whether a battery thermal management system claim is supported by a public paper, datasheet, test result, or measured dataset.

| Claim | Source Type | Source / Evidence ID | Operating Range | Confidence | Review Note |
|---|---|---|---|---|---|
| Liquid cooling reduces peak cell temperature for the target duty cycle. | Test result | Placeholder test report ID | 25 degC ambient, 1C pulse | Medium | Confirm coolant flow rate and module layout match the claim. |
| Phase-change material buffers short pulse heat. | Paper | Placeholder citation | Short pulses, recovery time stated | Low | Check whether heat rejection after melting is addressed. |
| Air cooling is sufficient for the pack concept. | Datasheet / simulation | Placeholder model ID | Nominal ambient only | Low | Add hot-day and degraded-fan cases before design review. |
| Calorimetry-informed heat source improves model fidelity. | Measured dataset | Placeholder dataset ID | C-rate and temperature range stated | High | Confirm cell format and aging state are comparable. |

## Source Review Fields

| Field | Review Prompt |
|---|---|
| Source type | Is the claim backed by a paper, datasheet, internal test, public dataset, or simulation only? |
| Claim supported | What exact claim does the source support, and what claim does it not support? |
| Operating range | Does the source cover the same C-rate, SOC, ambient, and cooling condition? |
| Scaling basis | Is the evidence cell-level, module-level, pack-level, or container-level? |
| Confidence | Is the evidence strong enough for education, screening, architecture choice, or design approval? |

## Practical Rule

Do not cite a source only because it mentions the same BTMS technology. Tie each claim to the operating condition, measurement method, and scale that the source actually supports.
