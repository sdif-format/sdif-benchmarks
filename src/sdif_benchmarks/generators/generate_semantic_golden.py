"""Generate semantic golden fixtures for the v1.1 SDIF Semantic Benchmark Suite.

Each fixture produces an ``equivalent.json`` (semantic source) and a
``source.sdif`` (derived SDIF representation with rel/rules blocks).

Usage:
    python -m sdif_benchmarks.generators.generate_semantic_golden [--output-dir PATH]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from sdif_benchmarks.infra import BENCHMARK_DIR as BENCHMARKS_ROOT
SDIF_CORE_REPO = (
    Path(os.environ.get("SDIF_CORE_REPO") or str(BENCHMARKS_ROOT.parent)).expanduser().resolve()
)
SDIF_SRC = SDIF_CORE_REPO / "src"
DEFAULT_OUTPUT_DIR = SDIF_CORE_REPO / "examples" / "golden"

JsonObject = dict[str, Any]

FIXTURE_NAMES = [
    "semantic-narrative",
    "audit-provenance",
    "agent-workflow",
    "llm-api-response",
]


def _ensure_sdif_on_path() -> None:
    """Add SDIF src to sys.path if not already present."""
    sdif_src = str(SDIF_SRC)
    if sdif_src not in sys.path:
        sys.path.insert(0, sdif_src)


def _rel(subject: str, predicate: str, obj: str) -> JsonObject:
    return {"subject": subject, "predicate": predicate, "object": obj}


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------


def _narrative_findings() -> list[JsonObject]:
    return [
        {"id": "F001", "category": "security", "severity": "high", "source": "pentest-2026-Q1"},
        {"id": "F002", "category": "privacy", "severity": "medium", "source": "gdpr-review"},
        {"id": "F003", "category": "availability", "severity": "low", "source": "sla-audit"},
        {"id": "F004", "category": "integrity", "severity": "high", "source": "code-review"},
    ]


def _narrative_recommendations() -> list[JsonObject]:
    return [
        {"id": "R001", "finding_id": "F001", "action": "rotate-credentials", "priority": "P1"},
        {"id": "R002", "finding_id": "F002", "action": "anonymize-logs", "priority": "P2"},
        {"id": "R003", "finding_id": "F003", "action": "add-redundancy", "priority": "P2"},
        {"id": "R004", "finding_id": "F004", "action": "enforce-signing", "priority": "P1"},
    ]


def make_semantic_narrative() -> JsonObject:
    """Build the semantic-narrative fixture (ResearchReport kind)."""
    return {
        "kind": "ResearchReport",
        "id": "RPT-2026-001",
        "title": "Security and Reliability Assessment Q1 2026",
        "status": "published",
        "narrative_methodology": (
            "Automated scanning combined with manual expert review across four domains."
        ),
        "narrative_conclusion": (
            "Four findings require remediation before the next release window."
        ),
        "findings": _narrative_findings(),
        "recommendations": _narrative_recommendations(),
        "rel": [
            _rel("R001", "addresses", "F001"),
            _rel("R002", "addresses", "F002"),
            _rel("R003", "addresses", "F003"),
            _rel("R004", "addresses", "F004"),
            _rel("F001", "escalates", "F004"),
        ],
        "rules": [
            "(deny publish-if-unresolved finding.severity high finding.status open)",
            "(warn missing-sign-off recommendation.priority P1)",
        ],
    }


def _audit_events() -> list[JsonObject]:
    return [
        {"id": "EVT-001", "actor": "alice", "action": "create", "timestamp": "2026-05-01T09:00Z"},
        {"id": "EVT-002", "actor": "bob", "action": "review", "timestamp": "2026-05-01T10:30Z"},
        {"id": "EVT-003", "actor": "carol", "action": "approve", "timestamp": "2026-05-01T11:45Z"},
        {"id": "EVT-004", "actor": "dave", "action": "publish", "timestamp": "2026-05-01T14:00Z"},
        {"id": "EVT-005", "actor": "eve", "action": "archive", "timestamp": "2026-05-02T08:00Z"},
    ]


def _audit_provenance() -> list[JsonObject]:
    return [
        {
            "artifact": "report-v2.sdif",
            "derived_from": "report-v1.sdif",
            "via": "patch-20260501",
        },
        {
            "artifact": "summary.pdf",
            "derived_from": "report-v2.sdif",
            "via": "render-pipeline",
        },
    ]


def make_audit_provenance() -> JsonObject:
    """Build the audit-provenance fixture (AuditLog kind)."""
    return {
        "kind": "AuditLog",
        "id": "AUDIT-2026-05",
        "artifact": "report-v2.sdif",
        "events": _audit_events(),
        "provenance": _audit_provenance(),
        "rel": [
            _rel("EVT-001", "follows", "EVT-002"),
            _rel("EVT-002", "follows", "EVT-003"),
            _rel("EVT-003", "follows", "EVT-004"),
            _rel("report-v2.sdif", "derived_from", "report-v1.sdif"),
            _rel("EVT-003", "approves", "report-v2.sdif"),
        ],
        "rules": [
            "(deny delete-event event.actor system)",
            "(warn insufficient-approvers artifact.sensitivity high)",
        ],
    }


def _workflow_tasks() -> list[JsonObject]:
    return [
        {"id": "T001", "agent": "planner", "action": "decompose", "status": "done", "tokens": 312},
        {"id": "T002", "agent": "researcher", "action": "search", "status": "done", "tokens": 870},
        {"id": "T003", "agent": "coder", "action": "implement", "status": "done", "tokens": 1540},
        {"id": "T004", "agent": "reviewer", "action": "critique", "status": "done", "tokens": 640},
        {"id": "T005", "agent": "writer", "action": "summarise", "status": "done", "tokens": 420},
    ]


def _workflow_tool_calls() -> list[JsonObject]:
    return [
        {"task_id": "T002", "tool": "web_search", "count": 4},
        {"task_id": "T003", "tool": "bash", "count": 11},
        {"task_id": "T003", "tool": "edit_file", "count": 7},
        {"task_id": "T004", "tool": "read_file", "count": 3},
    ]


def make_agent_workflow() -> JsonObject:
    """Build the agent-workflow fixture (AgentWorkflow kind)."""
    return {
        "kind": "AgentWorkflow",
        "id": "WF-2026-0521",
        "session_id": "sess-abc123",
        "model": "claude-sonnet-4-6",
        "tasks": _workflow_tasks(),
        "tool_calls": _workflow_tool_calls(),
        "rel": [
            _rel("T001", "depends_on", "T002"),
            _rel("T002", "depends_on", "T003"),
            _rel("T003", "depends_on", "T004"),
            _rel("T004", "depends_on", "T005"),
            _rel("T003", "uses_output_of", "T002"),
        ],
        "rules": [
            "(deny start-task task.depends_on.status pending)",
            "(warn token-budget-exceeded task.tokens 1000)",
        ],
    }


def _api_repos() -> list[JsonObject]:
    return [
        {
            "id": "REPO-001",
            "name": "tree-sitter",
            "language": "C",
            "stars": 18200,
            "last_commit": "2026-05-20",
        },
        {
            "id": "REPO-002",
            "name": "pygments",
            "language": "Python",
            "stars": 9400,
            "last_commit": "2026-05-18",
        },
        {
            "id": "REPO-003",
            "name": "bat",
            "language": "Rust",
            "stars": 47000,
            "last_commit": "2026-05-19",
        },
        {
            "id": "REPO-004",
            "name": "highlight.js",
            "language": "JavaScript",
            "stars": 23100,
            "last_commit": "2026-04-30",
        },
    ]


def _api_contributors() -> list[JsonObject]:
    return [
        {"repo_id": "REPO-001", "login": "maxbrunsfeld", "commits": 612},
        {"repo_id": "REPO-002", "login": "birkenfeld", "commits": 1430},
        {"repo_id": "REPO-003", "login": "sharkdp", "commits": 890},
        {"repo_id": "REPO-004", "login": "jvilk", "commits": 340},
    ]


def make_llm_api_response() -> JsonObject:
    """Build the llm-api-response fixture (APISnapshot kind)."""
    return {
        "kind": "APISnapshot",
        "id": "SNAP-2026-0521",
        "source": "github-api-v4",
        "filtered_for": "syntax-highlighting",
        "metadata_fetched_at": "2026-05-21T00:00:00Z",
        "metadata_min_stars": 5000,
        "metadata_active_last_days": 90,
        "repos": _api_repos(),
        "contributors": _api_contributors(),
        "rel": [
            _rel("REPO-001", "benchmarks", "REPO-002"),
            _rel("REPO-003", "provides_editor_for", "REPO-001"),
            _rel("REPO-004", "provides_editor_for", "REPO-001"),
            _rel("REPO-002", "contributes_to", "REPO-004"),
            _rel("REPO-003", "contributes_to", "REPO-002"),
        ],
        "rules": [
            "(deny include-repo repo.stars below-threshold)",
            "(warn stale-metadata metadata.age_days 7)",
        ],
    }


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------


FIXTURE_BUILDERS: dict[str, Callable[[], JsonObject]] = {
    "semantic-narrative": make_semantic_narrative,
    "audit-provenance": make_audit_provenance,
    "agent-workflow": make_agent_workflow,
    "llm-api-response": make_llm_api_response,
}


def write_fixture(output_dir: Path, name: str, data: JsonObject) -> None:
    """Write equivalent.json, source.sdif, canonical.sdif, and canonical.sha256."""
    _ensure_sdif_on_path()
    from sdif import canonicalize, sdif_hash  # deferred: SDIF src path injected by _ensure_sdif_on_path() above
    from sdif.json import json_data_to_sdif  # deferred: SDIF src path injected by _ensure_sdif_on_path() above

    fixture_dir = output_dir / name
    fixture_dir.mkdir(parents=True, exist_ok=True)

    (fixture_dir / "equivalent.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    sdif_text = json_data_to_sdif(data, include_header=True)
    (fixture_dir / "source.sdif").write_text(sdif_text, encoding="utf-8")
    canonical_text = canonicalize(sdif_text)
    (fixture_dir / "canonical.sdif").write_text(canonical_text, encoding="utf-8")
    (fixture_dir / "canonical.sha256").write_text(sdif_hash(sdif_text) + "\n", encoding="utf-8")


def generate_all(output_dir: Path) -> None:
    """Generate all four semantic fixtures into output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, builder in FIXTURE_BUILDERS.items():
        write_fixture(output_dir, name, builder())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Entry point for the generate_semantic_golden CLI."""
    parser = argparse.ArgumentParser(
        description="Generate semantic golden fixtures for the SDIF benchmark suite."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to write fixtures into (default: ../sdif/examples/golden/)",
    )
    args = parser.parse_args(argv)

    generate_all(args.output_dir)
    print(f"Generated {len(FIXTURE_BUILDERS)} semantic fixtures in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
