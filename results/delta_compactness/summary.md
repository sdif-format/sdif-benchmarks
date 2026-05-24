# SDIF Mutation Sensitivity Benchmark — Summary

> **Framing**: this benchmark measures full-document resend overhead after a 10% leaf mutation.
> It is not a semantic patch/delta benchmark; patch-only payloads should be measured separately.

- Generated at: `2026-05-24T20:38:06Z`
- Tokenizer: `tiktoken/cl100k_base`
- Mutation: `10%` of leaf values changed
- Documents: `24`

## Key Findings

A 10% leaf mutation provides a repeatable full-resend sensitivity baseline.
Token delta measures the cost of resending the whole mutated document, not the size of a semantic patch.
Diff-line counts are a coarse text-level signal and should not be interpreted as semantic delta size.

| Format | Avg Δ tokens % | Avg diff lines |
| --- | ---: | ---: |
| XML | +1.6% | 2365.0 |
| JSON Pretty | +1.9% | 2365.0 |
| YAML | +2.7% | 1569.1 |
| JSON Compact | +3.0% | 2.0 |
| TOON | +4.3% | 404.9 |
| CSV Bundle | +4.5% | 404.9 |
| SDIF | +4.6% | 404.9 |
| SDIF AI | +4.7% | 405.0 |

## Methodology

- Mutation: first `10%` of leaves (sorted by key path) are changed.
  - Strings: append `-v2`.
  - Numbers: multiply by `1.1`.
  - Booleans: flip.
- **Token delta**: `tokens(mutated) - tokens(original)` — full-document resend model.
- **Diff lines**: unified diff added + removed lines — coarse text-level churn, not semantic patch size.
- This benchmark does **not** measure SDIF semantic delta encoding (`kind Delta`).
- A dedicated delta benchmark should compare patch-only payloads separately from full-document resend.
