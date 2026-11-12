"""Keep the public synthetic benchmark executable as part of the test suite."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class BenchmarkTests(unittest.TestCase):
    def test_versioned_synthetic_benchmark_passes(self):
        result = subprocess.run(
            [sys.executable, "-B", "benchmarks/run.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("PASS replacement-likely-pattern", result.stdout)
        self.assertIn("PASS replacement-ai-allowlist", result.stdout)


if __name__ == "__main__":
    unittest.main()
