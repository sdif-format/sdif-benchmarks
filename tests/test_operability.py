"""Tests for the operability matrix benchmark.

Verifies that build_operability_matrix() returns accurate capability records
for each supported format, focusing on semantic distinctions that matter:
rule declaration vs evaluation, standard vs built-in canonicalization, and
native relation support.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def _load_operability_module():
    module_path = Path("scripts/operability.py")
    spec = importlib.util.spec_from_file_location("operability", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["operability"] = module
    spec.loader.exec_module(module)
    return module


operability = _load_operability_module()
build_operability_matrix = operability.build_operability_matrix


def test_build_operability_matrix_returns_all_formats() -> None:
    matrix = build_operability_matrix()
    names = {r.format_name for r in matrix}
    assert "SDIF" in names
    assert "SDIF AI" in names
    assert "JSON Compact" in names
    assert "CSV Bundle" in names


def test_sdif_distinguishes_rule_declaration_from_evaluation() -> None:
    sdif = next(r for r in build_operability_matrix() if r.format_name == "SDIF")
    assert sdif.rule_declaration_support is True
    assert sdif.rule_evaluation_support is False


def test_xml_standard_but_not_builtin_canonical() -> None:
    xml = next(r for r in build_operability_matrix() if r.format_name == "XML")
    assert xml.standard_canonical_form is True
    assert xml.builtin_canonical_form is False


def test_json_has_no_semantic_type_vocabulary() -> None:
    json_c = next(r for r in build_operability_matrix() if r.format_name == "JSON Compact")
    assert json_c.native_relation_support is False
    assert json_c.semantic_type_vocabulary is False


def test_sdif_ai_notes_via_expansion() -> None:
    sdif_ai = next(r for r in build_operability_matrix() if r.format_name == "SDIF AI")
    assert "via expansion" in sdif_ai.notes.lower()


def test_csv_bundle_no_native_relation_support() -> None:
    csv = next(r for r in build_operability_matrix() if r.format_name == "CSV Bundle")
    assert csv.native_relation_support is False
    assert csv.rule_declaration_support is False


def test_main_writes_suite_compatible_summary_artifacts(tmp_path) -> None:
    exit_code = operability.main(["--output-dir", str(tmp_path)])

    assert exit_code == 0
    assert (tmp_path / "summary.md").is_file()
    assert (tmp_path / "summary.json").is_file()
    assert (tmp_path / "operability_matrix.md").is_file()

    payload = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert payload["kind"] == "OperabilityMatrixReport"
    assert any(row["format"] == "SDIF" for row in payload["formats"])
