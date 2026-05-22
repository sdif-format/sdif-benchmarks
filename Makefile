PYTHON ?= python3
SDIF_CORE_REPO ?= ..
export SDIF_CORE_REPO
export PYTHONPATH := src:$(SDIF_CORE_REPO)/src:$(PYTHONPATH)

.PHONY: test benchmark-suite benchmark-token benchmark-quality benchmark-corpus benchmark-large-corpus benchmark-packing benchmark-roundtrip benchmark-delta benchmark-retrieval clean

test:
	SDIF_ENV_OVERRIDE=0 SDIF_BENCHMARK_TOON=0 SDIF_BENCHMARK_TOKENX=0 SDIF_BENCHMARK_LLAMA=0 SDIF_BENCHMARK_CLAUDE=0 $(PYTHON) -m pytest -q

benchmark-suite:
	$(PYTHON) scripts/run_suite.py

benchmark-token:
	$(PYTHON) scripts/token_efficiency.py

benchmark-quality:
	$(PYTHON) scripts/check_semantic_quality.py

benchmark-corpus:
	$(PYTHON) scripts/generate_benchmark_golden.py

benchmark-large-corpus:
	$(PYTHON) scripts/generate_large_golden.py

benchmark-packing:
	$(PYTHON) scripts/context_packing.py

benchmark-roundtrip:
	$(PYTHON) scripts/roundtrip_fidelity.py

benchmark-delta:
	$(PYTHON) scripts/delta_compactness.py

benchmark-retrieval:
	SDIF_BENCHMARK_RETRIEVAL=1 $(PYTHON) scripts/retrieval_accuracy.py

clean:
	rm -rf tmp .pytest_cache .ruff_cache .mypy_cache tests/__pycache__ scripts/__pycache__ src/__pycache__
