# SDIF Context Packing Benchmark — Summary

- Generated at: `2026-05-23T08:48:39Z`
- Tokenizer: `estimate (4 bytes/token)`
- Documents: `20`
- Budgets: `4K`, `8K`, `32K`, `128K` tokens

## Key Finding

- **CSV Bundle** is the most compact format: avg 35396 tokens (55.3% of JSON Compact).
- In an 8K context, CSV Bundle fits 40% of documents vs 35% for JSON Compact.

## Fit Rate: % of 20 documents that fit at least once

| Format | Avg tokens | vs JSON | `4K` | `8K` | `32K` | `128K` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CSV Bundle | 35396 | 55.3% | 35% | 40% | 60% | 100% |
| SDIF AI | 35463 | 55.4% | 35% | 40% | 60% | 100% |
| SDIF | 36664 | 57.3% | 35% | 40% | 60% | 100% |
| TOON | 36690 | 57.4% | 35% | 40% | 60% | 100% |
| YAML | 61708 | 96.5% | 35% | 35% | 55% | 80% |
| JSON Compact | 63957 | 100.0% | 35% | 35% | 55% | 80% |
| JSON Pretty | 88630 | 138.6% | 35% | 35% | 40% | 65% |
| XML | 108113 | 169.0% | 35% | 35% | 35% | 65% |

## Avg documents per context budget

| Format | `4K` | `8K` | `32K` | `128K` |
| --- | ---: | ---: | ---: | ---: |
| CSV Bundle | 4.9 | 10.0 | 41.0 | 165.6 |
| SDIF AI | 5.2 | 10.6 | 43.6 | 175.8 |
| SDIF | 5.1 | 10.3 | 42.2 | 170.2 |
| TOON | 5.0 | 10.1 | 41.1 | 166.2 |
| YAML | 3.5 | 7.2 | 29.6 | 119.4 |
| JSON Compact | 3.3 | 6.8 | 27.8 | 112.0 |
| JSON Pretty | 2.3 | 4.8 | 19.8 | 80.5 |
| XML | 1.8 | 3.8 | 16.1 | 65.2 |

## Methodology

- All formats are derived from the same canonical `equivalent.json` source.
- **Fit rate**: % of corpus documents where `floor(budget / tokens) >= 1`.
- **Avg docs**: mean number of copies that fit per document across the corpus.
- Tokenizer: `estimate (4 bytes/token)`.
- Ratios computed against JSON Compact as the stable baseline.
