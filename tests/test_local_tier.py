import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from delegate import record_metric
from local_tier_common import ConfigError, parse_env_file, validate_loopback_url


class LocalTierTest(unittest.TestCase):
    def test_config_is_parsed_as_data(self):
        with tempfile.TemporaryDirectory() as temporary:
            marker = Path(temporary) / "executed"
            config = Path(temporary) / "local-tier.env"
            config.write_text(
                f"LOCAL_TIER_URL=http://127.0.0.1:8080\n"
                f"LOCAL_TIER_API_KEY=$(touch {marker})\n",
                encoding="utf-8",
            )
            values = parse_env_file(config)
            self.assertEqual(values["LOCAL_TIER_API_KEY"], f"$(touch {marker})")
            self.assertFalse(marker.exists())

    def test_unknown_config_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / "local-tier.env"
            config.write_text("UNEXPECTED=value\n", encoding="utf-8")
            with self.assertRaises(ConfigError):
                parse_env_file(config)

    def test_remote_and_embedded_credentials_are_rejected(self):
        for url in (
            "https://example.com",
            "http://example.com:8080",
            "http://localhost:8080",
            "http://user:key@127.0.0.1:8080",
        ):
            with self.subTest(url=url), self.assertRaises(ConfigError):
                validate_loopback_url(url)

    def test_metrics_are_valid_json_for_untrusted_labels(self):
        with tempfile.TemporaryDirectory() as temporary:
            metrics = Path(temporary) / "metrics.jsonl"
            record_metric(metrics, 'task"id', 'model\nname', "ok", {}, 5)
            record = json.loads(metrics.read_text(encoding="utf-8"))
        self.assertEqual(record["task_id"], 'task"id')
        self.assertEqual(record["model"], "model\nname")


if __name__ == "__main__":
    unittest.main()
