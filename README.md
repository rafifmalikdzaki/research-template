# Research template

A template for **one research study per GitHub repository**. Make one copy for
each question: for example, one repository for image classification and
another for an language-model evaluation. Do not mix unrelated projects together.

## Start here: what you do

Research in this repository follows this sequence:

```text
Question → data and fair split → baseline → experiments → saved evidence → report
```

1. State a question: “Can model X predict Y from data Z?”
2. Define the data, the independent unit, and the train/validation/test split.
3. Run a simple baseline before complex models.
4. Change one meaningful choice per experiment.
5. Save predictions, metrics, settings, and model/checkpoint provenance.
6. Write conclusions only from reviewed saved evidence.

The template provides structure and tooling. It does not choose your model,
dataset, evaluation design, or research conclusion.

## Make a separate repository for each study

### Recommended: use the study generator

The **Cookiecutter generator** asks for the study name, repository slug, Python
version, research profile, visibility, notebooks, and tracking. It creates a clean
project with your chosen names already applied to the package, configuration, and
README. This is preferable when starting a new study.

```bash
uvx --from cookiecutter cookiecutter gh:rafifmalikdzaki/research-template --directory cookiecutter
cd YOUR-REPOSITORY-SLUG
git init -b main
git add .
git commit -m "chore: initialise research study"
gh repo create YOUR-REPOSITORY-SLUG --private --source . --push
```

Cookiecutter prompts for each choice. Select the profile matching the study; the
generated README gives the exact `uv sync --extra ...` command. If the project is
public, select `public` at the GitHub command instead.

### Simple alternative: GitHub's static template button

In GitHub, open [this template](https://github.com/rafifmalikdzaki/research-template),
click **Use this template**, create a private repository, then clone it. Or run:

```bash
gh repo create my-study --template rafifmalikdzaki/research-template --private --clone
cd my-study
uv python install 3.11
```

Examples of useful repository names:

| Research question | Repository name | Dependency profile |
| --- | --- | --- |
| Classify retinal images | `image-classification-study` | vision |
| Evaluate Indonesian LLMs | `language-model-evaluation` | llm |
| Predict outcome from a CSV | `tabular-prediction-study` | tabular |
| Image plus clinical variables | `multimodal-fusion-study` | multimodal + tabular |
| Model a physical process | `scientific-modeling-study` | scientific |

## The five steps after creating a repository

1. Fill in [docs/protocol.md](docs/protocol.md): question, target, data source,
   independent unit, split, metric, baseline, and acceptance criterion.
2. Put local data in `data/raw/`. Do not commit private records or credentials.
3. Select a profile below, install it, and run its smoke check.
4. Add real preparation, training, and evaluation code in `src/`; keep named
   experiment settings in `configs/`.
5. Add every verified result to [reports/README.md](reports/README.md)'s results
   table and update [docs/HANDOVER.md](docs/HANDOVER.md) before pausing work.

Keep all related samples in the same split: images of one patient, records from
one machine run, windows from one time series, or prompts from one document. This
prevents leakage that can make scores look better than they really are.

See [validation status](docs/validation.md) for tested environments and remaining checks.

## Verify your fresh copy

After creating the repository and choosing the profile, verify the basic
environment with this small synthetic example:

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

## Turn the template into a real study

The included commands are smoke checks. They prove that packages and a small model
can run locally; they are not your actual research experiment.

For your study, make the commands look like this:

```bash
uv run python -m your_package.prepare_data --config configs/data.yaml
uv run python -m your_package.train --config configs/baseline.yaml
uv run python -m your_package.evaluate --config configs/baseline.yaml --checkpoint outputs/RUN/model.pt
```

Create one configuration for each meaningful experiment:

```text
configs/
├── baseline.yaml
├── resnet18.yaml
├── catboost.yaml
└── image_clinical_fusion.yaml
```

Every real run should retain its config, split membership, per-example predictions,
metrics, installed package versions, Git revision, and source checkpoint hash.
The provided synthetic demo creates this kind of run bundle in `outputs/`.

### The design rules for each profile

| Profile | What must be defined before training |
| --- | --- |
| Tabular | Which columns are available at prediction time; patient/group/time split; preprocessing fitted on training only. |
| Vision | Patient/slide/eye grouping; image normalization; training-only augmentation; held-out site or time period where possible. |
| LLM | Dataset and model revision; prompt/chat template; generation settings; contamination/overlap check; equal evaluation budget. |
| Multimodal | Safe join key; one shared group split; missing-modality policy; single-modality baselines and fusion ablation. |
| Scientific | Units; boundary conditions; measured vs simulated data; trajectory/condition split; physical and numerical baseline. |

For multimodal work, fusion is supported only if image-only, tabular-only, and
fusion models are compared on the same held-out groups. For simulation work, solver
convergence means a solver completed; it is not by itself predictive accuracy.

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
