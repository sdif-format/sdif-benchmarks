# SDIF Context Packing Benchmark — Summary

- Generated at: `2026-05-23T19:39:59Z`
- Tokenizer: `tiktoken/cl100k_base`
- Documents: `20`
- Budgets: `4K`, `8K`, `32K`, `128K` tokens

## Key Finding

- **SDIF AI** is the most compact format: avg 44741 tokens (64.6% of JSON Compact).

## Fit Rate: % of 20 documents that fit at least once

| Format | Avg tokens | vs JSON | `4K` | `8K` | `32K` | `128K` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SDIF AI | 44741 | 64.6% | 35% | 35% | 60% | 90% |
| CSV Bundle | 45207 | 65.3% | 35% | 35% | 60% | 90% |
| SDIF | 47248 | 68.2% | 35% | 35% | 60% | 90% |
| TOON | 47769 | 69.0% | 35% | 35% | 60% | 90% |
| JSON Compact | 69248 | 100.0% | 35% | 35% | 45% | 70% |
| YAML | 78747 | 113.7% | 35% | 35% | 40% | 65% |
| JSON Pretty | 105691 | 152.6% | 35% | 35% | 35% | 65% |
| XML | 127520 | 184.1% | 35% | 35% | 35% | 65% |

## Avg documents per context budget

| Format | `4K` | `8K` | `32K` | `128K` |
| --- | ---: | ---: | ---: | ---: |
| SDIF AI | 5.2 | 10.5 | 42.9 | 172.9 |
| CSV Bundle | 4.5 | 9.1 | 37.0 | 149.0 |
| SDIF | 4.9 | 10.0 | 40.6 | 163.3 |
| TOON | 4.4 | 9.1 | 37.0 | 149.2 |
| JSON Compact | 3.5 | 7.2 | 29.2 | 118.4 |
| YAML | 3.1 | 6.5 | 26.4 | 106.3 |
| JSON Pretty | 2.0 | 4.3 | 17.5 | 71.2 |
| XML | 1.6 | 3.4 | 13.9 | 56.6 |

## Methodology

- All formats are derived from the same canonical `equivalent.json` source.
- **Fit rate**: % of corpus documents where `floor(budget / tokens) >= 1`.
- **Avg docs**: mean number of copies that fit per document across the corpus.
- Tokenizer: `tiktoken/cl100k_base`.
- Ratios computed against JSON Compact as the stable baseline.
