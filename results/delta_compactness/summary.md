# SDIF Mutation Sensitivity Benchmark — Summary

> **Framing**: this benchmark measures full-document resend overhead after a 10% leaf mutation.
> It is NOT a true SDIF delta benchmark. A semantic delta (base + patch) would be even smaller.

- Generated at: `2026-05-23T21:28:15Z`
- Tokenizer: `tiktoken/cl100k_base`
- Mutation: `10%` of leaf values changed
- Documents: `20`

## Key Findings

A 10% leaf mutation simulates a typical incremental document update.
Formats with smaller token delta and fewer diff lines produce less noise on full-resend.

| Format | Avg Δ tokens % | Avg diff lines |
| --- | ---: | ---: |
| XML | +1.6% | 2835.7 |
| JSON Pretty | +1.9% | 2835.7 |
| YAML | +2.6% | 1880.6 |
| JSON Compact | +3.0% | 2.0 |
| TOON | +4.4% | 484.9 |
| SDIF | +4.6% | 484.9 |
| CSV Bundle | +4.6% | 484.9 |
| SDIF AI | +4.8% | 484.9 |

## Methodology

- Mutation: first `10%` of leaves (sorted by key path) are changed.
  - Strings: append `-v2`.
  - Numbers: multiply by `1.1`.
  - Booleans: flip.
- **Token delta**: `tokens(mutated) - tokens(original)` — full-document resend model.
- **Diff lines**: unified diff added + removed lines — format-level verbosity in patches.
- This benchmark does **not** measure SDIF semantic delta encoding (`kind Delta`), which
  would transmit only changed fields as a patch. That is a separate benchmark.
