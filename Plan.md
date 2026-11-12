# PlanWhy — Product Plan and Engineering Roadmap

> **Purpose:** the source of truth for product direction, safety constraints, phase status, and implementation decisions. Attach this file to coding prompts. `README.md` is the public human-facing guide; its required contents are specified in [README.md specification](#9-readmemd-specification-for-future-agents).

## 1. Product definition

| Item | Decision |
| --- | --- |
| Name | **PlanWhy** — Terraform + “Why did this happen?” |
| Product | Local-first Terraform engineering companion |
| Interface | Python CLI |
| Primary users | Platform/DevOps/SRE engineers, Terraform consultants, and infrastructure teams |
| License and launch | Free, MIT-licensed, GitHub-first public pilot promoted through YouTube and developer feedback |
| Current state | Phases 1–12 reported complete; Phase 13 (public pilot) is next |

PlanWhy helps an engineer understand Terraform changes, investigate supported replacement and drift evidence, review bounded risks and standards issues, and evaluate a proposed fix. It is **not** a replacement for Terraform, provider documentation, security scanners, or human review.

### Product promise

**Explain what the available Terraform evidence establishes, what it does not establish, and what a careful next step is.**

### Non-goals for the current product

- No `terraform apply` or `terraform destroy`.
- No autonomous infrastructure changes, shell execution from model output, or silent edits to user files.
- No hosted AI, remote backend, account system, telemetry by default, or cloud credentials required for static analysis.
- No promise to diagnose or repair arbitrary Terraform errors, cover every provider, detect every secret, or eliminate all AI hallucinations.

## 2. Principles and safety rules

1. **Evidence before explanation.** A report labels confirmed facts, hypotheses, and unknowns separately.
2. **Deterministic core.** Parsing, rules, confidence, safety classification, and verification work without AI.
3. **AI is optional and non-authoritative.** It explains permitted deterministic findings only; it cannot alter a finding’s severity, confidence, evidence, status, or verification result.
4. **Local-first and privacy-first.** No telemetry by default. Plans, state, configuration, logs, history, and model context are sensitive.
5. **No destructive actions.** Never run `terraform apply` or `terraform destroy`; never silently overwrite or delete configuration.
6. **Minimise data.** Use allowlisted metadata; do not print, persist, or send raw plan JSON, Terraform state, raw attributes, environment variables, credentials, API keys, or unrestricted HCL to the model.
7. **Honest uncertainty.** Ambiguous evidence becomes `Unknown`/`Inconclusive`, never a fabricated cause.
8. **Verification is literal.** A fix is “verified” only when the documented checks actually ran and passed.
9. **Small, testable increments.** Avoid agent frameworks, broad refactors, and new dependencies unless a phase requires them.
10. **Bugs outrank roadmap order.** Fix reproducible security, privacy, destructive-action, and correctness bugs with regression coverage.

### Terraform semantics that must not be weakened

- `replace_paths` identifies a path that triggered replacement; it does **not** prove the upstream business or configuration root cause.
- `count`, `for_each`, timestamps, data sources, AMI lookups, and random resources are not root-cause proof by themselves.
- PlanWhy’s drift analysis is evidence-based and offline: it can interpret supplied configuration, state-derived material, or a user-generated plan. It does **not** connect to a provider, refresh remote state, independently discover live drift, or reliably determine who changed a remote resource.
- A Terraform validation failure caused by an unavailable provider/plugin must be reported as that limitation, not as a configuration defect.

## 3. Architecture boundary

```text
CLI
├── Deterministic workflows
│   ├── plan/configuration loading and inspection
│   ├── analyzers, rules, confidence, and verification
│   └── terminal / Markdown / JSON rendering
└── Explicit optional AI explanation
    ├── sanitized allowlisted finding/evidence builder
    ├── versioned task-specific prompt
    ├── local Ollama adapter
    ├── bounded response parser/validator
    └── separately labelled AI renderer
```

Architecture requirements:

- Parsing, analysis, verification, rendering, persistence, and model integration remain independently testable.
- Raw Terraform values stay out of normalized findings and renderers.
- Ordinary commands must not contact a model. AI requires an explicit command/option.
- The Ollama adapter is small, local-only, loopback-only, and isolated from the deterministic core; do not add a generic multi-provider layer yet.
- Never download a model automatically. A user selects and installs it themselves.
- Prompts are versioned, bounded, task-specific, and built only from sanitized allowlisted metadata.
- Treat comments, names, descriptions, and all model output as untrusted text. Do not let either supply instructions to the application.
- Bound request/response size and timeout; handle unavailable Ollama, missing model, timeout, malformed/empty/oversized response, and invalid model input safely.

## 4. Evidence status and repository audit note

The following is **historical, user-reported project evidence** recovered from the prior plan. It is useful context, not a substitute for rerunning checks in the actual PlanWhy checkout.

| Phase | Status | Reported evidence |
| --- | --- | --- |
| 1 — Plan explainer | Complete | Plan actions with terminal, Markdown, and JSON output |
| 2 — Replacement analysis | Complete | Conservative evidence and confidence states |
| 3 — Standards/security review | Complete | Configurable standards and selected security checks |
| 4 — Fix proposals/verification | Complete | Reviewable diffs and explicit approval/verification outcomes |
| 5 — Local history | Complete | Opt-in sanitized history, schema validation, corruption handling |
| 6 — Packaging/release readiness | Complete | Console script, documentation, CI checks |
| 7 — Reliability hardening | Complete | Regression fixes and CLI smoke tests |
| 8 — Install from any project | Complete for a local checkout | `pipx install .` and outside-repository smoke tests; PyPI not established |
| 9 — Configuration understanding | Complete | 43 tests reported at phase close |
| 10 — Import and permission assistance | Complete | 52 tests reported at phase close |
| 11 — Drift and upgrade assistance | Complete | 58 tests reported; AWS fixture validation blocked by unavailable provider |
| 12 — Optional local AI explanations | Complete | 72 tests reported passing; local `llama3.2` replacement, standards, and drift smoke tests reported passing |

**Current repository audit (2026-11-12):** the actual checkout, package metadata, MIT license, release checklist, CI workflow, CLI help, source, and tests were inspected. The code matches the local-first, deterministic-core, explicit-Ollama, no-apply/no-destroy architecture in this plan. The full suite passed with 77 tests. A clean temporary-environment build produced and installed the `planwhy 0.1.0` wheel, and the installed console script ran from outside the checkout. Safe deterministic CLI smoke checks passed for `explain`, `drift`, `review`, and import preview. Real local `llama3.2:latest` smoke tests passed for a replacement explanation and a repeated standards-rule explanation. A repeated-standards-finding AI-selection defect was fixed with an explicit one-based `--occurrence N` selector; its payload remains the same allowlisted rule context and never includes a location, address, or finding free text. Phase 13 readiness now also includes `planwhy --version`, visible one-based occurrences in terminal/Markdown review output plus JSON `occurrence` fields, a public synthetic first-run example, and a versioned no-cloud benchmark that runs as part of the suite.

**Brand migration status (2026-11-12):** the local Python distribution, package/module, CLI command, rule IDs, prompts, examples, tests, documentation, history location, and MIT attribution use **PlanWhy** / `planwhy` / `PLANWHY-*`. A clean install of the renamed package passed the same synthetic example and version smoke checks. Public GitHub/PyPI screening found no exact `planwhy` repository-name match or registered PyPI package at the time checked; that is a practical namespace screen, not trademark or domain clearance. The hosted GitHub repository still needs to be renamed by its owner before the remote URL and public release links can use `PlanWhy`.

Confirmed by the project owner after the earlier plan: local Ollama is now working. The prior plan further reports successful real local `llama3.2` smoke tests. This means “Ollama unavailable” is no longer the current product status; it remains a failure case that the program must handle.

## 5. Completed Phase 12 contract — local Ollama explanations

Phase 12 is complete only so long as these behaviours remain true:

- The user explicitly invokes AI explanation for supported deterministic findings.
- The current CLI contract is `planwhy ai-explain --kind {replacement,standards,drift} --finding ID --model MODEL`; repeated standards rule IDs additionally require `--occurrence N` to select one finding without broadening model context.
- `--model` is explicit; PlanWhy must not silently choose or download a model.
- The adapter calls only local Ollama and sends sanitized, allowlisted metadata—not raw plans, state, source trees, HCL, credentials, environment variables, addresses, filenames, locations, or raw finding text.
- The response separates facts, interpretation, uncertainty, and conservative next steps, and is labelled as untrusted local-model interpretation.
- Unknown or inconclusive findings cannot become certainty through model prose.
- Model output never changes deterministic results or writes user files.

Expected verification on the actual checkout before any related change:

```bash
python3 -m compileall -q src tests
# Run the repository’s documented complete test command.
planwhy ai-explain --help
```

Then run the smallest relevant synthetic smoke test for each affected `replacement`, `standards`, or `drift` workflow. Never include a private plan, state file, or credentials in a test report.

## 6. Roadmap and phase gates

Only the active phase introduces planned features. Later phases may be refined from pilot evidence. Bug/security/privacy fixes are always allowed.

### Phase 13 — Public pilot and feedback (ACTIVE)

**Goal:** establish whether real engineers can install, understand, and trust PlanWhy before expanding its scope.

- [x] Inspect the actual repository and reconcile this plan, README, license, packaging metadata, CLI help, CI, and release checklist with reality.
- [x] Run the full suite, relevant CLI smoke tests, and a clean-install package check; record actual outcomes and environment limitations.
- [ ] Run every README command block against the release candidate where feasible, or label/remove any command that cannot be verified safely.
- [ ] Publish a GitHub release only after the project owner reviews the release checklist and MIT licensing.
- [ ] Publish GitHub-first installation and limitations guidance; promote it through YouTube and relevant developer communities.
- [ ] Invite voluntary feedback through GitHub Issues/Discussions. Never collect or request private Terraform plans, state, credentials, source, prompts, or sessions.
- [x] Use issue templates/categories for installation failures, false positives/negatives, confusing output, local model compatibility, latency, and documentation gaps.
- [x] Build and maintain a versioned synthetic benchmark for deterministic findings and AI-prompt allowlisting; AI answer quality remains a human-reviewed pilot signal, not a benchmark score.
- [x] Fix reproducible defects with regression tests; review findings regularly and decide the next small scope from evidence.
- [x] Provide an installed-version command and explicit repeated-standards selectors so pilot feedback is reproducible.

**Exit criteria:** engineers outside the creator’s immediate circle can install and use the tool; feedback identifies concrete, reproducible improvements; repeat usage and trust are assessed without calling downloads, views, or likes product-market fit.

### Phase 14 — Guided troubleshooting and fix assistance (FUTURE; after pilot evidence)

**Goal:** users can describe a supported Terraform problem, while PlanWhy asks only decision-relevant questions and produces reviewable proposals.

- Define supported intents and evidence requirements before implementation.
- Inspect only an explicit project directory; do not silently traverse arbitrary paths.
- Run documented safe checks only; never apply/destroy or use cloud operations.
- Gather available facts before asking concise targeted questions.
- Separate confirmed findings, hypotheses, unknowns, and next steps.
- Generate diffs/proposals only for supported cases; require explicit approval for a narrow file write.
- Test multi-issue projects, ambiguity, malicious comments, synthetic secret markers, and insufficient-context cases.

**Not yet an implemented command:** do not document an illustrative `planwhy fix "..."` command as available until the code and tests exist.

### Phase 15 — CI and pull-request workflows (FUTURE)

**Goal:** stable local findings become usable in ordinary review workflows.

- Define machine-readable schema and exit-code policy.
- Support non-interactive CI with configurable severity thresholds.
- Consider PR comments only after finding IDs and output are stable.
- Ensure logs and artifacts cannot leak raw plans or secrets; test permissions, duplicate output, provider failures, and noisy findings.

### Phase 16 — Business validation and model strategy (FUTURE; evidence-led)

**Goal:** decide whether a paid/team capability or any hosted/model investment is justified.

- Interview target users; measure repeat use, false-positive tolerance, trust, time saved, and willingness to pay.
- Identify one paid problem before building SaaS, accounts, or hosted infrastructure.
- Consider policy packs, shared reports, collaboration, and administration only if the pilot validates them.
- Reassess retention, access control, isolation, deletion, data disclosure, and cost before any hosted option.
- Consider fine-tuning only with lawful, consented, high-quality data and a measured evaluation advantage. Public use never implies permission to train on user code or conversations.

## 7. Test, release, and documentation policy

Every change requires the smallest relevant subset plus the full repository suite when practical:

1. Unit tests for parsers, analyzers, models, formatters, and helpers.
2. Golden/fixture tests for known plans/configurations.
3. Regression tests for reproducible bugs.
4. Negative tests for malformed input, missing fields, unsupported versions, ambiguity, and failed external tools.
5. Privacy tests with synthetic secret markers across reports, logs, history, diffs, and AI payloads.
6. Integration tests with synthetic Terraform projects/plans when available.
7. CLI smoke tests for affected commands, output formats, errors, and exit codes.
8. Packaging tests when distribution changes.
9. Compatibility tests for declared platforms, Python/Terraform versions, and local model/runtime combinations.

Completion checklist:

- [ ] Inspect the code and current behaviour first.
- [ ] Define acceptance criteria or reproduce the bug.
- [ ] Make the smallest effective change and focused test update.
- [ ] Run relevant tests, full suite, CLI smoke tests, and docs-command checks.
- [ ] Review diff for unrelated edits, secret leakage, unsafe writes, and misleading claims.
- [ ] Update `Plan.md` and `README.md` only when their claims remain true.
- [ ] Report exact commands/results and remaining limits. Never imply an unavailable provider, Terraform executable, or local model was tested.

## 8. Instructions for coding agents

Use this at the start of implementation prompts:

> Treat `Plan.md` as the source of truth. Inspect the current repository, `git status`, CLI help, tests, and active phase before coding. Work only on the requested bounded task in that phase. Do not invent unsupported commands, flags, output formats, integrations, models, test results, or security claims. Fix reproducible bugs with regression coverage. Run and report actual relevant tests, the full suite where practical, CLI smoke tests, and documentation command checks. Keep raw Terraform values and secrets out of logs, fixtures, prompts, and reports. If the request conflicts with this plan, explain the conflict before changing code.

Agent responsibilities:

- Preserve verified facts; classify all other facts as implementation targets or unverified history.
- Mark a phase complete only when its explicit exit criteria are evidenced.
- Update this plan after a genuine status, constraint, architecture, or roadmap decision change.
- Do not ask for production credentials, private state, real plans, or employer code. Use synthetic fixtures.
- The project owner decides whether to accept, commit, publish, enable writes, or use an external service.

## 9. README.md specification for future agents

`README.md` is the public GitHub landing page. It must be maintained separately from this engineering plan and must describe only checked-in, test-supported behaviour.

### Audience and tone

- Write for an engineer arriving from GitHub, a YouTube link, search, or a shared issue—many will not know the project history.
- Lead with the user problem and a plain-English explanation of PlanWhy. Use clear, calm, technically precise language; be helpful rather than promotional.
- Prefer “can analyse supplied evidence” to broad claims such as “understands everything” or “fixes Terraform.” Explain uncertainty without hiding it.
- State that AI is optional local assistance, not a source of truth. Never promise “no hallucinations”; instead describe the deterministic/evidence boundary.

### Required public structure

1. **Title and one-sentence value proposition:** spell the name **PlanWhy**, explain its Terraform + “Why” meaning, and say it is a local-first Python CLI.
2. **What it helps with:** concise supported areas, qualified by the source-backed evidence available at release (plans, replacement analysis, standards/security checks, reviewable fix proposals/verification, bounded import/permission/drift/upgrade assistance, and optional local AI explanation).
3. **What it does not do:** `terraform apply`/`destroy`, autonomous cloud operations, automatic file mutation, live cloud drift discovery, universal Terraform diagnosis, or perfect security/secret detection.
4. **Trust, privacy, and drift semantics:** deterministic findings first; AI is opt-in/untrusted; no telemetry by default; sensitive artifact warning; no raw sensitive material in AI payloads; `replace_paths` and offline drift limitations.
5. **Prerequisites and installation:** list only runtime/package-manager versions and commands confirmed in repository metadata or CI. Until PyPI publication is verified, document the reported local-checkout route `pipx install .` as a source install and do not present `pip install planwhy` as available. State any platform support only if tested.
6. **Quick start:** use only commands confirmed by the current `--help` output and tests. Pair each command with required input/artifact and expected output type. Never paste real plan/state/secrets.
7. **Optional local Ollama:** make it a separate opt-in section. Link to the [official Ollama quickstart](https://docs.ollama.com/quickstart); explain that the user installs/runs Ollama and pulls a model themselves. Preserve the current explicit-model rule. After verification in the checkout, document the supported command, historically `planwhy ai-explain --kind {replacement,standards,drift} --finding ID --model MODEL`, and an actual tested model (historically `llama3.2`). Explain local resource/latency variability and failure guidance. Never claim PlanWhy installs models or uses cloud AI.
8. **Examples and output:** use small synthetic, redacted examples. Label model-generated output separately from deterministic findings and show uncertainty where relevant.
9. **Limitations:** provider plugins may be required for Terraform validation; PyPI status; supported/unsupported cases; no live cloud drift detection; AI output can be wrong and must be reviewed.
10. **Feedback and contributing:** invite GitHub Issues/Discussions for reproducible bugs, false positives/negatives, install failures, model compatibility, and docs gaps. Ask contributors to use synthetic/redacted reproductions; never request credentials, state, raw plans, private source, or secrets. Include contribution/test commands only after verifying them in the repo.
11. **License and project status:** state MIT only if an `LICENSE` file is present and is MIT; identify pre-1.0/pilot status if still accurate.

### README claim and command rules

- Treat `--help`, packaging metadata, tested examples, CI, and release artifacts as the authority. If they disagree with this plan, fix the implementation/docs discrepancy rather than guessing.
- Do **not** invent subcommands, flags, config files, output formats, provider support, installation paths, package names, version support, benchmark scores, security guarantees, integrations, or roadmap features.
- Do not describe illustrative future commands (`planwhy fix`, chat, IDE, CI, hosted services) as present features.
- Do not claim an AI explanation is deterministic, safe to apply, or capable of overriding evidence.
- Use exact commands only after running them against the release candidate. Mark source-only/unverified commands clearly, or omit them.
- Keep `Plan.md` implementation-specific; keep `README.md` shorter, outcome-focused, and free of internal phase mechanics.

### README release gate

Before publishing, run every code block that contains a command in a clean/synthetic environment where feasible. Confirm links, headings, license statement, installation route, CLI syntax, model guidance, privacy wording, and stated limitations. If this cannot be done, remove or label the unverified content; do not publish a confident guess.

## 10. Pilot signals (not current achievements)

- Ten people outside the creator’s immediate circle try PlanWhy.
- Three return without prompting.
- Users can install it and use it from their own Terraform project directory.
- Feedback records false positives/negatives, unsupported cases, local-model compatibility, response quality, and whether PlanWhy changed a real decision or reduced investigation time.
- No user code, plan, state, prompt, or diagnostic session is collected by default.

These are learning signals, not revenue, traction, or product-market-fit claims.
