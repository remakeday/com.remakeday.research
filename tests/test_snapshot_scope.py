"""The public filter must not publish an explicitly excluded source appendix."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from snapshot_model_eval import apply_rules


class SnapshotScopeTests(unittest.TestCase):
    def test_excluded_section_keeps_following_peer_and_ignores_fenced_headings(self):
        source = """## Results
public evidence
### Private appendix
private example
#### Nested details
private table
```text
## Looks like a heading
```
### Next public appendix
public follow-up
"""
        rules = {"drop_line_prefixes": [], "replace": [],
                 "drop_section_prefixes": ["### Private appendix"]}
        self.assertEqual(apply_rules(source, rules), """## Results
public evidence
### Next public appendix
public follow-up
""")

    def test_excluded_final_section_does_not_leak_its_body(self):
        rules = {"drop_line_prefixes": [], "replace": [],
                 "drop_section_prefixes": ["### Not for publication"]}
        self.assertEqual(apply_rules("public\n### Not for publication\nprivate\n", rules), "public")

    def test_changed_exclusion_heading_stops_generation(self):
        rules = {"drop_line_prefixes": [], "replace": [],
                 "drop_section_prefixes": ["### Private appendix"]}
        with self.assertRaisesRegex(ValueError, "section exclusion did not match"):
            apply_rules("### Renamed appendix\nprivate content", rules)

    def test_legacy_line_filter_and_replacement_still_work_without_section_rules(self):
        rules = {"drop_line_prefixes": ["internal:"], "replace": [["old label", "public label"]]}
        self.assertEqual(apply_rules("## Evidence\ninternal: value\nold label\n", rules),
                         "## Evidence\npublic label\n")


if __name__ == "__main__":
    unittest.main()
