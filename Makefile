# -----------------------------------------------------------------------------
# Runtime configuration
# -----------------------------------------------------------------------------

PYTHON ?= python3
SDIF_CORE_REPO ?= ..

export SDIF_CORE_REPO
export PYTHONPATH := src:$(SDIF_CORE_REPO)/src:$(PYTHONPATH)


# -----------------------------------------------------------------------------
# Test configuration
# -----------------------------------------------------------------------------

TEST_ENV := \
	SDIF_ENV_OVERRIDE=0 \
	SDIF_BENCHMARK_TOON=0 \
	SDIF_BENCHMARK_TOKENX=0 \
	SDIF_BENCHMARK_LLAMA=0 \
	SDIF_BENCHMARK_CLAUDE=0


# -----------------------------------------------------------------------------
# Benchmark modules
# -----------------------------------------------------------------------------

BENCHMARK_SUITE_MOD := -m sdif_benchmarks.run_suite
BENCHMARK_TOKEN_MOD := -m sdif_benchmarks.tracks.token_efficiency
BENCHMARK_QUALITY_MOD := -m sdif_benchmarks.checks.check_semantic_quality
BENCHMARK_CORPUS_MOD := -m sdif_benchmarks.generators.generate_benchmark_golden
BENCHMARK_LARGE_CORPUS_MOD := -m sdif_benchmarks.generators.generate_large_golden
BENCHMARK_PACKING_MOD := -m sdif_benchmarks.tracks.context_packing
BENCHMARK_ROUNDTRIP_MOD := -m sdif_benchmarks.tracks.roundtrip_fidelity
BENCHMARK_DELTA_MOD := -m sdif_benchmarks.tracks.delta_compactness
BENCHMARK_RETRIEVAL_MOD := -m sdif_benchmarks.tracks.retrieval_accuracy
BENCHMARK_SEMANTIC_MOD := -m sdif_benchmarks.tracks.semantic_fidelity
BENCHMARK_OPERABILITY_MOD := -m sdif_benchmarks.tracks.operability


# -----------------------------------------------------------------------------
# Public targets
# -----------------------------------------------------------------------------

.PHONY: \
	test \
	benchmark-suite \
	benchmark-token \
	benchmark-quality \
	benchmark-corpus \
	benchmark-large-corpus \
	benchmark-packing \
	benchmark-roundtrip \
	benchmark-delta \
	benchmark-retrieval \
	benchmark-semantic \
	benchmark-operability \
	clean


test:
	$(TEST_ENV) $(PYTHON) -m pytest -q


benchmark-suite:
	$(PYTHON) $(BENCHMARK_SUITE_MOD)


benchmark-token:
	$(PYTHON) $(BENCHMARK_TOKEN_MOD)


benchmark-quality:
	$(PYTHON) $(BENCHMARK_QUALITY_MOD)


benchmark-corpus:
	$(PYTHON) $(BENCHMARK_CORPUS_MOD)


benchmark-large-corpus:
	$(PYTHON) $(BENCHMARK_LARGE_CORPUS_MOD)


benchmark-packing:
	$(PYTHON) $(BENCHMARK_PACKING_MOD)


benchmark-roundtrip:
	$(PYTHON) $(BENCHMARK_ROUNDTRIP_MOD)


benchmark-delta:
	$(PYTHON) $(BENCHMARK_DELTA_MOD)


benchmark-retrieval:
	SDIF_BENCHMARK_RETRIEVAL=1 $(PYTHON) $(BENCHMARK_RETRIEVAL_MOD)


benchmark-semantic:
	$(PYTHON) $(BENCHMARK_SEMANTIC_MOD)


benchmark-operability:
	$(PYTHON) $(BENCHMARK_OPERABILITY_MOD)


benchmark: benchmark-suite
	mkdir -p dist
	tar -czf dist/benchmark_results.tar.gz results/


clean:
	rm -rf \
		tmp/ \
		.pytest_cache/ \
		.ruff_cache/ \
		.mypy_cache/ \
		tests/__pycache__/ \
		src/__pycache__/
