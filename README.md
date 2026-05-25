<p align="center">
  <img src="https://raw.githubusercontent.com/sdif-format/.github/main/profile/assets/sdif-logo-t.png" alt="SDIF Benchmarks" width="320">
</p>

<p align="center">
  <strong>SDIF Benchmarks</strong>
</p>

<p align="center">
  Evidence-first benchmarks measuring SDIF against JSON, YAML, XML, CSV Bundle<br>
  and other formats from the perspective of AI and LLM developers.
</p>

<p align="center">
  <a href="#benchmark-tracks">Tracks</a>
  ·
  <a href="#quick-start">Quick start</a>
  ·
  <a href="#latest-results">Latest results</a>
  ·
  <a href="#corpus-model">Corpus model</a>
  ·
  <a href="#result-model">Result model</a>
  ·
  <a href="#environment">Environment</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/approach-evidence%20first-2563eb?style=flat-square" alt="Evidence first">
  <img src="https://img.shields.io/badge/corpus-shared%20canonical%20fixtures-0f766e?style=flat-square" alt="Shared canonical fixtures">
  <img src="https://img.shields.io/badge/validation-deterministic-374151?style=flat-square" alt="Deterministic">
</p>

<br>

Every compared representation is derived from the same canonical JSON source. Claims must name the tokenizer and document coverage that produced them. Optional external tools degrade gracefully.

<br>

---

## Benchmark tracks

<div align="center">

<table>
  <tr>
    <td width="33%" valign="top">
      <strong>Token efficiency</strong>
      <br><br>
      Byte and token reduction across shared semantic fixtures. Ranks all formats against JSON Compact as the stable baseline.
    </td>
    <td width="33%" valign="top">
      <strong>Context packing</strong>
      <br><br>
      How many document copies fit inside fixed token budgets (4K, 8K, 32K, 128K). Fit rate and median copies per budget.
    </td>
    <td width="33%" valign="top">
      <strong>Round-trip fidelity</strong>
      <br><br>
      JSON→format→JSON preservation. Scores value, type and structure fidelity. N/A for SDIF AI and TOON.
    </td>
  </tr>
  <tr>
    <td width="33%" valign="top">
      <strong>Delta compactness</strong>
      <br><br>
      Token overhead of re-sending a mutated document. Applies a deterministic mutation to the first 10% of leaf values.
    </td>
    <td width="33%" valign="top">
      <strong>Retrieval accuracy</strong>
      <br><br>
      LLM answer quality by format. Deterministic validators — no LLM judge. Opt-in: requires <code>ANTHROPIC_API_KEY</code>.
    </td>
    <td width="33%" valign="top">
      <strong>Semantic quality</strong>
      <br><br>
      Guards that SDIF preserves relations, rules, schema validation, canonicalization and reversible AI projection boundaries.
    </td>
  </tr>
  <tr>
    <td width="33%" valign="top">
      <strong>Semantic fidelity</strong>
      <br><br>
      Structural recovery after format conversion. Separate axes for relations, rules, tables, and scalar fields. Unparsed formats report <code>not_measured</code>, not zero.
    </td>
    <td width="33%" valign="top">
      <strong>Operability</strong>
      <br><br>
      Static capability matrix across 8 formats: canonical forms, stable hashing, native relation support, rule declaration vs. evaluation, semantic type vocabulary.
    </td>
    <td width="33%" valign="top">
    </td>
  </tr>
</table>

</div>

<br>

---

## Quick start

This repository expects access to the core SDIF repository. By default it looks for it at `../sdif`; override this with `SDIF_CORE_REPO`.

```bash
# Token reduction across formats
make benchmark-token

# Context-window fit rate by budget
make benchmark-packing

# JSON→format→JSON round-trip fidelity
make benchmark-roundtrip

# Mutation sensitivity (re-send overhead)
make benchmark-delta

# LLM retrieval accuracy by format — opt-in
SDIF_BENCHMARK_RETRIEVAL=1 ANTHROPIC_API_KEY=<key> make benchmark-retrieval

# Semantic quality checks
make benchmark-quality

# Structural recovery fidelity (semantic fidelity track)
make benchmark-semantic

# Format capability matrix (operability track)
make benchmark-operability
```

Alternatively, you can run them directly as Python modules or using the CLI command:

```bash
# Run the full suite using the CLI entry point
uv run sdif-benchmarks

# Run individual tracks as python modules
uv run python -m sdif_benchmarks.tracks.token_efficiency
uv run python -m sdif_benchmarks.tracks.context_packing
uv run python -m sdif_benchmarks.tracks.roundtrip_fidelity
uv run python -m sdif_benchmarks.tracks.delta_compactness
uv run python -m sdif_benchmarks.tracks.semantic_fidelity
uv run python -m sdif_benchmarks.tracks.operability
uv run python -m sdif_benchmarks.checks.check_semantic_quality
```

<br>

---

## Latest results

Results from the most recent token efficiency run across 21 documents and 3 tokenizers (Estimate, TokenX, tiktoken).

<div align="center">

| Format | Consensus avg rank | Median ratio vs JSON Compact | Wins (63 pairs) |
| --- | ---: | ---: | ---: |
| **SDIF AI** | **1.10** | **56.8%** | **57** |
| SDIF | 2.60 | 59.5% | 2 |
| CSV Bundle | 2.70 | 61.2% | 4 |
| TOON | 3.60 | 63.2% | 0 |
| YAML | 5.35 | 95.3% | 0 |
| JSON Compact | 5.65 | 100.0% | 0 |
| JSON Pretty | 7.00 | 137.3% | 0 |
| XML | 8.00 | 171.7% | 0 |

</div>

<br>

Tokenizer-specific winners:

<div align="center">

| Tokenizer | Winning format | Wins |
| --- | --- | ---: |
| Estimate | SDIF AI | 19/21 |
| TokenX | SDIF AI | 20/21 |
| tiktoken | SDIF AI | 18/21 |

</div>

<br>

These results are corpus-dependent. Results for Claude and Llama3 tokenizers require separate opt-in. Full per-document breakdowns live in [`results/token_efficiency/`](results/token_efficiency/).

<br>

---

## Corpus model

The canonical semantic corpus lives in the core repo's `examples/golden/` directory, not duplicated here. This avoids drift between parser fixtures and benchmark fixtures.

Each fixture contains:

```text
../sdif/examples/golden/<fixture>/
├── equivalent.json     # canonical semantic source (benchmark input)
├── source.sdif         # hand-authored or generated SDIF source
├── canonical.sdif      # canonical SDIF form
└── canonical.sha256    # canonical hash evidence
```

The benchmark path defaults to `../sdif/examples/golden/` and can be overridden with `SDIF_BENCHMARK_GOLDEN_DIR`.

<br>

---

## Result model

Each benchmark run writes scratch output to `tmp/<track>/` while running and promotes it to `results/<track>/` on success. Failed runs leave `tmp/<track>/` for diagnosis without touching the last clean result.

```text
results/<track>/
├── comparison.log       # console output
├── comparison.md        # per-document detail
├── summary.md           # key findings
├── summary.json         # machine-readable summary
├── summary.sdif         # SDIF encoding
├── summary.sdif.ai      # compact AI projection
├── dashboard.html       # self-contained HTML dashboard
└── corpus/              # exact format files measured
    └── <document>/
        ├── json_compact.json
        ├── json_pretty.json
        ├── yaml.yaml
        ├── xml.xml
        ├── csv_bundle.csv
        ├── sdif.sdif
        ├── sdif_ai.sdif.ai
        └── toon.toon    # when TOON is enabled
```

<br>

---

## Environment

Common switches (all tracks):

```bash
SDIF_BENCHMARK_OUTPUT_DIR=/tmp/sdif-benchmarks   # redirect all output
SDIF_CORE_REPO=../sdif                            # path to core repo
SDIF_BENCHMARK_GOLDEN_DIR=/tmp/golden-fixtures    # use a custom corpus
SDIF_BENCHMARK_TOON=0                             # disable TOON comparison
SDIF_BENCHMARK_VERBOSE=1                          # print optional-tool diagnostics
SDIF_ENV_OVERRIDE=0                               # keep existing env vars; skip .env
```

Token efficiency additional switches:

```bash
SDIF_TIKTOKEN_ENCODING=cl100k_base    # tiktoken encoding (default)
SDIF_BENCHMARK_TOKENX=0               # disable TokenX estimation
SDIF_BENCHMARK_LLAMA=0                # disable Llama tokenizer
SDIF_BENCHMARK_CLAUDE=1               # enable Claude counting; needs ANTHROPIC_API_KEY
```

Retrieval accuracy:

```bash
SDIF_BENCHMARK_RETRIEVAL=1    # opt-in
ANTHROPIC_API_KEY=<key>       # required
```

All scripts load `.env` from the repository root when present, unless `SDIF_ENV_OVERRIDE=0`.

<br>

---

## Project structure

```text
sdif-benchmarks/
├── src/           # packaged source code, helpers, tracks, generators, checks
├── results/       # completed benchmark output (committed evidence)
└── tmp/           # in-progress output (gitignored)
```

<br>

---

## Organization contract

- Packaged modules (tracks, generators, checks) belong under `src/sdif_benchmarks/`.
- Reusable helpers belong under `src/sdif_benchmarks/` — e.g. `formats.py`, `infra.py`, `report.py`.
- Each track writes scratch output to `tmp/<track>/`; completed evidence goes to `results/<track>/`.
- Canonical semantic sources belong in the `sdif` core repo's `examples/golden/`, unless `SDIF_BENCHMARK_GOLDEN_DIR` overrides.
- Optional external tools (TOON, tiktoken) must degrade gracefully.
- Claims must name the tokenizer and model coverage that produced them.
- Retrieval accuracy must use deterministic validators, not subjective LLM judging.

<br>

---

## Ecosystem

This GitHub organization hosts the official SDIF ecosystem: the core format, reference tooling, benchmarks, examples, libraries, and editor extensions.

<div align="center">

<table>
  <tr>
    <td width="33%" valign="top">
      <p><sub>PYTHON CLIENT & CLI</sub></p>
      <h3>sdif-py</h3>
      <p>
        Specification, parser, canonicalizer, and CLI.<br>
        The normative reference implementation.
      </p>
      <p><a href="https://github.com/sdif-format/sdif-py"><strong>Explore sdif-py →</strong></a></p>
    </td>
    <td width="33%" valign="top">
      <p><sub>SPECIFICATION (SSOT)</sub></p>
      <h3>sdif-spec</h3>
      <p>
        Official format specification, canonicalization rules,<br>
        and portable conformance test suite.
      </p>
      <p><a href="https://github.com/sdif-format/sdif-spec"><strong>View specification →</strong></a></p>
    </td>
    <td width="33%" valign="top">
      <p><sub>BENCHMARKS</sub></p>
      <h3>sdif-benchmarks</h3>
      <p>
        Reproducible benchmark datasets and reports comparing SDIF with JSON, YAML, XML, and CSV.
      </p>
      <p><a href="https://github.com/sdif-format/sdif-benchmarks"><strong>View benchmarks →</strong></a></p>
    </td>
  </tr>
  <tr>
    <td width="33%" valign="top">
      <p><sub>RUST IMPLEMENTATION</sub></p>
      <h3>sdif-rs</h3>
      <p>
        Pure Rust parser implementation with a span-annotated AST designed for editor tooling.
      </p>
      <p><a href="https://github.com/sdif-format/sdif-rs"><strong>Explore sdif-rs →</strong></a></p>
    </td>
    <td width="33%" valign="top">
      <p><sub>LANGUAGE SERVER (LSP)</sub></p>
      <h3>sdif-lsp</h3>
      <p>
        LSP language server binary (tower-lsp) providing real-time diagnostics and IDE features.
      </p>
      <p><a href="https://github.com/sdif-format/sdif-lsp"><strong>View sdif-lsp →</strong></a></p>
    </td>
    <td width="33%" valign="top">
      <p><sub>EDITOR INTEGRATION</sub></p>
      <h3>vscode-sdif</h3>
      <p>
        VS Code extension client providing syntax highlighting, diagnostics, and LSP configuration.
      </p>
      <p><a href="https://github.com/sdif-format/vscode-sdif"><strong>Open extension →</strong></a></p>
    </td>
  </tr>
  <tr>
    <td width="33%" valign="top">
      <p><sub>GRAMMAR FOUNDATION</sub></p>
      <h3>tree-sitter-sdif</h3>
      <p>
        Tree-sitter grammar foundation for syntax highlighting and incremental parsing.
      </p>
      <p><a href="https://github.com/sdif-format/tree-sitter-sdif"><strong>Open grammar →</strong></a></p>
    </td>
    <td width="33%" valign="top">
      <p><sub>DOCUMENTATION</sub></p>
      <h3>sdif-format.github.io</h3>
      <p>
        Official documentation website containing specification guides, tutorials, and examples.
      </p>
      <p><a href="https://github.com/sdif-format/sdif-format.github.io"><strong>Read docs →</strong></a></p>
    </td>
    <td width="33%" valign="top">
      <p><sub>ORGANIZATION META</sub></p>
      <h3>.github</h3>
      <p>
        Organization profile, assets, and shared community configuration files.
      </p>
      <p><a href="https://github.com/sdif-format/.github"><strong>View profile →</strong></a></p>
    </td>
  </tr>
</table>

</div>

<br>

<details>
  <summary><strong>Repository map</strong></summary>

<br>

| Repository | Purpose |
| --------------------------------------------------------------------- | ---------------------------------------------------------------- |
| [`sdif-py`](https://github.com/sdif-format/sdif-py)                   | Core Python parser, validator, canonicalizer, and CLI |
| [`sdif-spec`](https://github.com/sdif-format/sdif-spec)               | Official format specification and conformance test suite (SSOT) |
| [`sdif-benchmarks`](https://github.com/sdif-format/sdif-benchmarks)   | Benchmark datasets, reports, and comparison tooling |
| [`sdif-rs`](https://github.com/sdif-format/sdif-rs)                   | Rust parser crate with span-annotated AST |
| [`sdif-lsp`](https://github.com/sdif-format/sdif-lsp)                 | LSP language server binary |
| [`tree-sitter-sdif`](https://github.com/sdif-format/tree-sitter-sdif) | Tree-sitter grammar foundation for syntax highlighting |
| [`vscode-sdif`](https://github.com/sdif-format/vscode-sdif)           | VS Code extension client for SDIF |
| [`sdif-format.github.io`](https://github.com/sdif-format/sdif-format.github.io) | Public documentation website (Docusaurus) |
| [`.github`](https://github.com/sdif-format/.github)                   | Organization profile, assets, and shared GitHub community files |

</details>

<br>

## License

MIT. See [LICENSE](LICENSE).
