"""Tests that the retrieval accuracy module is discoverable and refuses to run without opt-in env vars."""

from __future__ import annotations

import os
import subprocess
import sys


def test_retrieval_accuracy_module_exists() -> None:
    try:
        import sdif_benchmarks.tracks.retrieval_accuracy
    except ImportError:
        assert False, "Expected sdif_benchmarks.tracks.retrieval_accuracy to be importable"


def test_exits_nonzero_without_retrieval_env() -> None:
    env = os.environ.copy()
    env.pop("SDIF_BENCHMARK_RETRIEVAL", None)
    env.pop("ANTHROPIC_API_KEY", None)

    result = subprocess.run(
        [sys.executable, "-m", "sdif_benchmarks.tracks.retrieval_accuracy"],
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode != 0
    assert "SDIF_BENCHMARK_RETRIEVAL" in result.stdout + result.stderr
