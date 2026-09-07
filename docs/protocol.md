# Study protocol — fill before experiments

- Question and falsifiable hypothesis:
- Task, target, intended use, and limits:
- Dataset source/version/hash, license/consent, inclusion/exclusion criteria:
- Evidence type: measured / inferred / proxy / synthetic / diagnostic:
- Unit of independence: entity / subject / site / batch / trajectory / document:
- Split policy and immutable split-manifest location:
- Train/validation/test sizes, groups, time/site boundaries:
- Primary metric, aggregation unit, uncertainty method, and acceptance criterion:
- Baselines, ablations, matched tuning budgets, seeds, and stopping rule:
- Compute/storage budget and checkpoint retention policy:

Fit preprocessing, feature selection, imputation, resampling, and tuning on
training folds only. Use validation for selection and reserve test data for final
evaluation. Keep repeated entities/images, near-duplicate documents, overlapping
windows, and related trajectories within one split. For temporal claims, use a
temporal split. Bootstrap at the independent unit, not correlated observations.

## Domain checklist

| Domain | Define explicitly |
| --- | --- |
| Vision | Sample/source grouping, image normalization, augmentation, held-out-source validation |
| LLM | Dataset and model revisions, prompt/chat template, tokenizer, contamination checks, generation settings, token budget |
| Tabular | Target-derived columns, training-only preprocessing, group/time split, class imbalance, feature availability at inference |
| Multimodal | Join key, aligned subject splits, missing modalities, modality ablations, leakage through metadata |
| Scientific | Units, boundary conditions, conservation, solver tolerances, measured versus simulated data, raw versus corrected rollout |
| Other | Independent unit, data contract, fair comparators, appropriate uncertainty |

## Evidence acceptance

A successful process is not scientific success. Retain per-sample predictions,
config, splits, environment, data/model revisions, metrics, and source checkpoint
hashes. Separate smoke, diagnostic, incomplete, failed, and accepted runs.
For TTA, compare against the same source checkpoint; finish dependent evaluations
and verify an archive before deleting that checkpoint.
