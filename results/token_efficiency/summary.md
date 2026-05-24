# SDIF Benchmark Summary

- Generated at: `2026-05-24T12:15:24Z`
- Run directory: `results/token_efficiency`
- Full report: `results/token_efficiency/comparison.md`
- Structured JSON: `results/token_efficiency/comparison.json`
- Structured SDIF: `results/token_efficiency/comparison.sdif`
- SDIF AI projection: `results/token_efficiency/comparison.sdif.ai`
- Raw log: `results/token_efficiency/comparison.log`
- Documents compared: `24`
- Available tokenizers: `Estimate, TokenX, tiktoken`

## Key Findings

- Best consensus format: **SDIF AI** (avg rank `1.15`, median ratio `57.2%`, coverage `72/72`).
- Ratios are computed independently per tokenizer against `JSON Compact`.
- `Estimate` winners: SDIF AI 21/24, SDIF 2/24, CSV Bundle 1/24.
- `TokenX` winners: SDIF AI 19/24, SDIF 5/24.
- `tiktoken` winners: SDIF AI 21/24, CSV Bundle 3/24.

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
| SDIF AI | 1.15 | 57.2% | 26.3% | 83.1% | 1 | 72/72 |
| SDIF | 2.43 | 60.0% | 26.3% | 83.4% | 3 | 72/72 |
| CSV Bundle | 2.89 | 62.3% | 28.7% | 95.4% | 3 | 72/72 |
| TOON | 3.53 | 63.9% | 29.4% | 91.4% | 1 | 72/72 |
| YAML | 5.35 | 95.1% | 75.7% | 137.8% | 1 | 72/72 |
| JSON Compact | 5.65 | 100.0% | 100.0% | 100.0% | 1 | 72/72 |
| JSON Pretty | 7.00 | 141.6% | 100.7% | 192.5% | 0 | 72/72 |
| XML | 8.00 | 176.6% | 141.5% | 229.8% | 0 | 72/72 |

## Direct Comparison

Focused comparison of the main formats a reader is most likely to care about.

| Format | Consensus Avg Rank | Consensus Median Ratio | Wins Across Tokenizer/Document Pairs | `Estimate` Avg Ratio | `TokenX` Avg Ratio | `tiktoken` Avg Ratio |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 1.15 | 57.2% | 61 | 56.6% | 49.9% | 65.5% |
| SDIF | 2.43 | 60.0% | 7 | 58.2% | 49.8% | 68.9% |
| TOON | 3.53 | 63.9% | 0 | 59.0% | 60.4% | 72.0% |
| CSV Bundle | 2.89 | 62.3% | 4 | 58.0% | 61.1% | 69.9% |
| JSON Compact | 5.65 | 100.0% | 0 | 100.0% | 100.0% | 100.0% |

## Artifacts

- Full benchmark report: `results/token_efficiency/comparison.md`
- Structured JSON report: `results/token_efficiency/comparison.json`
- Structured SDIF report: `results/token_efficiency/comparison.sdif`
- SDIF AI projection: `results/token_efficiency/comparison.sdif.ai`
- Raw benchmark log: `results/token_efficiency/comparison.log`
- Compared corpus files: `results/token_efficiency/corpus`
- Result directory: `results/token_efficiency`
