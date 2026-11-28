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


def mentions_category(text):
    """Câu hỏi có nhắc một nhóm chi (ăn uống, tiền nhà…) hay không."""
    return _category(normalize_text(text)) is not None


def _category(text):
    for alias, category in CATEGORY_ALIASES.items():
        if alias in text:
            return category
    return None


RELATIVE_TAIL = r"(?:GAN DAY|GAN NHAT|VUA QUA|QUA|TRO LAI DAY|TRO LAI|DO LAI DAY)"
_UNTIL_NOW = re.compile(r"(?:DEN|TOI) (?:NAY|HOM NAY|BAY GIO)")
COMPARE_WORDS = re.compile(r"\bSO (?:VOI|SANH)\b|\bKHAC\b|\bCHENH\b|\bHON\b")
WEEK_ORDINALS = {"DAU TIEN": 1, "DAU": 1, "NHAT": 1, "MOT": 1, "1": 1, "HAI": 2, "2": 2, "BA": 3, "3": 3,
                 "BON": 4, "TU": 4, "4": 4, "NAM": 5, "5": 5, "CUOI CUNG": -1, "CUOI": -1}
WORD_NUMBERS = {"MOT": 1, "HAI": 2, "BA": 3, "BON": 4, "NAM": 5, "SAU": 6, "BAY": 7, "TAM": 8, "CHIN": 9,
                "MUOI": 10, "MUOI LAM": 15, "HAI MUOI": 20, "BA MUOI": 30}
_NUMBER = r"(\d{1,3}|MUOI LAM|HAI MUOI|BA MUOI|MOT|HAI|BA|BON|NAM|SAU|BAY|TAM|CHIN|MUOI)"


# "tháng sáu" và "tháng sau" trùng nhau khi bỏ dấu nên không đổi SAU.
MONTH_WORDS = (("MUOI HAI", 12), ("MUOI MOT", 11), ("MUOI", 10), ("CHIN", 9), ("TAM", 8), ("BAY", 7),
               ("NAM", 5), ("TU", 4), ("BON", 4), ("BA", 3), ("HAI", 2), ("MOT", 1), ("GIENG", 1))
WEEKDAYS = {"HAI": 0, "2": 0, "BA": 1, "3": 1, "TU": 2, "4": 2, "NAM": 3, "5": 3,
            "SAU": 4, "6": 4, "BAY": 5, "7": 5}
_WEEKDAY = re.compile(r"(?<!TUAN )\b(?:THU (HAI|BA|TU|NAM|SAU|BAY|[2-7])|(CHU NHAT|CN))\b")
_RECENT = re.compile(r"VUA ROI|VUA QUA|\bROI\b|TRUOC")


def _canon(text):
    """'tháng chín' → 'THANG 9' để các luật số đọc được."""
    for word, number in MONTH_WORDS:
        text = re.sub(r"\bTHANG %s\b" % word, "THANG %d" % number, text)
    return text


def _keep_dates(text):
    """Như normalize_text nhưng giữ / và - để đọc được 5/9, 05-09-2026, 05.09."""
    value = str(text or "").replace("–", "-").replace("—", "-")
    value = re.sub(r"(?<=\d)\.(?=\d{1,2}\b)", "/", value)
    value = re.sub(r"[^\w/\-]+", " ", value)
    value = normalize_text(value.replace("/", " SLASH ").replace("-", " DASH "))
    return _canon(re.sub(r"\s*SLASH\s*", "/", re.sub(r"\s*DASH\s*", "-", value)))


def _count(token):
    return int(token) if token.isdigit() else WORD_NUMBERS[token]


def _month_end(year, month):
    import calendar
    return date(year, month, calendar.monthrange(year, month)[1])


def _day(year, month, day):
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _explicit_dates(text, months=()):
    """Ngày cụ thể: 5/9, 05/09/2026, 'ngày (mùng) 5 tháng 9', 'ngày 15 tháng trước', 'ngày 5'.
    Ngày không kèm tháng: lấy tháng được nhắc trong câu, không có thì lấy lần gần nhất đã qua."""
    found = []
    for match in re.finditer(r"(?<![\d/])(\d{1,2})[/-](\d{1,2})(?:[/-](20\d{2}))?(?![\d/])", text):
        value = _day(int(match.group(3) or REFERENCE_DATE.year), int(match.group(2)), int(match.group(1)))
        if value:
            found.append((match.start(), value))
    day_word = r"(?:NGAY|MUNG|HOM)\s+(?:MUNG\s+)?(\d{1,2})"
    for match in re.finditer(day_word + r"\s+THANG\s+(\d{1,2})(?:\s+(?:NAM\s+)?(20\d{2}))?", text):
        value = _day(int(match.group(3) or REFERENCE_DATE.year), int(match.group(2)), int(match.group(1)))
        if value:
            found.append((match.start(), value))
    for match in re.finditer(day_word + r"\b(?!\s*(?:[/\-]|THANG\s+\d))", text):
        day = int(match.group(1))
        if months:
            year, number = [int(part) for part in months[0].split("-")]
            value = _day(year, number, day)
        else:
            value = _day(REFERENCE_DATE.year, REFERENCE_DATE.month, day)
            if not value or value > REFERENCE_DATE:
                previous = [int(part) for part in _previous_month().split("-")]
                value = _day(previous[0], previous[1], day)
        if value:
            found.append((match.start(), value))
    return [value for _, value in sorted(found)]


def _sub_month(text, months):
    """Tuần thứ N / nửa / đầu-giữa-cuối của một tháng. Tuần thứ N = ngày 7N-6 đến 7N (tuần cuối = 7 ngày cuối)."""
    month = months[0] if months else "%04d-%02d" % (REFERENCE_DATE.year, REFERENCE_DATE.month)
    year, number = [int(part) for part in month.split("-")]
    end = _month_end(year, number)
    week = re.search(r"TUAN\s+(?:THU\s+)?(DAU TIEN|CUOI CUNG|DAU|NHAT|CUOI|MOT|HAI|BA|BON|TU|NAM|[1-5])\b", text)
    if week:
        index = WEEK_ORDINALS[week.group(1)]
        if index == -1:
            return end - timedelta(days=6), end
        start = date(year, number, 7 * index - 6) if 7 * index - 6 <= end.day else None
        return (start, min(end, start + timedelta(days=6))) if start else None
    span = re.search(_NUMBER + r"\s+NGAY\s+(DAU TIEN|DAU|CUOI CUNG|CUOI)\b", text)
    if span:
        count = min(_count(span.group(1)), end.day)
        if span.group(2).startswith("DAU"):
            return date(year, number, 1), date(year, number, count)
        return end - timedelta(days=count - 1), end
    if "NUA DAU" in text:
        return date(year, number, 1), date(year, number, 15)
    if re.search(r"NUA (?:CUOI|SAU)", text):
        return date(year, number, 16), end
    if re.search(r"\bTU DAU THANG\b", text) or (re.search(r"\bDAU THANG\b", text) and _UNTIL_NOW.search(text)):
        return date(year, number, 1), end
    if re.search(r"\bDAU THANG\b", text):
        return date(year, number, 1), date(year, number, 10)
    if re.search(r"\bGIUA THANG\b", text):
        return date(year, number, 11), date(year, number, 20)
    if re.search(r"\bCUOI THANG\b", text):
        return date(year, number, 21), end
    return None


def _relative(text):
    ref = REFERENCE_DATE
    if "HOM NAY" in text:
        return ref, ref
    if "HOM KIA" in text:
        return ref - timedelta(days=2), ref - timedelta(days=2)
    if "HOM QUA" in text:
        return ref - timedelta(days=1), ref - timedelta(days=1)
    match = re.search(_NUMBER + r"\s+(NGAY|TUAN|THANG)\s+" + RELATIVE_TAIL, text)
    if match:
        count, unit = _count(match.group(1)), match.group(2)
        if unit == "NGAY":
            return ref - timedelta(days=count - 1), ref
        if unit == "TUAN":
            return ref - timedelta(days=7 * count - 1), ref
        month_index = ref.year * 12 + ref.month - 1 - (count - 1)
        return date(month_index // 12, month_index % 12 + 1, 1), ref
    monday = ref - timedelta(days=ref.weekday())
    week_start = (monday - timedelta(days=14) if "TUAN TRUOC NUA" in text
                  else monday - timedelta(days=7) if re.search(r"TUAN (?:TRUOC|VUA ROI|VUA QUA|ROI)\b", text)
                  else monday if "TUAN NAY" in text else None)
    weekday = _WEEKDAY.search(text)
    if weekday:
        index = 6 if weekday.group(2) else WEEKDAYS[weekday.group(1)]
        if week_start:
            day = week_start + timedelta(days=index)
        else:
            day = ref - timedelta(days=(ref.weekday() - index) % 7)
            if day == ref and _RECENT.search(text):
                day -= timedelta(days=7)
        return day, day
    if "CUOI TUAN" in text:
        saturday = (week_start or monday - timedelta(days=7 if ref.weekday() < 5 else 0)) + timedelta(days=5)
        return saturday, saturday + timedelta(days=1)
    if week_start:
        return week_start, min(ref, week_start + timedelta(days=6))
    if re.search(r"\bTUAN (?:QUA|GAN DAY|GAN NHAT)\b", text):
        return ref - timedelta(days=6), ref
    if "QUY NAY" in text:
        return date(ref.year, 3 * ((ref.month - 1) // 3) + 1, 1), ref
    return None


def _date_range(text, months, raw=""):
    """Khoảng ngày (start, end) đọc được bằng luật, hoặc None. Cuối khoảng không vượt ngày tham chiếu."""
    dated = _keep_dates(raw) if raw else text
    shared = re.search(r"(?<![\d/])(?<!THANG )(\d{1,2})\s*(?:DEN|TOI|-)\s*(?:NGAY\s+)?(\d{1,2})\s*(?:/|THANG\s+)(\d{1,2})(?![\d])", dated)
    period = None
    if shared:
        month = int(shared.group(3))
        period = (_day(REFERENCE_DATE.year, month, int(shared.group(1))),
                  _day(REFERENCE_DATE.year, month, int(shared.group(2))))
        period = period if all(period) and period[0] <= period[1] else None
    if not period:
        dates = _explicit_dates(dated, months)
        if len(dates) >= 2:
            period = min(dates[:2]), max(dates[:2])
        elif dates and _UNTIL_NOW.search(text):
            period = dates[0], REFERENCE_DATE
        elif dates:
            period = dates[0], dates[0]
    period = period or _sub_month(text, months) or _relative(text)
    if not period and len(months) == 1:
        year, number = [int(part) for part in months[0].split("-")]
        period = date(year, number, 1), _month_end(year, number)
    if not period:
        return None
    start, end = period
    if start <= REFERENCE_DATE < end:
        end = REFERENCE_DATE
    return start, end


def parse_with_rules(text):
    normalized = _canon(normalize_text(text))
    if "LAT VAT" in normalized:
        return {"in_scope": True, "intent": None, "from": None, "to": None, "months": [],
                "category": None,
                "clarify": "Bạn muốn tính ‘lặt vặt’ theo ngưỡng tiền nào hoặc theo nhóm chi nào?"}
    months = _months(normalized)
    category = _category(normalized)
    period = _date_range(normalized, months, text)
    if len(months) >= 2 and (period is None or COMPARE_WORDS.search(normalized)):
        # Comparison deltas always mean later month minus earlier month,
        # regardless of the order in which the user mentions them.
        return {"in_scope": True, "intent": "so_sanh", "from": None, "to": None,
                "months": sorted(months[:2]), "category": category, "clarify": None}
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
    system = ("Chuyển câu hỏi chi tiêu thành JSON duy nhất. intent là tong_hop, so_sanh, mot_nhom, kiem_trung "
              "hoặc ngoai_pham_vi. Chỉ dùng 4 loại đầu khi câu hỏi hỏi về giao dịch / chi tiêu ĐÃ XẢY RA của chính "
              "người dùng trong sao kê. Mọi thứ khác (thời tiết, giá coin/vàng/cổ phiếu, kiến thức chung, lời khuyên, "
              "tán gẫu, viết code, dịch, kế hoạch tương lai…) trả {\"intent\": \"ngoai_pham_vi\"}. "
              "Với so_sanh trả months gồm 2 tháng YYYY-MM; loại khác trả from/to dạng YYYY-MM-DD. "
              "category là một nhóm chi hợp lệ hoặc null (%s). Không thêm chữ ngoài JSON. "
              "Hôm nay là %s; dữ liệu có từ 2026-09-01 đến %s. Năm mặc định là %d. "
              "Quy ước: tuần thứ N của tháng = ngày 7N-6 đến 7N; tuần trước = thứ Hai đến Chủ nhật tuần trước; "
              "'N ngày qua' tính cả hôm nay; to không vượt quá hôm nay."
              % (", ".join(SPENDING_CATEGORIES), REFERENCE_DATE.isoformat(), REFERENCE_DATE.isoformat(),
                 REFERENCE_DATE.year))
    reply = call_model(system, text)
    value = _json_object(reply["text"])
    if isinstance(value, dict) and value.get("intent") == "ngoai_pham_vi":
        return {"in_scope": False, "out_of_scope": True, "intent": None, "from": None, "to": None,
                "months": [], "category": None, "clarify": None}
    parsed = _validated(value)
    if parsed:
        return parsed
    return {"in_scope": True, "intent": None, "from": None, "to": None, "months": [], "category": None,
            "clarify": "Bạn muốn xem tháng nào? Ví dụ: tháng này hoặc tháng trước."}
