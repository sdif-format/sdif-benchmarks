# Changelog

## [Unreleased]

### Added — v1.1 Semantic Benchmark Suite

- **Semantic golden fixture generator** (`scripts/generate_semantic_golden.py`): generates four
  semantic fixture types (`semantic-narrative`, `audit-provenance`, `agent-workflow`,
  `llm-api-response`) under `../sdif/examples/golden/`. Each fixture produces
  `equivalent.json` and `source.sdif` with `rel:` triples, `rules:` declarations, and
  named-column tables.

- **Semantic fidelity track** (`scripts/semantic_fidelity.py`): measures structural recovery
  after format conversion (relation, rule, table, and field axes). Uses nullable metrics
  (`float | None`) — empty source axes and unimplemented parse-backs return `None`, never
  a fake `0.0`. CSV Bundle parse-back implemented (recovers `# table:rel` sections
  honestly). XML marked `best_effort`. TOON marked `not_measured`. Writes
  `results/semantic_fidelity/summary.md`.

- **Operability matrix track** (`scripts/operability.py`): documents format capabilities
  across 8 formats (SDIF, SDIF AI, JSON, YAML, XML, CSV Bundle, TOON). Covers canonical
  forms, stable hashing, schema validation, native relation support, rule declaration vs.
  rule evaluation (split), semantic type vocabulary, and deterministic output. Writes
  `results/operability_matrix.md`.

- **Public extraction validation tests** (`tests/test_semantic_extraction.py`): proves that
  `document_to_json_data()` exposes `rel` as `[{subject, predicate, object}]` and `rules`
  as `[str]` without touching AST internals.

- **Retrieval accuracy opt-in tests** (`tests/test_retrieval_accuracy_integration.py`):
  verifies the retrieval script refuses to run without `SDIF_BENCHMARK_RETRIEVAL=1`.

- **Makefile targets**: `benchmark-semantic` and `benchmark-operability` added.

- **manifest.sdif**: `semantic-fidelity` and `operability` tracks registered as `active`.
  `retrieval-accuracy` promoted from `planned` to `active` (opt-in via env var).

- **run_suite.py**: `semantic_fidelity` and `operability` wired as non-optional suite tracks.
  `retrieval_accuracy` remains `optional: True` — default suite runs without `ANTHROPIC_API_KEY`.

### Fixed

- SDIF canonical and SDIF AI both round-trip losslessly across the full benchmark corpus.
- `github.openapi` / SDIF AI now reaches 100% overall fidelity. Root cause: after
  `expand_ai_doc()` strips the `$` suffix from column names and records their indices in
  `Table.quoted_columns`, the core decoder (`_parse_table_cell` in `sdif.json.converter`)
  ignored that set and coerced numeric-looking HTTP status codes (e.g. `"200"`, `"404"`)
  to integers. Fixed in the core library; benchmarks inherit the fix via the `sdif` package.
- `parse_sdif_ai()` in `roundtrip_fidelity.py` now uses `expand_ai_doc()` instead of
  `sdif_from_ai()`. The previous path called `canonicalize()`, which reordered rules
  alphabetically, sorted relations, and converted list literals containing quoted strings
  into quoted strings — causing `plan`, `registry`, and `validation-report` to score below
  100% despite valid encoding. All three now reach 100% overall fidelity.

### Benchmark

- Re-ran the round-trip fidelity benchmark after the SDIF AI and canonicalization fixes.
  SDIF AI now reaches 100% round-trip fidelity across all 20 benchmark documents.
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
- `test_roundtrip_sdif_ai_numeric_string_table_cells_preserved` — regression guard for
  numeric-looking strings in `$`-suffixed table columns (HTTP status codes, booleans, null)
  surviving the SDIF AI → `expand_ai_doc` → JSON decode path as strings.

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
