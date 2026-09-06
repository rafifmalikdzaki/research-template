# Research contributor contract

- Use uv and commit dependency changes with the updated lock.
- Preserve unrelated work. Keep datasets, credentials, checkpoints, and generated
  runs out of Git.
- Keep reusable code under src; configs and documented commands must agree.
- Fit transforms inside training folds and split at the independent unit.
- Label synthetic, proxy, diagnostic, incomplete, and measured evidence explicitly.
- Preserve predictions, split/config/environment provenance, and source checkpoint
  hashes for downstream evaluations.
- Run Ruff and focused tests before claiming implementation completion. Report
  unavailable GPU or domain validation honestly.
- Update the protocol/results/handover when changing a study contract.
