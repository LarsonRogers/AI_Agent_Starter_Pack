import tempfile
import unittest
from pathlib import Path

import run_evals
from run_evals import artifact_component, prepare_fixture


class RunEvalsTest(unittest.TestCase):
    def test_artifact_component_is_portable(self):
        self.assertEqual(artifact_component("qwen2.5-coder:7b"), "qwen2.5-coder_7b")
        self.assertEqual(artifact_component("org/model"), "org_model")
        self.assertEqual(artifact_component(":/"), "model")

    def test_prepare_fixture_excludes_runtime_caches(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = root / "fixture"
            fixture.mkdir()
            (fixture / "target.py").write_text("value = 1\n", encoding="utf-8")
            cache = fixture / "__pycache__"
            cache.mkdir()
            (cache / "target.pyc").write_bytes(b"cache")
            destination = root / "copy"
            previous = run_evals.EVAL_ROOT
            run_evals.EVAL_ROOT = root
            try:
                prepare_fixture({"fixture": "fixture"}, destination)
            finally:
                run_evals.EVAL_ROOT = previous
            self.assertTrue((destination / "target.py").is_file())
            self.assertFalse((destination / "__pycache__").exists())


if __name__ == "__main__":
    unittest.main()
