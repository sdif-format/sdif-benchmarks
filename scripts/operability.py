#!/usr/bin/env python3
"""Operability matrix benchmark for SDIF and peer formats.

Evaluates each format across eight semantic-capability axes:

- Canonical form availability (standard spec vs built-in implementation)
- Stable content-addressable hashing
- Schema validation
- Native relation support
- Rule declaration and evaluation
- Semantic type vocabulary
- Deterministic output

Results are written to results/operability_matrix.md as a Markdown table.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

RESULTS_FILENAME = "operability_matrix.md"

TABLE_HEADER = (
    "| Format | Std Canon | Builtin Canon | Stable Hash | Schema Val"
    " | Native Rel | Rule Decl | Rule Eval | Sem Types | Deterministic |\n"
)
TABLE_SEP = (
    "|--------|-----------|---------------|-------------|----------"
    "-|------------|-----------|-----------|-----------|---------------|\n"
)


@dataclass
class FormatOperability:
    """Capability record for a single serialization format."""

    format_name: str

    standard_canonical_form: bool
    builtin_canonical_form: bool
    stable_hash: bool
    schema_validation: bool

    native_relation_support: bool
    rule_declaration_support: bool
    rule_evaluation_support: bool
    semantic_type_vocabulary: bool

    deterministic_output: bool
    notes: str = ""


def build_operability_matrix() -> list[FormatOperability]:
    """Return capability records for all benchmark formats."""
    return [
        FormatOperability(
            format_name="SDIF",
            standard_canonical_form=True,
            builtin_canonical_form=True,
            stable_hash=True,
            schema_validation=True,
            native_relation_support=True,
            rule_declaration_support=True,
            rule_evaluation_support=False,  # no evaluator exists yet
            semantic_type_vocabulary=True,
            deterministic_output=True,
        ),
        FormatOperability(
            format_name="SDIF AI",
            standard_canonical_form=True,
            builtin_canonical_form=True,  # expand+canonicalize is built-in
            stable_hash=True,  # via expansion to canonical SDIF
            schema_validation=True,  # via expansion
            native_relation_support=True,  # via expansion
            rule_declaration_support=True,  # via expansion
            rule_evaluation_support=False,
            semantic_type_vocabulary=False,
            deterministic_output=True,
            notes="Available via expansion to canonical SDIF, not independently native.",
        ),
        FormatOperability(
            format_name="JSON Compact",
            standard_canonical_form=False,
            builtin_canonical_form=False,
            stable_hash=False,
            schema_validation=False,
            native_relation_support=False,
            rule_declaration_support=False,
            rule_evaluation_support=False,
            semantic_type_vocabulary=False,
            deterministic_output=True,
            notes="JSON Schema and RFC 8785 canonicalization exist externally.",
        ),
        FormatOperability(
            format_name="JSON Pretty",
            standard_canonical_form=False,
            builtin_canonical_form=False,
            stable_hash=False,
            schema_validation=False,
            native_relation_support=False,
            rule_declaration_support=False,
            rule_evaluation_support=False,
            semantic_type_vocabulary=False,
            deterministic_output=True,
            notes="JSON Schema and RFC 8785 canonicalization exist externally.",
        ),
        FormatOperability(
            format_name="YAML",
            standard_canonical_form=False,
            builtin_canonical_form=False,
            stable_hash=False,
            schema_validation=False,
            native_relation_support=False,
            rule_declaration_support=False,
            rule_evaluation_support=False,
            semantic_type_vocabulary=False,
            deterministic_output=False,  # anchors/aliases, tag ordering
            notes="No standard canonical form; multiple representations possible.",
        ),
        FormatOperability(
            format_name="XML",
            standard_canonical_form=True,
            builtin_canonical_form=False,  # W3C C14N exists but not built into this impl
            stable_hash=False,
            schema_validation=False,  # XSD exists externally
            native_relation_support=False,
            rule_declaration_support=False,
            rule_evaluation_support=False,
            semantic_type_vocabulary=False,
            deterministic_output=True,
            notes="W3C C14N and XSD exist externally; not built into this implementation.",
        ),
        FormatOperability(
            format_name="CSV Bundle",
            standard_canonical_form=False,
            builtin_canonical_form=False,
            stable_hash=False,
            schema_validation=False,
            native_relation_support=False,
            rule_declaration_support=False,
            rule_evaluation_support=False,
            semantic_type_vocabulary=False,
            deterministic_output=True,
            notes="Relations can be encoded as tables but are not native semantics.",
        ),
        FormatOperability(
            format_name="TOON",
            standard_canonical_form=False,
            builtin_canonical_form=False,
            stable_hash=False,
            schema_validation=False,
            native_relation_support=False,
            rule_declaration_support=False,
            rule_evaluation_support=False,
            semantic_type_vocabulary=False,
            deterministic_output=False,
            notes="Optional format; availability depends on SDIF_BENCHMARK_TOON=1.",
        ),
    ]


def _bool_cell(value: bool) -> str:
    """Render a boolean as a compact markdown table cell value."""
    return "Yes" if value else "No"


def _render_markdown_table(matrix: list[FormatOperability]) -> str:
    """Produce the full Markdown table string for the operability matrix."""
    lines: list[str] = [TABLE_HEADER, TABLE_SEP]
    for row in matrix:
        lines.append(
            f"| {row.format_name}"
            f" | {_bool_cell(row.standard_canonical_form)}"
            f" | {_bool_cell(row.builtin_canonical_form)}"
            f" | {_bool_cell(row.stable_hash)}"
            f" | {_bool_cell(row.schema_validation)}"
            f" | {_bool_cell(row.native_relation_support)}"
            f" | {_bool_cell(row.rule_declaration_support)}"
            f" | {_bool_cell(row.rule_evaluation_support)}"
            f" | {_bool_cell(row.semantic_type_vocabulary)}"
            f" | {_bool_cell(row.deterministic_output)}"
            f" |\n"
        )
    notes_section = _render_notes_section(matrix)
    return "".join(lines) + notes_section


def _render_notes_section(matrix: list[FormatOperability]) -> str:
    """Append a notes section for formats that carry extra context."""
    noted = [row for row in matrix if row.notes]
    if not noted:
        return ""
    parts = ["\n## Notes\n\n"]
    for row in noted:
        parts.append(f"**{row.format_name}**: {row.notes}\n\n")
    return "".join(parts)


def _write_results(output_dir: Path, content: str) -> Path:
    """Write the markdown table to output_dir, returning the output path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / RESULTS_FILENAME
    output_path.write_text(content, encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> int:
    """Run the operability benchmark, print summary to stdout, write file."""
    parser = argparse.ArgumentParser(
        description="Emit an operability matrix for SDIF and peer formats."
    )
    parser.add_argument(
        "--output-dir",
        default="results/",
        help="Directory to write results/operability_matrix.md (default: results/)",
    )
    args = parser.parse_args(argv)

    matrix = build_operability_matrix()
    table = _render_markdown_table(matrix)

    print(table)

    output_path = _write_results(Path(args.output_dir), table)
    print(f"Results written to {output_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
