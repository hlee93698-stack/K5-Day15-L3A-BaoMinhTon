"""Đọc dữ liệu runtime và chuẩn hóa giao dịch. Không đọc file đáp án eval."""
import calendar
import csv
import os
from datetime import date, datetime

from session import current_user_id

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
BANK = os.path.join(DATA, "transactions_bank.csv")
CARD = os.path.join(DATA, "transactions_card.csv")


def _integer(value):
    text = str(value or "0").strip().replace(",", "")
    return int(float(text)) if text else 0


def _bank_rows():
    with open(BANK, encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            debit = _integer(row["phat_sinh_no"])
            credit = _integer(row["phat_sinh_co"])
            stamp = datetime.strptime(row["ngay_giao_dich"], "%d/%m/%Y %H:%M:%S")
            amount = debit or credit
            if amount <= 0 or bool(debit) == bool(credit):
                raise ValueError("Giao dịch tài khoản không hợp lệ: %s" % row["tx_id"])
            yield {
                "tx_id": row["tx_id"], "user_id": row["user_id"], "source": "tai_khoan",
                "date": stamp.strftime("%Y-%m-%d"), "time": stamp.strftime("%H:%M:%S"),
                "description": row.get("dien_giai", ""), "amount": amount,
                "direction": "out" if debit else "in", "fee": 0,
            }


def _card_rows():
    with open(CARD, encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            signed = _integer(row["so_tien_thanh_toan"])
            if signed == 0:
                raise ValueError("Giao dịch thẻ có số tiền bằng 0: %s" % row["tx_id"])
            stamp = datetime.strptime(row["ngay_gd"], "%d/%m/%Y")
            yield {
                "tx_id": row["tx_id"], "user_id": row["user_id"], "source": "the",
                "date": stamp.strftime("%Y-%m-%d"), "time": "",
                "description": row.get("chi_tiet_giao_dich", ""), "amount": abs(signed),
                "direction": "out" if signed > 0 else "in", "fee": _integer(row.get("phi")),
            }


def all_transactions():
    """Trả toàn bộ giao dịch của đúng người dùng phiên."""
    user_id = current_user_id()
    rows = [row for row in list(_bank_rows()) + list(_card_rows()) if row["user_id"] == user_id]
    rows.sort(key=lambda row: (row["date"], row["time"], row["tx_id"]))
    return rows


def get_transactions(from_date, to_date):
    """Lọc giao dịch theo hai đầu ngày, không cho caller chọn user_id."""
    start = date.fromisoformat(from_date)
    end = date.fromisoformat(to_date)
    if start > end:
        raise ValueError("from_date phải không sau to_date")
    return [row for row in all_transactions() if start <= date.fromisoformat(row["date"]) <= end]


def month_bounds(month, last_day=None):
    year, number = [int(part) for part in month.split("-")]
    final = calendar.monthrange(year, number)[1]
    final = min(final, last_day) if last_day else final
    return date(year, number, 1).isoformat(), date(year, number, final).isoformat()


def available_range():
    rows = all_transactions()
    return (rows[0]["date"], rows[-1]["date"]) if rows else (None, None)
