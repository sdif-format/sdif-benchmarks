# Changelog

## 1.0.0 - 2026-05-22

### First stable benchmark release

- Establishes `sdif-benchmarks` as the dedicated repository for SDIF benchmark methodology, runners, generated corpus artifacts, and evidence reports.
- Keeps benchmark code outside the core `sdif` repository so benchmark dependencies and CI gates do not expand the reference implementation boundary.
- Uses the core repository's `examples/golden/` corpus by default, with `SDIF_CORE_REPO` and `SDIF_BENCHMARK_GOLDEN_DIR` overrides for reproducible external runs.

### Benchmark tracks

- Provides token-efficiency benchmarks across JSON Compact, JSON Pretty, YAML, XML, CSV Bundle, canonical SDIF, SDIF AI, and optional TOON.
- Provides context-packing, round-trip-fidelity, delta-compactness, retrieval-accuracy, and semantic-quality benchmark entry points.
- Writes completed evidence under `results/<track>/` only after successful runs, while failed runs remain under `tmp/<track>/` for diagnosis.

### v1.0.0 evidence model

- Commits generated token-efficiency outputs, including Markdown, JSON, SDIF, SDIF AI, dashboard HTML, and per-document corpus files.
- Documents tokenizer coverage and environment switches for deterministic local runs.
- Keeps optional external tokenizers and retrieval dependencies opt-in.

### CI and verification

- Adds benchmark-owned CI and Makefile gates for token benchmarks, semantic-quality checks, lint/type checks, and tests.
- Aligns large golden fixture generation with the split core/benchmark repository layout.
