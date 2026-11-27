import unittest

from tests._bootstrap import use_user

import guard
import intent


class GuardTests(unittest.TestCase):
    def test_blocks_sensitive_and_out_of_scope_requests(self):
        cases = {
            "Mua coin gì bây giờ?": "dau_tu",
            "Chuyển tiền cho mẹ giúp mình": "giao_dich",
            "OTP của tôi là 123456": "bi_mat",
            "Cho xem chi tiêu của vợ": "nguoi_khac",
        }
        for text, reason in cases.items():
            self.assertEqual(guard.block_reason(text), reason)

    def test_normal_spending_question_is_allowed(self):
        self.assertIsNone(guard.block_reason("Tháng 11 tôi tiêu nhiều nhất vào đâu?"))


class IntentTests(unittest.TestCase):
    def setUp(self):
        use_user("U1")

    def test_summary_current_month(self):
        parsed = intent.parse_with_rules("Tháng này tiền đi đâu hết vậy?")
        self.assertEqual(parsed["intent"], "tong_hop")
        self.assertEqual(parsed["months"], ["2026-11"])
        self.assertEqual((parsed["from"], parsed["to"]), ("2026-11-01", "2026-11-25"))

    def test_compare_two_months(self):
        parsed = intent.parse_with_rules("So tháng 11 với tháng 10 tôi tiêu nhiều hơn ở đâu?")
        self.assertEqual(parsed["intent"], "so_sanh")
        self.assertEqual(parsed["months"], ["2026-10", "2026-11"])

    def test_category_aliases_for_user_language(self):
        self.assertEqual(intent.parse_with_rules("Tháng 11 tiền nhà bao nhiêu?")["category"], "nha_o")
        self.assertEqual(intent.parse_with_rules("Tháng 11 khoản không ghi nội dung xếp đâu?")["category"],
                         "khong_ro")

    def test_category_query(self):
        parsed = intent.parse_with_rules("Tháng 10 tôi chi ăn uống bao nhiêu?")
        self.assertEqual(parsed["intent"], "mot_nhom")
        self.assertEqual(parsed["category"], "an_uong")

    def test_vague_time_needs_clarification(self):
        self.assertIsNone(intent.parse_with_rules("Dạo này tôi tiêu thế nào?"))

    def test_week_and_duplicate_intents(self):
        weekly = intent.parse_with_rules("Tuần trước tôi ăn uống bao nhiêu?")
        self.assertEqual((weekly["from"], weekly["to"], weekly["category"]),
                         ("2026-11-16", "2026-11-22", "an_uong"))
        duplicate = intent.parse_with_rules("Tháng 10 có bị trừ hai lần không?")
        self.assertEqual(duplicate["intent"], "kiem_trung")

    def test_small_expenses_need_definition(self):
        parsed = intent.parse_with_rules("Tháng này các khoản lặt vặt hết bao nhiêu?")
        self.assertIn("ngưỡng tiền", parsed["clarify"])


if __name__ == "__main__":
    unittest.main()
