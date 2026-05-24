"""Tests for the semantic_fidelity benchmark script.

Covers:
- SDIF→SDIF round-trip returns 1.0 on all axes
- JSON preserves relations structurally (rel key round-trips)
- SemanticFidelityResult has no native_relation_support attribute
- CSV Bundle parse-back recovers flat tables
- Formats without parsers (TOON) use None, not 0.0, for metrics
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


BENCHMARKS_ROOT = Path(__file__).resolve().parents[1]
SDIF_SRC = BENCHMARKS_ROOT.parent / "src"
SCRIPTS_DIR = BENCHMARKS_ROOT / "scripts"

if str(SDIF_SRC) not in sys.path:
    sys.path.insert(0, str(SDIF_SRC))
if str(BENCHMARKS_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(BENCHMARKS_ROOT / "src"))


def _load_module(name: str, path: Path) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


sf = _load_module("semantic_fidelity", SCRIPTS_DIR / "semantic_fidelity.py")

measure_semantic_fidelity = sf.measure_semantic_fidelity  # type: ignore[attr-defined]
SemanticFidelityResult = sf.SemanticFidelityResult  # type: ignore[attr-defined]

# ---------------------------------------------------------------------------
# Shared SDIF fixture with all semantic axes
# ---------------------------------------------------------------------------

FULL_SOURCE = (
    "@sdif 1.0\n"
    "kind Test\n"
    "id t.1\n"
    "\n"
    "items[id,value]:\n"
    "  A\t1\n"
    "  B\t2\n"
    "\n"
    "rel:\n"
    "  A\tdepends_on\tB\n"
    "\n"
    "rules:\n"
    "  (deny missing(id))\n"
)


# ---------------------------------------------------------------------------
# SDIF round-trip: all structural axes should be 1.0
# ---------------------------------------------------------------------------


def test_sdif_roundtrip_structural_fidelity_is_1() -> None:
    """SDIF→SDIF: canonicalized text round-trips all axes to 1.0."""
    from sdif.canonical import canonicalize

    canonical = canonicalize(FULL_SOURCE)
    result = measure_semantic_fidelity("SDIF", FULL_SOURCE, canonical)
    assert result.relation_structural_fidelity == 1.0, (
        f"Expected relation_structural_fidelity=1.0, got {result.relation_structural_fidelity}"
    )
    assert result.table_structural_fidelity == 1.0, (
        f"Expected table_structural_fidelity=1.0, got {result.table_structural_fidelity}"
    )
    assert result.field_structural_fidelity == 1.0, (
        f"Expected field_structural_fidelity=1.0, got {result.field_structural_fidelity}"
    )


def test_sdif_roundtrip_parse_back_status_is_ok() -> None:
    """SDIF format parse-back status is 'ok'."""
    from sdif.canonical import canonicalize

    canonical = canonicalize(FULL_SOURCE)
    result = measure_semantic_fidelity("SDIF", FULL_SOURCE, canonical)
    assert result.parse_back_status == "ok"


# ---------------------------------------------------------------------------
# JSON preserves relations structurally
# ---------------------------------------------------------------------------


def test_json_preserves_relations_structurally() -> None:
    """JSON output preserves rel key as uniform object array → fidelity=1.0."""
    from sdif import parse_text
    from sdif.json import document_to_json_data

    json_text = json.dumps(document_to_json_data(parse_text(FULL_SOURCE)))
    result = measure_semantic_fidelity("JSON Compact", FULL_SOURCE, json_text)
    assert result.relation_structural_fidelity == 1.0, (
        f"Expected 1.0, got {result.relation_structural_fidelity}"
    )
    assert result.parse_back_status == "ok"


# ---------------------------------------------------------------------------
# No capability flags on the result dataclass
# ---------------------------------------------------------------------------


def test_semantic_fidelity_result_has_no_native_relation_support_attr() -> None:
    """Capability flags belong in operability.py, not in SemanticFidelityResult."""
    from sdif.canonical import canonicalize

    canonical = canonicalize(FULL_SOURCE)
    result = measure_semantic_fidelity("SDIF", FULL_SOURCE, canonical)
    assert not hasattr(result, "native_relation_support"), (
        "native_relation_support is a capability flag and must not appear on SemanticFidelityResult"
    )


# ---------------------------------------------------------------------------
# CSV Bundle recovers flat table
# ---------------------------------------------------------------------------


def test_csv_bundle_recovers_flat_table() -> None:
    """CSV Bundle parse-back should recover table rows → table_structural_fidelity=1.0."""
    from formats import build_formats_dict
    from sdif import parse_text
    from sdif.json import document_to_json_data

    data = document_to_json_data(parse_text(FULL_SOURCE))
    formats = build_formats_dict(data)
    csv_text = formats.get("CSV Bundle", "")
    result = measure_semantic_fidelity("CSV Bundle", FULL_SOURCE, csv_text)
    if result.table_structural_fidelity is not None:
        assert result.table_structural_fidelity == 1.0, (
            f"CSV Bundle should recover table rows, got {result.table_structural_fidelity}"
        )


def test_csv_bundle_recovers_rules_as_list() -> None:
    """CSV Bundle encodes rules as JSON-encoded string; parse-back should recover it."""
    from formats import build_formats_dict
    from sdif import parse_text
    from sdif.json import document_to_json_data

    data = document_to_json_data(parse_text(FULL_SOURCE))
    formats = build_formats_dict(data)
    csv_text = formats.get("CSV Bundle", "")
    result = measure_semantic_fidelity("CSV Bundle", FULL_SOURCE, csv_text)
    # rules are scalars in CSV, but json.loads should recover the list
    # rule_structural_fidelity should be 1.0 or None (not 0.0)
    if result.rule_structural_fidelity is not None:
        assert result.rule_structural_fidelity == 1.0, (
            f"CSV Bundle should recover rules via json.loads, got {result.rule_structural_fidelity}"
        )


# ---------------------------------------------------------------------------
# TOON (no parser) uses None, not 0.0
# ---------------------------------------------------------------------------


def test_unparsed_formats_use_none_not_zero() -> None:
    """TOON (no parser) yields None for all metrics and 'not_measured' status."""
    result = measure_semantic_fidelity("TOON", FULL_SOURCE, "some toon content")
    assert result.table_structural_fidelity is None, (
        f"Expected None for TOON, got {result.table_structural_fidelity}"
    )
    assert result.relation_structural_fidelity is None
    assert result.rule_structural_fidelity is None
    assert result.field_structural_fidelity is None
    assert result.parse_back_status == "not_measured"


# ---------------------------------------------------------------------------
# Result dataclass has the correct fields
# ---------------------------------------------------------------------------


def test_semantic_fidelity_result_fields() -> None:
    """SemanticFidelityResult has all documented nullable metric fields."""
    from sdif.canonical import canonicalize

    canonical = canonicalize(FULL_SOURCE)
    result = measure_semantic_fidelity("SDIF", FULL_SOURCE, canonical)
    assert hasattr(result, "format_name")
    assert hasattr(result, "relation_structural_fidelity")
    assert hasattr(result, "rule_structural_fidelity")
    assert hasattr(result, "table_structural_fidelity")
    assert hasattr(result, "field_structural_fidelity")
    assert hasattr(result, "parse_back_status")
    assert hasattr(result, "note")
    assert result.format_name == "SDIF"


# ---------------------------------------------------------------------------
# parse_back_status values are valid
# ---------------------------------------------------------------------------


def test_parse_back_status_valid_values() -> None:
    """parse_back_status must be one of the four defined values."""
    valid = {"ok", "best_effort", "not_measured", "parse_error"}
    from formats import build_formats_dict
    from sdif import parse_text
    from sdif.json import document_to_json_data

    data = document_to_json_data(parse_text(FULL_SOURCE))
    formats = build_formats_dict(data)

    for format_name, text in formats.items():
        result = measure_semantic_fidelity(format_name, FULL_SOURCE, text)
        assert result.parse_back_status in valid, (
            f"Format {format_name!r} returned invalid parse_back_status={result.parse_back_status!r}"
        )


# ---------------------------------------------------------------------------
# Empty axis → None (not 0.0)
# ---------------------------------------------------------------------------


SOURCE_NO_REL = "@sdif 1.0\nkind Test\nid t.1\n\nitems[id,value]:\n  A\t1\n"


def test_empty_rel_axis_returns_none() -> None:
    """When source has no relations, relation_structural_fidelity should be None."""
    from sdif.canonical import canonicalize

    canonical = canonicalize(SOURCE_NO_REL)
    result = measure_semantic_fidelity("SDIF", SOURCE_NO_REL, canonical)
    assert result.relation_structural_fidelity is None, (
        f"No rels in source → should be None, got {result.relation_structural_fidelity}"
    )
