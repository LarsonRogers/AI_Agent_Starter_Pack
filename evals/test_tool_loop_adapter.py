import tempfile
import unittest
from pathlib import Path

from tool_loop_adapter import confine, execute, final_result_event, run_shell


class ConfinementTest(unittest.TestCase):
    def setUp(self):
        self._temporary = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary.name).resolve()
        self.addCleanup(self._temporary.cleanup)

    def test_confine_allows_inside_and_blocks_escape(self):
        self.assertEqual(confine(self.root, "sub/file.py"), self.root / "sub" / "file.py")
        for escape in ("../outside.py", "sub/../../outside.py", "C:/Windows/hosts"):
            with self.assertRaises(ValueError):
                confine(self.root, escape)

    def test_shell_allowlist_and_path_arguments(self):
        self.assertIn("not allowed: curl", run_shell(self.root, "curl http://example.com"))
        self.assertIn("path argument not allowed", run_shell(self.root, "cat ../secrets.txt"))
        self.assertIn("path argument not allowed", run_shell(self.root, "cat /etc/passwd"))
        result = run_shell(self.root, "python -c \"print('ok')\"")
        self.assertIn("exit=0", result)
        self.assertIn("ok", result)

    def test_replace_text_requires_unique_span(self):
        target = self.root / "module.py"
        target.write_text("a = 1\na = 1\n", encoding="utf-8")
        result = execute(self.root, "replace_text", {
            "path": "module.py", "old_text": "a = 1", "new_text": "a = 2",
        })
        self.assertIn("exactly once", result)
        self.assertEqual(target.read_text(encoding="utf-8"), "a = 1\na = 1\n")

    def test_execute_reports_errors_instead_of_raising(self):
        self.assertIn("error:", execute(self.root, "read_file", {"path": "missing.py"}))
        self.assertIn("error: unknown tool", execute(self.root, "launch_missiles", {}))

    def test_final_result_event_keeps_diagnostics_on_empty_content(self):
        event = final_result_event(
            {"content": "", "reasoning_content": "x" * 3000}, "stop"
        )
        self.assertEqual(event["result"], "")
        self.assertEqual(event["finish_reason"], "stop")
        self.assertEqual(event["reasoning_chars"], 3000)
        self.assertEqual(event["content_type"], "str")
        self.assertEqual(len(event["reasoning_tail"]), 2000)

    def test_final_result_event_plain_on_nonempty_content(self):
        event = final_result_event(
            {"content": "LANDING AUDIT", "reasoning_content": "thinking"}, "stop"
        )
        self.assertEqual(event["result"], "LANDING AUDIT")
        self.assertNotIn("reasoning_tail", event)
        self.assertNotIn("content_type", event)


if __name__ == "__main__":
    unittest.main()
