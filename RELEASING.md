# Releasing TFWhy

This document is the release checklist for the free, local-first CLI. It assumes a clean working tree and does not publish anything automatically.

## Before Release

1. Review the intended version in `pyproject.toml`.
2. Confirm `Plan.md` and `README.md` describe actual behavior.
3. Run the complete test suite:

   ```bash
   python -m unittest discover -s tests -v
   ```

4. Check formatting and whitespace:

   ```bash
   terraform fmt -check -recursive tests/fixtures/corporate_project/infra
   git diff --check
   ```

5. Run the offline fixture without cloud credentials:

   ```bash
   terraform -chdir=tests/fixtures/corporate_project/infra init -backend=false
   terraform -chdir=tests/fixtures/corporate_project/infra validate
   terraform -chdir=tests/fixtures/corporate_project/infra plan -out=/tmp/tfwhy-release.tfplan
   terraform -chdir=tests/fixtures/corporate_project/infra show -json /tmp/tfwhy-release.tfplan > /tmp/tfwhy-release.json
   tfwhy explain /tmp/tfwhy-release.json --dir tests/fixtures/corporate_project/infra
   ```

6. Confirm no plan, state, credential, history, or virtual-environment files are staged.
7. Review the generated package metadata and console script in a clean environment.

## Local Package Smoke Test

For an unreleased checkout:

```bash
python3 -m venv /tmp/tfwhy-release-venv
/tmp/tfwhy-release-venv/bin/python -m pip install -e .
cd /tmp
/tmp/tfwhy-release-venv/bin/tfwhy --help
```

For an install-once local workflow:

```bash
pipx install .
tfwhy --help
```

The `pipx install tfwhy` command should only be used after a package has actually been published to PyPI.

## Publish Later

Publishing to PyPI requires a verified package account and an approved release version. Before publishing, build and inspect the artifacts with a trusted Python packaging workflow, upload only after review, and test installation from the published version in a clean environment.

TFWhy must remain local-first: publishing the package must not add telemetry, cloud access, automatic model downloads, or a requirement for AWS credentials.
