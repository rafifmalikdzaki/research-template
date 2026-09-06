# Research template

A uv-managed starting point for vision, LLM, tabular, multimodal, and scientific
research. Small shared utilities, selectable dependencies, runnable CPU examples,
and an explicit experiment record. No private data, model weights, or credentials.

## Start a project

Use GitHub's **Use this template** button, or:

```bash
gh repo create my-study --template rafifmalikdzaki/research-template --private --clone
cd my-study
uv python install 3.11
uv sync --locked
uv run research demo
uv run pytest -q
```

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first.
The demo trains a logistic regression on synthetic repeated-subject data with a
group-held-out split. It is a plumbing check, not research evidence. Nothing is
downloaded beyond Python packages. Run commands from the repository root.

## Choose your dependencies

| Research | Install | Starting point |
| --- | --- | --- |
| Tabular | `uv sync --locked --extra tabular` | `uv run --no-sync research demo` |
| Vision | `uv sync --locked --extra vision` | `uv run --no-sync python examples/modality_smoke.py vision` |
| LLM | `uv sync --locked --extra llm` | `uv run --no-sync python examples/modality_smoke.py llm` |
| Multimodal | `uv sync --locked --extra multimodal` | `uv run --no-sync python examples/modality_smoke.py multimodal` |
| Scientific / simulation | `uv sync --locked --extra scientific` | `uv run --no-sync python examples/modality_smoke.py scientific` |
| Other research | `uv sync --locked` | Add domain packages with `uv add` |

Combine extras in one command, e.g. `uv sync --locked --extra vision --extra
tabular --extra notebooks --extra tracking`. uv sync is exact: select all wanted
extras each time. Use `uv run --no-sync` after syncing optional dependencies, or
repeat the extras on `uv run`. Tracking services are opt-in; no automatic uploads.
The tabular demo uses sklearn; boosted-tree libraries are available to extend it.

The vision example uses a random ResNet18; the LLM example uses a tiny random GPT-2;
multimodal demonstrates image + nine numeric features; scientific checks an ODE
against an analytic solution. These are executable smoke examples, not finished
training pipelines. Replace them with your study's actual model and data contract.

## Python and hardware

Python **3.11** is the compatibility-first default, with **3.12** also supported
(`>=3.11,<3.13`). This follows the existing projects' common baseline and avoids
promising support for newer interpreters before testing compiled extensions.
The lock resolves every optional dependency together; it does not prove GPU or
every-platform runtime compatibility. The supplied CI configuration checks the
core on 3.11/3.12 and modality smokes on 3.11 Linux once enabled. See
[environment guidance](docs/environment.md) for CUDA,
vLLM, FlashAttention, PyG, and changing Python versions.

## Layout

```text
configs/                 Versioned experiment configurations
src/research_template/   Importable code and experiment CLI
examples/               Small executable modality examples
tests/                  Leakage, reproducibility, and artifact checks
data/                   Ignored datasets; commit only its README
outputs/                Ignored run bundles and checkpoints
notebooks/              Exploration; move reusable logic to src/
reports/                Reviewed results and figures
docs/                   Protocol, environment, and handover templates
docs/github-actions.yml Ready-to-enable GitHub Actions CI
```

Every demo produces resolved config, metrics, per-observation predictions,
split membership, installed package versions, and a manifest with file hashes,
dataset hash, Git revision/dirty state, seed, command arguments, and lock hash.
The demo does not persist a trained model. Add model serialization and a source
checkpoint hash before building checkpoint-dependent evaluation or TTA.

## Make it your own

1. Rename `project.name` and the README. You may retain the internal
   `research_template` package; if renaming it, update the package directory,
   imports, script entry point, and wheel configuration together.
2. Run `uv lock` after metadata or dependency edits and commit `uv.lock`.
3. Fill in [the study protocol](docs/protocol.md) before selecting models.
4. Add dataset loaders and train/evaluate commands under `src/`; keep machine
   paths and secrets outside versioned configs.
5. Publish reviewed results using [the result schema](reports/README.md), and keep
   [the handover](docs/HANDOVER.md) current.
6. Choose a license before sharing publicly. No license is imposed by this template.

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
uv build
```

### Enable GitHub Actions

CI is supplied as [docs/github-actions.yml](docs/github-actions.yml), inactive.
The publishing token did not have GitHub's `workflow` permission. To activate it,
copy this file to `.github/workflows/ci.yml` and commit/push using credentials
with workflow permission (or add it through GitHub's web editor). It checks both
Python versions, packaging, reproducibility, and the modality smoke examples.

## Design origins

The structure draws on the local retinal multimodal, histopathology, language,
spray-dryer tabular, and particle-surrogate projects: `src/configs/tests/docs`,
separate data and outputs, optional heavy dependencies, grouped evaluation,
artifact provenance, and checkpoint lifecycle documentation. It contains new
generic scaffolding, not copied study code or experimental results.
