import copy
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import refresh_research_data as research_data  # noqa: E402


class SubmissionEvidenceTests(unittest.TestCase):
    def test_clarified_repeat_caption_stays_with_the_initial_30_items(self):
        text = (ROOT / "experiments/model-selection.md").read_text()
        text = text.replace(
            "**반복 n=3(1차 골든, 조용한 GPU)",
            "**초기 30문장 반복 n=3(검수 22문장과 별도, 조용한 GPU)",
        )
        repeat = research_data.parse_embedding(text)["repeat_check"]
        self.assertEqual(repeat["items"], 30)
        self.assertEqual(repeat["repetitions"], 3)
        self.assertFalse(repeat["applies_to_reviewed_table"])

    def test_equal_lengths_do_not_become_verified_identical_content(self):
        text = (ROOT / "experiments/human-observations.md").read_text()
        tester = research_data.parse_human_observations(text)["tester6"]

        self.assertEqual(tester["equal_length_rounds"], [3, 4, 5])
        self.assertEqual(tester["submission_length"], 266)
        self.assertFalse(tester["content_identity_verified"])
        self.assertEqual(tester["monotonic_scoring_lock"], "conditional")
        self.assertNotIn("same_text_rounds", tester)


class ResearchDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = research_data.build_dataset(ROOT)

    def test_reviewed_embedding_figure_uses_only_the_22_item_source(self):
        embedding = self.dataset["model_selection"]["embedding"]

        self.assertEqual(embedding["reviewed_items"], 22)
        self.assertNotIn("repetitions", embedding)
        self.assertEqual(
            [(item["id"], item["top1_correct"], item["latency_p50_ms"]) for item in embedding["conditions"]],
            [
                ("stem", 8, 0),
                ("qwen-2560", 20, 86),
                ("qwen-1536", 18, 84),
                ("bge-1024", 20, 109),
                ("gemini-1536", 21, 418),
                ("gemini-2560", 21, 407),
            ],
        )

    def test_embedding_repeat_check_is_scoped_to_unreviewed_30_item_source(self):
        repeat_check = self.dataset["model_selection"]["embedding"]["repeat_check"]

        self.assertEqual(
            repeat_check,
            {
                "items": 30,
                "review_status": "unreviewed",
                "repetitions": 3,
                "applies_to_reviewed_table": False,
            },
        )

    def test_reviewed_embedding_table_rejects_changed_column_meaning(self):
        marker = "#### 6. 정본 수치 — Scenario Director 검수 골든(22문장)"
        original_header = "| 셀 | dims | top-1 | top-3 | p50 ms | top-1 오답 |"
        changed_headers = (
            "| 셀 | dims | top-1 | top-3 | p95 ms | top-1 오답 |",
            "| 셀 | dims | top-3 | top-1 | p50 ms | top-1 오답 |",
        )

        for changed_header in changed_headers:
            with self.subTest(header=changed_header), tempfile.TemporaryDirectory() as temp_dir:
                temp_root = Path(temp_dir)
                for relative_path in research_data.SOURCE_PATHS:
                    source = ROOT / relative_path
                    target = temp_root / relative_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)

                model_path = temp_root / "experiments" / "model-selection.md"
                model = model_path.read_text(encoding="utf-8")
                marker_at = model.index(marker)
                before, reviewed = model[:marker_at], model[marker_at:]
                self.assertIn(original_header, reviewed)
                model_path.write_text(
                    before + reviewed.replace(original_header, changed_header, 1),
                    encoding="utf-8",
                )

                with self.assertRaisesRegex(research_data.SourceError, "reviewed embedding table header"):
                    research_data.build_dataset(temp_root)

    def test_public_dates_and_plain_language_stage_labels_are_derived(self):
        self.assertEqual(self.dataset["model_selection"]["embedding"]["measured_on"], "2026-09-18")
        self.assertEqual(self.dataset["human_observations"]["aggregate"]["measured_on"], "2026-09-15")
        self.assertEqual(self.dataset["human_observations"]["tester6"]["measured_on"], "2026-09-16")
        self.assertEqual(
            [stage["label"] for stage in self.dataset["model_selection"]["stages"]],
            [
                "응답 형식 확인",
                "기본 동작 확인",
                "역할별 정식 평가",
                "메모리에 함께 올리기",
                "실제 게임 실행",
            ],
        )

    def test_rendered_numeric_copy_follows_refreshed_source_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir) / "site"
            shutil.copytree(
                ROOT,
                temp_root,
                ignore=shutil.ignore_patterns(".git", "_site", ".jekyll-cache", "artwork", "docs"),
            )

            human_path = temp_root / "experiments" / "human-observations.md"
            human = human_path.read_text(encoding="utf-8")
            human = human.replace(
                "원숭이손 수락 6 + AI 추천 옵션 선택 8",
                "원숭이손 수락 5 + AI 추천 옵션 선택 9",
                1,
            ).replace("| 2 | 64.2 |", "| 2 | 63.2 |", 1)
            human_path.write_text(human, encoding="utf-8")

            model_path = temp_root / "experiments" / "model-selection.md"
            model = model_path.read_text(encoding="utf-8")
            old_row = "| gemini-embedding-001 | **2560** | **0.955** | 1.000 | 407 |"
            new_row = "| gemini-embedding-001 | **2560** | **0.909** | 1.000 | 407 |"
            self.assertIn(old_row, model)
            model_path.write_text(model.replace(old_row, new_row, 1), encoding="utf-8")

            subprocess.run(
                [sys.executable, str(temp_root / "scripts" / "refresh_research_data.py")],
                cwd=temp_root,
                check=True,
                capture_output=True,
                text=True,
            )
            destination = Path(temp_dir) / "built"
            completed = subprocess.run(
                ["bundle", "exec", "jekyll", "build", "--source", str(temp_root), "--destination", str(destination)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)

            human_html = (destination / "experiments" / "human-observations" / "index.html").read_text()
            self.assertIn(
                'aria-label="AI 개입 수락 5회, AI 추천 선택 9회, 직접 작성 6회"',
                human_html,
            )
            self.assertIn("8.8점, 63.2점, 94.2점, 94.2점, 94.2점", human_html)

            model_html = (destination / "experiments" / "model-selection" / "index.html").read_text()
            gemini_2560 = re.search(
                r'<div class="metric-row">\s*<strong>Gemini</strong>.*?벡터 2560차원.*?</div>',
                model_html,
                re.DOTALL,
            )
            self.assertIsNotNone(gemini_2560)
            self.assertIn('aria-label="Gemini 벡터 2560차원: 첫 추천 적중 20/22"', gemini_2560.group(0))

    def test_check_mode_detects_public_source_drift(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "research_figures.json"
            output.write_text(
                json.dumps(self.dataset, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            changed = copy.deepcopy(self.dataset)
            changed["sources"][0]["sha256"] = "0" * 64

            errors = research_data.validate_dataset(changed, ROOT, expected=self.dataset)

        self.assertTrue(any("source drift" in error for error in errors), errors)

    def test_unmeasured_preregistration_cannot_gain_a_numeric_result(self):
        changed = copy.deepcopy(self.dataset)
        changed["preregistration"]["result"] = {"acceptance_rate_delta": 0}

        errors = research_data.validate_dataset(changed, ROOT)

        self.assertTrue(any("NOT RUN" in error for error in errors), errors)

    def test_tester6_must_remain_separate_from_the_six_session_aggregate(self):
        changed = copy.deepcopy(self.dataset)
        changed["human_observations"]["tester6"]["group"] = "six-session-aggregate"

        errors = research_data.validate_dataset(changed, ROOT)

        self.assertTrue(any("Tester 6" in error and "separate" in error for error in errors), errors)

    def test_selection_counts_must_match_the_source_denominator(self):
        changed = copy.deepcopy(self.dataset)
        changed["human_observations"]["aggregate"]["denominator"] = 21

        errors = research_data.validate_dataset(changed, ROOT)

        self.assertTrue(any("denominator" in error for error in errors), errors)

    def test_checked_artifact_matches_current_public_sources(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "refresh_research_data.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)


if __name__ == "__main__":
    unittest.main()
