"""Hiểu loại câu hỏi. Luật xử lý câu rõ, model chỉ xử lý phần còn lại."""
import json
import re
from datetime import date, timedelta

from ai import call_model
from rules import SPENDING_CATEGORIES, normalize_text
from session import REFERENCE_DATE

CATEGORY_ALIASES = {
    "AN UONG": "an_uong", "DI LAI": "di_lai", "MUA SAM": "mua_sam",
    "HOA DON": "hoa_don", "NHA O": "nha_o", "TIEN NHA": "nha_o", "GIAI TRI": "giai_tri",
    "SUC KHOE": "suc_khoe", "GIAO DUC": "giao_duc", "TIEN MAT": "tien_mat",
    "GIA DINH": "gia_dinh", "KHONG RO": "khong_ro", "KHONG GHI NOI DUNG": "khong_ro",
    "KHONG NOI DUNG": "khong_ro", "STREAMBOX": "giai_tri",
}


def _previous_month():
    year, month = REFERENCE_DATE.year, REFERENCE_DATE.month - 1
    if month == 0:
        year, month = year - 1, 12
    return "%04d-%02d" % (year, month)


def _months(text):
    months = []
    if "THANG NAY" in text:
        months.append("%04d-%02d" % (REFERENCE_DATE.year, REFERENCE_DATE.month))
    if "THANG TRUOC" in text:
        months.append(_previous_month())
    for match in re.finditer(r"(?:THANG|\bT)\s*(1[0-2]|[1-9])(?:\s*/\s*(20\d{2}))?", text):
        number, year = int(match.group(1)), int(match.group(2) or REFERENCE_DATE.year)
        value = "%04d-%02d" % (year, number)
        if value not in months:
            months.append(value)
    return months


def _category(text):
    for alias, category in CATEGORY_ALIASES.items():
        if alias in text:
            return category
    return None


def _date_range(text, months):
    monday = REFERENCE_DATE - timedelta(days=REFERENCE_DATE.weekday())
    if "TUAN TRUOC" in text:
        return monday - timedelta(days=7), monday - timedelta(days=1)
    if "TUAN NAY" in text:
        return monday, REFERENCE_DATE
    if len(months) == 1:
        year, month = [int(part) for part in months[0].split("-")]
        start = date(year, month, 1)
        if (year, month) == (REFERENCE_DATE.year, REFERENCE_DATE.month):
            end = REFERENCE_DATE
        else:
            import calendar
            end = date(year, month, calendar.monthrange(year, month)[1])
        return start, end
    return None


def parse_with_rules(text):
    normalized = normalize_text(text)
    if "LAT VAT" in normalized:
        return {"in_scope": True, "intent": None, "from": None, "to": None, "months": [],
                "category": None,
                "clarify": "Bạn muốn tính ‘lặt vặt’ theo ngưỡng tiền nào hoặc theo nhóm chi nào?"}
    months = _months(normalized)
    category = _category(normalized)
    if len(months) >= 2:
        # Comparison deltas always mean later month minus earlier month,
        # regardless of the order in which the user mentions them.
        return {"in_scope": True, "intent": "so_sanh", "from": None, "to": None,
                "months": sorted(months[:2]), "category": category, "clarify": None}
    period = _date_range(normalized, months)
    if period:
        if not category and "KHOAN" in normalized and ("QUEN" in normalized or "KHONG NHO" in normalized):
            category = "khong_ro"
        duplicate = any(needle in normalized for needle in ("TRU HAI LAN", "TRU 2 LAN", "TRUNG"))
        return {"in_scope": True, "intent": "kiem_trung" if duplicate else "mot_nhom" if category else "tong_hop",
                "from": period[0].isoformat(), "to": period[1].isoformat(), "months": months,
                "category": category, "clarify": None}
    return None


def _json_object(text):
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        value = json.loads(text[start:end + 1])
    except ValueError:
        return None
    return value if isinstance(value, dict) else None


def _validated(value):
    if not isinstance(value, dict) or value.get("intent") not in ("tong_hop", "so_sanh", "mot_nhom", "kiem_trung"):
        return None
    months = value.get("months") or []
    if value["intent"] == "so_sanh":
        if (not isinstance(months, list) or len(months) != 2
                or any(not re.fullmatch(r"20\d{2}-(0[1-9]|1[0-2])", str(m)) for m in months)):
            return None
    else:
        try:
            start, end = date.fromisoformat(value.get("from", "")), date.fromisoformat(value.get("to", ""))
        except (TypeError, ValueError):
            return None
        if start > end:
            return None
    category = value.get("category")
    if category is not None and category not in SPENDING_CATEGORIES:
        return None
    if value["intent"] == "mot_nhom" and category is None:
        return None
    if value["intent"] == "so_sanh":
        months = sorted(months)
        start = end = None
    return {"in_scope": True, "intent": value["intent"], "from": start.isoformat() if start else None,
            "to": end.isoformat() if end else None, "months": months, "category": category, "clarify": None}


def parse_intent(text):
    parsed = parse_with_rules(text)
    if parsed:
        return parsed
    system = ("Chuyển câu hỏi chi tiêu thành JSON duy nhất. intent là tong_hop, so_sanh, mot_nhom hoặc kiem_trung. "
              "Với so_sanh trả months gồm 2 tháng YYYY-MM; loại khác trả from/to dạng YYYY-MM-DD. "
              "category là một nhóm chi hợp lệ hoặc null. Không thêm chữ ngoài JSON.")
    reply = call_model(system, text)
    parsed = _validated(_json_object(reply["text"]))
    if parsed:
        return parsed
    return {"in_scope": True, "intent": None, "from": None, "to": None, "months": [], "category": None,
            "clarify": "Bạn muốn xem tháng nào? Ví dụ: tháng này hoặc tháng trước."}
