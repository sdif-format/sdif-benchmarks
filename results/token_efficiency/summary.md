# SDIF Benchmark Summary

- Generated at: `2026-05-23T21:25:50Z`
- Run directory: `results/token_efficiency`
- Full report: `results/token_efficiency/comparison.md`
- Structured JSON: `results/token_efficiency/comparison.json`
- Structured SDIF: `results/token_efficiency/comparison.sdif`
- SDIF AI projection: `results/token_efficiency/comparison.sdif.ai`
- Raw log: `results/token_efficiency/comparison.log`
- Documents compared: `20`
- Available tokenizers: `Estimate, TokenX, tiktoken`

## Key Findings

- Best consensus format: **SDIF AI** (avg rank `1.10`, median ratio `56.6%`, coverage `60/60`).
- Ratios are computed independently per tokenizer against `JSON Compact`.
- `Estimate` winners: SDIF AI 18/20, CSV Bundle 1/20, SDIF 1/20.
- `TokenX` winners: SDIF AI 19/20, SDIF 1/20.
- `tiktoken` winners: SDIF AI 17/20, CSV Bundle 3/20.

## Tokenizer Availability

| Tokenizer | Status | Type | Notes |
| --- | --- | --- | --- |
| `Estimate` | available | heuristic | Deterministic fallback: 4 UTF-8 bytes per token. |
| `TokenX` | available | heuristic | Resolved through Node.js, local/global npm, or npx fallback. |
| `tiktoken` | available | model tokenizer | Encoding: cl100k_base. |
| `Llama3` | disabled | model tokenizer | Disabled through SDIF_BENCHMARK_LLAMA=0. |
| `Claude` | disabled | API tokenizer | Disabled. Set SDIF_BENCHMARK_CLAUDE=1 to enable API token counting. |

## Consensus Ranking

| Format | Avg Rank | Median Ratio | Best Ratio | Worst Ratio | Rank Spread | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SDIF AI | 1.10 | 56.6% | 26.3% | 83.1% | 1 | 60/60 |
| SDIF | 2.60 | 59.5% | 26.3% | 83.4% | 3 | 60/60 |
| CSV Bundle | 2.72 | 60.9% | 28.7% | 95.4% | 3 | 60/60 |
| TOON | 3.58 | 62.5% | 29.4% | 91.4% | 1 | 60/60 |
| YAML | 5.35 | 95.3% | 75.7% | 137.8% | 1 | 60/60 |
| JSON Compact | 5.65 | 100.0% | 100.0% | 100.0% | 1 | 60/60 |
| JSON Pretty | 7.00 | 139.7% | 100.7% | 192.5% | 0 | 60/60 |
| XML | 8.00 | 171.9% | 141.5% | 229.8% | 0 | 60/60 |

## Direct Comparison

Focused comparison of the main formats a reader is most likely to care about.

| Format | Consensus Avg Rank | Consensus Median Ratio | Wins Across Tokenizer/Document Pairs | `Estimate` Avg Ratio | `TokenX` Avg Ratio | `tiktoken` Avg Ratio |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 1.10 | 56.6% | 54 | 55.7% | 49.1% | 64.3% |
| SDIF | 2.60 | 59.5% | 2 | 57.6% | 49.3% | 68.0% |
| TOON | 3.58 | 62.5% | 0 | 58.1% | 59.6% | 70.3% |
| CSV Bundle | 2.72 | 60.9% | 4 | 56.8% | 59.8% | 67.8% |
| JSON Compact | 5.65 | 100.0% | 0 | 100.0% | 100.0% | 100.0% |

## Artifacts

- Full benchmark report: `results/token_efficiency/comparison.md`
- Structured JSON report: `results/token_efficiency/comparison.json`
- Structured SDIF report: `results/token_efficiency/comparison.sdif`
- SDIF AI projection: `results/token_efficiency/comparison.sdif.ai`
- Raw benchmark log: `results/token_efficiency/comparison.log`
- Compared corpus files: `results/token_efficiency/corpus`
- Result directory: `results/token_efficiency`
