"""Kiểm số trong phần lời của model có thuộc facts do code tính hay không."""
import re

PERCENT = re.compile(r"(?<!\d)(\d+(?:[.,]\d+)?)\s*%")
MONEY = re.compile(r"(?<![\d/])(\d{1,3}(?:[.,]\d{3})+|\d{4,}|\d+(?:[.,]\d+)?)\s*(triệu|trieu|tr|k|đ|vnd)?", re.I)


def _money_value(number, suffix):
    suffix = (suffix or "").lower()
    if suffix in ("triệu", "trieu", "tr"):
        return round(float(number.replace(",", ".")) * 1_000_000)
    if suffix == "k":
        return round(float(number.replace(",", ".")) * 1_000)
    return int(re.sub(r"[.,]", "", number))


def verify_numbers(text, allowed_money, allowed_percent):
    """Trả (đạt, danh sách số lạ)."""
    invalid = []
    percent_spans = []
    for match in PERCENT.finditer(text):
        value = round(float(match.group(1).replace(",", ".")), 1)
        if all(abs(value - allowed) > 0.05 for allowed in allowed_percent):
            invalid.append(match.group(0))
        percent_spans.append(match.span())

    def inside_percent(start, end):
        return any(start >= left and end <= right for left, right in percent_spans)

    for match in MONEY.finditer(text):
        if inside_percent(*match.span()):
            continue
        suffix = match.group(2)
        raw = match.group(1)
        if not suffix and not (re.search(r"[.,]\d{3}", raw) or len(raw) >= 4):
            continue
        value = _money_value(raw, suffix)
        if not suffix and 1900 <= value <= 2100:
            continue
        if value not in allowed_money:
            invalid.append(match.group(0))
    return not invalid, invalid
