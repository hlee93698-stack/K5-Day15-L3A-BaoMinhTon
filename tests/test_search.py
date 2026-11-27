import unittest

import tests._bootstrap  # noqa: F401

import agent
import search


class SearchByDescriptionTest(unittest.TestCase):
    def test_coffee_synonyms_and_shop_names(self):
        result = agent.answer("Tháng 9 tôi đã uống cafe hết bao nhiêu tiền")
        data = result["data"]
        self.assertEqual(data["kind"], "tim_kiem")
        self.assertEqual((data["total"], data["count"]), (286000, 5))
        self.assertEqual({row["description"] for row in data["items"]},
                         {"GIONAM COFFEE 03", "gio nam cafe", "QR-GIO NAM CF", "CA PHE GIO NAM"})
        self.assertIn("286.000đ", result["output"])

    def test_vietnamese_with_accents_matches_too(self):
        self.assertEqual(agent.answer("Tháng 10 uống cà phê bao nhiêu?")["data"]["total"], 327000)

    def test_shop_name_from_user_statement(self):
        data = agent.answer("Tháng 10 mua hàng Sanvat bao nhiêu?")["data"]
        self.assertEqual(data["kind"], "tim_kiem")
        self.assertTrue(all("SANVAT" in row["description"] for row in data["items"]))

    def test_refund_and_income_not_counted(self):
        rows = [{"direction": "in", "category": "hoan_tien", "description": "HOAN TIEN SANVAT*ORDER 8812"},
                {"direction": "out", "category": "noi_bo", "description": "SANVAT"}]
        self.assertFalse(any(search.matches(row, ("SANVAT",)) for row in rows))

    def test_category_questions_keep_old_behaviour(self):
        self.assertEqual(agent.answer("Tháng 10 tôi chi ăn uống bao nhiêu?")["data"]["kind"], "mot_nhom")
        self.assertEqual(agent.answer("Tháng này tiền đi đâu hết vậy?")["data"]["kind"], "tong_hop")


if __name__ == "__main__":
    unittest.main()
