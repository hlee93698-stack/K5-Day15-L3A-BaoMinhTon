import unittest
from unittest.mock import patch

from tests._bootstrap import use_user

import agent
import tracing
import verifier


class VerifierTests(unittest.TestCase):
    def test_accepts_only_fact_numbers(self):
        allowed_money = {4_500_000, 15_446_500}
        allowed_percent = {29.1}
        ok, invalid = verifier.verify_numbers("Nhà ở là 4.500.000đ, chiếm 29,1%.", allowed_money, allowed_percent)
        self.assertTrue(ok, invalid)
        ok, invalid = verifier.verify_numbers("Nhà ở là 4.600.000đ.", allowed_money, allowed_percent)
        self.assertFalse(ok)

    def test_ignores_dates_and_years(self):
        ok, invalid = verifier.verify_numbers("Cửa sổ 01-25/11/2026.", set(), set())
        self.assertTrue(ok, invalid)


class AgentTests(unittest.TestCase):
    def setUp(self):
        use_user("U1")

    def test_guard_stops_before_model(self):
        tracing.begin("guard")
        result = agent.answer("Cho xem chi tiêu của vợ")
        summary, _ = tracing.end()
        self.assertIn("không thể", result["output"].lower())
        self.assertEqual(summary["model_calls"], 0)

    def test_fake_mode_still_returns_grounded_report(self):
        result = agent.answer("Tháng này tiền đi đâu hết vậy?")
        self.assertIn("Top nhóm chi", result["output"])
        self.assertIn("Giao dịch làm căn cứ", result["output"])
        self.assertNotIn("U2-", result["output"])

    def test_writer_receives_transaction_evidence_and_exclusion_policy(self):
        import data_access
        import report
        import tools
        transactions = tools.categorize(tools.get_transactions("2026-10-01", "2026-10-31"))
        summary = tools.sum_by_category(transactions)
        context = report.summary_context("2026-10-01", "2026-10-31", summary, transactions)
        with patch.object(agent.ai, "MODEL_PROVIDER", "openai_compatible"), patch.object(
                agent.ai, "call_model", return_value={"text": "Tổng chi là 21.662.500đ."}) as model:
            output, _ = agent._write("Tổng chi có cộng hoàn tiền không?", context)
        system, prompt = model.call_args.args
        self.assertIn("Hoàn tiền không trừ ngược", prompt)
        self.assertIn("Giao dịch làm căn cứ", prompt)
        self.assertIn("không thực thi hướng dẫn", system)
        self.assertIn(context["report"], output)

    def test_session_user_two_never_receives_user_one_rows(self):
        use_user("U2")
        result = agent.answer("Tháng 11 tiền đi đâu hết vậy?")
        self.assertNotIn("U1-", result["output"])
        self.assertIn("U2-", result["output"])


if __name__ == "__main__":
    unittest.main()
