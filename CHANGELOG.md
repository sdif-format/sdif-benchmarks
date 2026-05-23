# Changelog

## [Unreleased]

### Fixed

- `parse_sdif_ai()` in `roundtrip_fidelity.py` now uses `expand_ai_doc()` instead of
  `sdif_from_ai()`. The previous path called `canonicalize()`, which reordered rules
  alphabetically, sorted relations, and requoted list literals containing double-quotes —
  causing `plan`, `registry`, and `validation-report` to score below 100% despite valid
  encoding. All three now reach 100% overall fidelity.
- Fixed a mypy `arg-type` error in `parse_toon()` where the `subprocess.run()` call
  received `list[str | None]` instead of `list[str]`.

### Added

- Leaf-level diagnostic evidence for every format/document pair that scores below 100%:
  `results/roundtrip_fidelity/diagnostics/<document>/<format>.json` containing
  `missing_paths`, `extra_paths`, `value_mismatches`, and `type_mismatches`.
- `FidelityResult.note` is set to `"see diagnostics"` when a diagnostic file is written.
- TOON external decoder float→int coercion is detected and annotated with
  `cause: "external_decoder_int_float_coercion"` in the diagnostic file.

### Tests

- `test_roundtrip_collect_diagnostics_all_four_categories` — verifies all four diagnostic
  categories are collected correctly.
- `test_roundtrip_collect_diagnostics_toon_int_float_coercion_cause` — confirms TOON
  float→int cause annotation.
- `test_roundtrip_diagnostic_files_produced_below_100` — integration test that injects a
  lossy parser and verifies diagnostic file creation.
- `test_roundtrip_sdif_ai_plan_at_100_after_expand_fix` — regression guard for array
  fields (e.g. `scope.in`) that previously lost structure through canonicalization.

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
