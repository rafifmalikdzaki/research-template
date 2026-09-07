# {{ cookiecutter.project_name }}

Research profile: `{{ cookiecutter.research_profile }}`. Repository visibility:
`{{ cookiecutter.repository_visibility }}`.

## First setup

```bash
uv python install {{ cookiecutter.python_version }}
uv sync
uv run research doctor
uv run pytest -q
```

{% if cookiecutter.research_profile == "vision" %}
```bash
uv sync --extra vision
```
{% elif cookiecutter.research_profile == "llm" %}
```bash
uv sync --extra llm
```
{% elif cookiecutter.research_profile == "tabular" %}
```bash
uv sync --extra tabular
```
{% elif cookiecutter.research_profile == "multimodal" %}
```bash
uv sync --extra multimodal --extra tabular
```
{% elif cookiecutter.research_profile == "scientific" %}
```bash
uv sync --extra scientific
```
{% endif %}

## Study contract

- Question and hypothesis:
- Target and intended use:
- Dataset source, version, license, and access conditions:
- Independent unit and grouping key:
- Train/validation/test split policy:
- Primary metric and uncertainty method:
- Baseline and acceptance criterion:

Keep records from the same independent unit in the same split. Fit preprocessing,
feature selection, resampling, and tuning on training data only. Record real runs
in `reports/results.csv`; keep data, outputs, credentials, and checkpoints out of
Git.

## Layout

```text
configs/     Named experiment settings
src/         Reusable preparation, model, train, and evaluation code
tests/       Tests for reusable code, splits, and metrics
data/        Local data, ignored by Git
outputs/     Predictions, logs, checkpoints, ignored by Git
reports/     Reviewed result table and figures
```
