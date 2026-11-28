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

    def test_crypto_slang_is_investment(self):
        for text in ("ÔI giá Bít Coi đẹp quá, tôi có nên DCA không", "Ooi giá ETH", "Giá BTC hiện tại là bao nhiêu"):
            self.assertEqual(guard.block_reason(text), "dau_tu", text)

    def test_off_topic_without_spending_signal(self):
        for text in ("Thời tiết ngày mai tại Hà Nội ntn", "Hôm nay ăn gì ngon", "Kể chuyện cười đi",
                     "Chỉ tôi cách nấu phở", "Chị ơi hôm nay đẹp trời", "1 + 1 bằng mấy"):
            self.assertFalse(guard.in_scope(text), text)

    def test_spending_signals_with_or_without_accents(self):
        for text in ("Tháng 10 tôi tiêu bao nhiêu?", "thang 10 chi bao nhieu", "Hôm qua xài hết nhiêu",
                     "Tháng này tiền đi đâu hết vậy?", "Có bị trừ hai lần không?"):
            self.assertTrue(guard.in_scope(text), text)
        self.assertTrue(guard.in_scope("Tháng 9 uống cafe", has_topic=True))


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

    def _span(self, text):
        parsed = intent.parse_with_rules(text)
        self.assertIsNotNone(parsed, text)
        return parsed["from"], parsed["to"]

    def test_week_of_month(self):
        self.assertEqual(self._span("Tuần đầu tiên của tháng 9 tôi đã tiêu hết bao nhiêu tiền"),
                         ("2026-09-01", "2026-09-07"))
        self.assertEqual(self._span("Tuần thứ 2 tháng 10 ăn uống bao nhiêu?"), ("2026-10-08", "2026-10-14"))
        self.assertEqual(self._span("Tuần cuối tháng 10 tiêu bao nhiêu?"), ("2026-10-25", "2026-10-31"))
        self.assertEqual(self._span("Tuần cuối tháng này"), ("2026-11-24", "2026-11-25"))

    def test_explicit_dates(self):
        self.assertEqual(self._span("Từ 5/9 đến 12/9 tiêu bao nhiêu?"), ("2026-09-05", "2026-09-12"))
        self.assertEqual(self._span("Từ ngày 5 đến ngày 12 tháng 9"), ("2026-09-05", "2026-09-12"))
        self.assertEqual(self._span("Ngày 16/11 tiêu gì?"), ("2026-11-16", "2026-11-16"))
        self.assertEqual(self._span("Từ 20/11 đến nay"), ("2026-11-20", "2026-11-25"))
        cross = intent.parse_with_rules("Từ ngày 25 tháng 9 đến ngày 5 tháng 10 tiêu bao nhiêu?")
        self.assertEqual((cross["intent"], cross["from"], cross["to"]), ("tong_hop", "2026-09-25", "2026-10-05"))

    def test_relative_and_partial_month(self):
        self.assertEqual(self._span("Hôm qua tiêu bao nhiêu?"), ("2026-11-24", "2026-11-24"))
        self.assertEqual(self._span("10 ngày gần đây tiêu bao nhiêu?"), ("2026-11-16", "2026-11-25"))
        self.assertEqual(self._span("Hai tuần qua ăn uống bao nhiêu?"), ("2026-11-12", "2026-11-25"))
        self.assertEqual(self._span("3 tháng qua tiêu bao nhiêu?"), ("2026-09-01", "2026-11-25"))
        self.assertEqual(self._span("Nửa đầu tháng 11"), ("2026-11-01", "2026-11-15"))
        self.assertEqual(self._span("10 ngày đầu tháng 9"), ("2026-09-01", "2026-09-10"))
        self.assertEqual(self._span("Từ đầu tháng đến nay"), ("2026-11-01", "2026-11-25"))

    def test_specific_days_and_weekdays(self):
        self.assertEqual(self._span("Ngày mùng 1 tháng 10 chi gì?"), ("2026-10-01", "2026-10-01"))
        self.assertEqual(self._span("Ngày 15 tháng trước tiêu gì?"), ("2026-10-15", "2026-10-15"))
        self.assertEqual(self._span("Ngày 05.09 tiêu gì?"), ("2026-09-05", "2026-09-05"))
        self.assertEqual(self._span("Ngày 28 tiêu gì?"), ("2026-10-28", "2026-10-28"))
        self.assertEqual(self._span("Chủ nhật tuần trước tiêu gì?"), ("2026-11-22", "2026-11-22"))
        self.assertEqual(self._span("Thứ 7 vừa rồi tiêu bao nhiêu?"), ("2026-11-21", "2026-11-21"))
        self.assertEqual(self._span("Cuối tuần trước tiêu bao nhiêu?"), ("2026-11-21", "2026-11-22"))
        self.assertEqual(self._span("Tuần trước nữa tiêu bao nhiêu?"), ("2026-11-09", "2026-11-15"))
        self.assertEqual(self._span("Tuần qua tiêu bao nhiêu?"), ("2026-11-19", "2026-11-25"))
        self.assertEqual(self._span("2 tuần vừa qua tiêu bao nhiêu?"), ("2026-11-12", "2026-11-25"))

    def test_month_words(self):
        self.assertEqual(self._span("Tuần thứ ba của tháng mười"), ("2026-10-15", "2026-10-21"))
        self.assertEqual(self._span("Tháng chín tiêu bao nhiêu?"), ("2026-09-01", "2026-09-30"))

    def test_two_months_still_compare(self):
        self.assertEqual(intent.parse_with_rules("Tháng 9 và tháng 10 khác gì?")["intent"], "so_sanh")

    def test_small_expenses_need_definition(self):
        parsed = intent.parse_with_rules("Tháng này các khoản lặt vặt hết bao nhiêu?")
        self.assertIn("ngưỡng tiền", parsed["clarify"])


if __name__ == "__main__":
    unittest.main()
