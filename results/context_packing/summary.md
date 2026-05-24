# SDIF Context Packing Benchmark — Summary

- Generated at: `2026-05-24T12:15:58Z`
- Tokenizer: `tiktoken/cl100k_base`
- Documents: `24`
- Budgets: `4K`, `8K`, `32K`, `128K` tokens

## Key Finding

- **SDIF AI** is the most compact format: avg 37326 tokens (64.6% of JSON Compact).

## Fit Rate: % of 24 documents that fit at least once

| Format | Avg tokens | vs JSON | `4K` | `8K` | `32K` | `128K` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SDIF AI | 37326 | 64.6% | 46% | 46% | 67% | 92% |
| CSV Bundle | 37720 | 65.3% | 46% | 46% | 67% | 92% |
| SDIF | 39417 | 68.2% | 46% | 46% | 67% | 92% |
| TOON | 39856 | 69.0% | 46% | 46% | 67% | 92% |
| JSON Compact | 57766 | 100.0% | 46% | 46% | 54% | 75% |
| YAML | 65688 | 113.7% | 46% | 46% | 50% | 71% |
| JSON Pretty | 88173 | 152.6% | 46% | 46% | 46% | 71% |
| XML | 106385 | 184.2% | 46% | 46% | 46% | 71% |

## Avg documents per context budget

| Format | `4K` | `8K` | `32K` | `128K` |
| --- | ---: | ---: | ---: | ---: |
| SDIF AI | 6.9 | 14.1 | 57.5 | 231.6 |
| CSV Bundle | 6.1 | 12.3 | 50.1 | 201.9 |
| SDIF | 6.6 | 13.5 | 55.0 | 221.2 |
| TOON | 6.0 | 12.3 | 50.1 | 201.4 |
| JSON Compact | 4.7 | 9.8 | 39.8 | 160.5 |
| YAML | 4.2 | 8.8 | 35.7 | 143.9 |
| JSON Pretty | 2.8 | 5.9 | 24.0 | 96.9 |
| XML | 2.2 | 4.6 | 19.2 | 78.0 |

## Methodology

- All formats are derived from the same canonical `equivalent.json` source.
- **Fit rate**: % of corpus documents where `floor(budget / tokens) >= 1`.
- **Avg docs**: mean number of copies that fit per document across the corpus.
- Tokenizer: `tiktoken/cl100k_base`.
- Ratios computed against JSON Compact as the stable baseline.
