"""Tests verifying that the public SDIF API exposes semantic axes needed by the benchmark.

Covers:
- Relations extracted as ``rel`` list of subject/predicate/object dicts
- Rules extracted as ``rules`` list of strings
- Tables extracted as uniform object arrays (separate from rel and rules)
- Scalar fields extracted correctly
- ``expand_ai_doc`` result passes through ``document_to_json_data`` and preserves rel
- ``_can_emit_as_table`` correctly distinguishes uniform dicts from plain strings
"""

from __future__ import annotations

import sys
from pathlib import Path


BENCHMARKS_ROOT = Path(__file__).resolve().parents[1]
SDIF_SRC = BENCHMARKS_ROOT.parent / "src"

if str(SDIF_SRC) not in sys.path:
    sys.path.insert(0, str(SDIF_SRC))

from sdif import parse_text  # noqa: E402
from sdif.ai import expand_ai_doc  # noqa: E402
from sdif.json import document_to_json_data  # noqa: E402
from sdif.json.converter import _can_emit_as_table  # noqa: E402

# ---------------------------------------------------------------------------
# Shared SDIF fixture source used by multiple tests
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


def _parse_full() -> dict[str, object]:
    """Parse FULL_SOURCE and return JSON data."""
    return document_to_json_data(parse_text(FULL_SOURCE))


# ---------------------------------------------------------------------------
# Relation extraction
# ---------------------------------------------------------------------------


def test_public_extraction_detects_relations() -> None:
    data = _parse_full()
    assert "rel" in data
    assert data["rel"]


def test_relation_entries_have_subject_predicate_object() -> None:
    data = _parse_full()
    rel = data["rel"]
    assert isinstance(rel, list)
    entry = rel[0]
    assert isinstance(entry, dict)
    assert set(entry.keys()) >= {"subject", "predicate", "object"}


def test_relation_values_are_correct() -> None:
    data = _parse_full()
    entry = data["rel"][0]
    assert entry["subject"] == "A"
    assert entry["predicate"] == "depends_on"
    assert entry["object"] == "B"


# ---------------------------------------------------------------------------
# Rule extraction
# ---------------------------------------------------------------------------


def test_public_extraction_detects_rules() -> None:
    data = _parse_full()
    assert "rules" in data
    assert data["rules"]


def test_rules_are_list_of_strings() -> None:
    data = _parse_full()
    rules = data["rules"]
    assert isinstance(rules, list)
    assert all(isinstance(r, str) for r in rules)


def test_rule_value_is_correct() -> None:
    data = _parse_full()
    assert data["rules"][0] == "(deny missing(id))"


# ---------------------------------------------------------------------------
# Table extraction
# ---------------------------------------------------------------------------


def test_table_extracted_as_uniform_object_array() -> None:
    data = _parse_full()
    assert "items" in data
    items = data["items"]
    assert isinstance(items, list)
    assert all(isinstance(row, dict) for row in items)


def test_table_rows_have_correct_columns() -> None:
    data = _parse_full()
    items = data["items"]
    assert items[0] == {"id": "A", "value": 1}
    assert items[1] == {"id": "B", "value": 2}


def test_table_does_not_appear_under_rel_or_rules_keys() -> None:
    data = _parse_full()
    # rel and rules must remain their own semantic keys, not folded into a table
    assert isinstance(data.get("rel"), list)
    assert isinstance(data.get("rules"), list)
    assert not isinstance(data.get("rel", [{}])[0], str)


# ---------------------------------------------------------------------------
# Scalar field extraction
# ---------------------------------------------------------------------------


def test_scalar_fields_extracted_correctly() -> None:
    data = _parse_full()
    assert data["kind"] == "Test"
    assert data["id"] == "t.1"


# ---------------------------------------------------------------------------
# expand_ai_doc round-trip with rel preservation
# ---------------------------------------------------------------------------


AI_SOURCE_WITH_REL = "@sdif.ai 1.0\nalias[d=depends_on]\nkind Test\nid t.1\n\nrel:\n  A\td\tB\n"


def test_expand_ai_doc_result_passes_to_document_to_json_data() -> None:
    doc = expand_ai_doc(AI_SOURCE_WITH_REL)
    data = document_to_json_data(doc)
    assert isinstance(data, dict)


def test_expand_ai_doc_preserves_rel_after_alias_expansion() -> None:
    doc = expand_ai_doc(AI_SOURCE_WITH_REL)
    data = document_to_json_data(doc)
    assert "rel" in data
    assert data["rel"]
    entry = data["rel"][0]
    assert entry["subject"] == "A"
    assert entry["predicate"] == "depends_on", (
        "alias 'd' should be expanded to canonical 'depends_on'"
    )
    assert entry["object"] == "B"


# ---------------------------------------------------------------------------
# _can_emit_as_table distinguishes uniform dicts from plain strings
# ---------------------------------------------------------------------------

REL_LIST = [{"subject": "A", "predicate": "depends_on", "object": "B"}]
RULES_LIST = ["(deny missing(id))"]
ITEMS_LIST = [{"id": "A", "value": 1}, {"id": "B", "value": 2}]


def test_uniform_object_array_is_recognised_as_table_candidate() -> None:
    assert _can_emit_as_table(ITEMS_LIST) is True


def test_rel_list_is_recognised_as_table_candidate() -> None:
    # rel entries are uniform dicts — _can_emit_as_table returns True
    assert _can_emit_as_table(REL_LIST) is True


def test_rules_list_of_strings_is_not_a_table_candidate() -> None:
    # rules are plain strings, not uniform dicts
    assert _can_emit_as_table(RULES_LIST) is False


def test_empty_list_is_not_a_table_candidate() -> None:
    assert _can_emit_as_table([]) is False
