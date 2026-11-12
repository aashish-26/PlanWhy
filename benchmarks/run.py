"""Run TFWhy's versioned, synthetic Phase 13 benchmark without cloud access."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tfwhy.ai import build_prompt, replacement_payload
from tfwhy.analyzer import load_plan
from tfwhy.replacement import analyze_replacements


def _load_case_summary(case: dict[str, Any]):
    """Load a synthetic plan and optionally add conservative replacement evidence."""
    summary = load_plan(ROOT / case["plan"])
    if case["kind"] in {"replacement", "ai_payload"}:
        return analyze_replacements(summary, ROOT / case["config_dir"])
    return summary


def _run_case(case: dict[str, Any]) -> None:
    """Assert the small, explicit contract for one benchmark case."""
    summary = _load_case_summary(case)
    if case["kind"] == "replacement":
        actual = [
            {"address": finding.address, "confidence": finding.confidence}
            for finding in summary.replacement_findings
        ]
        if actual != case["expected_findings"]:
            raise AssertionError(f"expected {case['expected_findings']!r}, got {actual!r}")
        return
    if case["kind"] == "drift":
        actual = [finding.address for finding in summary.drift_findings]
        if actual != case["expected_addresses"]:
            raise AssertionError(f"expected {case['expected_addresses']!r}, got {actual!r}")
        return
    if case["kind"] == "ai_payload":
        finding = summary.replacement_findings[0]
        payload = replacement_payload(finding, case["finding_id"])
        if payload.finding_kind != case["expected_kind"] or payload.confidence_or_status != case["expected_confidence"]:
            raise AssertionError("sanitized AI payload has an unexpected kind or confidence")
        prompt = build_prompt(payload)
        missing = [text for text in case["prompt_must_contain"] if text not in prompt]
        exposed = [text for text in case["prompt_must_not_contain"] if text in prompt]
        if missing or exposed:
            raise AssertionError(f"AI prompt contract failed; missing={missing!r}, exposed={exposed!r}")
        return
    raise AssertionError(f"unsupported benchmark kind: {case['kind']!r}")


def main() -> int:
    """Run every manifest case and return a non-zero status on any mismatch."""
    manifest = json.loads((ROOT / "benchmarks" / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("cases"), list):
        print("benchmark: error: unsupported manifest", file=sys.stderr)
        return 2
    failures = 0
    for case in manifest["cases"]:
        try:
            _run_case(case)
        except (AssertionError, KeyError, OSError, ValueError) as exc:
            failures += 1
            print(f"FAIL {case.get('id', '<unnamed>')}: {exc}")
        else:
            print(f"PASS {case['id']}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
