# Thermal Source Confidence Guide

Use this guide to rank confidence in battery thermal sources before using them to support a BTMS claim, validation result, or modeling assumption.

| Source Type | Typical Confidence | Useful For | Main Risk |
|---|---|---|---|
| Measured dataset | High | Validation, parameter fitting, condition-aware heat generation. | May not match the project cell, age, SOC, or thermal boundary. |
| Test report | High to medium | Design review and acceptance evidence when conditions are documented. | Test setup may not cover the full operating envelope. |
| Peer-reviewed paper | Medium | Explaining methods, trends, and public assumptions. | Cell chemistry, geometry, and duty cycle may differ from the project. |
| Datasheet | Medium to low | Initial limits, capacity, resistance ranges, and rough assumptions. | Often lacks heat-generation detail and operating-condition context. |
| Simulation-only evidence | Low | Early screening, sensitivity studies, and education. | Can look precise while relying on unvalidated inputs. |

## Confidence Ranking

| Rank | Evidence Standard | Review Question |
|---|---|---|
| 5 | Measured project-relevant dataset | Does it cover the same cell/module, C-rate, SOC, ambient, and cooling condition? |
| 4 | Controlled test report | Are setup, instruments, units, and boundary conditions traceable? |
| 3 | Public paper or benchmark | Is the method relevant even if the hardware is different? |
| 2 | Datasheet or supplier summary | Which assumptions are stated, and which are missing? |
| 1 | Simulation-only placeholder | Is it clearly marked as screening-level evidence? |

## Review Rule

Confidence should come from operating-condition match, measurement quality, and traceability. A source is not high confidence simply because it is technical or published.
