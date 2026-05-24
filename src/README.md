# Packaged Benchmark Library & Tracks

This directory contains the `sdif_benchmarks` package which implements the benchmark suite tracks, corpus generators, checks, and reusable core helpers.

## Package Layout (`src/sdif_benchmarks/`)

### Core Library Modules
- [infra.py](file:///home/alessbarb/workspace/repos/incubating/sdif/sdif-benchmarks/src/sdif_benchmarks/infra.py): Path calculations, environment variables loading, directory lifecycle (`create_benchmark_run_dir`, `publish_benchmark_result`), and common utilities.
- [formats.py](file:///home/alessbarb/workspace/repos/incubating/sdif/sdif-benchmarks/src/sdif_benchmarks/formats.py): Format generators (JSON Compact, JSON Pretty, YAML, XML, CSV Bundle, SDIF, and SDIF AI).
- [report.py](file:///home/alessbarb/workspace/repos/incubating/sdif/sdif-benchmarks/src/sdif_benchmarks/report.py): Common rendering helpers for JSON, SDIF, and HTML evidence reports.
- [optional_deps.py](file:///home/alessbarb/workspace/repos/incubating/sdif/sdif-benchmarks/src/sdif_benchmarks/optional_deps.py): Graceful import checker for optional benchmark dependencies (Anthropic API, Tiktoken, etc.).
- [run_suite.py](file:///home/alessbarb/workspace/repos/incubating/sdif/sdif-benchmarks/src/sdif_benchmarks/run_suite.py): The main suite coordinator and entrypoint.

### Sub-packages
- [tracks/](file:///home/alessbarb/workspace/repos/incubating/sdif/sdif-benchmarks/src/sdif_benchmarks/tracks): Individual benchmark track implementations (e.g., token efficiency, context packing, operability).
- [generators/](file:///home/alessbarb/workspace/repos/incubating/sdif/sdif-benchmarks/src/sdif_benchmarks/generators): Fixture corpus golden generators.
- [checks/](file:///home/alessbarb/workspace/repos/incubating/sdif/sdif-benchmarks/src/sdif_benchmarks/checks): Code and semantic quality checks.

---

## Invocation

All track, generator, and checks modules can be executed directly via Python module flags:
```bash
python -m sdif_benchmarks.tracks.token_efficiency
```

The main runner is registered as a CLI entry point:
```bash
sdif-benchmarks --help
```
