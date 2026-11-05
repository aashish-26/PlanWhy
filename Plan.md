TFWhy — Product Vision & Engineering Roadmap
Single source of truth for product direction, architecture, engineering rules, phase status, and the active roadmap.

Field	Current position
Product	tfwhy
Type	Local-first Terraform engineering assistant
Current interface	Python CLI
Primary users	Platform engineers, DevOps engineers, SREs, Terraform consultants, infrastructure teams
Active phase	No active phase — Phase 12 is complete
Latest reported core validation	Phase 12 complete; 72 Python unit tests passed on 2026-11-05; local Ollama `llama3.2` replacement, standards, and drift smoke tests passed; MIT license and release checklist added
Core constraints	No terraform apply, no terraform destroy, no telemetry by default, no raw-plan persistence, no cloud access required for static analysis


Working agreement: GitHub Copilot implements bounded tasks. ChatGPT supports architecture, Terraform semantics, test strategy, and review. Automated tests—not an AI assertion—establish expected behavior.
How to use this document
Attach Plan.md to implementation prompts. Before coding, inspect the current repository and identify the active phase. Work only on the active phase. Do not jump ahead. Fix reproducible bugs whenever found, add regression tests, run relevant tests and the full suite, and report actual results. Update this document when a phase status, roadmap, constraint, or meaningful architectural decision changes.
1. Product vision
TFWhy helps engineers understand Terraform's proposed changes, investigate resource replacements and drift, identify supported risks and standards violations, propose conservative corrections, and check whether a proposed fix achieves its intended result.
Core promise
Understand why Terraform is planning a change, determine what can and cannot be concluded safely, and verify whether a proposed fix achieves the intended result.
Product principles
1. Evidence before explanation. Findings must be grounded in plan metadata or inspected configuration. Distinguish confirmed facts, hypotheses, and unknown causes.
2. Deterministic core. Parsing, rule evaluation, safety classification, and verification work without AI.
3. Local-first by default. No telemetry or network transmission in core workflows by default.
4. Safe by design. Never run terraform apply or terraform destroy; never silently mutate user configuration.
5. Privacy by design. Treat plan JSON, state, configuration, logs, and history as potentially sensitive. Use explicit allowlists and never persist raw plans or secrets.
6. Honest uncertainty. Missing or ambiguous evidence results in Unknown, Inconclusive, or equivalent—not fabricated certainty.
7. Useful over clever. Prefer small, testable changes over agent frameworks, unnecessary dependencies, or broad refactors.
8. Verify outcomes. Do not claim a fix is verified unless the defined checks actually ran and passed.
9. Fix bugs whenever found. Reproducible correctness, security, privacy, or destructive-action bugs take priority over feature work.
10. Follow the roadmap. Do not implement future features early, except for bug fixes and urgent security corrections.
11. AI is an assistant, not an authority. AI can explain or help investigate; it cannot override deterministic findings, certify safety, or autonomously change infrastructure.
Long-term product direction
The long-term ambition is an interactive Terraform engineering assistant. An engineer may eventually describe a problem in ordinary language, and TFWhy will inspect permitted project evidence, run safe checks, ask targeted follow-up questions, explain multiple findings, and propose reviewable fixes. A conversational UI or editor integration may be considered only after the CLI is useful and validated with real users.
This long-term vision is not the current scope. The current scope is a reliable CLI with optional local AI explanations of existing deterministic findings.
2. Non-negotiable safety and privacy rules
- Never execute terraform apply or terraform destroy.
- Do not run commands that modify cloud infrastructure or require cloud credentials for static analysis.
- Do not silently change, delete, or overwrite user configuration.
- Show proposed fixes as diffs or separate files first. Any file write must be explicit, narrowly scoped, and approved.
- Do not claim a fix is verified unless the defined checks actually ran and passed.
- replace_paths identifies a replacement-triggering path; it does not necessarily prove the upstream root cause.
- Do not treat count, for_each, timestamps, AMI lookups, data sources, or random resources alone as proof of root cause.
- Never print or store raw plan JSON, Terraform state, raw resource attribute values, environment variables, credentials, or API keys in reports, logs, history, or AI payloads.
- Use allowlisted metadata extraction. Do not pass full Terraform change objects into renderers, logs, history, or AI prompts.
- Keep history opt-in and sanitized.
- No telemetry by default.
- Do not commit real plan files, state files, credentials, or private employer code.
- Treat local model output as untrusted text. Never execute model-generated commands or code.
- Prompt-injection-like text in Terraform comments, names, or user-provided descriptions is untrusted input, not instructions to the application.
- When evidence is incomplete or ambiguous, say so clearly.
3. Architecture direction
Keep the architecture modular and small. Do not build one giant prompt that performs all analysis.
CLI
 |
 +--> Existing deterministic workflows
 |     plan loading / configuration inspection
 |     analyzers / rules / confidence / verification
 |     terminal / Markdown / JSON renderers
 |
 +--> Explicit optional AI explanation workflow
       allowlisted finding/evidence builder
       task-specific prompt template
       local Ollama adapter
       bounded response parser/validator
       AI explanation renderer (separate from findings)
Architecture rules
- Keep parsing, analysis, verification, presentation, persistence, and model integration independently testable.
- Keep raw Terraform values outside normalized findings and renderers.
- Keep AI disabled unless explicitly invoked or enabled by a clearly documented user action; ordinary commands must not contact a model.
- Phase 12 uses Ollama on the user's local machine only. Do not add cloud AI providers, hosted inference, telemetry, accounts, or a remote backend in this phase.
- Use an explicit, small model adapter so the deterministic core is not coupled to Ollama-specific response details. Do not build a generic multi-provider framework yet.
- Do not silently download models. Document how users install Ollama and pull a model themselves.
- Do not assume one model is installed. Check local Ollama availability and selected model, and provide a useful error if unavailable.
- Use a configurable model name with a documented default only after testing a candidate locally. Never claim a model is universally best.
- Keep prompts versioned/testable and task-specific. Build them from a strict allowlist of sanitized finding metadata.
- Do not pass raw plan JSON, state, full source trees, unrestricted HCL, or raw attribute values to the model as a convenience.
- Keep model output separate from deterministic findings. It must not change severity, confidence, status, rule IDs, or verification results.
- Bound request size, response size, and timeouts where the client/runtime supports them. Handle Ollama missing, unavailable, timeout, model-not-found, malformed-response, and empty-response cases gracefully.
- No agent loop, tool calling, shell access, filesystem access by the model, or autonomous execution in Phase 12.
- Future guided troubleshooting may add targeted project inspection and questioning, but only in a separately scoped phase with explicit user control and tests.
4. Current repository status
The following status reflects the latest user-reported progress. Re-run tests against the current local repository before relying on counts as current evidence.
Milestone	Status	Latest reported evidence
Phase 1 — Plan explainer	Complete	Plan actions and terminal/Markdown/JSON output
Phase 2 — Replacement analysis	Complete	Conservative evidence and confidence states
Phase 3 — Standards/security review	Complete	Configurable standards and selected security checks
Phase 4 — Fix proposals/verification	Complete	Reviewable diffs and explicit approval/verification outcomes
Phase 5 — Local history	Complete	Opt-in sanitized history, schema validation, corruption handling
Phase 6 — Packaging/release readiness	Complete	Console script, docs, CI checks
Phase 7 — Reliability hardening	Complete	Regression fixes and CLI smoke tests
Phase 8 — Install once, run from any project	Complete for local repository install	pipx install . and outside-repository smoke tests; PyPI release not established
Phase 9 — Configuration understanding	Complete	43 tests reported at phase close
Phase 10 — Import and permission assistance	Complete	52 tests reported at phase close
Phase 11 — Drift and upgrade assistance	Complete	58 tests reported; drift CLI terminal/Markdown/JSON smoke tests and git diff --check passed; AWS fixture validation unavailable because provider was not installed
Phase 12 — Optional local AI explanations	Complete	72 tests passed; explicit local-only Ollama adapter, conservative replacement-cause safeguards, allowlisted prompts, mocked CLI/output/failure coverage, and real `llama3.2` replacement/standards/drift smoke tests


Known scope boundaries
- TFWhy is a Python CLI, not yet a conversational application or editor extension.
- PyPI publication and installation remain unverified until a package is actually published.
- The repository is licensed under MIT; the project remains pre-1.0 and requires release review before publication.
- Terraform validate can require provider plugins; report provider-unavailable limitations accurately.
- Drift analysis does not perform cloud/state refresh and cannot reliably establish who caused a remote change.
- Current import generation and provider migration checks are bounded to implemented/tested cases.
- Do not market arbitrary Terraform diagnosis, automatic repair, perfect secret detection, or comprehensive provider coverage until demonstrated by tests.
5. Roadmap and phase gates
Only the active phase may introduce its planned feature set. Later phases can be refined after user feedback. Bug fixes and urgent security fixes are always allowed.
Phase 7 — Reliability hardening COMPLETE
Goal: Improve correctness of the existing MVP without expanding product scope.
Reported exit evidence: Fixed a public-ingress variable-default false negative with regression coverage; full suite reported 35 tests at phase close; review output smoke-tested. Later test discovery fixes were also reported.
Phase 8 — Install once, run from any Terraform project COMPLETE for local repository installation
Goal: Make the CLI usable outside its source repository.
Reported exit evidence: pipx install . from a local checkout and outside-repository CLI smoke tests passed. No PyPI package was available to test.
Phase 9 — Improve Terraform configuration understanding COMPLETE
Goal: Improve module-aware evidence linking and conservative tracing.
Reported exit evidence: 43 tests passed; compile checks and explain output-format smoke tests passed. Terraform validation of a fixture was blocked by a locally unavailable provider.
Phase 10 — Import and permission assistance COMPLETE
Goal: Add bounded import assistance and conservative permission findings.
Reported exit evidence: 52 tests passed; import/review CLI smoke tests and fixture formatting passed. AWS provider validation was unavailable locally.
Phase 11 — Drift and upgrade assistance COMPLETE
Goal: Explain supported drift and migration cases using user-generated plans/configuration.
Reported exit evidence: 58 tests passed; drift terminal/Markdown/JSON, explain JSON and review JSON smoke tests passed; git diff --check passed. No terraform init, apply, destroy, cloud access, or credentials used. AWS fixture validation was not completed because the provider was unavailable.
Phase 12 — Optional local AI explanations with Ollama COMPLETE
Goal: Make existing deterministic TFWhy findings easier to understand using an optional local language model, without weakening reliability, privacy, or safety.
Initial product scope: Explain findings already produced by TFWhy. Do not implement open-ended project diagnosis, guided cross-questioning, arbitrary code review, automatic fixes, cloud inference, or a chat UI in this phase.
User experience target
- Existing commands continue to work exactly as before without AI or Ollama.
- A user explicitly invokes an AI explanation for supported existing findings, using a CLI option/subcommand chosen after inspecting the current CLI conventions.
- TFWhy constructs the prompt; users do not need to write prompts themselves.
- AI explanation appears as a distinct section, clearly labelled as model-generated interpretation.
- Findings, severity, confidence, evidence, and verification results remain deterministic and unchanged.
Implementation tasks
- [x] Inspect the current code, CLI conventions, test suite, README, and Plan.md; rerun the 58-test baseline before coding.
- [x] Add a dependency-free standard-library HTTP adapter for only Ollama's loopback `POST /api/generate` endpoint; no multi-provider framework was added.
- [x] Add explicit `tfwhy ai-explain --kind {replacement,standards,drift} --finding ID --model MODEL` UX. `--model` is required, so TFWhy never selects or downloads a model silently.
- [x] Keep the adapter separate from deterministic analyzers and report renderers; no ordinary command enters the model call path.
- [x] Build strict, versioned allowlisted payloads. They omit raw values/plans/state/HCL, configuration files, credentials, environment variables, finding free text, addresses, filenames, and locations.
- [x] Use fixed standards-rule context and restrictive safe structural-path handling so prompt-injection-like plan/configuration text is excluded.
- [x] Require a task-specific JSON response that separates facts, interpretation, uncertainty, and conservative next steps; Unknown/Inconclusive findings prohibit certainty claims.
- [x] Bound request/response size, response sections, and timeout; label rendered output as untrusted local-model interpretation and never mutate deterministic results.
- [x] Handle absent Ollama, missing models, connection failure, timeout, empty/malformed/oversized replies, invalid model names, and ambiguous standards findings with safe errors.
- [x] Add mocked privacy, allowlist, injection-like input, uncertainty, malformed-response, failure, ambiguity, terminal/Markdown/JSON rendering, and ordinary-command no-contact tests.
- [x] Record that manual Ollama smoke testing was unavailable: `ollama` is not installed in this environment; no model was downloaded or tested.
- [x] Update README with explicit opt-in usage, local data flow, manual model installation/pull, timeout, resource guidance, privacy boundaries, and limitations.
- [x] Run full tests, compile checks, mocked CLI/output smoke tests, real unavailable-Ollama error smoke, and diff checks.
Phase 12 exclusions
- No cloud AI providers or hosted inference.
- No automatic model download.
- No telemetry, analytics, remote backend, user accounts, or central collection of prompts/responses.
- No raw plan/state/configuration passed wholesale to the model.
- No arbitrary tfwhy fix, open-ended diagnosis, cross-questioning, chat UI, IDE extension, model training/fine-tuning, or agent loop.
- No Terraform apply/destroy, cloud operations, or autonomous file edits.
Exit criteria
- AI is explicitly opt-in and local to Ollama; ordinary CLI behavior is unchanged when AI is unused.
- Only allowlisted sanitized finding metadata enters the model request.
- Model explanations are separate from deterministic findings and cannot override them.
- Uncertainty and unsupported evidence remain explicit.
- Failure cases produce clear errors and do not break non-AI workflows.
- Privacy/security regression tests, full test suite, compile checks, relevant CLI smoke tests, and diff checks pass.
- README and this plan accurately describe actual behavior and limitations.
- Any manual Ollama test is reported honestly; if Ollama cannot be tested, that limitation is recorded.
Reported exit evidence: The 2026-10-19 baseline passed 58 tests and the latest suite passed 72. `python3 -m compileall -q src tests` passed previously. Mocked CLI tests exercised terminal, Markdown, and JSON model renderers; real `llama3.2` smoke tests passed for replacement/terminal, standards/Markdown, and drift/JSON explanations. Missing-model guidance, likely replacement-cause overstatement safeguards, and privacy-safe resource summaries were fixed with regression coverage. No cloud call, Terraform apply/destroy, telemetry, or infrastructure operation was performed; the explicitly selected local model was downloaded by the user workflow.
Phase 13 — Public pilot and feedback FUTURE; AFTER PHASE 12
Goal: Distribute a usable local CLI, learn from real users, and prioritize improvements from evidence rather than assumptions.
- [ ] Prepare a release checklist and clear installation/troubleshooting instructions.
- [ ] Test with a small group first, then broaden distribution when critical issues are resolved.
- [ ] Invite voluntary, consent-based feedback. Do not add telemetry by default or upload users' Terraform code, plans, prompts, or secrets.
- [ ] Track issues users choose to report: installation failures, false positives/negatives, explanation quality, latency, model compatibility, and confusing UX.
- [ ] Establish a repeatable synthetic benchmark for deterministic findings and AI explanations.
- [ ] Review feedback regularly and fix reproducible bugs with regression tests.
- [ ] Use an initial two-to-three-month observation window as a planning target, not a deadline or proof of success.
Exit criteria: Real engineers outside the creator's immediate circle can install and use TFWhy; feedback identifies concrete improvements; repeat usage and trust are assessed without overclaiming product-market fit.
Phase 14 — Guided troubleshooting and fix assistance FUTURE; ONLY AFTER PILOT EVIDENCE
Goal: Let users describe a Terraform problem in ordinary language while TFWhy gathers relevant evidence and asks useful follow-up questions.
Potential CLI direction (illustrative; not implemented):
tfwhy fix "Find mistakes in my Terraform code"
- [ ] Define supported diagnostic intents and what evidence each needs.
- [ ] Inspect only relevant project files under an explicit project directory; do not silently traverse arbitrary filesystem locations.
- [ ] Run only documented safe checks; never run apply or destroy.
- [ ] Determine which facts can be gathered from files/tools before asking the user.
- [ ] Ask concise, targeted follow-up questions only when answers can materially change the diagnosis or proposed fix.
- [ ] Keep answers scoped to the current investigation; do not persist sensitive dialogue by default.
- [ ] Construct task-specific prompts from allowlisted evidence and user-provided answers.
- [ ] Separate confirmed findings, hypotheses, unknowns, and next steps.
- [ ] Generate reviewable diffs/proposals only for supported cases; require explicit approval for writes and never apply infrastructure changes.
- [ ] Add scenario-based regression tests, including multi-issue projects, ambiguous errors, malicious comments, secret markers, and insufficient context.
Exit criteria: Supported workflows are documented and tested; the tool asks questions only when useful, explains uncertainty, and never claims arbitrary Terraform can be safely repaired.
Phase 15 — CI and pull-request workflows FUTURE
Goal: Bring stable TFWhy findings into normal review workflows.
- [ ] Define stable machine-readable output and exit-code policy.
- [ ] Support CI usage without interactive prompts.
- [ ] Define configurable severity thresholds and failure behavior.
- [ ] Consider pull-request comments only after local output and finding IDs are stable.
- [ ] Ensure logs and artifacts do not leak secrets or raw plans.
- [ ] Test permissions, duplicate comments, provider failures, and noisy findings.
Exit criteria: CI behavior is predictable, configurable, documented, and makes no infrastructure changes.
Phase 16 — Business validation and future model strategy FUTURE; EVIDENCE-LED
Goal: Determine whether a paid/team product or custom model is justified by real demand.
- [ ] Interview target users and observe real workflows.
- [ ] Measure repeat usage, false-positive tolerance, trust, time saved, and willingness to pay.
- [ ] Identify a specific problem customers will pay to solve before building hosted infrastructure.
- [ ] Evaluate potential team features such as policy packs, shared reports, collaboration, and administration only when validated.
- [ ] Reassess data retention, access controls, tenant isolation, deletion, and security before any hosted offering.
- [ ] Consider remote AI providers or hosted inference only as explicit, separately consented options with clear data disclosure and cost controls.
- [ ] Consider fine-tuning or a custom model only if lawful, consented, high-quality training/evaluation data exists and measured results justify the compute and maintenance cost. Public use does not automatically grant permission to train on user code or sessions.
Exit criteria: Repeat usage and demand for a specific paid capability are demonstrated. Downloads and social engagement alone are not product-market fit. Custom model development is a separate evidence-based decision, not an assumed milestone.
6. Testing and release policy
Every phase and bug fix must follow this policy.
Required test layers
1. Unit tests for parsers, analyzers, models, formatters, and helpers.
2. Golden/fixture tests for known plans and configurations.
3. Regression tests for every reproducible bug fixed where practical.
4. Negative tests for malformed input, missing fields, unsupported versions, ambiguity, and failed external tools.
5. Privacy tests using synthetic secret markers across reports, logs, history, diffs, and AI payloads.
6. Integration tests with synthetic Terraform projects and Terraform-generated plans when available.
7. CLI smoke tests for affected commands, output formats, errors, and exit codes.
8. Packaging tests when installation/distribution changes.
9. Compatibility tests for declared platforms, Python versions, Terraform versions, and model/runtime combinations.
Standard completion checklist
- [ ] Inspect existing code and behavior before changing it.
- [ ] Reproduce the bug or define measurable acceptance criteria.
- [ ] Make the smallest effective change.
- [ ] Add focused tests, including regression tests for bugs fixed.
- [ ] Run relevant tests and the full suite.
- [ ] Run relevant CLI smoke tests.
- [ ] Review the diff for unrelated changes, secret leakage, unsafe file operations, and misleading claims.
- [ ] Update docs only when behavior or limitations change.
- [ ] Report actual commands and results; never claim tests ran if they did not.
- [ ] Report remaining limitations and anything that could not be tested.
If a test cannot run because Terraform, a provider plugin, or Ollama is unavailable, state that clearly. Mocked tests do not prove that the real executable works in that environment.
Bug-fix policy
Bugs are not restricted to the active roadmap phase. Reproduce and assess severity; fix critical security/privacy/destructive-action bugs immediately; fix reproducible correctness bugs with minimal patches and regression tests; run the relevant tests and full suite. If a safe fix is not possible, document impact, workaround, and reason for deferral. Do not leave a known serious bug merely because the roadmap points elsewhere.
7. Working with Copilot and ChatGPT
Use this instruction at the top of implementation prompts:
Treat Plan.md as the source of truth. Inspect the current repository and identify the active phase before coding. Work only on the requested task within that phase. Do not jump to future phases or add unrelated features. Fix reproducible bugs discovered along the way, add regression tests, run relevant tests and the full suite, and report actual results. Never claim unsupported behavior or test results. If the request conflicts with this plan, explain the conflict before changing code. Update Plan.md only when phase status, roadmap, constraints, or an architectural decision genuinely changes.

Copilot responsibilities
- Inspect the current repository and relevant tests first.
- Implement one bounded task at a time.
- Include implementation, tests, full-suite validation, relevant smoke tests, docs, and phase-plan updates in the same prompt where practical.
- Report files changed, bugs fixed, tests run/passed/failed, smoke-test results, and limitations.
- Do not mark a phase complete based solely on generated code; use exit criteria.
ChatGPT responsibilities
- Help interpret behavior, Terraform semantics, architecture trade-offs, test strategy, and results.
- Challenge unsupported root-cause claims and unsafe assumptions.
- Prepare concise, implementation-ready prompts.
- Respect the current phase and avoid unnecessary work.
- Do not request real credentials, production state, sensitive plan JSON, or private employer code.
User approval
The user owns the final decision to accept changes, commit them, release the product, or enable any behavior that writes files or sends data externally.
8. Early product validation measures
These are proposed targets, not current achievements.
- At least 10 people outside the creator's immediate circle try TFWhy.
- At least 3 users return to use it without prompting.
- Users can install and use it from their own Terraform project directory.
- Record false positives, false negatives, unsupported cases, local model compatibility, and response quality using synthetic tests and voluntary reports.
- Ask whether TFWhy changes a real decision, reduces investigation time, or improves user understanding.
- Do not collect user code, plan files, prompts, or diagnostic sessions by default.
- Use the results to choose the next improvement rather than assuming every planned feature should be built.
