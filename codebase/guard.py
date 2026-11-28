"""Chặn yêu cầu ngoài phạm vi trước khi gọi model.

Ba lớp, chạy theo thứ tự:
  1. block_reason(): chủ đề bị cấm (đầu tư/crypto, chuyển tiền, OTP/mật khẩu, dữ liệu người khác) → từ chối riêng.
  2. in_scope(): câu hỏi phải có dấu hiệu nói về tiền/chi tiêu của chính người dùng; không có → từ chối.
  3. intent.parse_intent(): câu không đọc được bằng luật thì model phân loại, được phép trả "ngoai_pham_vi".
"""
import re
import unicodedata

from rules import normalize_text

BLOCKS = {
    "dau_tu": ("CO PHIEU", "CHUNG KHOAN", "COIN", "CRYPTO", "DAU TU", "MUA VANG", "GIA VANG",
               "BITCOIN", "BIT COIN", "BIT COI", "BTC", "ETH", "ETHEREUM", "USDT", "BINANCE", "ALTCOIN", "DCA",
               "NFT", "FOREX", "TIEN AO", "TIEN DIEN TU", "TRAI PHIEU", "CHUNG CHI QUY", "CO TUC", "LAI SUAT",
               "LUOT SONG", "DONG COIN", "SAN GIAO DICH", "VAY TIEN", "VAY NO"),
    "giao_dich": ("CHUYEN GIUP", "CHUYEN TIEN CHO", "THANH TOAN GIUP", "TRA HO GIUP"),
    "bi_mat": ("OTP", "MAT KHAU", "SO THE", "CVV"),
    "nguoi_khac": ("CUA VO", "CUA CHONG", "CUA BAN", "USER 2", "U2", "NGUOI KHAC"),
}

# Dấu hiệu câu hỏi nói về tiền / chi tiêu. So trên chữ thường GIỮ DẤU để "chỉ"/"chị" không bị coi là "chi",
# kèm bản không dấu cho người gõ không dấu.
SIGNALS = re.compile(r"\b(?:" + "|".join((
    "chi", "chi tiêu", "tiêu", "tieu", "xài", "xai", "tốn", "ton", "tiền", "tien", "đồng",
    "dùng", "dung", "quẩy", "quay", "đốt", "hết bao nhiêu", "het bao nhieu", "hết nhiêu", "het nhieu",
    "giao dịch", "giao dich", "sao kê", "sao ke", "khoản", "khoan", "trừ", "tru", "thanh toán", "thanh toan",
    "mua", "trả", "nạp", "nap", "gửi", "gui", "đóng", "phí", "phi", "hóa đơn", "hoá đơn", "hoa don",
    "ngân sách", "ngan sach", "lương", "luong", "hoàn tiền", "hoan tien", "nhóm", "nhom",
)) + r")\b")


def _words(text):
    return unicodedata.normalize("NFC", str(text or "")).lower()


def block_reason(text):
    normalized = normalize_text(text)
    for reason, needles in BLOCKS.items():
        if any(re.search(r"\b%s\b" % re.escape(needle), normalized) for needle in needles):
            return reason
    return None


def in_scope(text, has_topic=False):
    """True nếu câu hỏi có dấu hiệu về tiền/chi tiêu, hoặc nhắc một nhóm chi/chủ đề/cửa hàng có trong sao kê."""
    return has_topic or SIGNALS.search(_words(text)) is not None


def refusal(reason):
    messages = {
        "dau_tu": "Mình không thể tư vấn đầu tư hoặc đề xuất sản phẩm tài chính.",
        "giao_dich": "Mình không thể chuyển tiền hay thanh toán thay bạn.",
        "bi_mat": "Mình không thể nhận hoặc xử lý OTP, mật khẩu hay số thẻ.",
        "nguoi_khac": "Mình không thể xem hoặc tiết lộ chi tiêu của người khác.",
    }
    if reason == "ngoai_pham_vi":
        return ("Câu này nằm ngoài phạm vi của mình. Mình chỉ trả lời về chi tiêu của chính bạn trong sao kê, "
                "ví dụ “Tháng 10 tôi tiêu bao nhiêu?” hoặc “Tuần trước uống cà phê hết bao nhiêu?”.")
    return messages[reason] + " Mình có thể giúp bạn xem lại chi tiêu của chính mình."
