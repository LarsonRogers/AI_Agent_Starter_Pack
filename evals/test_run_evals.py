import tempfile
import unittest
from pathlib import Path

import run_evals
from run_evals import artifact_component, kit_prompt_for, prepare_fixture


class RunEvalsTest(unittest.TestCase):
    def test_artifact_component_is_portable(self):
        self.assertEqual(artifact_component("qwen2.5-coder:7b"), "qwen2.5-coder_7b")
        self.assertEqual(artifact_component("org/model"), "org_model")
        self.assertEqual(artifact_component(":/"), "model")

    def test_kit_prompt_micro_uses_task_class_slice(self):
        path, profile = kit_prompt_for("micro", {"task_class": "landing"})
        self.assertEqual(profile, "micro-landing")
        self.assertEqual(path.name, "fablized-micro-landing.md")
        self.assertTrue(path.is_file())

    def test_kit_prompt_without_task_class_keeps_profile(self):
        path, profile = kit_prompt_for("micro", {})
        self.assertEqual(profile, "micro")
        self.assertEqual(path, run_evals.PROMPTS["micro"])

    def test_kit_prompt_slice_applies_only_to_micro_profile(self):
        path, profile = kit_prompt_for("full", {"task_class": "landing"})
        self.assertEqual(profile, "full")
        self.assertEqual(path, run_evals.PROMPTS["full"])

    def test_kit_prompt_unknown_task_class_keeps_profile(self):
        path, profile = kit_prompt_for("micro", {"task_class": "nonsense"})
        self.assertEqual(profile, "micro")
        self.assertEqual(path, run_evals.PROMPTS["micro"])

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
