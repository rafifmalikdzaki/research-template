# Template validation

Checked on 2026-09-06, Linux x86_64. This verifies scaffolding, not study outcomes.

| Check | Result |
| --- | --- |
| `uv lock` | Passed; 248 packages resolved across optional profiles |
| Python 3.11.13 core tests | 5 passed |
| Python 3.12.11 core tests, isolated environment | 5 passed |
| Synthetic grouped demo, both Python versions | Passed; run bundles produced |
| Scientific ODE smoke, Python 3.11 | Passed against analytic solution |
| Ruff lint and formatting | Passed |
| `uv build` | Source distribution and wheel built |
| Python 3.12 `uv sync --locked --all-extras --dry-run` | Install plan passed; not a runtime test |
| Deep-learning profile installation | Incomplete: network timeout downloading `nvidia-cublas==13.1.1.3` |
| Vision / LLM / multimodal runtime smokes | Not run; installation did not finish |
| Boosting, notebook, tracking extras | Dependency resolution only; not runtime tested |
| GPU / macOS / Windows | Not tested |
| GitHub Actions | Inactive configuration in `docs/github-actions.yml`; publishing token lacks workflow permission |

The tests check independent-group splits, reproducible predictions, recomputed
metrics, artifact hashes, and rejection of invalid configs before creating runs.

To finish optional runtime validation on a reliable connection:

```bash
UV_HTTP_TIMEOUT=180 uv sync --locked --extra multimodal --extra scientific
uv run --no-sync python examples/modality_smoke.py vision
uv run --no-sync python examples/modality_smoke.py llm
uv run --no-sync python examples/modality_smoke.py multimodal
uv run --no-sync python examples/modality_smoke.py scientific
```

CPU examples do not validate a CUDA driver or training performance. For GPU
research, follow `docs/environment.md` and verify the actual target hardware.
