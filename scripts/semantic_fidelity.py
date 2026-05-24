#!/usr/bin/env python3
"""Semantic fidelity benchmark.

Measures structural recoverability of SDIF semantic axes (relations, rules,
tables, scalar fields) after converting to each format and parsing back.

For each format, the benchmark:
1. Extracts the source semantic axes from the SDIF document.
2. Converts to format via build_formats_dict.
3. Parses back where a parser is available.
4. Compares each axis structurally (tuple-equality or key-set overlap).

Axes measured:
- relation_structural_fidelity: fraction of (subject, predicate, object) triples recovered
- rule_structural_fidelity:     fraction of rule strings recovered
- table_structural_fidelity:    fraction of table row objects recovered
- field_structural_fidelity:    fraction of scalar fields recovered

None means the axis was not present in the source (nothing to measure) or that
no parser is available for the format.  0.0 means measured and nothing survived.

Each run writes persistent evidence to:
- benchmarks/tmp/semantic_fidelity  while running
- benchmarks/results/semantic_fidelity  on success

Environment variables:
- SDIF_BENCHMARK_OUTPUT_DIR=<path>  Redirect evidence. Default: benchmarks/.
- SDIF_BENCHMARK_GOLDEN_DIR=<path>  Corpus directory. Default: examples/golden.
- SDIF_BENCHMARK_TOON=0            Disable TOON evaluation.
- SDIF_BENCHMARK_VERBOSE=1         Print diagnostic warnings.
"""

from __future__ import annotations

import contextlib
import csv
import json
import sys
import xml.etree.ElementTree as ET

import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_BENCHMARK_DIR = Path(__file__).resolve().parent.parent
if str(_BENCHMARK_DIR / "src") not in sys.path:
    sys.path.insert(0, str(_BENCHMARK_DIR / "src"))

import formats as fmt  # noqa: E402
from infra import (  # noqa: E402
    REPO_ROOT,
    Tee,
    benchmark_golden_dir,
    benchmark_result_dir,
    create_benchmark_run_dir,
    discover_documents,
    display_path,
    load_env_file,
    markdown_escape,
    publish_benchmark_result,
    utc_now_iso,
    verbose_warning,
)

from sdif.ai import ai_view, expand_ai_doc  # noqa: E402
from sdif.canonical import canonicalize  # noqa: E402
from sdif.core.policy import Policy  # noqa: E402
from sdif.json import document_to_json_data  # noqa: E402
from sdif import parse_text  # noqa: E402

BENCHMARK_TRACK_NAME = "semantic_fidelity"

_BENCHMARK_POLICY = Policy(
    max_document_size=10_000_000,
    max_table_row_count=100_000,
    max_string_length=1_000_000,
)

_DISCLAIMER = (
    "Structural fidelity measures recoverability of data.\n"
    "A missing parser is reported as not_measured, not 0%.\n"
    "CSV may preserve flat tables well but has no native relation semantics.\n"
    "JSON/YAML may preserve rel structurally but do not have native relation semantics.\n"
    "XML/TOON may be best-effort depending on parse-back support.\n"
)


# ====================
# Data model
# ====================


@dataclass
class SemanticFidelityResult:
    """Per-format semantic fidelity measurement."""

    format_name: str
    relation_structural_fidelity: float | None
    rule_structural_fidelity: float | None
    table_structural_fidelity: float | None
    field_structural_fidelity: float | None
    parse_back_status: str  # "ok" | "best_effort" | "not_measured" | "parse_error"
    note: str = ""


@dataclass
class DocumentFidelity:
    """All format measurements for one document."""

    document_name: str
    results: list[SemanticFidelityResult]


@dataclass
class SemanticFidelityEvidence:
    """Full benchmark run evidence."""

    generated_at: str
    run_dir: Path
    golden_dir: Path
    documents: list[DocumentFidelity]
    env_file_loaded: bool


# ====================
# Source axis extraction
# ====================


def _extract_axes(
    source_sdif: str,
) -> tuple[
    list[tuple[str, str, str]],  # relations
    list[str],                   # rules
    dict[str, list[dict[str, Any]]],  # tables (name -> rows)
    dict[str, Any],              # scalar fields
]:
    """Extract semantic axes from SDIF source using the public API."""
    doc = parse_text(source_sdif, policy=_BENCHMARK_POLICY)
    json_repr = document_to_json_data(doc)
    relations = [
        (r["subject"], r["predicate"], r["object"])
        for r in json_repr.get("rel", [])
        if isinstance(r, dict)
    ]
    rules = [str(r) for r in json_repr.get("rules", [])]
    tables = {
        k: v
        for k, v in json_repr.items()
        if isinstance(v, list) and v and isinstance(v[0], dict) and k not in {"rel", "rules"}
    }
    fields = {k: v for k, v in json_repr.items() if not isinstance(v, (list, dict))}
    return relations, rules, tables, fields


# ====================
# Structural overlap scoring
# ====================


def _frac(recovered: int, total: int) -> float:
    """Return fraction of items recovered, avoiding division by zero."""
    return recovered / total if total > 0 else 0.0


def _structural_overlap_none_if_empty(
    source_items: list[Any], recovered_items: list[Any] | None
) -> float | None:
    """Return overlap fraction, or None if source is empty."""
    if not source_items:
        return None
    if recovered_items is None:
        return None
    source_set = set(
        json.dumps(item, sort_keys=True) if isinstance(item, dict) else str(item)
        for item in source_items
    )
    recovered_set = set(
        json.dumps(item, sort_keys=True) if isinstance(item, dict) else str(item)
        for item in recovered_items
    )
    matched = len(source_set & recovered_set)
    return _frac(matched, len(source_set))


def _relation_fidelity(
    source_rels: list[tuple[str, str, str]],
    recovered_data: dict[str, Any] | None,
) -> float | None:
    """Structural fidelity for relation triples."""
    if not source_rels:
        return None
    if recovered_data is None:
        return None
    raw = recovered_data.get("rel", [])
    if not isinstance(raw, list):
        return 0.0
    recovered_rels = [
        (r["subject"], r["predicate"], r["object"])
        for r in raw
        if isinstance(r, dict) and "subject" in r and "predicate" in r and "object" in r
    ]
    return _frac(
        len(set(source_rels) & set(recovered_rels)),
        len(set(source_rels)),
    )


def _rule_fidelity(
    source_rules: list[str],
    recovered_data: dict[str, Any] | None,
) -> float | None:
    """Structural fidelity for rule strings."""
    if not source_rules:
        return None
    if recovered_data is None:
        return None
    raw = recovered_data.get("rules", [])
    if isinstance(raw, str):
        # Some formats (CSV) encode rules as JSON-encoded string
        try:
            raw = json.loads(raw)
        except Exception:
            raw = [raw]
    if not isinstance(raw, list):
        return 0.0
    recovered_rules = [str(r) for r in raw]
    return _frac(
        len(set(source_rules) & set(recovered_rules)),
        len(set(source_rules)),
    )


def _table_fidelity(
    source_tables: dict[str, list[dict[str, Any]]],
    recovered_data: dict[str, Any] | None,
) -> float | None:
    """Structural fidelity for uniform table rows across all tables."""
    if not source_tables:
        return None
    if recovered_data is None:
        return None
    total_rows = 0
    matched_rows = 0
    for table_name, src_rows in source_tables.items():
        rec_raw = recovered_data.get(table_name)
        if not isinstance(rec_raw, list):
            total_rows += len(src_rows)
            continue
        src_set = {json.dumps(r, sort_keys=True) for r in src_rows}
        rec_set = {json.dumps(r, sort_keys=True) for r in rec_raw if isinstance(r, dict)}
        matched_rows += len(src_set & rec_set)
        total_rows += len(src_set)
    return _frac(matched_rows, total_rows) if total_rows > 0 else None


def _field_fidelity(
    source_fields: dict[str, Any],
    recovered_data: dict[str, Any] | None,
) -> float | None:
    """Structural fidelity for scalar fields."""
    if not source_fields:
        return None
    if recovered_data is None:
        return None
    matched = 0
    for key, val in source_fields.items():
        rec = recovered_data.get(key)
        if rec is not None and str(rec) == str(val):
            matched += 1
    return _frac(matched, len(source_fields))


# ====================
# Parse-back by format
# ====================


def _parse_json(text: str) -> dict[str, Any] | None:
    try:
        result = json.loads(text)
        return result if isinstance(result, dict) else None
    except Exception as exc:
        verbose_warning(f"JSON parse-back failed: {exc}")
        return None


def _parse_yaml(text: str) -> dict[str, Any] | None:
    try:
        result = yaml.safe_load(text)
        return result if isinstance(result, dict) else None
    except Exception as exc:
        verbose_warning(f"YAML parse-back failed: {exc}")
        return None


def _parse_xml(text: str) -> dict[str, Any] | None:
    try:
        src = text.split("\n", 1)[1] if text.startswith("<?xml") else text
        root = ET.fromstring(src)
        wrapped = _xml_to_dict(root)
        result = wrapped.get("document", wrapped) if isinstance(wrapped, dict) else wrapped
        return result if isinstance(result, dict) else None
    except Exception as exc:
        verbose_warning(f"XML parse-back failed: {exc}")
        return None


def _xml_to_dict(elem: ET.Element) -> dict[str, Any]:
    children = list(elem)
    if not children:
        return {elem.tag: elem.text or ""}
    result: dict[str, Any] = {}
    child_tags = [c.tag for c in children]
    if all(t == "item" for t in child_tags):
        items = [_xml_to_dict(c).get("item", c.text or "") for c in children]
        return {elem.tag: items}
    for child in children:
        child_children = list(child)
        if not child_children:
            result[child.tag] = child.text or ""
        elif all(c.tag == "item" for c in child_children):
            result[child.tag] = [
                _xml_to_dict(c).get("item", c.text or "") for c in child_children
            ]
        else:
            result[child.tag] = _xml_to_dict(child).get(child.tag, {})
    return {elem.tag: result}


def _parse_csv_bundle(text: str) -> dict[str, Any] | None:
    """Parse CSV Bundle format back to dict, recovering rules via json.loads."""
    try:
        result: dict[str, Any] = {}
        current_section: str | None = None
        current_rows: list[str] = []
        is_fields = False

        def flush() -> None:
            nonlocal current_rows, is_fields
            if not current_rows:
                return
            reader = csv.reader(current_rows)
            headers = next(reader, None)
            if headers is None:
                return
            if is_fields:
                for row in reader:
                    if len(row) >= 2:
                        result[row[0]] = _recover_csv_scalar(row[1])
            else:
                rows_list: list[dict[str, Any]] = []
                for row in reader:
                    rows_list.append(
                        {headers[i]: _recover_csv_scalar(row[i]) for i in range(min(len(headers), len(row)))}
                    )
                if current_section:
                    result[current_section] = rows_list
            current_rows = []

        for line in text.splitlines():
            if line.startswith("# fields"):
                flush()
                current_section = None
                is_fields = True
            elif line.startswith("# table:"):
                flush()
                current_section = line[len("# table:"):].strip()
                is_fields = False
            else:
                current_rows.append(line)

        flush()

        # Try to recover rules list from JSON-encoded scalar
        if "rules" in result and isinstance(result["rules"], str):
            try:
                parsed = json.loads(result["rules"])
                if isinstance(parsed, list):
                    result["rules"] = parsed
            except Exception:
                pass

        return result
    except Exception as exc:
        verbose_warning(f"CSV Bundle parse-back failed: {exc}")
        return None


def _recover_csv_scalar(value: str) -> str | int | float | bool | None:
    """Recover typed scalar from CSV string."""
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _parse_sdif(text: str) -> dict[str, Any] | None:
    try:
        doc = parse_text(text, policy=_BENCHMARK_POLICY)
        return document_to_json_data(doc)
    except Exception as exc:
        verbose_warning(f"SDIF parse-back failed: {exc}")
        return None


def _parse_sdif_ai(text: str) -> dict[str, Any] | None:
    try:
        if not text.startswith("@sdif"):
            text = "@sdif.ai 1.0\n" + text
        doc = expand_ai_doc(text, policy=_BENCHMARK_POLICY)
        return document_to_json_data(doc)
    except Exception as exc:
        verbose_warning(f"SDIF AI parse-back failed: {exc}")
        return None


# ====================
# Core measurement
# ====================


def measure_semantic_fidelity(
    format_name: str,
    source_sdif: str,
    converted_text: str,
) -> SemanticFidelityResult:
    """Measure structural fidelity of semantic axes for one format conversion."""
    source_rels, source_rules, source_tables, source_fields = _extract_axes(source_sdif)

    # TOON: no parser available
    if format_name == "TOON":
        return SemanticFidelityResult(
            format_name=format_name,
            relation_structural_fidelity=None,
            rule_structural_fidelity=None,
            table_structural_fidelity=None,
            field_structural_fidelity=None,
            parse_back_status="not_measured",
            note="no parser available",
        )

    # Attempt parse-back
    recovered: dict[str, Any] | None = None
    parse_status: str
    note: str = ""

    if format_name in ("JSON Compact", "JSON Pretty"):
        recovered = _parse_json(converted_text)
        parse_status = "ok" if recovered is not None else "parse_error"
    elif format_name == "YAML":
        recovered = _parse_yaml(converted_text)
        parse_status = "ok" if recovered is not None else "parse_error"
    elif format_name == "SDIF":
        recovered = _parse_sdif(converted_text)
        parse_status = "ok" if recovered is not None else "parse_error"
    elif format_name == "SDIF AI":
        recovered = _parse_sdif_ai(converted_text)
        parse_status = "ok" if recovered is not None else "parse_error"
    elif format_name == "CSV Bundle":
        recovered = _parse_csv_bundle(converted_text)
        parse_status = "ok" if recovered is not None else "parse_error"
        if recovered is not None:
            # CSV Bundle is lossy for nested structures
            parse_status = "best_effort"
    elif format_name == "XML":
        recovered = _parse_xml(converted_text)
        # XML parse-back is always best-effort due to type erasure
        parse_status = "best_effort" if recovered is not None else "parse_error"
    else:
        parse_status = "not_measured"

    if recovered is None and parse_status not in ("not_measured",):
        parse_status = "parse_error"
        note = "parse-back failed"
        return SemanticFidelityResult(
            format_name=format_name,
            relation_structural_fidelity=None,
            rule_structural_fidelity=None,
            table_structural_fidelity=None,
            field_structural_fidelity=None,
            parse_back_status=parse_status,
            note=note,
        )

    rel_fid = _relation_fidelity(source_rels, recovered)
    rule_fid = _rule_fidelity(source_rules, recovered)
    tbl_fid = _table_fidelity(source_tables, recovered)
    fld_fid = _field_fidelity(source_fields, recovered)

    return SemanticFidelityResult(
        format_name=format_name,
        relation_structural_fidelity=rel_fid,
        rule_structural_fidelity=rule_fid,
        table_structural_fidelity=tbl_fid,
        field_structural_fidelity=fld_fid,
        parse_back_status=parse_status,
        note=note,
    )


# ====================
# Benchmark runner
# ====================


def _build_format_texts(source_sdif: str) -> dict[str, str]:
    """Build format texts for all formats from SDIF source."""
    doc = parse_text(source_sdif, policy=_BENCHMARK_POLICY)
    json_data = document_to_json_data(doc)
    format_texts = fmt.build_formats_dict(json_data)
    # Override SDIF with the canonical form of the actual source
    format_texts["SDIF"] = canonicalize(source_sdif, policy=_BENCHMARK_POLICY)
    # Override SDIF AI with ai_view of actual source
    format_texts["SDIF AI"] = ai_view(source_sdif, fmt.AI_ALIASES, policy=_BENCHMARK_POLICY)
    return format_texts


def run_benchmark(
    run_dir: Path, *, env_file_loaded: bool
) -> SemanticFidelityEvidence:
    """Run the full semantic fidelity benchmark."""
    golden_dir = benchmark_golden_dir()
    doc_names = discover_documents(golden_dir)
    if not doc_names:
        raise SystemExit("No golden files found under examples/golden/*/equivalent.json")

    print("SDIF SEMANTIC FIDELITY BENCHMARK")
    print("Measures: structural recoverability of semantic axes per format\n")
    print(
        f"{'Document':<28} {'Format':<14} {'Rel':>6} {'Rule':>6} {'Table':>6} {'Field':>6}  Status"
    )
    print("=" * 100)

    all_results: list[DocumentFidelity] = []

    for doc_name in doc_names:
        source_path = golden_dir / doc_name / "source.sdif"
        json_path = golden_dir / doc_name / "equivalent.json"

        if source_path.exists():
            source_sdif = source_path.read_text(encoding="utf-8")
        else:
            from sdif.json import json_data_to_sdif
            json_data = json.loads(json_path.read_text(encoding="utf-8"))
            source_sdif = json_data_to_sdif(json_data, include_header=True)

        format_texts = _build_format_texts(source_sdif)
        results: list[SemanticFidelityResult] = []
        first = True

        for format_name, converted_text in format_texts.items():
            result = measure_semantic_fidelity(format_name, source_sdif, converted_text)
            results.append(result)

            prefix = doc_name if first else ""

            def _fmt(v: float | None) -> str:
                if v is None:
                    return "  N/A"
                return f"{v * 100:.0f}%"

            print(
                f"{prefix:<28} {result.format_name:<14} "
                f"{_fmt(result.relation_structural_fidelity):>6} "
                f"{_fmt(result.rule_structural_fidelity):>6} "
                f"{_fmt(result.table_structural_fidelity):>6} "
                f"{_fmt(result.field_structural_fidelity):>6}  "
                f"{result.parse_back_status}"
            )
            first = False

        print("-" * 100)
        all_results.append(DocumentFidelity(document_name=doc_name, results=results))

    return SemanticFidelityEvidence(
        generated_at=utc_now_iso(),
        run_dir=benchmark_result_dir(BENCHMARK_TRACK_NAME),
        golden_dir=golden_dir,
        documents=all_results,
        env_file_loaded=env_file_loaded,
    )


# ====================
# Reporting
# ====================


def _structured_data(evidence: SemanticFidelityEvidence) -> dict[str, Any]:
    return {
        "kind": "SemanticFidelityReport",
        "version": "1.0",
        "generatedAt": evidence.generated_at,
        "runDirectory": display_path(evidence.run_dir),
        "semanticSource": f"{display_path(evidence.golden_dir)}/<document>/source.sdif",
        "envFileLoaded": evidence.env_file_loaded,
        "documents": [
            {
                "name": doc.document_name,
                "formats": [
                    {
                        "format": r.format_name,
                        "relationStructuralFidelity": r.relation_structural_fidelity,
                        "ruleStructuralFidelity": r.rule_structural_fidelity,
                        "tableStructuralFidelity": r.table_structural_fidelity,
                        "fieldStructuralFidelity": r.field_structural_fidelity,
                        "parseBackStatus": r.parse_back_status,
                        "note": r.note,
                    }
                    for r in doc.results
                ],
            }
            for doc in evidence.documents
        ],
    }


def _fmt_score(v: float | None) -> str:
    if v is None:
        return "N/A"
    return f"{v * 100:.0f}%"


def _summary_md(evidence: SemanticFidelityEvidence) -> str:
    lines: list[str] = [
        "# SDIF Semantic Fidelity Benchmark — Summary",
        "",
        f"- Generated at: `{evidence.generated_at}`",
        f"- Documents: `{len(evidence.documents)}`",
        "",
        "## Disclaimer",
        "",
    ]
    lines.extend(_DISCLAIMER.splitlines())
    lines.extend([
        "",
        "## Results by Format",
        "",
        "| Format | Rel Fidelity | Rule Fidelity | Table Fidelity | Field Fidelity | Status |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ])

    # Aggregate by format
    format_scores: dict[str, dict[str, list[float]]] = {}
    for doc in evidence.documents:
        for r in doc.results:
            bucket = format_scores.setdefault(r.format_name, {
                "rel": [], "rule": [], "table": [], "field": []
            })
            if r.relation_structural_fidelity is not None:
                bucket["rel"].append(r.relation_structural_fidelity)
            if r.rule_structural_fidelity is not None:
                bucket["rule"].append(r.rule_structural_fidelity)
            if r.table_structural_fidelity is not None:
                bucket["table"].append(r.table_structural_fidelity)
            if r.field_structural_fidelity is not None:
                bucket["field"].append(r.field_structural_fidelity)

    def _avg(vals: list[float]) -> float | None:
        return sum(vals) / len(vals) if vals else None

    for fmt_name, buckets in sorted(format_scores.items()):
        lines.append(
            f"| {markdown_escape(fmt_name)} "
            f"| {_fmt_score(_avg(buckets['rel']))} "
            f"| {_fmt_score(_avg(buckets['rule']))} "
            f"| {_fmt_score(_avg(buckets['table']))} "
            f"| {_fmt_score(_avg(buckets['field']))} "
            f"| (see detail) |"
        )

    lines.append("")
    return "\n".join(lines)


def _comparison_json_data(evidence: SemanticFidelityEvidence) -> dict[str, Any]:
    """Per-document per-format detail for comparison.json."""
    rows: list[dict[str, Any]] = []
    for doc in evidence.documents:
        for r in doc.results:
            rows.append({
                "document": doc.document_name,
                "format": r.format_name,
                "relationStructuralFidelity": r.relation_structural_fidelity,
                "ruleStructuralFidelity": r.rule_structural_fidelity,
                "tableStructuralFidelity": r.table_structural_fidelity,
                "fieldStructuralFidelity": r.field_structural_fidelity,
                "parseBackStatus": r.parse_back_status,
                "note": r.note,
            })
    return {
        "kind": "SemanticFidelityComparison",
        "version": "1.0",
        "generatedAt": evidence.generated_at,
        "rows": rows,
    }


# ====================
# Main
# ====================


def main() -> int:
    """Run the semantic fidelity benchmark and write evidence."""
    env_file_loaded = load_env_file(REPO_ROOT / ".env")
    run_dir = create_benchmark_run_dir(BENCHMARK_TRACK_NAME)
    log_path = run_dir / "comparison.log"

    with log_path.open("w", encoding="utf-8") as log_file:
        with contextlib.redirect_stdout(Tee(sys.stdout, log_file)):
            evidence = run_benchmark(run_dir, env_file_loaded=env_file_loaded)
            structured = _structured_data(evidence)
            summary = _summary_md(evidence)
            comparison = _comparison_json_data(evidence)

            # Some format conversion helpers may clean benchmark tmp directories;
            # keep the evidence writer resilient so suite-level runs always publish
            # the semantic report artifacts for indexing.
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "summary.md").write_text(summary, encoding="utf-8")
            (run_dir / "summary.json").write_text(
                json.dumps(structured, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            (run_dir / "comparison.json").write_text(
                json.dumps(comparison, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            published = publish_benchmark_result(run_dir, BENCHMARK_TRACK_NAME)
            print(f"\nEvidence written to {display_path(published)}")
            print(f"  summary.md:      {display_path(published / 'summary.md')}")
            print(f"  summary.json:    {display_path(published / 'summary.json')}")
            print(f"  comparison.json: {display_path(published / 'comparison.json')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
