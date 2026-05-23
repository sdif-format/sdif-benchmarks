# SDIF Benchmark Summary

- Generated at: `2026-05-23T08:48:14Z`
- Run directory: `results/token_efficiency`
- Full report: `results/token_efficiency/comparison.md`
- Structured JSON: `results/token_efficiency/comparison.json`
- Structured SDIF: `results/token_efficiency/comparison.sdif`
- SDIF AI projection: `results/token_efficiency/comparison.sdif.ai`
- Raw log: `results/token_efficiency/comparison.log`
- Documents compared: `20`
- Available tokenizers: `Estimate, TokenX`

## Key Findings

- Best consensus format: **SDIF AI** (avg rank `1.07`, median ratio `51.9%`, coverage `40/40`).
- Ratios are computed independently per tokenizer against `JSON Compact`.
- `Estimate` winners: SDIF AI 18/20, CSV Bundle 1/20, SDIF 1/20.
- `TokenX` winners: SDIF AI 19/20, SDIF 1/20.

## Tokenizer Availability

| Tokenizer | Status | Type | Notes |
| --- | --- | --- | --- |
| `Estimate` | available | heuristic | Deterministic fallback: 4 UTF-8 bytes per token. |
| `TokenX` | available | heuristic | Resolved through Node.js, local/global npm, or npx fallback. |
| `tiktoken` | unavailable | model tokenizer | Unavailable because Python package `tiktoken` is not installed. |
| `Llama3` | disabled | model tokenizer | Disabled through SDIF_BENCHMARK_LLAMA=0. |
| `Claude` | disabled | API tokenizer | Disabled. Set SDIF_BENCHMARK_CLAUDE=1 to enable API token counting. |

## Consensus Ranking

| Format | Avg Rank | Median Ratio | Best Ratio | Worst Ratio | Rank Spread | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SDIF AI | 1.07 | 51.9% | 26.3% | 78.9% | 1 | 40/40 |
| SDIF | 2.42 | 53.9% | 26.3% | 77.6% | 3 | 40/40 |
| CSV Bundle | 2.95 | 56.9% | 28.7% | 83.3% | 3 | 40/40 |
| TOON | 3.55 | 56.8% | 29.4% | 79.2% | 1 | 40/40 |
| YAML | 5.03 | 91.5% | 75.7% | 108.4% | 1 | 40/40 |
| JSON Compact | 5.97 | 100.0% | 100.0% | 100.0% | 1 | 40/40 |
| JSON Pretty | 7.00 | 116.4% | 100.7% | 192.5% | 0 | 40/40 |
| XML | 8.00 | 164.8% | 141.5% | 229.8% | 0 | 40/40 |

## Direct Comparison

Focused comparison of the main formats a reader is most likely to care about.

| Format | Consensus Avg Rank | Consensus Median Ratio | Wins Across Tokenizer/Document Pairs | `Estimate` Avg Ratio | `TokenX` Avg Ratio |
| --- | ---: |---:|---:|---:|---:|
| SDIF AI | 1.07 | 51.9% | 37 | 55.7% | 49.1% |
| SDIF | 2.42 | 53.9% | 2 | 57.6% | 49.3% |
| TOON | 3.55 | 56.8% | 0 | 58.1% | 59.6% |
| CSV Bundle | 2.95 | 56.9% | 1 | 56.8% | 59.8% |
| JSON Compact | 5.97 | 100.0% | 0 | 100.0% | 100.0% |

## Artifacts

- Full benchmark report: `results/token_efficiency/comparison.md`
- Structured JSON report: `results/token_efficiency/comparison.json`
- Structured SDIF report: `results/token_efficiency/comparison.sdif`
- SDIF AI projection: `results/token_efficiency/comparison.sdif.ai`
- Raw benchmark log: `results/token_efficiency/comparison.log`
- Compared corpus files: `results/token_efficiency/corpus`
- Result directory: `results/token_efficiency`
