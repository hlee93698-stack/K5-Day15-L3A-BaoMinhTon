"""Workflow cố định của bản chạy thử."""
import re

import ai
import data_access
import guard
import intent
import report
import verifier
from rules import SPENDING_CATEGORIES, normalize_text
from session import DATA_START, REFERENCE_DATE, current_user_id
from tools import (categorize, compare_months, find_duplicates, get_transactions,
                   sum_by_category, update_category)
from tracing import note

WRITE_SYSTEM = ("Bạn giải thích chi tiêu bằng tiếng Việt, ngắn và trung tính. Chỉ dùng số có trong FACTS, "
                "không tính lại, không thêm lời khuyên đầu tư. Không lặp bảng.")
_LAST_CHANGES = {}


def _correction(text):
    match = re.match(r"^\s*(?:/sua|sửa|sua)\s+(U[12]-(?:BA|CC)-\d{4})\s*(?:(?:=|thành|thanh)\s*)?([a-zA-Z_]+)\s*$", text, re.I)
    if not match:
        return None
    category = normalize_text(match.group(2)).lower().replace(" ", "_")
    return match.group(1).upper(), category


def _missing_month(month):
    return month < "2026-09" or month > "2026-11"


def _missing_range(from_date, to_date):
    return from_date < DATA_START.isoformat() or to_date > REFERENCE_DATE.isoformat()


def _write(question, context):
    prompt = "FACTS:\n%s\n\nCâu hỏi: %s" % (context["facts"], question)
    if ai.MODEL_PROVIDER == "fake":
        ai.call_model(WRITE_SYSTEM, prompt)
        note("R7: chế độ fake, dùng báo cáo code")
        return context["report"]
    for attempt in range(2):
        suffix = "\nViết lại, lần trước có số ngoài FACTS." if attempt else ""
        reply = ai.call_model(WRITE_SYSTEM, prompt + suffix)
        ok, invalid = verifier.verify_numbers(reply["text"], context["allowed_money"], context["allowed_percent"])
        if ok:
            note("R7: phần lời khớp facts")
            return reply["text"].strip() + "\n\n" + context["report"]
        note("R7: số lạ %s" % ", ".join(invalid))
    note("R7: fallback báo cáo code")
    return context["report"]


def answer(text):
    if normalize_text(text) == "HOANTAC":
        previous = _LAST_CHANGES.pop(current_user_id(), None)
        if not previous:
            return {"output": "Chưa có lần sửa nhóm nào trong phiên để hoàn tác."}
        changed = update_category(previous["tx_id"], previous["cu"])
        return {"output": "Đã hoàn tác %s về `%s`." % (changed["tx_id"], previous["cu"])}

    correction = _correction(text)
    if correction:
        tx_id, category = correction
        if category not in SPENDING_CATEGORIES:
            return {"output": "Nhóm chi không hợp lệ. Hãy chọn một nhóm trong: %s." % ", ".join(SPENDING_CATEGORIES)}
        changed = update_category(tx_id, category)
        _LAST_CHANGES[current_user_id()] = changed
        return {"output": "Đã đổi %s từ `%s` sang `%s`. Bạn có thể hỏi lại để xem kết quả mới." %
                (changed["tx_id"], changed["cu"], changed["moi"])}

    reason = guard.block_reason(text)
    if reason:
        note("R1: chặn %s" % reason)
        return {"output": guard.refusal(reason)}

    parsed = intent.parse_intent(text)
    if parsed.get("clarify"):
        note("R2: hỏi lại thời gian")
        return {"output": parsed["clarify"]}
    if any(_missing_month(month) for month in parsed["months"]):
        note("R3: tháng ngoài dữ liệu")
        return {"output": "Mình chưa có dữ liệu cho tháng đó. Dữ liệu hiện có từ 01/09/2026 đến 25/11/2026."}

    if parsed["intent"] == "so_sanh":
        months = parsed["months"]
        current_month = "%04d-%02d" % (REFERENCE_DATE.year, REFERENCE_DATE.month)
        last_day = REFERENCE_DATE.day if current_month in months else None
        bounds = [data_access.month_bounds(month, last_day) for month in months]
        raw = [get_transactions(*period) for period in bounds]
        if not raw[0] or not raw[1]:
            missing = months[0] if not raw[0] else months[1]
            note("R3: thiếu dữ liệu tháng so sánh")
            return {"output": "Mình chưa có dữ liệu tháng %s nên không thể so sánh." % missing}
        combined = categorize(raw[0] + raw[1])
        categorized = [[row for row in combined if row["date"][:7] == month] for month in months]
        result = compare_months(categorized[0], categorized[1],
                                "01-%02d" % last_day if last_day else "ca_thang")
        return {"output": _write(text, report.comparison_context(result))}

    start, end = parsed["from"], parsed["to"]
    if _missing_range(start, end):
        note("R3: khoảng ngoài dữ liệu")
        return {"output": "Mình chưa có dữ liệu cho khoảng đó. Dữ liệu hiện có từ 01/09/2026 đến 25/11/2026."}
    transactions = get_transactions(start, end)
    if not transactions:
        note("R3: không có giao dịch")
        return {"output": "Mình chưa có dữ liệu cho tháng đó."}
    categorized = categorize(transactions)
    summary = sum_by_category(categorized)
    duplicates = find_duplicates(categorized)
    if parsed["intent"] == "kiem_trung":
        context = report.duplicates_context(start, end, summary, duplicates)
        return {"output": _write(text, context)}
    context = report.summary_context(start, end, summary, categorized, parsed.get("category"), duplicates)
    return {"output": _write(text, context)}
