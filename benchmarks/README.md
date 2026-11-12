# TFWhy synthetic benchmark

This is a small, versioned release-regression benchmark. It exercises deterministic replacement and drift semantics plus the AI payload privacy contract with synthetic repository inputs only. It does not use Terraform state, credentials, cloud APIs, or a local model.

Run it from a source checkout:

```bash
python3 benchmarks/run.py
```

The benchmark is deliberately not a claim of broad Terraform compatibility, security coverage, or AI-answer quality. It guards these specific contracts:

- a dynamic `user_data` pattern is reported as a **Likely** possibility, not proof;
- drift is reported only when Terraform supplied `resource_drift` metadata;
- ordinary planned changes are not relabelled as remote drift;
- the replacement AI prompt carries allowlisted structural facts and excludes the resource address and deterministic explanation text.

AI answer quality remains a separate, human-reviewed pilot signal. Before an optional local-model smoke test, use a synthetic fixture, inspect the deterministic result first, and confirm the response preserves uncertainty. Never paste a private plan, state file, credentials, raw configuration, or model conversation into the benchmark or an issue.
