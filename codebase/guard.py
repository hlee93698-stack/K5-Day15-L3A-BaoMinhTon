"""Chặn yêu cầu ngoài phạm vi trước khi gọi model."""
from rules import normalize_text

BLOCKS = {
    "dau_tu": ("CO PHIEU", "CHUNG KHOAN", "COIN", "CRYPTO", "DAU TU", "MUA VANG"),
    "giao_dich": ("CHUYEN GIUP", "CHUYEN TIEN CHO", "THANH TOAN GIUP", "TRA HO GIUP"),
    "bi_mat": ("OTP", "MAT KHAU", "SO THE", "CVV"),
    "nguoi_khac": ("CUA VO", "CUA CHONG", "CUA BAN", "USER 2", "U2", "NGUOI KHAC"),
}


def block_reason(text):
    normalized = normalize_text(text)
    for reason, needles in BLOCKS.items():
        if any(needle in normalized for needle in needles):
            return reason
    return None


def refusal(reason):
    messages = {
        "dau_tu": "Mình không thể tư vấn đầu tư hoặc đề xuất sản phẩm tài chính.",
        "giao_dich": "Mình không thể chuyển tiền hay thanh toán thay bạn.",
        "bi_mat": "Mình không thể nhận hoặc xử lý OTP, mật khẩu hay số thẻ.",
        "nguoi_khac": "Mình không thể xem hoặc tiết lộ chi tiêu của người khác.",
    }
    return messages[reason] + " Mình có thể giúp bạn xem lại chi tiêu của chính mình."
