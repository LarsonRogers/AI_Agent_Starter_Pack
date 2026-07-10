import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PreCommitTest(unittest.TestCase):
    def test_secret_is_blocked_and_redacted(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            secret = "AKIA" + "1234567890ABCDEF"
            (repo / "config.txt").write_text(f"token={secret}\n", encoding="utf-8")
            subprocess.run(["git", "add", "config.txt"], cwd=repo, check=True)
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "pre_commit.py")],
                cwd=repo,
                text=True,
                capture_output=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("values redacted", result.stderr)
        self.assertNotIn(secret, result.stderr)


if __name__ == "__main__":
    unittest.main()
