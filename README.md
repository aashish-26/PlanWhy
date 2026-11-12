# PlanWhy

**PlanWhy** means “Terraform: why did this change happen?” It is a local-first Python CLI that explains supplied Terraform plan evidence, reviews bounded configuration risks, proposes conservative refactorings, and offers optional local AI explanations without requiring cloud credentials.

> 🧭 **Current status:** PlanWhy is a pre-1.0, GitHub-first public pilot. Please use synthetic or fully redacted inputs when reporting a problem.

| Capability | Command | Safety boundary |
| --- | --- | --- |
| 📋 Explain a plan | `planwhy explain PLAN.json` | Reads user-supplied JSON; never applies infrastructure |
| 🔍 Review standards | `planwhy review` | Uses local configuration and optional Terraform checks |
| 🌊 Inspect drift | `planwhy drift PLAN.json` | Reads explicit `resource_drift`; never refreshes state |
| 🧠 Explain one finding locally | `planwhy ai-explain ...` | Sends only an allowlisted payload to local Ollama |
| 🛠️ Propose a fix | `planwhy fix ... --dry-run` | Preview-first; writes require explicit approval |
| 🧾 Keep history | `planwhy explain ... --save-history` | Opt-in sanitized metadata only |

## Why PlanWhy

- 🧪 **Evidence first:** deterministic findings remain authoritative.
- 🔒 **Privacy first:** raw plans, state, values, secrets, and credentials stay out of reports and history.
- 🧱 **Safe by default:** no `terraform apply`, `terraform destroy`, telemetry, or cloud access.
- 🧭 **Honest uncertainty:** ambiguous causes remain `Unknown` or `Inconclusive`.
- 🆓 **Free core:** AI is optional, local, and never required for the CLI.

## Installation

Requires Python 3.11 or newer. From a checkout:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

No runtime dependency or cloud credential is required.

For an install-once workflow from this local checkout or another unreleased source checkout, install directly from that checkout:

```bash
pipx install .
```

Alternatively, use an editable virtual-environment install:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

PlanWhy is released under the [MIT License](LICENSE). It is still a pre-1.0 project, so behavior and compatibility boundaries may change.

## Quick start

Install from this source checkout, confirm the version, then run the included synthetic replacement example:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
planwhy --version
planwhy explain examples/unexpected-replacement-plan.json --dir examples/replacement-config
```

This reports a replacement and a **Likely** possible `timestamp()` pattern; it does not prove a root cause, contact a cloud provider, or modify files. See [examples/README.md](examples/README.md) for the input boundary. The console command works from outside the checkout after installation.

## Release and Contribution Hygiene

See [RELEASING.md](RELEASING.md) for the pre-release checklist. Do not commit Terraform plans, state, credentials, variable files, local history, or virtual environments. Run the full test suite, synthetic benchmark, and `git diff --check` before opening a release pull request.

## Repository Layout

```text
src/planwhy/                         Python package and CLI
tests/                             Unit, integration, and privacy tests
tests/fixtures/corporate_project/  Provider-free module test project
tests/fixtures/aws_scanner/       AWS-only static security-review fixture
.github/workflows/                 Continuous integration
```

Terraform projects under `tests/fixtures/` are test inputs only. They must not be applied to real infrastructure.

## Run From a Terraform Project

After installation, change to any Terraform project directory and run:

```bash
planwhy review
planwhy review --format json
planwhy explain ./tfplan.json --dir .
planwhy drift ./tfplan.json
```

Use `--dir PATH` when the configuration is elsewhere. `explain` always requires an explicit plan path; PlanWhy does not guess which plan to use. History is opt-in and defaults to `~/.planwhy/history.json`, never the Terraform project directory. Use `--history-file PATH` for an explicit alternate location.

### Troubleshooting

```bash
planwhy --version
python3 -m unittest discover -s tests -v
python3 benchmarks/run.py
```

If `planwhy` is not found after a `pipx` install, reopen the shell or ensure the pipx bin directory is on `PATH`. PlanWhy is not currently published on PyPI; use `pipx install .` from this checkout. Terraform is optional for plan explanation; `review` reports Terraform formatting/validation as unavailable when the executable is absent. AWS credentials are not required for offline plan JSON analysis.

## Offline Terraform plan fixture

The AWS fixture at `tests/fixtures/aws_scanner/main.tf` is intended for static scanner testing and does not provide credentials. For a complicated corporate-style plan JSON without AWS access, use the provider-free `tests/fixtures/corporate_project/infra/modules/dev` fixture:

```bash
cd tests/fixtures/corporate_project
terraform -chdir=infra init -backend=false
terraform -chdir=infra plan -out=/tmp/planwhy-corporate.tfplan
terraform -chdir=infra show -json /tmp/planwhy-corporate.tfplan > tfplan.json
planwhy explain tfplan.json --dir ./infra
planwhy review --dir ./infra
```

It uses Terraform's built-in `terraform_data` resource and the local `random` provider, and creates no cloud resources. The generated `tfplan.json` is ignored by Git. Run `terraform show` with `-chdir=infra` so Terraform can load the provider initialized for that configuration.

## Usage

```bash
planwhy explain plan.json
planwhy explain plan.json --format markdown
planwhy explain plan.json --format json
planwhy explain plan.json --dir ./infra
planwhy drift plan.json
planwhy drift plan.json --format json
planwhy ai-explain --kind replacement --finding PLANWHY-001 --plan plan.json --dir ./infra --model MODEL
planwhy review --dir ./infra
planwhy review --dir ./infra --required-tag Environment --skip-rule PLANWHY-SEC-002
planwhy import --address aws_s3_bucket.logs --id example-logs --starter-config
planwhy import --address aws_s3_bucket.logs --id example-logs --starter-config --out ./planwhy-import.tf --apply --approve
planwhy fix --finding PLANWHY-001 --plan plan.json --dir ./infra --dry-run
planwhy verify --plan after-change-plan.json --from aws_instance.old --to aws_instance.new --kind resource_rename
planwhy explain plan.json --save-history
planwhy history
planwhy history show 1
planwhy history clear --confirm
```

The current implementation supports Terraform plan JSON format versions with major version `1` and a numeric `MINOR` component, such as `1.0` and newer compatible `1.x` versions. It rejects malformed versions and unsupported major versions, such as `2.0`; accepting a newer minor version does not claim support for a different major version. It reports create, update, delete, replacement, read, and no-op resources, including addresses, types, replacement paths, and supported action reasons: `replace_because_cannot_update`, `replace_because_tainted`, `replace_by_request`, `delete_because_no_move`, `read_because_config_unknown`, `read_because_dependency_pending`, and `read_because_deferred`.

### Resource summary output

Plan reports include a concise resource summary in terminal, Markdown, and JSON output. Each resource shows:

- A friendly kind such as `EC2 Instance`, `S3 Bucket`, or `Lambda Function`.
- The Terraform local resource label and full address.
- A clear action such as `Created`, `Updated`, `Destroyed`, `Replaced`, or `No-op`.
- Changed attribute paths when Terraform provides comparable `before`/`after` objects.

Attribute values are never rendered. For example, a Lambda version change is reported as `Changed attributes (values redacted): version`, not as `3 -> 4`. Runtime names such as an evaluated S3 bucket name are also not inferred from sensitive plan values; the report uses the safe Terraform resource label instead.

| Compatibility surface | Exercised support | Boundary |
| --- | --- | --- |
| Plan JSON format | `1.0`, `1.1`, and other numeric `1.x` minors | Major versions other than `1` are rejected. |
| Terraform version metadata | Synthetic `1.6.0` and `1.9.0` metadata | The version is reported, not evaluated for provider behavior. |
| Remote-drift metadata | Optional `resource_drift` and structural `relevant_attributes` in format `1.x` | Ordinary `resource_changes` are never inferred to be remote drift. |
| Configuration evidence | Root module and literal local child-module sources under `--dir` | Remote, computed, and local sources outside `--dir` remain inconclusive. |

Replacement paths are evidence supplied by Terraform; `planwhy` does not infer a root cause from them. Unknown action reasons are omitted rather than presented as supported evidence. Invalid JSON, unsupported versions, missing required fields, and malformed resource changes produce an error and non-zero exit status.

## Drift assistance

`planwhy drift PLAN.json` is a local reader for Terraform's optional `resource_drift` plan metadata. It never refreshes state, queries a provider, accesses a cloud account, or needs credentials. The same safe drift findings also appear in `planwhy explain` output, after the separate list of planned resource changes.

Terraform can report a resource in both `resource_changes` and `resource_drift`. PlanWhy reports that overlap and any structural `relevant_attributes` paths as correlation only: neither proves that drift caused a planned action, who changed a remote object, or that the plan was generated with `terraform plan -refresh-only`. Terraform's JSON plan format has no supported refresh-only-mode marker that PlanWhy relies on. If `resource_drift` is absent, PlanWhy reports no detected remote drift rather than guessing from normal actions. Raw before/after values are not retained or rendered.

The supported drift path is a user-generated plan that Terraform has already produced, including refresh-only plans when their JSON contains `resource_drift`. OpenTofu behavior is not claimed or specially handled because this repository has no reproduced OpenTofu JSON compatibility case.

## Optional local AI explanations

AI explanations are strictly opt-in. Existing commands never contact Ollama, and PlanWhy has no cloud-AI, telemetry, API-key, or model-download path. The dedicated command calls only Ollama's local loopback endpoint at `http://127.0.0.1:11434/api/generate` after it has first produced the selected deterministic finding.

### First-time setup

Install Ollama using its [official installation instructions](https://docs.ollama.com/quickstart). Then start the local service if your platform does not start it automatically, and pull a model yourself. PlanWhy intentionally has no default model and never downloads one:

```bash
# Confirm Ollama is installed and the local service is reachable.
ollama --version
ollama list

# Choose a model suitable for your own hardware.
ollama pull llama3.2
ollama list
```

Use the exact model name shown by `ollama list`; `MODEL` in examples is a placeholder, not a literal model name.

### Explain a finding

First run the deterministic command that creates the finding. Replacement and drift IDs are ordinal; standards findings use their rule ID:

```bash
# Replacement: the first replacement in the plan.
planwhy explain tests/fixtures/replacement_plan.json --dir tests/fixtures/replacement_config
planwhy ai-explain \
  --kind replacement \
  --finding PLANWHY-001 \
  --plan tests/fixtures/replacement_plan.json \
  --dir tests/fixtures/replacement_config \
  --model llama3.2

# Standards: review output shows each rule's one-based occurrence selector.
planwhy review --dir ./infra
planwhy ai-explain \
  --kind standards \
  --finding PLANWHY-TAG-001 \
  --occurrence 2 \
  --dir ./infra \
  --model llama3.2 \
  --format markdown

# Drift: the plan must contain Terraform's resource_drift metadata.
planwhy drift plan.json
planwhy ai-explain \
  --kind drift \
  --finding PLANWHY-DRIFT-001 \
  --plan plan.json \
  --model llama3.2 \
  --format json
```

The AI command explains one existing deterministic finding; it does not discover arbitrary Terraform problems, change findings, or run fixes. Ollama output is labelled untrusted local-model interpretation.

### Troubleshooting

- `could not contact local Ollama`: start Ollama and confirm `http://127.0.0.1:11434` is reachable.
- `could not find model 'name'`: run `ollama pull name`, then retry with the exact name from `ollama list`.
- `--plan is required`: replacement and drift explanations need the same user-generated plan used by the deterministic command.
- `finding ID does not identify a finding`: rerun `explain`, `drift`, or `review` and use an ID from that output.
- `multiple standards findings`: use the `occurrence N` displayed beside the matching rule in review output, then add `--occurrence N`; the first matching rule is occurrence `1`.
- Slow or failed responses: choose a model that fits available RAM/VRAM or pass `--timeout SECONDS` from 1 through 120.

Replacement IDs are ordinal (`PLANWHY-001` is the first replacement); drift IDs are also ordinal (`PLANWHY-DRIFT-001` is the first drift finding). Standards explanations use a stable rule ID; if the rule appears multiple times, pass its one-based `--occurrence N` shown in review output. JSON review output includes an `occurrence` field for every finding. `--timeout` defaults to 30 seconds and accepts values from 1 through 120 seconds. A missing local service, model, malformed/empty reply, timeout, or oversized reply returns a non-zero error without changing the deterministic workflow.

### Local data and privacy boundary

PlanWhy sends only a compact, versioned allowlist to the local model: the finding ID and kind; fixed deterministic facts; replacement confidence or drift status; standards severity; and safe replacement structural paths when they match a restrictive identifier grammar. For standards findings, PlanWhy uses a built-in rule-context catalogue instead of sending finding text. It does **not** send resource addresses, filenames, locations, raw evidence text, explanations, raw plan JSON, Terraform state, HCL/configuration, before/after values, credentials, environment variables, import identifiers, or history. Prompts and responses are not persisted by PlanWhy.

The model must return a bounded JSON explanation with facts, cautious interpretation, uncertainty, and conservative next steps. PlanWhy renders that content in a separately labelled **untrusted local-model interpretation** section together with the deterministic context it sent. Model text never changes PlanWhy rule IDs, evidence, severity, confidence, drift status, or verification outcomes, and PlanWhy never executes model-generated commands or code. Prompt-injection-like content is treated as data and excluded from the request where it does not meet the allowlist.

Local model resource use depends on the model, context, and your hardware. Download and memory requirements can be significant; choose and pull a model only after reviewing its Ollama listing and your available disk/RAM/VRAM. See Ollama's [local API generate endpoint](https://docs.ollama.com/api/generate) for the local protocol PlanWhy uses. PlanWhy does not claim compatibility with every Ollama release or model. It does not provide open-ended troubleshooting, chat, arbitrary code review, automatic fixes, cloud inference, or model training.

## Security and limitations

Reports and CLI errors contain only an explicit allowlist of plan metadata and safe structural diagnostics. They never include Terraform before/after values, sensitive values, complete change objects, or raw plan content. Terraform plan JSON can itself contain sensitive data, so reading a plan necessarily processes that input in memory. The core CLI makes no network calls and never runs `terraform apply` or `terraform destroy`.

This release does not fully evaluate Terraform configuration, resolve arbitrary modules or variables, or determine replacement root causes conclusively. Its `verify` command performs a deliberately narrow, plan-based check: it reports `verified` only when the supplied after-change plan shows the requested target as `no-op` and the old address absent. The configuration scanner only inspects bounded, conservative evidence.

## Replacement-cause analysis

When a replacement is present, `planwhy` emits a replacement finding with the resource address and type, Terraform's replacement paths, safe evidence, an explanation, and one of three confidence categories:

- **Confirmed** means Terraform directly supplied a cause-specific reason such as taint or an explicit replacement request. Generic replacement metadata, provider replacement requirements, and address changes alone do not confirm an upstream root cause.
- **Likely** means an optional configuration directory contains a matching resource block and a recognizable timestamp, random-value, AMI/data-source, `user_data`, `count`, or `for_each` pattern.
- **Unknown** means the plan or available configuration does not provide enough evidence to identify an upstream cause. A replacement path alone is never treated as proof of that cause.

Configuration inspection is a small, dependency-free, HCL-aware scanner. It matches the complete resource address (after removing instance indexes), including literal local child-module sources beneath `--dir`; resources with the same type and name in different modules are not cross-matched. It records only relative file paths, line numbers, attribute names, and recognized pattern labels. For a direct, single-line expression it can link an attribute to a variable default, local, data source, or managed-resource declaration and report the relevant source locations. A data source or dynamic timestamp/random expression is only a possible cause; a managed-resource reference is evidence of a link, not proof that its value changed.

The scanner is not a Terraform language evaluator and deliberately has no HCL-parser dependency. Conditional and multiline expressions, functions other than the recognized dynamic patterns, computed defaults, module outputs, remote or computed module sources, local modules outside `--dir`, generated configuration, and indirect dependency graphs remain **Unknown**. `count`, `for_each`, indexed addresses, and `moved` blocks are recorded only as contextual metadata and never establish a replacement cause. Terraform behavior, state, and before/after values are not evaluated or exposed.

## Standards and security review

Phase 3 adds the deterministic `review` command. Reports are available in terminal, Markdown, and JSON formats:

```bash
planwhy review --dir ./infra
planwhy review --dir ./infra --format json
```

The default required tag is `Name` for supported AWS resources. Use repeated `--required-tag TAG` options to replace that default policy, and repeated `--skip-rule RULE_ID` options to disable applicable checks.

Current rule IDs include:

- `PLANWHY-TF-001`, `PLANWHY-TF-002`: Terraform version constraint missing or unbounded.
- `PLANWHY-PROVIDER-001`, `PLANWHY-PROVIDER-002`: provider constraints missing or unbounded.
- `PLANWHY-TAG-001`: required AWS resource tag missing.
- `PLANWHY-DOC-001`: variable or output description missing.
- `PLANWHY-NAME-001`: basic lowercase snake_case naming violation.
- `PLANWHY-SEC-001`: public security-group ingress detected.
- `PLANWHY-SEC-002`: supported storage resource lacks explicit encryption configuration.
- `PLANWHY-IAM-001`, `PLANWHY-IAM-002`: statically visible IAM Allow action or resource wildcards.
- `PLANWHY-NET-002`: unrestricted all-protocol security-group egress.
- `PLANWHY-NET-003`: public network-ACL SSH/RDP or all-protocol ingress.
- `PLANWHY-UPGRADE-001`: literal `hashicorp/terraform` provider source, which HashiCorp documents as legacy and incompatible with Terraform 0.11 and later.
- `PLANWHY-FMT-001`, `PLANWHY-VALIDATE-001`: Terraform formatting or validation failed.
- `PLANWHY-TOOL-001`: Terraform is unavailable, so Terraform-dependent checks were skipped; this is informational, not a security finding.
- `PLANWHY-CONFIG-001`: configuration file could not be safely scanned.

Formatting uses `terraform fmt -check -recursive`; validation uses `terraform validate -no-color`. These commands never apply or destroy infrastructure. If Terraform is not installed, the review reports an informational unavailable-tool finding. TFLint, Trivy, cloud APIs, network calls, and telemetry are not required or used.

The security checks are intentionally narrow and high-confidence. They cover unrestricted IPv4/IPv6 security-group ingress, including direct references to literal variable defaults; all-protocol unrestricted security-group egress; statically visible public network-ACL SSH/RDP or all-protocol ingress; missing explicit encryption settings for selected AWS storage resources; and literal IAM `Allow` statements with global or service action wildcards or a global resource wildcard. These findings identify potentially broad permissions, not reachability or exploitability. They are not a comprehensive AWS, Terraform, or policy security scanner. Complex HCL, computed tags, provider defaults, modules, indirect expressions, IAM policy documents outside supported `jsonencode` literals, and unsupported resource types may remain unreported or require manual review.

The upgrade check is intentionally a single, source-backed migration rule: it recognizes only a literal line declaring `source = "hashicorp/terraform"` within `required_providers`. Its remediation is to remove that legacy requirement and review use of Terraform's built-in provider features; it does not rewrite configuration or infer a provider-version upgrade path. Comments, computed sources, arbitrary deprecated arguments, provider schemas, and OpenTofu-specific migrations remain unsupported. See HashiCorp's [provider requirements documentation](https://developer.hashicorp.com/terraform/language/providers/requirements) for the legacy-provider compatibility statement.

## Import proposals

`planwhy import` creates a reviewable Terraform `import` block only from the address and identifier you explicitly provide. It never queries a cloud account, state file, or provider API.

```bash
# Preview a unified diff; no file is written.
planwhy import --address aws_s3_bucket.logs --id example-logs --starter-config

# Writing requires a new, explicit path plus both approval flags.
planwhy import --address aws_s3_bucket.logs --id example-logs --starter-config \
  --out ./planwhy-import.tf --apply --approve
```

The initial starter-configuration support is intentionally limited to a root, unindexed `aws_s3_bucket`: its supplied import ID is its bucket name. Other supported managed-resource addresses receive an import block but no guessed resource body; the report explains that provider-specific required arguments are missing. Module instances, `count`/`for_each` targets, data sources, malformed addresses, cloud discovery, state inspection, and arbitrary provider schemas are unsupported. The import identifier appears only in the user-requested generated diff or file and is never saved to history; avoid placing secrets in an import identifier.

## Local plan history

History is disabled by default. Save sanitized metadata only when explicitly requested:

```bash
planwhy explain plan.json --save-history
planwhy explain plan.json --save-history --history-file ./planwhy-history.json
planwhy history
planwhy history show 1 --format json
planwhy history clear --confirm
```

The default history file is `~/.planwhy/history.json`; `--history-file` overrides it. Entries contain a schema version, timestamp, Terraform/plan format versions, action counts, and allowlisted resource metadata: address, type, action, replacement paths, and supported action reasons. Raw plan JSON, state, before/after values, configuration expressions, credentials, and secrets are never persisted. Corrupt or unsupported history files are reported without being overwritten. Clearing history requires `--confirm` and deletes only the selected local history file.

History can identify repeated replacement metadata such as the same address and replacement paths across saved runs. Recurrence is an observation, not proof of a root cause or evidence that the same upstream configuration expression caused every occurrence.

## Verified refactoring

Phase 4 supports conservative, plan-driven proposals:

```bash
planwhy fix --finding PLANWHY-001 --plan plan.json --dir ./infra --dry-run
planwhy fix --finding PLANWHY-001 --plan plan.json --dir ./infra --apply --approve
planwhy verify --plan after-change-plan.json --from aws_instance.old --to aws_instance.new --kind resource_rename
```

Fix IDs are ordinal within the replacement resources in the supplied plan (`PLANWHY-001` is the first replacement). Dry-run is the default and emits a proposed `moved.tf` unified diff without writing files. Writing requires both `--apply` and explicit `--approve`; an existing `moved.tf` is never overwritten. The command never runs `terraform apply` or `terraform destroy` and never changes Terraform state.

The initial proposal scope is an unambiguous root-level resource rename or a single numeric-to-string instance mapping that supports a `count` to `for_each` migration. Ambiguous, module-addressed, unsupported, or value-dependent mappings produce no fix. Verification consumes a user-generated plan and reports `verified` only when the target address is `no-op` and the old address is absent; otherwise it reports `not_verified` or `inconclusive`. A clean plan by itself is not considered proof of success.

## Tests

Run the dependency-free test suite with:

```bash
python3 -m unittest discover -s tests -v
```

## Synthetic benchmark

Run the versioned, no-cloud benchmark from a source checkout:

```bash
python3 benchmarks/run.py
```

It checks a conservative replacement classification, explicit Terraform drift semantics, and the local-AI prompt allowlist. It does not claim broad provider compatibility, security coverage, or AI-answer quality. See [benchmarks/README.md](benchmarks/README.md) for the exact cases and safe model-review rubric.

## MVP scope

- Deterministic Terraform plan summaries in terminal, Markdown, and JSON.
- Conservative replacement-cause evidence without cloud access, plus explicitly invoked local Ollama explanations of selected deterministic findings.
- Local standards and narrow AWS security checks.
- Dry-run Terraform refactoring proposals with explicit approval for writes.
- Opt-in, sanitized local plan history with recurrence observations.

Plan JSON, Terraform state, variable files, credentials, and sensitive configuration should never be committed. Terraform plan JSON may contain sensitive data and is processed in memory; PlanWhy does not transmit it or persist raw plan values.

## Feedback and contributions

PlanWhy is a GitHub-first public pilot, promoted through YouTube and developer feedback. Use the GitHub **Bug report** form for installation failures, reproducible false positives/negatives, unclear output, local-model compatibility, and documentation problems. Use the **Focused improvement** form for a specific Terraform workflow that needs to be better.

Use a minimal **synthetic or fully redacted** reproduction. Include the `planwhy --version` output, expected and actual behavior, Terraform version, operating system, and the exact safe command used. Never post credentials, state files, raw plans, private Terraform code, API keys, or unredacted model prompts/responses.

Contributors should make focused changes, add regression coverage for bugs, run relevant tests plus the full suite where practical, and report exact results. Check `Plan.md` before proposing feature work so the public-pilot scope and safety boundaries remain intact.
