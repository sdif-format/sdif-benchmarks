"""Tests that the retrieval accuracy script is discoverable and refuses to run without opt-in env vars."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

BENCHMARK_DIR = Path(__file__).parent.parent
SCRIPT = BENCHMARK_DIR / "scripts" / "retrieval_accuracy.py"


def test_retrieval_accuracy_script_exists() -> None:
    assert SCRIPT.exists(), f"Expected {SCRIPT} to exist"


def test_exits_nonzero_without_retrieval_env() -> None:
    env = os.environ.copy()
    env.pop("SDIF_BENCHMARK_RETRIEVAL", None)
    env.pop("ANTHROPIC_API_KEY", None)
    env["PYTHONPATH"] = str(BENCHMARK_DIR / "src") + ":" + str(BENCHMARK_DIR.parent / "src")

    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode != 0
    assert "SDIF_BENCHMARK_RETRIEVAL" in result.stdout + result.stderr
