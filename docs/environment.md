# Environment contract

Default: CPython 3.11. Supported project interval: 3.11 and 3.12.
The version file selects a minor; the run bundle records the exact interpreter.
For strict replay, pin the exact patch with `uv python pin 3.11.X` after selecting
an available release. Commit that change alongside the lock.

Primary compatibility references checked during template creation:

- [PyTorch installation selector](https://pytorch.org/get-started/locally/)
- [Transformers installation](https://huggingface.co/docs/transformers/installation)
- [uv optional dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [uv PyTorch integration](https://docs.astral.sh/uv/guides/integration/pytorch/)

Python 3.11 is a conservative choice, not a claim that every research package
supports every operating system. For 3.12, run `uv sync --locked --python 3.12`
and the tests. Dependency upgrades are deliberate: `uv lock --upgrade`, inspect
the diff, and rerun the relevant examples and study-specific tests.

## GPUs and specialized stacks

The default uses PyPI. On Linux, PyTorch may pull large CUDA libraries even for a
CPU smoke. Check disk space before installing deep-learning extras. CUDA wheels
do not prove your host driver is compatible. Select a matched torch/torchvision
pair and index using the official PyTorch selector and uv integration guide;
record the index in `tool.uv.sources`, regenerate the lock, and verify a real
forward/backward pass on the target GPU. Avoid ad-hoc `uv pip install` changes
that are absent from the lock.

Keep vLLM serving, FlashAttention, bitsandbytes, TensorFlow/JAX, PhysicsNeMo,
torch-scatter, and other compiled accelerator extensions in a separate uv project
and lock when their Torch/CUDA constraints conflict with the study environment.
PyG extension wheels must match the selected Torch and CUDA versions. A dedicated
`environments/<backend>/pyproject.toml` can live in a downstream repository; invoke
it with `uv run --project environments/<backend> ...`. Do not add incompatible
backends to one shared lock just to expose an extra.

Record GPU model, driver, CUDA runtime, exact dependencies, model revision, and
checkpoint SHA-256 in real training manifests. Seeds alone cannot guarantee
bitwise reproducibility across devices or library releases.

Optional tracking credentials can be exported by your shell; `.env.example` is
documentation, not an automatically loaded configuration. Do not publish private
samples or identifiers through MLflow/W&B artifacts.
