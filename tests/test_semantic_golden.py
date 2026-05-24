"""Tests for the semantic golden fixture generator.

Verifies that generate_semantic_golden.py produces valid fixture directories
with both equivalent.json and source.sdif for each of the four semantic types.
"""

from __future__ import annotations

import importlib.util
import hashlib
import json
import sys
import types
from pathlib import Path
from typing import Any

import pytest

BENCHMARKS_ROOT = Path(__file__).resolve().parents[1]
SDIF_SRC = BENCHMARKS_ROOT.parent / "src"


def load_generator() -> types.ModuleType:
    """Load the generate_semantic_golden module dynamically."""
    module_path = BENCHMARKS_ROOT / "scripts" / "generate_semantic_golden.py"
    spec = importlib.util.spec_from_file_location("generate_semantic_golden", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["generate_semantic_golden"] = module
    spec.loader.exec_module(module)
    return module


def load_sdif_parse() -> tuple[Any, Any]:
    """Return the parse_text and document_to_json_data callables."""
    if str(SDIF_SRC) not in sys.path:
        sys.path.insert(0, str(SDIF_SRC))
    from sdif import parse_text  # type: ignore[import]
    from sdif.json import document_to_json_data  # type: ignore[import]
    return parse_text, document_to_json_data


def load_sdif_canonical() -> tuple[Any, Any]:
    """Return the canonicalize and sdif_hash callables."""
    if str(SDIF_SRC) not in sys.path:
        sys.path.insert(0, str(SDIF_SRC))
    from sdif import canonicalize, sdif_hash  # type: ignore[import]
    return canonicalize, sdif_hash


FIXTURE_NAMES = [
    "semantic-narrative",
    "audit-provenance",
    "agent-workflow",
    "llm-api-response",
]


@pytest.fixture(scope="module")
def generated_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Run the generator once and return the output directory."""
    out = tmp_path_factory.mktemp("semantic_golden")
    gen = load_generator()
    gen.generate_all(out)  # type: ignore[attr-defined]
    return out


# ---------------------------------------------------------------------------
# Structure tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_fixture_directory_exists(generated_dir: Path, name: str) -> None:
    assert (generated_dir / name).is_dir(), f"{name}/ directory missing"


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_equivalent_json_exists(generated_dir: Path, name: str) -> None:
    assert (generated_dir / name / "equivalent.json").is_file()


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_source_sdif_exists(generated_dir: Path, name: str) -> None:
    assert (generated_dir / name / "source.sdif").is_file()


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_canonical_sdif_exists(generated_dir: Path, name: str) -> None:
    assert (generated_dir / name / "canonical.sdif").is_file()


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_canonical_sha256_exists(generated_dir: Path, name: str) -> None:
    assert (generated_dir / name / "canonical.sha256").is_file()


# ---------------------------------------------------------------------------
# equivalent.json shape tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_equivalent_json_is_valid_json(generated_dir: Path, name: str) -> None:
    text = (generated_dir / name / "equivalent.json").read_text(encoding="utf-8")
    obj = json.loads(text)
    assert isinstance(obj, dict)


def _load_json(generated_dir: Path, name: str) -> dict[str, Any]:
    return json.loads((generated_dir / name / "equivalent.json").read_text(encoding="utf-8"))


def test_semantic_narrative_scalar_fields(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "semantic-narrative")
    for field in ("id", "title", "status", "narrative_methodology", "narrative_conclusion"):
        assert field in data, f"scalar field {field!r} missing from semantic-narrative"
    assert data.get("kind") == "ResearchReport"


def test_semantic_narrative_tables(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "semantic-narrative")
    findings = data.get("findings", [])
    assert len(findings) >= 3, "findings must have ≥3 rows"
    assert all({"id", "category", "severity", "source"} <= set(r) for r in findings)
    recs = data.get("recommendations", [])
    assert len(recs) >= 3, "recommendations must have ≥3 rows"
    assert all({"id", "finding_id", "action", "priority"} <= set(r) for r in recs)


def test_semantic_narrative_rel_and_rules(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "semantic-narrative")
    rels = data.get("rel", [])
    assert len(rels) >= 4, "semantic-narrative must have ≥4 rel entries (3 addresses + 1 escalates)"
    predicates = {r["predicate"] for r in rels}
    assert "addresses" in predicates
    assert "escalates" in predicates
    rules = data.get("rules", [])
    assert len(rules) >= 2, "semantic-narrative must have ≥2 rules"


def test_audit_provenance_scalar_fields(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "audit-provenance")
    for field in ("id", "artifact"):
        assert field in data, f"scalar field {field!r} missing from audit-provenance"
    assert data.get("kind") == "AuditLog"


def test_audit_provenance_tables(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "audit-provenance")
    events = data.get("events", [])
    assert len(events) >= 4, "events must have ≥4 rows"
    assert all({"id", "actor", "action", "timestamp"} <= set(r) for r in events)
    prov = data.get("provenance", [])
    assert len(prov) >= 2, "provenance must have ≥2 rows"
    assert all({"artifact", "derived_from", "via"} <= set(r) for r in prov)


def test_audit_provenance_rel_and_rules(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "audit-provenance")
    rels = data.get("rel", [])
    assert len(rels) >= 5, "audit-provenance must have ≥5 rel entries"
    predicates = {r["predicate"] for r in rels}
    assert "follows" in predicates
    assert "derived_from" in predicates
    assert "approves" in predicates
    rules = data.get("rules", [])
    assert len(rules) >= 2


def test_agent_workflow_scalar_fields(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "agent-workflow")
    for field in ("id", "session_id", "model"):
        assert field in data, f"scalar field {field!r} missing from agent-workflow"
    assert data.get("kind") == "AgentWorkflow"


def test_agent_workflow_tables(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "agent-workflow")
    tasks = data.get("tasks", [])
    assert len(tasks) >= 5, "tasks must have ≥5 rows"
    assert all({"id", "agent", "action", "status", "tokens"} <= set(r) for r in tasks)
    tool_calls = data.get("tool_calls", [])
    assert len(tool_calls) >= 4, "tool_calls must have ≥4 rows"
    assert all({"task_id", "tool", "count"} <= set(r) for r in tool_calls)


def test_agent_workflow_rel_and_rules(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "agent-workflow")
    rels = data.get("rel", [])
    assert len(rels) >= 5, "agent-workflow must have ≥5 rel entries"
    predicates = {r["predicate"] for r in rels}
    assert "depends_on" in predicates
    assert "uses_output_of" in predicates
    rules = data.get("rules", [])
    assert len(rules) >= 2


def test_llm_api_response_scalar_fields(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "llm-api-response")
    for field in (
        "id",
        "source",
        "filtered_for",
        "metadata_fetched_at",
        "metadata_min_stars",
        "metadata_active_last_days",
    ):
        assert field in data, f"scalar field {field!r} missing from llm-api-response"
    assert data.get("kind") == "APISnapshot"


def test_llm_api_response_tables(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "llm-api-response")
    repos = data.get("repos", [])
    assert len(repos) >= 4, "repos must have ≥4 rows"
    assert all({"id", "name", "language", "stars", "last_commit"} <= set(r) for r in repos)
    contributors = data.get("contributors", [])
    assert len(contributors) >= 4, "contributors must have ≥4 rows"
    assert all({"repo_id", "login", "commits"} <= set(r) for r in contributors)


def test_llm_api_response_rel_and_rules(generated_dir: Path) -> None:
    data = _load_json(generated_dir, "llm-api-response")
    rels = data.get("rel", [])
    assert len(rels) >= 5, "llm-api-response must have ≥5 rel entries"
    predicates = {r["predicate"] for r in rels}
    assert "benchmarks" in predicates
    rules = data.get("rules", [])
    assert len(rules) >= 2


# ---------------------------------------------------------------------------
# source.sdif parse tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_source_sdif_parses_successfully(generated_dir: Path, name: str) -> None:
    parse_text, _ = load_sdif_parse()
    sdif_text = (generated_dir / name / "source.sdif").read_text(encoding="utf-8")
    doc = parse_text(sdif_text)
    assert doc is not None, f"parse_text returned None for {name}"


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_source_sdif_relations_via_document_to_json_data(generated_dir: Path, name: str) -> None:
    """Relations must be accessible via document_to_json_data, not doc.relations."""
    parse_text, document_to_json_data = load_sdif_parse()
    sdif_text = (generated_dir / name / "source.sdif").read_text(encoding="utf-8")
    doc = parse_text(sdif_text)
    result = document_to_json_data(doc)
    rels = result.get("rel", [])
    assert len(rels) >= 2, f"{name} must expose ≥2 relations via document_to_json_data"


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_source_sdif_rules_are_exposed(generated_dir: Path, name: str) -> None:
    """Rules must be accessible as a list of strings via document_to_json_data."""
    parse_text, document_to_json_data = load_sdif_parse()
    sdif_text = (generated_dir / name / "source.sdif").read_text(encoding="utf-8")
    doc = parse_text(sdif_text)
    result = document_to_json_data(doc)
    rules = result.get("rules", [])
    assert len(rules) >= 2, f"{name} must expose ≥2 rules via document_to_json_data"
    assert all(isinstance(r, str) for r in rules), "rules must be strings"


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_canonical_fixture_matches_source_and_hash(generated_dir: Path, name: str) -> None:
    canonicalize, sdif_hash = load_sdif_canonical()
    source_text = (generated_dir / name / "source.sdif").read_text(encoding="utf-8")
    canonical_text = (generated_dir / name / "canonical.sdif").read_text(encoding="utf-8")
    hash_text = (generated_dir / name / "canonical.sha256").read_text(encoding="utf-8").strip()

    assert canonical_text == canonicalize(source_text)
    assert hash_text == sdif_hash(source_text)
    assert hash_text == hashlib.sha256(canonical_text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------


def test_generator_cli_runs_without_error(tmp_path: Path) -> None:
    """The generator's main() must return 0 and write all 4 fixtures."""
    gen = load_generator()
    result = gen.main(["--output-dir", str(tmp_path)])  # type: ignore[attr-defined]
    assert result == 0
    for name in FIXTURE_NAMES:
        assert (tmp_path / name / "equivalent.json").is_file()
        assert (tmp_path / name / "source.sdif").is_file()
        assert (tmp_path / name / "canonical.sdif").is_file()
        assert (tmp_path / name / "canonical.sha256").is_file()
