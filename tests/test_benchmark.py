"""Benchmark suite tests covering token efficiency, roundtrip fidelity, and suite wiring."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


def load_token_efficiency_module():
    module_path = Path("scripts/token_efficiency.py")
    spec = importlib.util.spec_from_file_location("token_efficiency", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["token_efficiency"] = module
    spec.loader.exec_module(module)
    return module


token_efficiency = load_token_efficiency_module()


def path_snapshot(path):
    try:
        stat = path.lstat()
    except FileNotFoundError:
        return None

    target = os.readlink(path) if path.is_symlink() else None
    return (stat.st_mode, stat.st_size, stat.st_mtime_ns, target)


def test_benchmark_main_discovers_golden_fixtures_from_script_location(
    monkeypatch,
    tmp_path,
    capsys,
):
    golden = tmp_path / "golden" / "plan"
    golden.mkdir(parents=True)
    (golden / "equivalent.json").write_text(
        '{"kind":"Plan","id":"demo","items":[{"id":"I1","status":"open"}]}',
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SDIF_ENV_OVERRIDE", "0")
    monkeypatch.setenv("SDIF_BENCHMARK_TOON", "0")
    monkeypatch.setenv("SDIF_BENCHMARK_GOLDEN_DIR", str(tmp_path / "golden"))
    monkeypatch.setenv("SDIF_BENCHMARK_OUTPUT_DIR", str(tmp_path / "benchmarks"))
    monkeypatch.setattr(
        token_efficiency,
        "available_tokenizers",
        lambda: [token_efficiency.TokenizerSpec("tiktoken", lambda text: len(text.split()))],
    )

    token_efficiency.main()

    output = capsys.readouterr().out
    assert "Semantic source:" in output
    assert "JSON Compact" in output
    assert "JSON Pretty" in output
    assert "YAML" in output
    assert "XML" in output
    assert "CSV Bundle" in output
    assert "SDIF" in output
    assert "SDIF AI" in output
    assert "TOON skipped" in output


def test_benchmark_sdif_ai_projection_is_not_larger_than_canonical_sdif(monkeypatch):
    monkeypatch.setenv("SDIF_BENCHMARK_TOON", "0")
    data = {
        "kind": "Plan",
        "id": "demo",
        "items": [
            {"id": "I1", "status": "open"},
            {"id": "I2", "status": "done"},
        ],
    }

    formats = dict(token_efficiency.build_formats(data))

    assert len(formats["SDIF AI"].encode("utf-8")) <= len(formats["SDIF"].encode("utf-8"))


def test_benchmark_has_estimated_token_counter_when_optional_tokenizers_unavailable(monkeypatch):
    monkeypatch.setattr(token_efficiency, "tiktoken_module", None)
    monkeypatch.setattr(token_efficiency, "auto_tokenizer_cls", None)
    monkeypatch.setattr(token_efficiency, "anthropic_client_cls", None)

    tokenizers = token_efficiency.available_tokenizers()
    names = [tokenizer.name for tokenizer in tokenizers]

    assert "Estimate" in names
    estimate = next(tokenizer for tokenizer in tokenizers if tokenizer.name == "Estimate")
    assert estimate.counter("abcd") == 1
    assert estimate.counter("abcde") == 2
    assert token_efficiency.select_primary_tokenizer(tokenizers, "abcd").name == "Estimate"


def test_benchmark_ratios_rankings_and_savings_use_json_compact_as_baseline():
    rows = [
        token_efficiency.FormatResult(
            name="JSON Compact",
            text="{}",
            bytes_size=100,
            tokens={"Estimate": 100},
            primary_ratio=100.0,
        ),
        token_efficiency.FormatResult(
            name="Compact Format",
            text="x",
            bytes_size=60,
            tokens={"Estimate": 60},
            primary_ratio=60.0,
        ),
        token_efficiency.FormatResult(
            name="Expanded Format",
            text="x",
            bytes_size=140,
            tokens={"Estimate": 140},
            primary_ratio=140.0,
        ),
    ]
    evidence = token_efficiency.BenchmarkEvidence(
        generated_at="2026-05-21T00:00:00Z",
        run_dir=token_efficiency.BENCHMARK_REPO_ROOT / "test",
        golden_dir=token_efficiency.REPO_ROOT / "examples" / "golden",
        primary_name="Estimate",
        tokenizers=[token_efficiency.TokenizerSpec("Estimate", lambda text: len(text))],
        results_by_document={"demo": rows},
        env_file_loaded=False,
    )

    observations = {
        observation.format_name: observation
        for observation in token_efficiency.iter_ranked_observations(evidence, "Estimate")
    }

    assert observations["Compact Format"].rank == 1
    assert observations["Compact Format"].ratio_value == 60.0
    assert observations["Compact Format"].saved_tokens == 40
    assert observations["JSON Compact"].ratio_value == 100.0
    assert observations["JSON Compact"].saved_tokens == 0
    assert observations["Expanded Format"].ratio_value == 140.0
    assert observations["Expanded Format"].saved_tokens == -40
    assert token_efficiency.wins_by_tokenizer(evidence, "Estimate") == {"Compact Format": 1}



def test_benchmark_golden_dir_can_be_overridden(monkeypatch, tmp_path):
    monkeypatch.delenv("SDIF_BENCHMARK_GOLDEN_DIR", raising=False)
    assert token_efficiency.benchmark_golden_dir() == token_efficiency.REPO_ROOT / "examples" / "golden"

    custom = tmp_path / "golden"
    monkeypatch.setenv("SDIF_BENCHMARK_GOLDEN_DIR", str(custom))

    assert token_efficiency.benchmark_golden_dir() == custom.resolve()


def test_benchmark_script_runs_directly_from_checkout(tmp_path):
    golden = tmp_path / "golden" / "plan"
    golden.mkdir(parents=True)
    (golden / "equivalent.json").write_text(
        '{"kind":"Plan","id":"demo","items":[{"id":"I1","status":"open"}]}',
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["SDIF_ENV_OVERRIDE"] = "0"
    env["SDIF_BENCHMARK_TOON"] = "0"
    env["SDIF_BENCHMARK_TOKENX"] = "0"
    env["SDIF_BENCHMARK_LLAMA"] = "0"
    env["SDIF_BENCHMARK_CLAUDE"] = "0"
    env["SDIF_BENCHMARK_GOLDEN_DIR"] = str(tmp_path / "golden")
    env["SDIF_BENCHMARK_OUTPUT_DIR"] = str(tmp_path / "benchmarks")
    env.pop("PYTHONPATH", None)

    repo_result = token_efficiency.BENCHMARK_REPO_ROOT / "results" / "token_efficiency"
    before = path_snapshot(repo_result)

    run = subprocess.run(
        [sys.executable, "scripts/token_efficiency.py"],
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )

    assert run.returncode == 0
    assert "XML" in run.stdout
    assert "CSV Bundle" in run.stdout
    assert path_snapshot(repo_result) == before
    assert (tmp_path / "benchmarks" / "results" / "token_efficiency").exists()
    assert not (tmp_path / "benchmarks" / "tmp" / "token_efficiency").exists()


def test_benchmark_main_emits_formal_summary_artifacts(monkeypatch, tmp_path):
    golden = tmp_path / "examples" / "golden" / "plan"
    golden.mkdir(parents=True)
    (golden / "equivalent.json").write_text(
        '{"kind":"Plan","id":"demo","items":[{"id":"I1","status":"open"}]}',
        encoding="utf-8",
    )

    monkeypatch.setattr(token_efficiency, "REPO_ROOT", tmp_path)
    monkeypatch.setenv("SDIF_BENCHMARK_OUTPUT_DIR", str(tmp_path))
    monkeypatch.setenv("SDIF_BENCHMARK_TOON", "0")
    monkeypatch.setattr(
        token_efficiency,
        "available_tokenizers",
        lambda: [token_efficiency.TokenizerSpec("Estimate", token_efficiency.count_estimate)],
    )

    token_efficiency.main()

    run_dir = tmp_path / "results" / "token_efficiency"

    assert (run_dir / "summary.md").is_file()
    assert (run_dir / "summary.json").is_file()
    assert (run_dir / "summary.sdif").is_file()
    assert (run_dir / "summary.sdif.ai").is_file()


def test_benchmark_main_emits_self_contained_html_dashboard(monkeypatch, tmp_path):
    golden = tmp_path / "examples" / "golden" / "plan"
    golden.mkdir(parents=True)
    (golden / "equivalent.json").write_text(
        '{"kind":"Plan","id":"demo","items":[{"id":"I1","status":"open"}]}',
        encoding="utf-8",
    )

    monkeypatch.setattr(token_efficiency, "REPO_ROOT", tmp_path)
    monkeypatch.setenv("SDIF_BENCHMARK_OUTPUT_DIR", str(tmp_path))
    monkeypatch.setenv("SDIF_BENCHMARK_TOON", "0")
    monkeypatch.setattr(
        token_efficiency,
        "available_tokenizers",
        lambda: [token_efficiency.TokenizerSpec("Estimate", token_efficiency.count_estimate)],
    )

    token_efficiency.main()

    run_dir = tmp_path / "results" / "token_efficiency"
    dashboard = run_dir / "dashboard.html"
    report = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    html = dashboard.read_text(encoding="utf-8")

    assert dashboard.is_file()
    assert 'id="report-data" type="application/json"' in html
    assert 'id="summary-md" type="application/json"' in html
    assert 'id="comparison-md-preview" type="application/json"' in html
    assert report["generatedAt"] in html
    assert "/home/alessbarb/Descargas" not in html
    assert report["artifacts"]["dashboard"] == str(dashboard)


def test_benchmark_main_publishes_compared_corpus_files(monkeypatch, tmp_path):
    golden = tmp_path / "examples" / "golden" / "plan"
    golden.mkdir(parents=True)
    (golden / "equivalent.json").write_text(
        '{"kind":"Plan","id":"demo","items":[{"id":"I1","status":"open"}]}',
        encoding="utf-8",
    )

    monkeypatch.setattr(token_efficiency, "REPO_ROOT", tmp_path)
    monkeypatch.setenv("SDIF_BENCHMARK_OUTPUT_DIR", str(tmp_path))
    monkeypatch.setenv("SDIF_BENCHMARK_TOON", "0")
    monkeypatch.setenv("SDIF_ENV_OVERRIDE", "0")
    monkeypatch.setattr(
        token_efficiency,
        "available_tokenizers",
        lambda: [token_efficiency.TokenizerSpec("Estimate", token_efficiency.count_estimate)],
    )

    token_efficiency.main()

    run_dir = tmp_path / "results" / "token_efficiency"
    corpus_dir = run_dir / "corpus" / "plan"
    report = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))

    assert (corpus_dir / "json_compact.json").read_text(encoding="utf-8").startswith(
        '{"kind":"Plan"'
    )
    assert (corpus_dir / "json_pretty.json").read_text(encoding="utf-8").startswith("{\n")
    assert (corpus_dir / "yaml.yaml").is_file()
    assert (corpus_dir / "xml.xml").is_file()
    assert (corpus_dir / "csv_bundle.csv").is_file()
    assert (corpus_dir / "sdif.sdif").is_file()
    assert (corpus_dir / "sdif_ai.sdif.ai").is_file()
    assert not (corpus_dir / "toon.toon").exists()
    assert report["artifacts"]["corpus"] == str(corpus_dir.parent)


def load_roundtrip_fidelity_module():
    module_path = Path("scripts/roundtrip_fidelity.py")
    spec = importlib.util.spec_from_file_location("roundtrip_fidelity", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["roundtrip_fidelity"] = module
    spec.loader.exec_module(module)
    return module


def test_roundtrip_parse_sdif_large_document():
    """Regression: large-audit-trail (>1MB) must parse without PolicyError."""
    golden = token_efficiency.REPO_ROOT / "examples" / "golden" / "large-audit-trail" / "source.sdif"
    if not golden.exists():
        pytest.skip("large-audit-trail golden fixture not found")

    rt = load_roundtrip_fidelity_module()
    text = golden.read_text(encoding="utf-8")

    assert len(text.encode("utf-8")) > 1_000_000, "fixture must exceed default 1MB policy limit"

    result = rt.parse_sdif(text)
    assert result is not None, "parse_sdif must succeed for large-audit-trail"


def test_roundtrip_no_na_formats():
    rt = load_roundtrip_fidelity_module()
    assert not hasattr(rt, "NA_FORMATS") or rt.NA_FORMATS == set()


def test_roundtrip_format_parsers_include_sdif_ai_and_toon():
    rt = load_roundtrip_fidelity_module()
    assert "SDIF AI" in rt.FORMAT_PARSERS
    assert "TOON" in rt.FORMAT_PARSERS


def test_roundtrip_parse_sdif_ai_basic():
    rt = load_roundtrip_fidelity_module()
    import formats as fmt_mod
    data = {"kind": "Plan", "id": "demo", "items": [{"id": "I1", "status": "open"}]}
    sdif_text = __import__("sdif.json", fromlist=["json_data_to_sdif"]).json_data_to_sdif(data, include_header=True)
    ai_text = fmt_mod.compact_ai_projection(sdif_text)
    result = rt.parse_sdif_ai(ai_text)
    assert result == data


def test_roundtrip_parse_sdif_ai_with_explicit_header():
    rt = load_roundtrip_fidelity_module()
    # Force the header-present branch by using ai_view directly
    from sdif.ai import ai_view
    from sdif.json import json_data_to_sdif
    data = {"name": "test", "count": 3}
    sdif_text = json_data_to_sdif(data, include_header=True)
    ai_text = ai_view(sdif_text, {}, include_header=True)
    assert ai_text.startswith("@sdif.ai")
    result = rt.parse_sdif_ai(ai_text)
    assert result == data


def test_roundtrip_parse_sdif_ai_scalar_ambiguity():
    rt = load_roundtrip_fidelity_module()
    import formats as fmt_mod
    from sdif.json import json_data_to_sdif
    data = {
        "a": None,
        "b": "null",
        "c": 42,
        "d": "42",
        "e": True,
        "f": "true",
        "g": "",
        "h": "  spaces  ",
    }
    sdif_text = json_data_to_sdif(data, include_header=True)
    ai_text = fmt_mod.compact_ai_projection(sdif_text)
    result = rt.parse_sdif_ai(ai_text)
    assert result == data, f"scalar round-trip mismatch: {result!r} != {data!r}"


def test_roundtrip_parse_toon_basic(monkeypatch):
    rt = load_roundtrip_fidelity_module()
    import formats as fmt_mod
    data = {"kind": "Plan", "id": "demo", "items": [{"id": "I1", "status": "open"}]}
    toon_text = fmt_mod.toon_from_cli(data)
    if toon_text is None:
        pytest.skip("TOON encoder not available")
    result = rt.parse_toon(toon_text)
    assert result == data


def test_roundtrip_parse_toon_scalar_ambiguity(monkeypatch):
    rt = load_roundtrip_fidelity_module()
    import formats as fmt_mod
    data = {"a": None, "b": True, "c": 42, "d": "42", "e": "null", "f": "true"}
    toon_text = fmt_mod.toon_from_cli(data)
    if toon_text is None:
        pytest.skip("TOON encoder not available")
    result = rt.parse_toon(toon_text)
    assert result == data, f"scalar round-trip mismatch: {result!r} != {data!r}"


def test_roundtrip_parse_toon_unavailable(monkeypatch):
    rt = load_roundtrip_fidelity_module()
    monkeypatch.setattr(rt.shutil, "which", lambda _name: None)
    result = rt.parse_toon("name: test\n")
    assert result is None


def test_roundtrip_collect_diagnostics_all_four_categories():
    rt = load_roundtrip_fidelity_module()
    original = {"a": 1, "b": "hello", "c": True, "d": "gone"}
    roundtripped = {"a": 2, "b": 42, "extra": "new"}

    diag = rt.collect_diagnostics(original, roundtripped)

    assert "d" in diag["missing_paths"]
    assert "extra" in diag["extra_paths"]
    assert any(m["path"] == "a" for m in diag["value_mismatches"])
    assert any(m["path"] == "b" for m in diag["type_mismatches"])


def test_roundtrip_collect_diagnostics_toon_int_float_coercion_cause():
    rt = load_roundtrip_fidelity_module()
    original = {"x": 5.0, "y": 3.0}
    roundtripped = {"x": 5, "y": 3}

    diag = rt.collect_diagnostics(original, roundtripped, format_name="TOON")

    assert diag.get("cause") == "external_decoder_int_float_coercion"
    assert diag["type_mismatches"][0]["expected_type"] == "float"
    assert diag["type_mismatches"][0]["actual_type"] == "int"


def test_roundtrip_diagnostic_files_produced_below_100(monkeypatch, tmp_path):
    golden = tmp_path / "examples" / "golden" / "plan"
    golden.mkdir(parents=True)
    (golden / "equivalent.json").write_text(
        '{"kind":"Plan","id":"demo","items":[{"id":"I1","status":"open"}]}',
        encoding="utf-8",
    )

    rt = load_roundtrip_fidelity_module()
    monkeypatch.setattr(rt, "REPO_ROOT", tmp_path)
    monkeypatch.setenv("SDIF_BENCHMARK_OUTPUT_DIR", str(tmp_path))
    monkeypatch.setenv("SDIF_BENCHMARK_TOON", "0")
    monkeypatch.setenv("SDIF_ENV_OVERRIDE", "0")

    # Inject a broken parser for JSON Compact that loses a field
    original_parsers = dict(rt.FORMAT_PARSERS)
    rt.FORMAT_PARSERS["JSON Compact"] = lambda text: {"kind": "Plan"}  # missing id, items
    try:
        rt.main()
    finally:
        rt.FORMAT_PARSERS.update(original_parsers)

    run_dir = tmp_path / "results" / "roundtrip_fidelity"
    diag_path = run_dir / "diagnostics" / "plan" / "json_compact.json"
    assert diag_path.is_file(), "diagnostic file not written for below-100% format"

    diag = json.loads(diag_path.read_text(encoding="utf-8"))
    assert "missing_paths" in diag
    assert "extra_paths" in diag
    assert "value_mismatches" in diag
    assert "type_mismatches" in diag


def test_roundtrip_sdif_ai_plan_at_100_after_expand_fix():
    rt = load_roundtrip_fidelity_module()
    import formats as fmt_mod
    from sdif.json import json_data_to_sdif

    data = {
        "kind": "Plan",
        "id": "demo",
        "scope": {"in": ["a", "b"], "out": ["c"]},
        "items": [{"id": "I1", "status": "open"}, {"id": "I2", "status": "done"}],
    }
    sdif_text = json_data_to_sdif(data, include_header=True)
    ai_text = fmt_mod.compact_ai_projection(sdif_text)
    result = rt.parse_sdif_ai(ai_text)

    assert result == data, f"SDIF AI round-trip mismatch: {result!r}"


def test_roundtrip_sdif_ai_numeric_string_table_cells_preserved():
    # Regression: HTTP-status-code strings like "200", "404" in a $-suffixed
    # column must survive the SDIF AI → expand_ai_doc → document_to_json_data
    # path as strings, not be coerced to integers.
    rt = load_roundtrip_fidelity_module()
    import formats as fmt_mod
    from sdif.json import json_data_to_sdif

    ambiguous = ["200", "404", "0", "-1", "1.0", "true", "false", "null"]
    data = {"responses": [{"code": s, "status": s} for s in ambiguous]}
    sdif_text = json_data_to_sdif(data, include_header=True)
    ai_text = fmt_mod.compact_ai_projection(sdif_text)
    result = rt.parse_sdif_ai(ai_text)

    assert isinstance(result, dict), "parse_sdif_ai must return a dict"
    for original, row in zip(ambiguous, result.get("responses", [])):
        for col in ("code", "status"):
            cell = row[col]
            assert cell == original, (
                f"SDIF AI expand lost {original!r} in column {col!r}: got {cell!r}"
            )
            assert isinstance(cell, str), (
                f"SDIF AI expand coerced {original!r} to {type(cell).__name__}"
            )


def load_run_suite_module() -> object:
    """Load the run_suite module from scripts/run_suite.py."""
    module_path = Path("scripts/run_suite.py")
    spec = importlib.util.spec_from_file_location("run_suite", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["run_suite"] = module
    spec.loader.exec_module(module)
    return module


mod = load_run_suite_module()


def test_run_suite_includes_semantic_and_operability_tracks() -> None:
    track_ids = {t["id"] for t in mod.TRACKS}
    assert "semantic_fidelity" in track_ids
    assert "operability" in track_ids


def test_retrieval_accuracy_is_optional() -> None:
    retrieval = next(t for t in mod.TRACKS if t["id"] == "retrieval_accuracy")
    assert retrieval["optional"] is True


def test_build_index_supports_semantic_and_operability_tracks(monkeypatch, tmp_path):
    semantic_dir = tmp_path / "semantic_fidelity"
    semantic_dir.mkdir()
    (semantic_dir / "summary.json").write_text(
        json.dumps(
            {
                "documents": [
                    {
                        "formats": [
                            {
                                "format": "SDIF",
                                "relationStructuralFidelity": 1.0,
                                "ruleStructuralFidelity": 1.0,
                                "tableStructuralFidelity": 1.0,
                                "fieldStructuralFidelity": 1.0,
                            }
                        ]
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    operability_dir = tmp_path / "operability"
    operability_dir.mkdir()
    (operability_dir / "summary.json").write_text(
        json.dumps(
            {
                "formats": [
                    {
                        "format": "SDIF",
                        "nativeRelationSupport": True,
                        "ruleDeclarationSupport": True,
                        "ruleEvaluationSupport": False,
                        "stableHash": True,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(mod, "benchmark_result_dir", lambda track_id: tmp_path / track_id)
    tracks = {track["id"]: track for track in mod.TRACKS}

    index = mod._build_index(
        [
            {"track": tracks["semantic_fidelity"], "ran": True, "success": True},
            {"track": tracks["operability"], "ran": True, "success": True},
        ],
        "2026-05-24T00:00:00Z",
        corpus_documents=4,
    )

    assert index["tracks"] == ["semantic_fidelity", "operability"]
    assert {entry["track"] for entry in index["scorecard"]} == {
        "semantic_fidelity",
        "operability",
    }
