# SDIF Round-Trip Fidelity Benchmark — Summary

- Generated at: `2026-05-23T08:49:18Z`
- Documents: `20`

## Key Findings

Fidelity measures semantic preservation when converting `JSON → format → JSON`.
100% = lossless. Lower = semantic loss (type coercion, nesting collapse, etc.).

| Format | Avg Overall | Coverage |
| --- | ---: | ---: |
| JSON Compact | 100.0% | 20/20 |
| JSON Pretty | 100.0% | 20/20 |
| YAML | 100.0% | 20/20 |
| SDIF | 100.0% | 20/20 |
| CSV Bundle | 98.6% | 20/20 |
| XML | 88.7% | 20/20 |

## Score Definitions

| Score | Definition |
| --- | --- |
| **Value fidelity** | % of leaf values that round-trip to the same value (string comparison). |
| **Type fidelity** | % of leaf values whose Python type is preserved exactly. |
| **Structure fidelity** | % of key paths from the original that exist in the round-tripped document. |
| **Overall fidelity** | Harmonic mean of the three scores above. |
