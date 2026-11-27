import unittest

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

    def test_session_user_two_never_receives_user_one_rows(self):
        use_user("U2")
        result = agent.answer("Tháng 11 tiền đi đâu hết vậy?")
        self.assertNotIn("U1-", result["output"])
        self.assertIn("U2-", result["output"])


if __name__ == "__main__":
    unittest.main()
