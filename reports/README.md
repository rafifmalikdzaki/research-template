# Reviewed research results

Keep a canonical results table here. Link to retained artifacts instead of
embedding unsupported headline metrics. Commit only reviewed, shareable figures.

Suggested columns:

```text
run_id,status,evidence_type,task,dataset_version,split_manifest,model,seed,
metric_name,metric_value,metric_unit,uncertainty,config,source_checkpoint_sha256,
predictions_path,manifest_path,git_commit,command,caveat
```

Use one row per metric per run. Include all verified runs relevant to the study,
not just the winner. Separate synthetic smoke and diagnostic evidence from real
held-out performance. Record failures and exclusions with reasons. Keep figure
generation code alongside the report or in `src/`, and link its source table.
