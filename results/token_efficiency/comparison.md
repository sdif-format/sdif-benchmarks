# SDIF Benchmark Evidence Report

- Generated at: `2026-05-23T08:48:14Z`
- Run directory: `results/token_efficiency`
- Semantic source: `examples/golden/<document>/equivalent.json`
- Ratios are computed independently per tokenizer against `JSON Compact`.
- All formats are derived from the same canonical JSON semantic source.
- Console ordering tokenizer: `Estimate`
- `.env` loaded: `yes`

## Executive Summary

### Tokenizer Availability

| Tokenizer | Status | Type | Notes |
| --- | --- | --- | --- |
| `Estimate` | available | heuristic | Deterministic fallback: 4 UTF-8 bytes per token. |
| `TokenX` | available | heuristic | Resolved through Node.js, local/global npm, or npx fallback. |
| `tiktoken` | unavailable | model tokenizer | Unavailable because Python package `tiktoken` is not installed. |
| `Llama3` | disabled | model tokenizer | Disabled through SDIF_BENCHMARK_LLAMA=0. |
| `Claude` | disabled | API tokenizer | Disabled. Set SDIF_BENCHMARK_CLAUDE=1 to enable API token counting. |

### Consensus Ranking

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

### Winners by Tokenizer

| Tokenizer | Winner Format | Wins | Documents |
| --- | --- | ---: | ---: |
| `Estimate` | SDIF AI | 18 | 20 |
| `Estimate` | CSV Bundle | 1 | 20 |
| `Estimate` | SDIF | 1 | 20 |
| `TokenX` | SDIF AI | 19 | 20 |
| `TokenX` | SDIF | 1 | 20 |

## Tokenizer Results

### `Estimate`

#### Summary

| Format | Avg Rank | Avg Ratio | Median Ratio | Avg Saved Tokens | Wins | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SDIF AI | 1.10 | 55.7% | 53.6% | 28495 | 18 | 20/20 |
| CSV Bundle | 2.25 | 56.8% | 54.7% | 28561 | 1 | 20/20 |
| SDIF | 2.90 | 57.6% | 55.4% | 27293 | 1 | 20/20 |
| TOON | 3.75 | 58.1% | 55.8% | 27268 | 0 | 20/20 |
| YAML | 5.05 | 96.0% | 95.3% | 2250 | 0 | 20/20 |
| JSON Compact | 5.95 | 100.0% | 100.0% | 0 | 0 | 20/20 |
| JSON Pretty | 7.00 | 142.9% | 139.7% | -24673 | 0 | 20/20 |
| XML | 8.00 | 174.5% | 170.5% | -44156 | 0 | 20/20 |

#### Per-document Ranking

| Document | Rank | Format | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| `deep-hierarchy-project` | 1 | SDIF AI | 73179 | 118574 | 45395 | 61.7% |
| `deep-hierarchy-project` | 2 | CSV Bundle | 73189 | 118574 | 45385 | 61.7% |
| `deep-hierarchy-project` | 3 | SDIF | 75551 | 118574 | 43023 | 63.7% |
| `deep-hierarchy-project` | 4 | TOON | 75554 | 118574 | 43020 | 63.7% |
| `deep-hierarchy-project` | 5 | YAML | 113041 | 118574 | 5533 | 95.3% |
| `deep-hierarchy-project` | 6 | JSON Compact | 118574 | 118574 | 0 | 100.0% |
| `deep-hierarchy-project` | 7 | JSON Pretty | 162017 | 118574 | -43443 | 136.6% |
| `deep-hierarchy-project` | 8 | XML | 192059 | 118574 | -73485 | 162.0% |
| `github.openapi` | 1 | SDIF AI | 41843 | 73106 | 31263 | 57.2% |
| `github.openapi` | 2 | CSV Bundle | 41885 | 73106 | 31221 | 57.3% |
| `github.openapi` | 3 | SDIF | 43413 | 73106 | 29693 | 59.4% |
| `github.openapi` | 4 | TOON | 43613 | 73106 | 29493 | 59.7% |
| `github.openapi` | 5 | YAML | 70814 | 73106 | 2292 | 96.9% |
| `github.openapi` | 6 | JSON Compact | 73106 | 73106 | 0 | 100.0% |
| `github.openapi` | 7 | JSON Pretty | 96711 | 73106 | -23605 | 132.3% |
| `github.openapi` | 8 | XML | 118164 | 73106 | -45058 | 161.6% |
| `large-knowledge-graph` | 1 | SDIF AI | 69895 | 129721 | 59826 | 53.9% |
| `large-knowledge-graph` | 2 | CSV Bundle | 69905 | 129721 | 59816 | 53.9% |
| `large-knowledge-graph` | 3 | TOON | 72242 | 129721 | 57479 | 55.7% |
| `large-knowledge-graph` | 4 | SDIF | 72311 | 129721 | 57410 | 55.7% |
| `large-knowledge-graph` | 5 | YAML | 123802 | 129721 | 5919 | 95.4% |
| `large-knowledge-graph` | 6 | JSON Compact | 129721 | 129721 | 0 | 100.0% |
| `large-knowledge-graph` | 7 | JSON Pretty | 183302 | 129721 | -53581 | 141.3% |
| `large-knowledge-graph` | 8 | XML | 221097 | 129721 | -91376 | 170.4% |
| `large-plan` | 1 | SDIF AI | 123089 | 201176 | 78087 | 61.2% |
| `large-plan` | 2 | CSV Bundle | 123104 | 201176 | 78072 | 61.2% |
| `large-plan` | 3 | SDIF | 126199 | 201176 | 74977 | 62.7% |
| `large-plan` | 4 | TOON | 126205 | 201176 | 74971 | 62.7% |
| `large-plan` | 5 | YAML | 195083 | 201176 | 6093 | 97.0% |
| `large-plan` | 6 | JSON Compact | 201176 | 201176 | 0 | 100.0% |
| `large-plan` | 7 | JSON Pretty | 262124 | 201176 | -60948 | 130.3% |
| `large-plan` | 8 | XML | 318407 | 201176 | -117231 | 158.3% |
| `large-registry` | 1 | SDIF AI | 100680 | 220956 | 120276 | 45.6% |
| `large-registry` | 2 | CSV Bundle | 100693 | 220956 | 120263 | 45.6% |
| `large-registry` | 3 | SDIF | 106542 | 220956 | 114414 | 48.2% |
| `large-registry` | 4 | TOON | 106547 | 220956 | 114409 | 48.2% |
| `large-registry` | 5 | YAML | 209988 | 220956 | 10968 | 95.0% |
| `large-registry` | 6 | JSON Compact | 220956 | 220956 | 0 | 100.0% |
| `large-registry` | 7 | JSON Pretty | 321329 | 220956 | -100373 | 145.4% |
| `large-registry` | 8 | XML | 413066 | 220956 | -192110 | 186.9% |
| `large-schema-catalog` | 1 | CSV Bundle | 53815 | 111880 | 58065 | 48.1% |
| `large-schema-catalog` | 2 | SDIF AI | 55400 | 111880 | 56480 | 49.5% |
| `large-schema-catalog` | 3 | SDIF | 57239 | 111880 | 54641 | 51.2% |
| `large-schema-catalog` | 4 | TOON | 57282 | 111880 | 54598 | 51.2% |
| `large-schema-catalog` | 5 | YAML | 108758 | 111880 | 3122 | 97.2% |
| `large-schema-catalog` | 6 | JSON Compact | 111880 | 111880 | 0 | 100.0% |
| `large-schema-catalog` | 7 | JSON Pretty | 163270 | 111880 | -51390 | 145.9% |
| `large-schema-catalog` | 8 | XML | 197509 | 111880 | -85629 | 176.5% |
| `large-support-export` | 1 | SDIF AI | 85512 | 148025 | 62513 | 57.8% |
| `large-support-export` | 2 | CSV Bundle | 85524 | 148025 | 62501 | 57.8% |
| `large-support-export` | 3 | SDIF | 88110 | 148025 | 59915 | 59.5% |
| `large-support-export` | 4 | TOON | 88114 | 148025 | 59911 | 59.5% |
| `large-support-export` | 5 | YAML | 143347 | 148025 | 4678 | 96.8% |
| `large-support-export` | 6 | JSON Compact | 148025 | 148025 | 0 | 100.0% |
| `large-support-export` | 7 | JSON Pretty | 202532 | 148025 | -54507 | 136.8% |
| `large-support-export` | 8 | XML | 246683 | 148025 | -98658 | 166.6% |
| `large-validation-report` | 1 | SDIF AI | 95944 | 139832 | 43888 | 68.6% |
| `large-validation-report` | 2 | CSV Bundle | 95956 | 139832 | 43876 | 68.6% |
| `large-validation-report` | 3 | SDIF | 97634 | 139832 | 42198 | 69.8% |
| `large-validation-report` | 4 | TOON | 97917 | 139832 | 41915 | 70.0% |
| `large-validation-report` | 5 | YAML | 137495 | 139832 | 2337 | 98.3% |
| `large-validation-report` | 6 | JSON Compact | 139832 | 139832 | 0 | 100.0% |
| `large-validation-report` | 7 | JSON Pretty | 177596 | 139832 | -37764 | 127.0% |
| `large-validation-report` | 8 | XML | 204665 | 139832 | -64833 | 146.4% |
| `medium-invoice-batch` | 1 | SDIF AI | 18476 | 34890 | 16414 | 53.0% |
| `medium-invoice-batch` | 2 | CSV Bundle | 18486 | 34890 | 16404 | 53.0% |
| `medium-invoice-batch` | 3 | SDIF | 18965 | 34890 | 15925 | 54.4% |
| `medium-invoice-batch` | 4 | TOON | 18967 | 34890 | 15923 | 54.4% |
| `medium-invoice-batch` | 5 | YAML | 34258 | 34890 | 632 | 98.2% |
| `medium-invoice-batch` | 6 | JSON Compact | 34890 | 34890 | 0 | 100.0% |
| `medium-invoice-batch` | 7 | JSON Pretty | 47898 | 34890 | -13008 | 137.3% |
| `medium-invoice-batch` | 8 | XML | 59542 | 34890 | -24652 | 170.7% |
| `medium-observability-run` | 1 | SDIF AI | 13983 | 28689 | 14706 | 48.7% |
| `medium-observability-run` | 2 | CSV Bundle | 13995 | 28689 | 14694 | 48.8% |
| `medium-observability-run` | 3 | SDIF | 14595 | 28689 | 14094 | 50.9% |
| `medium-observability-run` | 4 | TOON | 14598 | 28689 | 14091 | 50.9% |
| `medium-observability-run` | 5 | YAML | 27275 | 28689 | 1414 | 95.1% |
| `medium-observability-run` | 6 | JSON Compact | 28689 | 28689 | 0 | 100.0% |
| `medium-observability-run` | 7 | JSON Pretty | 41996 | 28689 | -13307 | 146.4% |
| `medium-observability-run` | 8 | XML | 51497 | 28689 | -22808 | 179.5% |
| `medium-policy-catalog` | 1 | SDIF AI | 12446 | 24394 | 11948 | 51.0% |
| `medium-policy-catalog` | 2 | CSV Bundle | 12456 | 24394 | 11938 | 51.1% |
| `medium-policy-catalog` | 3 | SDIF | 12918 | 24394 | 11476 | 53.0% |
| `medium-policy-catalog` | 4 | TOON | 12920 | 24394 | 11474 | 53.0% |
| `medium-policy-catalog` | 5 | YAML | 22907 | 24394 | 1487 | 93.9% |
| `medium-policy-catalog` | 6 | JSON Compact | 24394 | 24394 | 0 | 100.0% |
| `medium-policy-catalog` | 7 | JSON Pretty | 34838 | 24394 | -10444 | 142.8% |
| `medium-policy-catalog` | 8 | XML | 41875 | 24394 | -17481 | 171.7% |
| `medium-product-catalog` | 1 | SDIF AI | 11888 | 27843 | 15955 | 42.7% |
| `medium-product-catalog` | 2 | CSV Bundle | 11900 | 27843 | 15943 | 42.7% |
| `medium-product-catalog` | 3 | SDIF | 12696 | 27843 | 15147 | 45.6% |
| `medium-product-catalog` | 4 | TOON | 12700 | 27843 | 15143 | 45.6% |
| `medium-product-catalog` | 5 | YAML | 26180 | 27843 | 1663 | 94.0% |
| `medium-product-catalog` | 6 | JSON Compact | 27843 | 27843 | 0 | 100.0% |
| `medium-product-catalog` | 7 | JSON Pretty | 42264 | 27843 | -14421 | 151.8% |
| `medium-product-catalog` | 8 | XML | 53712 | 27843 | -25869 | 192.9% |
| `plan` | 1 | SDIF | 246 | 317 | 71 | 77.6% |
| `plan` | 2 | SDIF AI | 250 | 317 | 67 | 78.9% |
| `plan` | 3 | TOON | 251 | 317 | 66 | 79.2% |
| `plan` | 4 | CSV Bundle | 260 | 317 | 57 | 82.0% |
| `plan` | 5 | YAML | 300 | 317 | 17 | 94.6% |
| `plan` | 6 | JSON Compact | 317 | 317 | 0 | 100.0% |
| `plan` | 7 | JSON Pretty | 422 | 317 | -105 | 133.1% |
| `plan` | 8 | XML | 520 | 317 | -203 | 164.0% |
| `registry` | 1 | SDIF AI | 166 | 240 | 74 | 69.2% |
| `registry` | 2 | SDIF | 169 | 240 | 71 | 70.4% |
| `registry` | 3 | TOON | 175 | 240 | 65 | 72.9% |
| `registry` | 4 | CSV Bundle | 180 | 240 | 60 | 75.0% |
| `registry` | 5 | YAML | 224 | 240 | 16 | 93.3% |
| `registry` | 6 | JSON Compact | 240 | 240 | 0 | 100.0% |
| `registry` | 7 | JSON Pretty | 324 | 240 | -84 | 135.0% |
| `registry` | 8 | XML | 401 | 240 | -161 | 167.1% |
| `schema` | 1 | SDIF AI | 275 | 529 | 254 | 52.0% |
| `schema` | 2 | CSV Bundle | 291 | 529 | 238 | 55.0% |
| `schema` | 3 | SDIF | 291 | 529 | 238 | 55.0% |
| `schema` | 4 | TOON | 296 | 529 | 233 | 56.0% |
| `schema` | 5 | YAML | 501 | 529 | 28 | 94.7% |
| `schema` | 6 | JSON Compact | 529 | 529 | 0 | 100.0% |
| `schema` | 7 | JSON Pretty | 809 | 529 | -280 | 152.9% |
| `schema` | 8 | XML | 1048 | 529 | -519 | 198.1% |
| `small-api-catalog` | 1 | SDIF AI | 410 | 791 | 381 | 51.8% |
| `small-api-catalog` | 2 | CSV Bundle | 417 | 791 | 374 | 52.7% |
| `small-api-catalog` | 3 | SDIF | 429 | 791 | 362 | 54.2% |
| `small-api-catalog` | 4 | TOON | 430 | 791 | 361 | 54.4% |
| `small-api-catalog` | 5 | YAML | 728 | 791 | 63 | 92.0% |
| `small-api-catalog` | 6 | JSON Compact | 791 | 791 | 0 | 100.0% |
| `small-api-catalog` | 7 | JSON Pretty | 1213 | 791 | -422 | 153.4% |
| `small-api-catalog` | 8 | XML | 1412 | 791 | -621 | 178.5% |
| `small-incident` | 1 | SDIF AI | 641 | 1037 | 396 | 61.8% |
| `small-incident` | 2 | CSV Bundle | 649 | 1037 | 388 | 62.6% |
| `small-incident` | 3 | SDIF | 660 | 1037 | 377 | 63.6% |
| `small-incident` | 4 | TOON | 660 | 1037 | 377 | 63.6% |
| `small-incident` | 5 | YAML | 987 | 1037 | 50 | 95.2% |
| `small-incident` | 6 | JSON Compact | 1037 | 1037 | 0 | 100.0% |
| `small-incident` | 7 | JSON Pretty | 1432 | 1037 | -395 | 138.1% |
| `small-incident` | 8 | XML | 1702 | 1037 | -665 | 164.1% |
| `small-invoice` | 1 | SDIF AI | 352 | 661 | 309 | 53.3% |
| `small-invoice` | 2 | CSV Bundle | 360 | 661 | 301 | 54.5% |
| `small-invoice` | 3 | SDIF | 364 | 661 | 297 | 55.1% |
| `small-invoice` | 4 | TOON | 365 | 661 | 296 | 55.2% |
| `small-invoice` | 5 | YAML | 635 | 661 | 26 | 96.1% |
| `small-invoice` | 6 | JSON Compact | 661 | 661 | 0 | 100.0% |
| `small-invoice` | 7 | JSON Pretty | 941 | 661 | -280 | 142.4% |
| `small-invoice` | 8 | XML | 1185 | 661 | -524 | 179.3% |
| `validation-report` | 1 | SDIF AI | 173 | 254 | 81 | 68.1% |
| `validation-report` | 2 | SDIF | 184 | 254 | 70 | 72.4% |
| `validation-report` | 3 | TOON | 193 | 254 | 61 | 76.0% |
| `validation-report` | 4 | CSV Bundle | 194 | 254 | 60 | 76.4% |
| `validation-report` | 5 | YAML | 234 | 254 | 20 | 92.1% |
| `validation-report` | 6 | JSON Compact | 254 | 254 | 0 | 100.0% |
| `validation-report` | 7 | JSON Pretty | 345 | 254 | -91 | 135.8% |
| `validation-report` | 8 | XML | 422 | 254 | -168 | 166.1% |
| `wide-table-survey` | 1 | SDIF AI | 4652 | 16230 | 11578 | 28.7% |
| `wide-table-survey` | 2 | CSV Bundle | 4658 | 16230 | 11572 | 28.7% |
| `wide-table-survey` | 3 | TOON | 4764 | 16230 | 11466 | 29.4% |
| `wide-table-survey` | 4 | SDIF | 4764 | 16230 | 11466 | 29.4% |
| `wide-table-survey` | 5 | JSON Compact | 16230 | 16230 | 0 | 100.0% |
| `wide-table-survey` | 6 | YAML | 17594 | 16230 | -1364 | 108.4% |
| `wide-table-survey` | 7 | JSON Pretty | 31238 | 16230 | -15008 | 192.5% |
| `wide-table-survey` | 8 | XML | 37292 | 16230 | -21062 | 229.8% |

### `TokenX`

#### Summary

| Format | Avg Rank | Avg Ratio | Median Ratio | Avg Saved Tokens | Wins | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SDIF AI | 1.05 | 49.1% | 47.2% | 42161 | 19 | 20/20 |
| SDIF | 1.95 | 49.3% | 47.3% | 42157 | 1 | 20/20 |
| TOON | 3.35 | 59.6% | 57.3% | 35169 | 0 | 20/20 |
| CSV Bundle | 3.65 | 59.8% | 57.3% | 35491 | 0 | 20/20 |
| YAML | 5.00 | 84.0% | 84.3% | 11718 | 0 | 20/20 |
| JSON Compact | 6.00 | 100.0% | 100.0% | 0 | 0 | 20/20 |
| JSON Pretty | 7.00 | 103.2% | 103.0% | -2361 | 0 | 20/20 |
| XML | 8.00 | 159.8% | 158.0% | -45867 | 0 | 20/20 |

#### Per-document Ranking

| Document | Rank | Format | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| `deep-hierarchy-project` | 1 | SDIF AI | 81733 | 150426 | 68693 | 54.3% |
| `deep-hierarchy-project` | 2 | SDIF | 81738 | 150426 | 68688 | 54.3% |
| `deep-hierarchy-project` | 3 | CSV Bundle | 91221 | 150426 | 59205 | 60.6% |
| `deep-hierarchy-project` | 4 | TOON | 91221 | 150426 | 59205 | 60.6% |
| `deep-hierarchy-project` | 5 | YAML | 125936 | 150426 | 24490 | 83.7% |
| `deep-hierarchy-project` | 6 | JSON Compact | 150426 | 150426 | 0 | 100.0% |
| `deep-hierarchy-project` | 7 | JSON Pretty | 155171 | 150426 | -4745 | 103.2% |
| `deep-hierarchy-project` | 8 | XML | 219188 | 150426 | -68762 | 145.7% |
| `github.openapi` | 1 | SDIF AI | 46327 | 90705 | 44378 | 51.1% |
| `github.openapi` | 2 | SDIF | 46333 | 90705 | 44372 | 51.1% |
| `github.openapi` | 3 | CSV Bundle | 52839 | 90705 | 37866 | 58.3% |
| `github.openapi` | 4 | TOON | 53807 | 90705 | 36898 | 59.3% |
| `github.openapi` | 5 | YAML | 77837 | 90705 | 12868 | 85.8% |
| `github.openapi` | 6 | JSON Compact | 90705 | 90705 | 0 | 100.0% |
| `github.openapi` | 7 | JSON Pretty | 92880 | 90705 | -2175 | 102.4% |
| `github.openapi` | 8 | XML | 135694 | 90705 | -44989 | 149.6% |
| `large-knowledge-graph` | 1 | SDIF AI | 73765 | 157533 | 83768 | 46.8% |
| `large-knowledge-graph` | 2 | SDIF | 73770 | 157533 | 83763 | 46.8% |
| `large-knowledge-graph` | 3 | TOON | 89415 | 157533 | 68118 | 56.8% |
| `large-knowledge-graph` | 4 | CSV Bundle | 89705 | 157533 | 67828 | 56.9% |
| `large-knowledge-graph` | 5 | YAML | 129722 | 157533 | 27811 | 82.3% |
| `large-knowledge-graph` | 6 | JSON Compact | 157533 | 157533 | 0 | 100.0% |
| `large-knowledge-graph` | 7 | JSON Pretty | 162366 | 157533 | -4833 | 103.1% |
| `large-knowledge-graph` | 8 | XML | 245137 | 157533 | -87604 | 155.6% |
| `large-plan` | 1 | SDIF AI | 143535 | 255952 | 112417 | 56.1% |
| `large-plan` | 2 | SDIF | 143540 | 255952 | 112412 | 56.1% |
| `large-plan` | 3 | CSV Bundle | 159261 | 255952 | 96691 | 62.2% |
| `large-plan` | 4 | TOON | 159262 | 255952 | 96690 | 62.2% |
| `large-plan` | 5 | YAML | 229824 | 255952 | 26128 | 89.8% |
| `large-plan` | 6 | JSON Compact | 255952 | 255952 | 0 | 100.0% |
| `large-plan` | 7 | JSON Pretty | 262181 | 255952 | -6229 | 102.4% |
| `large-plan` | 8 | XML | 381913 | 255952 | -125961 | 149.2% |
| `large-registry` | 1 | SDIF AI | 148687 | 307177 | 158490 | 48.4% |
| `large-registry` | 2 | SDIF | 148692 | 307177 | 158485 | 48.4% |
| `large-registry` | 3 | CSV Bundle | 172514 | 307177 | 134663 | 56.2% |
| `large-registry` | 4 | TOON | 172514 | 307177 | 134663 | 56.2% |
| `large-registry` | 5 | YAML | 279687 | 307177 | 27490 | 91.1% |
| `large-registry` | 6 | JSON Compact | 307177 | 307177 | 0 | 100.0% |
| `large-registry` | 7 | JSON Pretty | 318906 | 307177 | -11729 | 103.8% |
| `large-registry` | 8 | XML | 528580 | 307177 | -221403 | 172.1% |
| `large-schema-catalog` | 1 | SDIF AI | 59885 | 146598 | 86713 | 40.8% |
| `large-schema-catalog` | 2 | SDIF | 59890 | 146598 | 86708 | 40.9% |
| `large-schema-catalog` | 3 | CSV Bundle | 77252 | 146598 | 69346 | 52.7% |
| `large-schema-catalog` | 4 | TOON | 77470 | 146598 | 69128 | 52.8% |
| `large-schema-catalog` | 5 | YAML | 119551 | 146598 | 27047 | 81.6% |
| `large-schema-catalog` | 6 | JSON Compact | 146598 | 146598 | 0 | 100.0% |
| `large-schema-catalog` | 7 | JSON Pretty | 150285 | 146598 | -3687 | 102.5% |
| `large-schema-catalog` | 8 | XML | 235160 | 146598 | -88562 | 160.4% |
| `large-support-export` | 1 | SDIF AI | 81684 | 188515 | 106831 | 43.3% |
| `large-support-export` | 2 | SDIF | 81689 | 188515 | 106826 | 43.3% |
| `large-support-export` | 3 | TOON | 94672 | 188515 | 93843 | 50.2% |
| `large-support-export` | 4 | CSV Bundle | 94673 | 188515 | 93842 | 50.2% |
| `large-support-export` | 5 | YAML | 149111 | 188515 | 39404 | 79.1% |
| `large-support-export` | 6 | JSON Compact | 188515 | 188515 | 0 | 100.0% |
| `large-support-export` | 7 | JSON Pretty | 193714 | 188515 | -5199 | 102.8% |
| `large-support-export` | 8 | XML | 276343 | 188515 | -87828 | 146.6% |
| `large-validation-report` | 1 | SDIF AI | 91318 | 160800 | 69482 | 56.8% |
| `large-validation-report` | 2 | SDIF | 91323 | 160800 | 69477 | 56.8% |
| `large-validation-report` | 3 | CSV Bundle | 100374 | 160800 | 60426 | 62.4% |
| `large-validation-report` | 4 | TOON | 105973 | 160800 | 54827 | 65.9% |
| `large-validation-report` | 5 | YAML | 142953 | 160800 | 17847 | 88.9% |
| `large-validation-report` | 6 | JSON Compact | 160800 | 160800 | 0 | 100.0% |
| `large-validation-report` | 7 | JSON Pretty | 164183 | 160800 | -3383 | 102.1% |
| `large-validation-report` | 8 | XML | 227604 | 160800 | -66804 | 141.5% |
| `medium-invoice-batch` | 1 | SDIF AI | 20702 | 45845 | 25143 | 45.2% |
| `medium-invoice-batch` | 2 | SDIF | 20707 | 45845 | 25138 | 45.2% |
| `medium-invoice-batch` | 3 | TOON | 24954 | 45845 | 20891 | 54.4% |
| `medium-invoice-batch` | 4 | CSV Bundle | 24956 | 45845 | 20889 | 54.4% |
| `medium-invoice-batch` | 5 | YAML | 39703 | 45845 | 6142 | 86.6% |
| `medium-invoice-batch` | 6 | JSON Compact | 45845 | 45845 | 0 | 100.0% |
| `medium-invoice-batch` | 7 | JSON Pretty | 46892 | 45845 | -1047 | 102.3% |
| `medium-invoice-batch` | 8 | XML | 72517 | 45845 | -26672 | 158.2% |
| `medium-observability-run` | 1 | SDIF AI | 16712 | 39221 | 22509 | 42.6% |
| `medium-observability-run` | 2 | SDIF | 16717 | 39221 | 22504 | 42.6% |
| `medium-observability-run` | 3 | TOON | 20632 | 39221 | 18589 | 52.6% |
| `medium-observability-run` | 4 | CSV Bundle | 20633 | 39221 | 18588 | 52.6% |
| `medium-observability-run` | 5 | YAML | 33200 | 39221 | 6021 | 84.6% |
| `medium-observability-run` | 6 | JSON Compact | 39221 | 39221 | 0 | 100.0% |
| `medium-observability-run` | 7 | JSON Pretty | 40448 | 39221 | -1227 | 103.1% |
| `medium-observability-run` | 8 | XML | 64697 | 39221 | -25476 | 165.0% |
| `medium-policy-catalog` | 1 | SDIF AI | 16021 | 33616 | 17595 | 47.7% |
| `medium-policy-catalog` | 2 | SDIF | 16026 | 33616 | 17590 | 47.7% |
| `medium-policy-catalog` | 3 | TOON | 19134 | 33616 | 14482 | 56.9% |
| `medium-policy-catalog` | 4 | CSV Bundle | 19136 | 33616 | 14480 | 56.9% |
| `medium-policy-catalog` | 5 | YAML | 27840 | 33616 | 5776 | 82.8% |
| `medium-policy-catalog` | 6 | JSON Compact | 33616 | 33616 | 0 | 100.0% |
| `medium-policy-catalog` | 7 | JSON Pretty | 34563 | 33616 | -947 | 102.8% |
| `medium-policy-catalog` | 8 | XML | 51599 | 33616 | -17983 | 153.5% |
| `medium-product-catalog` | 1 | SDIF AI | 14784 | 37474 | 22690 | 39.5% |
| `medium-product-catalog` | 2 | SDIF | 14789 | 37474 | 22685 | 39.5% |
| `medium-product-catalog` | 3 | TOON | 18377 | 37474 | 19097 | 49.0% |
| `medium-product-catalog` | 4 | CSV Bundle | 18378 | 37474 | 19096 | 49.0% |
| `medium-product-catalog` | 5 | YAML | 32289 | 37474 | 5185 | 86.2% |
| `medium-product-catalog` | 6 | JSON Compact | 37474 | 37474 | 0 | 100.0% |
| `medium-product-catalog` | 7 | JSON Pretty | 39094 | 37474 | -1620 | 104.3% |
| `medium-product-catalog` | 8 | XML | 66733 | 37474 | -29259 | 178.1% |
| `plan` | 1 | SDIF | 266 | 389 | 123 | 68.4% |
| `plan` | 2 | SDIF AI | 274 | 389 | 115 | 70.4% |
| `plan` | 3 | TOON | 307 | 389 | 82 | 78.9% |
| `plan` | 4 | CSV Bundle | 324 | 389 | 65 | 83.3% |
| `plan` | 5 | YAML | 333 | 389 | 56 | 85.6% |
| `plan` | 6 | JSON Compact | 389 | 389 | 0 | 100.0% |
| `plan` | 7 | JSON Pretty | 406 | 389 | -17 | 104.4% |
| `plan` | 8 | XML | 614 | 389 | -225 | 157.8% |
| `registry` | 1 | SDIF AI | 190 | 301 | 111 | 63.1% |
| `registry` | 2 | SDIF | 192 | 301 | 109 | 63.8% |
| `registry` | 3 | TOON | 227 | 301 | 74 | 75.4% |
| `registry` | 4 | CSV Bundle | 240 | 301 | 61 | 79.7% |
| `registry` | 5 | YAML | 255 | 301 | 46 | 84.7% |
| `registry` | 6 | JSON Compact | 301 | 301 | 0 | 100.0% |
| `registry` | 7 | JSON Pretty | 313 | 301 | -12 | 104.0% |
| `registry` | 8 | XML | 478 | 301 | -177 | 158.8% |
| `schema` | 1 | SDIF AI | 291 | 665 | 374 | 43.8% |
| `schema` | 2 | SDIF | 296 | 665 | 369 | 44.5% |
| `schema` | 3 | CSV Bundle | 384 | 665 | 281 | 57.7% |
| `schema` | 4 | TOON | 384 | 665 | 281 | 57.7% |
| `schema` | 5 | YAML | 554 | 665 | 111 | 83.3% |
| `schema` | 6 | JSON Compact | 665 | 665 | 0 | 100.0% |
| `schema` | 7 | JSON Pretty | 703 | 665 | -38 | 105.7% |
| `schema` | 8 | XML | 1242 | 665 | -577 | 186.8% |
| `small-api-catalog` | 1 | SDIF AI | 516 | 1126 | 610 | 45.8% |
| `small-api-catalog` | 2 | SDIF | 521 | 1126 | 605 | 46.3% |
| `small-api-catalog` | 3 | TOON | 624 | 1126 | 502 | 55.4% |
| `small-api-catalog` | 4 | CSV Bundle | 628 | 1126 | 498 | 55.8% |
| `small-api-catalog` | 5 | YAML | 876 | 1126 | 250 | 77.8% |
| `small-api-catalog` | 6 | JSON Compact | 1126 | 1126 | 0 | 100.0% |
| `small-api-catalog` | 7 | JSON Pretty | 1162 | 1126 | -36 | 103.2% |
| `small-api-catalog` | 8 | XML | 1742 | 1126 | -616 | 154.7% |
| `small-incident` | 1 | SDIF AI | 693 | 1304 | 611 | 53.1% |
| `small-incident` | 2 | SDIF | 698 | 1304 | 606 | 53.5% |
| `small-incident` | 3 | TOON | 824 | 1304 | 480 | 63.2% |
| `small-incident` | 4 | CSV Bundle | 827 | 1304 | 477 | 63.4% |
| `small-incident` | 5 | YAML | 1077 | 1304 | 227 | 82.6% |
| `small-incident` | 6 | JSON Compact | 1304 | 1304 | 0 | 100.0% |
| `small-incident` | 7 | JSON Pretty | 1341 | 1304 | -37 | 102.8% |
| `small-incident` | 8 | XML | 1968 | 1304 | -664 | 150.9% |
| `small-invoice` | 1 | SDIF AI | 391 | 848 | 457 | 46.1% |
| `small-invoice` | 2 | SDIF | 396 | 848 | 452 | 46.7% |
| `small-invoice` | 3 | TOON | 495 | 848 | 353 | 58.4% |
| `small-invoice` | 4 | CSV Bundle | 498 | 848 | 350 | 58.7% |
| `small-invoice` | 5 | YAML | 715 | 848 | 133 | 84.3% |
| `small-invoice` | 6 | JSON Compact | 848 | 848 | 0 | 100.0% |
| `small-invoice` | 7 | JSON Pretty | 872 | 848 | -24 | 102.8% |
| `small-invoice` | 8 | XML | 1443 | 848 | -595 | 170.2% |
| `validation-report` | 1 | SDIF AI | 180 | 300 | 120 | 60.0% |
| `validation-report` | 2 | SDIF | 190 | 300 | 110 | 63.3% |
| `validation-report` | 3 | TOON | 226 | 300 | 74 | 75.3% |
| `validation-report` | 4 | CSV Bundle | 228 | 300 | 72 | 76.0% |
| `validation-report` | 5 | YAML | 253 | 300 | 47 | 84.3% |
| `validation-report` | 6 | JSON Compact | 300 | 300 | 0 | 100.0% |
| `validation-report` | 7 | JSON Pretty | 316 | 300 | -16 | 105.3% |
| `validation-report` | 8 | XML | 494 | 300 | -194 | 164.7% |
| `wide-table-survey` | 1 | SDIF AI | 7878 | 29998 | 22120 | 26.3% |
| `wide-table-survey` | 2 | SDIF | 7883 | 29998 | 22115 | 26.3% |
| `wide-table-survey` | 3 | TOON | 14893 | 29998 | 15105 | 49.6% |
| `wide-table-survey` | 4 | CSV Bundle | 14897 | 29998 | 15101 | 49.7% |
| `wide-table-survey` | 5 | YAML | 22708 | 29998 | 7290 | 75.7% |
| `wide-table-survey` | 6 | JSON Compact | 29998 | 29998 | 0 | 100.0% |
| `wide-table-survey` | 7 | JSON Pretty | 30220 | 29998 | -222 | 100.7% |
| `wide-table-survey` | 8 | XML | 52992 | 29998 | -22994 | 176.7% |

### `tiktoken`

Unavailable. Unavailable because Python package `tiktoken` is not installed.

### `Llama3`

Disabled. Disabled through SDIF_BENCHMARK_LLAMA=0.

### `Claude`

Disabled. Disabled. Set SDIF_BENCHMARK_CLAUDE=1 to enable API token counting.

## Document Analysis

### `deep-hierarchy-project`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 73179 | 118574 | 45395 | 61.7% |
| `TokenX` | SDIF AI | 81733 | 150426 | 68693 | 54.3% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 61.7% | 54.3% |
| SDIF | 63.7% | 54.3% |
| CSV Bundle | 61.7% | 60.6% |
| TOON | 63.7% | 60.6% |
| YAML | 95.3% | 83.7% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 136.6% | 103.2% |
| XML | 162.0% | 145.7% |

### `github.openapi`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 41843 | 73106 | 31263 | 57.2% |
| `TokenX` | SDIF AI | 46327 | 90705 | 44378 | 51.1% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 57.2% | 51.1% |
| SDIF | 59.4% | 51.1% |
| CSV Bundle | 57.3% | 58.3% |
| TOON | 59.7% | 59.3% |
| YAML | 96.9% | 85.8% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 132.3% | 102.4% |
| XML | 161.6% | 149.6% |

### `large-knowledge-graph`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 69895 | 129721 | 59826 | 53.9% |
| `TokenX` | SDIF AI | 73765 | 157533 | 83768 | 46.8% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 53.9% | 46.8% |
| SDIF | 55.7% | 46.8% |
| CSV Bundle | 53.9% | 56.9% |
| TOON | 55.7% | 56.8% |
| YAML | 95.4% | 82.3% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 141.3% | 103.1% |
| XML | 170.4% | 155.6% |

### `large-plan`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 123089 | 201176 | 78087 | 61.2% |
| `TokenX` | SDIF AI | 143535 | 255952 | 112417 | 56.1% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 61.2% | 56.1% |
| SDIF | 62.7% | 56.1% |
| CSV Bundle | 61.2% | 62.2% |
| TOON | 62.7% | 62.2% |
| YAML | 97.0% | 89.8% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 130.3% | 102.4% |
| XML | 158.3% | 149.2% |

### `large-registry`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 100680 | 220956 | 120276 | 45.6% |
| `TokenX` | SDIF AI | 148687 | 307177 | 158490 | 48.4% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 45.6% | 48.4% |
| SDIF | 48.2% | 48.4% |
| CSV Bundle | 45.6% | 56.2% |
| TOON | 48.2% | 56.2% |
| YAML | 95.0% | 91.1% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 145.4% | 103.8% |
| XML | 186.9% | 172.1% |

### `large-schema-catalog`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | CSV Bundle | 53815 | 111880 | 58065 | 48.1% |
| `TokenX` | SDIF AI | 59885 | 146598 | 86713 | 40.8% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 49.5% | 40.8% |
| CSV Bundle | 48.1% | 52.7% |
| SDIF | 51.2% | 40.9% |
| TOON | 51.2% | 52.8% |
| YAML | 97.2% | 81.6% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 145.9% | 102.5% |
| XML | 176.5% | 160.4% |

### `large-support-export`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 85512 | 148025 | 62513 | 57.8% |
| `TokenX` | SDIF AI | 81684 | 188515 | 106831 | 43.3% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 57.8% | 43.3% |
| SDIF | 59.5% | 43.3% |
| CSV Bundle | 57.8% | 50.2% |
| TOON | 59.5% | 50.2% |
| YAML | 96.8% | 79.1% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 136.8% | 102.8% |
| XML | 166.6% | 146.6% |

### `large-validation-report`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 95944 | 139832 | 43888 | 68.6% |
| `TokenX` | SDIF AI | 91318 | 160800 | 69482 | 56.8% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 68.6% | 56.8% |
| SDIF | 69.8% | 56.8% |
| CSV Bundle | 68.6% | 62.4% |
| TOON | 70.0% | 65.9% |
| YAML | 98.3% | 88.9% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 127.0% | 102.1% |
| XML | 146.4% | 141.5% |

### `medium-invoice-batch`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 18476 | 34890 | 16414 | 53.0% |
| `TokenX` | SDIF AI | 20702 | 45845 | 25143 | 45.2% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 53.0% | 45.2% |
| SDIF | 54.4% | 45.2% |
| CSV Bundle | 53.0% | 54.4% |
| TOON | 54.4% | 54.4% |
| YAML | 98.2% | 86.6% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 137.3% | 102.3% |
| XML | 170.7% | 158.2% |

### `medium-observability-run`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 13983 | 28689 | 14706 | 48.7% |
| `TokenX` | SDIF AI | 16712 | 39221 | 22509 | 42.6% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 48.7% | 42.6% |
| SDIF | 50.9% | 42.6% |
| CSV Bundle | 48.8% | 52.6% |
| TOON | 50.9% | 52.6% |
| YAML | 95.1% | 84.6% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 146.4% | 103.1% |
| XML | 179.5% | 165.0% |

### `medium-policy-catalog`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 12446 | 24394 | 11948 | 51.0% |
| `TokenX` | SDIF AI | 16021 | 33616 | 17595 | 47.7% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 51.0% | 47.7% |
| SDIF | 53.0% | 47.7% |
| CSV Bundle | 51.1% | 56.9% |
| TOON | 53.0% | 56.9% |
| YAML | 93.9% | 82.8% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 142.8% | 102.8% |
| XML | 171.7% | 153.5% |

### `medium-product-catalog`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 11888 | 27843 | 15955 | 42.7% |
| `TokenX` | SDIF AI | 14784 | 37474 | 22690 | 39.5% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 42.7% | 39.5% |
| SDIF | 45.6% | 39.5% |
| CSV Bundle | 42.7% | 49.0% |
| TOON | 45.6% | 49.0% |
| YAML | 94.0% | 86.2% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 151.8% | 104.3% |
| XML | 192.9% | 178.1% |

### `plan`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF | 246 | 317 | 71 | 77.6% |
| `TokenX` | SDIF | 266 | 389 | 123 | 68.4% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF | 77.6% | 68.4% |
| SDIF AI | 78.9% | 70.4% |
| TOON | 79.2% | 78.9% |
| CSV Bundle | 82.0% | 83.3% |
| YAML | 94.6% | 85.6% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 133.1% | 104.4% |
| XML | 164.0% | 157.8% |

### `registry`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 166 | 240 | 74 | 69.2% |
| `TokenX` | SDIF AI | 190 | 301 | 111 | 63.1% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 69.2% | 63.1% |
| SDIF | 70.4% | 63.8% |
| TOON | 72.9% | 75.4% |
| CSV Bundle | 75.0% | 79.7% |
| YAML | 93.3% | 84.7% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 135.0% | 104.0% |
| XML | 167.1% | 158.8% |

### `schema`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 275 | 529 | 254 | 52.0% |
| `TokenX` | SDIF AI | 291 | 665 | 374 | 43.8% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 52.0% | 43.8% |
| SDIF | 55.0% | 44.5% |
| CSV Bundle | 55.0% | 57.7% |
| TOON | 56.0% | 57.7% |
| YAML | 94.7% | 83.3% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 152.9% | 105.7% |
| XML | 198.1% | 186.8% |

### `small-api-catalog`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 410 | 791 | 381 | 51.8% |
| `TokenX` | SDIF AI | 516 | 1126 | 610 | 45.8% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 51.8% | 45.8% |
| SDIF | 54.2% | 46.3% |
| CSV Bundle | 52.7% | 55.8% |
| TOON | 54.4% | 55.4% |
| YAML | 92.0% | 77.8% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 153.4% | 103.2% |
| XML | 178.5% | 154.7% |

### `small-incident`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 641 | 1037 | 396 | 61.8% |
| `TokenX` | SDIF AI | 693 | 1304 | 611 | 53.1% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 61.8% | 53.1% |
| SDIF | 63.6% | 53.5% |
| CSV Bundle | 62.6% | 63.4% |
| TOON | 63.6% | 63.2% |
| YAML | 95.2% | 82.6% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 138.1% | 102.8% |
| XML | 164.1% | 150.9% |

### `small-invoice`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 352 | 661 | 309 | 53.3% |
| `TokenX` | SDIF AI | 391 | 848 | 457 | 46.1% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 53.3% | 46.1% |
| SDIF | 55.1% | 46.7% |
| CSV Bundle | 54.5% | 58.7% |
| TOON | 55.2% | 58.4% |
| YAML | 96.1% | 84.3% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 142.4% | 102.8% |
| XML | 179.3% | 170.2% |

### `validation-report`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 173 | 254 | 81 | 68.1% |
| `TokenX` | SDIF AI | 180 | 300 | 120 | 60.0% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 68.1% | 60.0% |
| SDIF | 72.4% | 63.3% |
| TOON | 76.0% | 75.3% |
| CSV Bundle | 76.4% | 76.0% |
| YAML | 92.1% | 84.3% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 135.8% | 105.3% |
| XML | 166.1% | 164.7% |

### `wide-table-survey`

#### Winners by Tokenizer

| Tokenizer | Winner | Tokens | JSON Compact Tokens | Saved Tokens | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| `Estimate` | SDIF AI | 4652 | 16230 | 11578 | 28.7% |
| `TokenX` | SDIF AI | 7878 | 29998 | 22120 | 26.3% |

#### Ratio Matrix

| Format | `Estimate` | `TokenX` |
|---|---:|---:|
| SDIF AI | 28.7% | 26.3% |
| SDIF | 29.4% | 26.3% |
| CSV Bundle | 28.7% | 49.7% |
| TOON | 29.4% | 49.6% |
| YAML | 108.4% | 75.7% |
| JSON Compact | 100.0% | 100.0% |
| JSON Pretty | 192.5% | 100.7% |
| XML | 229.8% | 176.7% |

## Raw Count Matrix

This section contains raw counts only. Ratios are intentionally excluded here because they are tokenizer-specific.

### `deep-hierarchy-project`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 292716 | 73179 | 81733 | - | - | - |
| CSV Bundle | 292754 | 73189 | 91221 | - | - | - |
| SDIF | 302202 | 75551 | 81738 | - | - | - |
| TOON | 302214 | 75554 | 91221 | - | - | - |
| YAML | 452163 | 113041 | 125936 | - | - | - |
| JSON Compact | 474294 | 118574 | 150426 | - | - | - |
| JSON Pretty | 648068 | 162017 | 155171 | - | - | - |
| XML | 768236 | 192059 | 219188 | - | - | - |

### `github.openapi`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 167369 | 41843 | 46327 | - | - | - |
| CSV Bundle | 167539 | 41885 | 52839 | - | - | - |
| SDIF | 173649 | 43413 | 46333 | - | - | - |
| TOON | 174452 | 43613 | 53807 | - | - | - |
| YAML | 283256 | 70814 | 77837 | - | - | - |
| JSON Compact | 292422 | 73106 | 90705 | - | - | - |
| JSON Pretty | 386842 | 96711 | 92880 | - | - | - |
| XML | 472655 | 118164 | 135694 | - | - | - |

### `large-knowledge-graph`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 279580 | 69895 | 73765 | - | - | - |
| CSV Bundle | 279620 | 69905 | 89705 | - | - | - |
| TOON | 288966 | 72242 | 89415 | - | - | - |
| SDIF | 289242 | 72311 | 73770 | - | - | - |
| YAML | 495208 | 123802 | 129722 | - | - | - |
| JSON Compact | 518882 | 129721 | 157533 | - | - | - |
| JSON Pretty | 733208 | 183302 | 162366 | - | - | - |
| XML | 884387 | 221097 | 245137 | - | - | - |

### `large-plan`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 492354 | 123089 | 143535 | - | - | - |
| CSV Bundle | 492413 | 123104 | 159261 | - | - | - |
| SDIF | 504796 | 126199 | 143540 | - | - | - |
| TOON | 504817 | 126205 | 159262 | - | - | - |
| YAML | 780329 | 195083 | 229824 | - | - | - |
| JSON Compact | 804703 | 201176 | 255952 | - | - | - |
| JSON Pretty | 1048494 | 262124 | 262181 | - | - | - |
| XML | 1273626 | 318407 | 381913 | - | - | - |

### `large-registry`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 402720 | 100680 | 148687 | - | - | - |
| CSV Bundle | 402772 | 100693 | 172514 | - | - | - |
| SDIF | 426166 | 106542 | 148692 | - | - | - |
| TOON | 426185 | 106547 | 172514 | - | - | - |
| YAML | 839949 | 209988 | 279687 | - | - | - |
| JSON Compact | 883824 | 220956 | 307177 | - | - | - |
| JSON Pretty | 1285316 | 321329 | 318906 | - | - | - |
| XML | 1652261 | 413066 | 528580 | - | - | - |

### `large-schema-catalog`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| CSV Bundle | 215257 | 53815 | 77252 | - | - | - |
| SDIF AI | 221599 | 55400 | 59885 | - | - | - |
| SDIF | 228953 | 57239 | 59890 | - | - | - |
| TOON | 229126 | 57282 | 77470 | - | - | - |
| YAML | 435031 | 108758 | 119551 | - | - | - |
| JSON Compact | 447520 | 111880 | 146598 | - | - | - |
| JSON Pretty | 653078 | 163270 | 150285 | - | - | - |
| XML | 790035 | 197509 | 235160 | - | - | - |

### `large-support-export`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 342047 | 85512 | 81684 | - | - | - |
| CSV Bundle | 342094 | 85524 | 94673 | - | - | - |
| SDIF | 352437 | 88110 | 81689 | - | - | - |
| TOON | 352453 | 88114 | 94672 | - | - | - |
| YAML | 573388 | 143347 | 149111 | - | - | - |
| JSON Compact | 592098 | 148025 | 188515 | - | - | - |
| JSON Pretty | 810127 | 202532 | 193714 | - | - | - |
| XML | 986732 | 246683 | 276343 | - | - | - |

### `large-validation-report`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 383776 | 95944 | 91318 | - | - | - |
| CSV Bundle | 383821 | 95956 | 100374 | - | - | - |
| SDIF | 390534 | 97634 | 91323 | - | - | - |
| TOON | 391666 | 97917 | 105973 | - | - | - |
| YAML | 549978 | 137495 | 142953 | - | - | - |
| JSON Compact | 559328 | 139832 | 160800 | - | - | - |
| JSON Pretty | 710381 | 177596 | 164183 | - | - | - |
| XML | 818657 | 204665 | 227604 | - | - | - |

### `medium-invoice-batch`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 73903 | 18476 | 20702 | - | - | - |
| CSV Bundle | 73941 | 18486 | 24956 | - | - | - |
| SDIF | 75859 | 18965 | 20707 | - | - | - |
| TOON | 75867 | 18967 | 24954 | - | - | - |
| YAML | 137030 | 34258 | 39703 | - | - | - |
| JSON Compact | 139558 | 34890 | 45845 | - | - | - |
| JSON Pretty | 191590 | 47898 | 46892 | - | - | - |
| XML | 238165 | 59542 | 72517 | - | - | - |

### `medium-observability-run`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 55931 | 13983 | 16712 | - | - | - |
| CSV Bundle | 55978 | 13995 | 20633 | - | - | - |
| SDIF | 58377 | 14595 | 16717 | - | - | - |
| TOON | 58391 | 14598 | 20632 | - | - | - |
| YAML | 109099 | 27275 | 33200 | - | - | - |
| JSON Compact | 114756 | 28689 | 39221 | - | - | - |
| JSON Pretty | 167981 | 41996 | 40448 | - | - | - |
| XML | 205986 | 51497 | 64697 | - | - | - |

### `medium-policy-catalog`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 49782 | 12446 | 16021 | - | - | - |
| CSV Bundle | 49822 | 12456 | 19136 | - | - | - |
| SDIF | 51672 | 12918 | 16026 | - | - | - |
| TOON | 51680 | 12920 | 19134 | - | - | - |
| YAML | 91628 | 22907 | 27840 | - | - | - |
| JSON Compact | 97573 | 24394 | 33616 | - | - | - |
| JSON Pretty | 139351 | 34838 | 34563 | - | - | - |
| XML | 167499 | 41875 | 51599 | - | - | - |

### `medium-product-catalog`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 47552 | 11888 | 14784 | - | - | - |
| CSV Bundle | 47599 | 11900 | 18378 | - | - | - |
| SDIF | 50784 | 12696 | 14789 | - | - | - |
| TOON | 50798 | 12700 | 18377 | - | - | - |
| YAML | 104720 | 26180 | 32289 | - | - | - |
| JSON Compact | 111369 | 27843 | 37474 | - | - | - |
| JSON Pretty | 169056 | 42264 | 39094 | - | - | - |
| XML | 214848 | 53712 | 66733 | - | - | - |

### `plan`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF | 984 | 246 | 266 | - | - | - |
| SDIF AI | 1000 | 250 | 274 | - | - | - |
| TOON | 1002 | 251 | 307 | - | - | - |
| CSV Bundle | 1039 | 260 | 324 | - | - | - |
| YAML | 1197 | 300 | 333 | - | - | - |
| JSON Compact | 1268 | 317 | 389 | - | - | - |
| JSON Pretty | 1688 | 422 | 406 | - | - | - |
| XML | 2080 | 520 | 614 | - | - | - |

### `registry`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 662 | 166 | 190 | - | - | - |
| SDIF | 674 | 169 | 192 | - | - | - |
| TOON | 697 | 175 | 227 | - | - | - |
| CSV Bundle | 720 | 180 | 240 | - | - | - |
| YAML | 896 | 224 | 255 | - | - | - |
| JSON Compact | 960 | 240 | 301 | - | - | - |
| JSON Pretty | 1293 | 324 | 313 | - | - | - |
| XML | 1601 | 401 | 478 | - | - | - |

### `schema`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 1097 | 275 | 291 | - | - | - |
| CSV Bundle | 1161 | 291 | 384 | - | - | - |
| SDIF | 1161 | 291 | 296 | - | - | - |
| TOON | 1181 | 296 | 384 | - | - | - |
| YAML | 2004 | 501 | 554 | - | - | - |
| JSON Compact | 2113 | 529 | 665 | - | - | - |
| JSON Pretty | 3235 | 809 | 703 | - | - | - |
| XML | 4189 | 1048 | 1242 | - | - | - |

### `small-api-catalog`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 1640 | 410 | 516 | - | - | - |
| CSV Bundle | 1666 | 417 | 628 | - | - | - |
| SDIF | 1716 | 429 | 521 | - | - | - |
| TOON | 1718 | 430 | 624 | - | - | - |
| YAML | 2909 | 728 | 876 | - | - | - |
| JSON Compact | 3163 | 791 | 1126 | - | - | - |
| JSON Pretty | 4849 | 1213 | 1162 | - | - | - |
| XML | 5647 | 1412 | 1742 | - | - | - |

### `small-incident`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 2563 | 641 | 693 | - | - | - |
| CSV Bundle | 2594 | 649 | 827 | - | - | - |
| SDIF | 2637 | 660 | 698 | - | - | - |
| TOON | 2640 | 660 | 824 | - | - | - |
| YAML | 3947 | 987 | 1077 | - | - | - |
| JSON Compact | 4148 | 1037 | 1304 | - | - | - |
| JSON Pretty | 5727 | 1432 | 1341 | - | - | - |
| XML | 6808 | 1702 | 1968 | - | - | - |

### `small-invoice`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 1406 | 352 | 391 | - | - | - |
| CSV Bundle | 1439 | 360 | 498 | - | - | - |
| SDIF | 1454 | 364 | 396 | - | - | - |
| TOON | 1459 | 365 | 495 | - | - | - |
| YAML | 2537 | 635 | 715 | - | - | - |
| JSON Compact | 2643 | 661 | 848 | - | - | - |
| JSON Pretty | 3764 | 941 | 872 | - | - | - |
| XML | 4738 | 1185 | 1443 | - | - | - |

### `validation-report`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 691 | 173 | 180 | - | - | - |
| SDIF | 735 | 184 | 190 | - | - | - |
| TOON | 770 | 193 | 226 | - | - | - |
| CSV Bundle | 773 | 194 | 228 | - | - | - |
| YAML | 934 | 234 | 253 | - | - | - |
| JSON Compact | 1014 | 254 | 300 | - | - | - |
| JSON Pretty | 1378 | 345 | 316 | - | - | - |
| XML | 1685 | 422 | 494 | - | - | - |

### `wide-table-survey`

| Format | Bytes | `Estimate` | `TokenX` | `tiktoken` | `Llama3` | `Claude` |
| --- | ---: |---:|---:|---:|---:|---:|
| SDIF AI | 18606 | 4652 | 7878 | - | - | - |
| CSV Bundle | 18632 | 4658 | 14897 | - | - | - |
| TOON | 19053 | 4764 | 14893 | - | - | - |
| SDIF | 19054 | 4764 | 7883 | - | - | - |
| JSON Compact | 64917 | 16230 | 29998 | - | - | - |
| YAML | 70375 | 17594 | 22708 | - | - | - |
| JSON Pretty | 124951 | 31238 | 30220 | - | - | - |
| XML | 149167 | 37292 | 52992 | - | - | - |

## Environment

| Variable | Value |
| --- | --- |
| `.env loaded` | `yes` |
| `SDIF_BENCHMARK_TOON` | `1` |
| `SDIF_BENCHMARK_GOLDEN_DIR` | _unset_ |
| `SDIF_BENCHMARK_TOKENX` | `1` |
| `SDIF_TOKENX_DEFAULT_CHARS_PER_TOKEN` | `6` |
| `SDIF_TOKENX_RESOLVE_DIRS` | `tokenx_tokenizers` |
| `SDIF_BENCHMARK_CLAUDE` | `0` |
| `SDIF_CLAUDE_MODEL` | `claude-sonnet-4-6` |
| `SDIF_BENCHMARK_LLAMA` | `0` |
| `SDIF_LLAMA_TOKENIZER` | `meta-llama/Meta-Llama-3-8B` |
| `SDIF_LLAMA_LOCAL_ONLY` | `1` |
| `SDIF_TIKTOKEN_ENCODING` | `cl100k_base` |
| `HF_TOKEN` | _unset_ |
| `ANTHROPIC_API_KEY` | _unset_ |

## Notes

- `tiktoken` is unavailable: Unavailable because Python package `tiktoken` is not installed.
- `Llama3` is disabled: Disabled through SDIF_BENCHMARK_LLAMA=0.
- `Claude` is disabled: Disabled. Set SDIF_BENCHMARK_CLAUDE=1 to enable API token counting.

## Artifacts

- Raw log: `results/token_efficiency/comparison.log`
- Markdown report: `results/token_efficiency/comparison.md`
- Summary report: `results/token_efficiency/summary.md`
- Structured JSON report: `results/token_efficiency/comparison.json`
- Structured SDIF report: `results/token_efficiency/comparison.sdif`
- SDIF AI projection: `results/token_efficiency/comparison.sdif.ai`
- Compared corpus files: `results/token_efficiency/corpus`
- Result directory: `results/token_efficiency`
