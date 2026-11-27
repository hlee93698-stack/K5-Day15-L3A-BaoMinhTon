import csv
import os
import tempfile
import unittest
from pathlib import Path

from tests._bootstrap import ROOT, use_user

import tools
import report


class ToolTests(unittest.TestCase):
    def setUp(self):
        use_user("U1")
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["OVERRIDES_PATH"] = str(Path(self.tmp.name) / "overrides.json")

    def tearDown(self):
        self.tmp.cleanup()
        os.environ.pop("OVERRIDES_PATH", None)

    def test_summary_matches_seed_truth_for_rule_covered_month(self):
        txs = tools.get_transactions("2026-09-01", "2026-09-30")
        summary = tools.sum_by_category(tools.categorize(txs))
        truth = {}
        truth_total = None
        with open(ROOT / "data" / "summary_truth.csv", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row["user_id"] == "U1" and row["thang"] == "2026-09":
                    truth[row["nhom"]] = int(row["tong_tien"])
                    truth_total = int(row["tong_chi_thang"])
        actual = {row["nhom"]: row["tong_tien"] for row in summary["nhom"]}
        self.assertEqual(summary["tong_chi"], truth_total)
        self.assertEqual(actual, truth)

    def test_total_excludes_income_refund_and_card_payment(self):
        txs = tools.get_transactions("2026-10-01", "2026-10-31")
        summary = tools.sum_by_category(tools.categorize(txs))
        self.assertEqual(summary["tong_chi"], 21_662_500)
        self.assertEqual(summary["khong_tinh"], {
            "thu_nhap": 15_000_000, "hoan_tien": 450_000, "noi_bo": 5_181_500,
        })
        self.assertAlmostEqual(sum(row["phan_tram"] for row in summary["nhom"]), 100.0,
                               delta=0.1 * len(summary["nhom"]))

    def test_transaction_prompt_injection_is_data_not_instruction(self):
        txs = tools.get_transactions("2026-11-01", "2026-11-25")
        summary = tools.sum_by_category(tools.categorize(txs))
        injection = next(row for row in tools.categorize(txs) if row["tx_id"] == "U1-BA-0037")
        self.assertEqual(summary["tong_chi"], 28_845_500)
        self.assertEqual(injection["category"], "khong_ro")
        self.assertEqual(injection["amount"], 200_000)

    def test_compare_uses_same_day_window(self):
        combined = tools.categorize(tools.get_transactions("2026-10-01", "2026-11-25"))
        october = [row for row in combined if "2026-10-01" <= row["date"] <= "2026-10-25"]
        november = [row for row in combined if row["date"] >= "2026-11-01"]
        result = tools.compare_months(october, november, "01-25")
        self.assertEqual(result["cua_so"], "01-25")
        self.assertEqual(result["thang_1"]["tong_chi"], 20_970_500)
        self.assertEqual(result["thang_2"]["tong_chi"], 28_845_500)

    def test_code_report_contains_total_unknown_and_exclusions(self):
        txs = tools.get_transactions("2026-11-01", "2026-11-25")
        categorized = tools.categorize(txs)
        summary = tools.sum_by_category(categorized)
        output = report.summary_context("2026-11-01", "2026-11-25", summary, categorized)["report"]
        self.assertIn("28.845.500đ", output)
        self.assertIn("Khoản không rõ · 2.113.000đ", output)
        self.assertIn("noi_bo: 4.722.500đ", output)
        self.assertIn("DIEN MAY SAO BANG LAPTOP", output)

    def test_comparison_report_has_directional_total_delta(self):
        combined = tools.categorize(tools.get_transactions("2026-10-01", "2026-11-25"))
        result = tools.compare_months(
            [row for row in combined if "2026-10-01" <= row["date"] <= "2026-10-25"],
            [row for row in combined if row["date"] >= "2026-11-01"], "01-25")
        output = report.comparison_context(result)["report"]
        self.assertIn("Chênh lệch tổng: **+7.875.000đ**", output)
        self.assertIn("mua_sam | 2.138.000đ | 15.094.000đ | +12.956.000đ", output)

    def test_find_duplicates_returns_only_seed_pair(self):
        rows = tools.categorize(tools.get_transactions("2026-09-01", "2026-11-25"))
        found = tools.find_duplicates(rows)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["tx_ids"], ["U1-CC-0040", "U1-CC-0041"])
        self.assertEqual(found[0]["so_tien"], 45_000)

    def test_update_category_is_scoped_to_current_user(self):
        result = tools.update_category("U1-BA-0002", "giao_duc")
        self.assertEqual(result["moi"], "giao_duc")
        with self.assertRaises(ValueError):
            tools.update_category("U2-BA-0001", "giao_duc")


if __name__ == "__main__":
    unittest.main()
