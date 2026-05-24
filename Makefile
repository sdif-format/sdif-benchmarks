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
# Benchmark scripts
# -----------------------------------------------------------------------------

SCRIPT_DIR := scripts

BENCHMARK_SUITE_SCRIPT := $(SCRIPT_DIR)/run_suite.py
BENCHMARK_TOKEN_SCRIPT := $(SCRIPT_DIR)/token_efficiency.py
BENCHMARK_QUALITY_SCRIPT := $(SCRIPT_DIR)/check_semantic_quality.py
BENCHMARK_CORPUS_SCRIPT := $(SCRIPT_DIR)/generate_benchmark_golden.py
BENCHMARK_LARGE_CORPUS_SCRIPT := $(SCRIPT_DIR)/generate_large_golden.py
BENCHMARK_PACKING_SCRIPT := $(SCRIPT_DIR)/context_packing.py
BENCHMARK_ROUNDTRIP_SCRIPT := $(SCRIPT_DIR)/roundtrip_fidelity.py
BENCHMARK_DELTA_SCRIPT := $(SCRIPT_DIR)/delta_compactness.py
BENCHMARK_RETRIEVAL_SCRIPT := $(SCRIPT_DIR)/retrieval_accuracy.py
BENCHMARK_SEMANTIC_SCRIPT := $(SCRIPT_DIR)/semantic_fidelity.py
BENCHMARK_OPERABILITY_SCRIPT := $(SCRIPT_DIR)/operability.py


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
	$(PYTHON) $(BENCHMARK_SUITE_SCRIPT)


benchmark-token:
	$(PYTHON) $(BENCHMARK_TOKEN_SCRIPT)


benchmark-quality:
	$(PYTHON) $(BENCHMARK_QUALITY_SCRIPT)


benchmark-corpus:
	$(PYTHON) $(BENCHMARK_CORPUS_SCRIPT)


benchmark-large-corpus:
	$(PYTHON) $(BENCHMARK_LARGE_CORPUS_SCRIPT)


benchmark-packing:
	$(PYTHON) $(BENCHMARK_PACKING_SCRIPT)


benchmark-roundtrip:
	$(PYTHON) $(BENCHMARK_ROUNDTRIP_SCRIPT)


benchmark-delta:
	$(PYTHON) $(BENCHMARK_DELTA_SCRIPT)


benchmark-retrieval:
	SDIF_BENCHMARK_RETRIEVAL=1 $(PYTHON) $(BENCHMARK_RETRIEVAL_SCRIPT)


benchmark-semantic:
	$(PYTHON) $(BENCHMARK_SEMANTIC_SCRIPT)


benchmark-operability:
	$(PYTHON) $(BENCHMARK_OPERABILITY_SCRIPT)


clean:
	rm -rf \
		tmp/ \
		.pytest_cache/ \
		.ruff_cache/ \
		.mypy_cache/ \
		tests/__pycache__/ \
		scripts/__pycache__/ \
		src/__pycache__/
