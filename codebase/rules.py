"""Luật phân nhóm có thể kiểm lại được."""
import json
import os
import re
import unicodedata

from session import current_user_id

SPENDING_CATEGORIES = (
    "an_uong", "di_lai", "mua_sam", "hoa_don", "nha_o", "giai_tri",
    "suc_khoe", "giao_duc", "tien_mat", "gia_dinh", "khong_ro",
)
NON_SPENDING_CATEGORIES = ("thu_nhap", "hoan_tien", "noi_bo")
ALL_CATEGORIES = SPENDING_CATEGORIES + NON_SPENDING_CATEGORIES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def normalize_text(text):
    value = str(text or "").replace("đ", "d").replace("Đ", "D")
    value = unicodedata.normalize("NFD", value)
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = re.sub(r"[^A-Za-z0-9]+", " ", value.upper())
    return re.sub(r"\s+", " ", value).strip()


def _overrides_path():
    return os.environ.get("OVERRIDES_PATH") or os.path.join(ROOT, "runtime", "overrides.json")


def load_overrides():
    path = _overrides_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def save_override(tx_id, category):
    """Lưu nhãn người dùng đã chọn theo đúng user phiên."""
    if category not in SPENDING_CATEGORIES:
        raise ValueError("Nhóm chi không hợp lệ: %s" % category)
    user_id = current_user_id()
    data = load_overrides()
    data.setdefault(user_id, {})[tx_id] = category
    path = _overrides_path()
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)


def _contains(text, *needles):
    return any(needle in text for needle in needles)


def rule_category(transaction):
    """Trả (category, method), hoặc None nếu cần AI / giữ không rõ."""
    user_id = current_user_id()
    override = load_overrides().get(user_id, {}).get(transaction["tx_id"])
    if override in SPENDING_CATEGORIES:
        return override, "nguoi_dung"

    raw = str(transaction.get("description") or "").strip()
    text = normalize_text(raw)
    if transaction["direction"] == "in":
        return ("hoan_tien" if "HOAN TIEN" in text else "thu_nhap"), "luat"
    if "TT THE TIN DUNG" in text:
        return "noi_bo", "luat"
    if (not text or text in ("CK", "CHUYEN TIEN") or raw.upper().startswith("CK:")
            or re.fullmatch(r"IBFT \d+", text)
            or re.fullmatch(r"(?:QRPAY|POS) \d+(?: HN)?", text)
            or re.fullmatch(r"(?:DEMOBK|DEMOBANK) \d+ CHUYEN TIEN", text)):
        return "khong_ro", "luat"

    patterns = (
        (("XEMAU FOOD",), "an_uong"),
        (("XEMAU BIKE", "XE MAU"), "di_lai"),
        (("GIO NAM", "GIONAM", "TRA SUA", "MAYHONG TEA", "QUAN COM", "NHALAM KITCHEN",
          "TIEN AN TRUA", "TIEN BUN CHA", "CHIA TIEN AN"), "an_uong"),
        (("SIEUTHI LANH", "LANH MART", "SANVAT ORDER", "DIEN MAY"), "mua_sam"),
        (("TT HOA DON", "NET XANH", "NAP DT"), "hoa_don"),
        (("TIEN NHA", "TIEN PHONG"), "nha_o"),
        (("RAP SAO MAI", "STREAMBOX"), "giai_tri"),
        (("NHA THUOC", "PHONG TAP"), "suc_khoe"),
        (("HOC PHI",), "giao_duc"),
        (("RUT TIEN ATM",), "tien_mat"),
        (("GUI ME", "GUI NHA"), "gia_dinh"),
    )
    for needles, category in patterns:
        if _contains(text, *needles):
            return category, "luat"
    return None
