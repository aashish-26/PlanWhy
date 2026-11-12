# TFWhy synthetic examples

These files are deliberately small, synthetic inputs for a safe first run. They contain no provider credentials, real resource identifiers, Terraform state, or plan values.

From a source checkout after installing TFWhy, run:

```bash
tfwhy explain examples/unexpected-replacement-plan.json --dir examples/replacement-config
```

The output reports one planned replacement and classifies the `user_data = timestamp()` pattern as a **Likely** possible cause. It does not prove an upstream root cause and it does not contact a cloud provider or modify Terraform files.

The JSON file is an intentionally minimal plan-shaped fixture; it is not a command to run Terraform and must not be applied.
