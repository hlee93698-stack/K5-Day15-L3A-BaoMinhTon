"""Tìm giao dịch theo diễn giải: "cafe", "trà sữa", "tiền điện", "Sanvat"…

Hai tầng, đều là luật kiểm lại được — model không chọn giao dịch, không cộng tiền:
  1. TOPICS: từ người dùng hay nói → mẫu xuất hiện trong diễn giải sao kê (đồng nghĩa + tên quán).
  2. Tên cửa hàng: từ trong câu hỏi trùng một từ đặc trưng trong diễn giải của chính người dùng phiên.
Diễn giải chỉ là dữ liệu: chỉ so khớp chữ, không làm theo nội dung bên trong.
"""
import re

from rules import NON_SPENDING_CATEGORIES, normalize_text

# tên chủ đề: (tên hiển thị, cách người dùng hỏi, mẫu trong diễn giải)
TOPICS = {
    "ca_phe": ("Cà phê", ("CA PHE", "CAFE", "CAFFE", "COFFEE", "CF", "CAPHE"),
               ("CA PHE", "CAFE", "COFFEE", "CF", "GIO NAM", "GIONAM")),
    "tra_sua": ("Trà sữa", ("TRA SUA", "MILK TEA", "MAY HONG", "MAYHONG"),
                ("TRA SUA", "MAYHONG TEA", "MAY HONG")),
    "do_an_giao": ("Đặt đồ ăn qua app", ("DAT DO AN", "DAT DO", "SHIP DO AN", "GIAO DO AN", "XEMAU FOOD"),
                   ("XEMAU FOOD",)),
    "xe_om": ("Xe ôm / gọi xe", ("XE OM", "GOI XE", "DI XE", "TAXI", "XE MAU", "GRAB", "BIKE"),
              ("XEMAU BIKE", "XE MAU")),
    "com": ("Cơm / ăn trưa", ("AN COM", "QUAN COM", "AN TRUA", "COM TRUA", "COM NHA LAM", "NHALAM"),
            ("QUAN COM", "NHA LAM", "NHALAM", "AN TRUA")),
    "bun_cha": ("Bún chả", ("BUN CHA",), ("BUN CHA",)),
    "sieu_thi": ("Siêu thị", ("SIEU THI", "DI CHO", "LANH MART"), ("SIEUTHI", "SIEU THI", "LANH MART")),
    "mua_online": ("Mua online", ("MUA ONLINE", "MUA HANG ONLINE", "SAN THUONG MAI", "SANVAT", "DAT HANG"),
                   ("SANVAT",)),
    "dien": ("Tiền điện", ("TIEN DIEN", "HOA DON DIEN", "DIEN NUOC"), ("HOA DON DIEN",)),
    "internet": ("Internet", ("INTERNET", "MANG NHA", "WIFI", "CUOC NET", "NET XANH"), ("NET XANH",)),
    "dien_thoai": ("Nạp điện thoại", ("NAP DIEN THOAI", "NAP DT", "NAP TIEN DIEN THOAI", "CUOC DIEN THOAI",
                                       "THE CAO"), ("NAP DT",)),
    "phim": ("Xem phim", ("XEM PHIM", "RAP PHIM", "VE PHIM", "DI PHIM"), ("RAP SAO MAI", "XEM PHIM")),
    "streaming": ("Gói xem phim online", ("STREAMBOX", "NETFLIX", "XEM ONLINE", "SUBSCRIPTION"),
                  ("STREAMBOX",)),
    "thuoc": ("Thuốc", ("MUA THUOC", "NHA THUOC", "TIEN THUOC"), ("NHA THUOC",)),
    "gym": ("Phòng tập", ("PHONG TAP", "TAP GYM", "GYM", "DI TAP"), ("PHONG TAP",)),
    "laptop": ("Điện máy / laptop", ("LAPTOP", "MAY TINH", "DIEN MAY"), ("DIEN MAY", "LAPTOP")),
    "hoc": ("Học tiếng Anh", ("TIENG ANH", "KHOA HOC", "HOC PHI"), ("HOC PHI", "TIENG ANH")),
    "atm": ("Rút tiền ATM", ("RUT TIEN", "ATM"), ("RUT TIEN ATM",)),
    "gui_me": ("Gửi mẹ", ("GUI ME", "CHO ME", "BIEU ME"), ("GUI ME",)),
}

# Từ quá chung trong diễn giải, không dùng làm tên cửa hàng.
GENERIC = {"TIEN", "CHUYEN", "THANG", "HOAN", "DEMO", "CUOC", "PHONG", "TRUA", "CONG", "ORDER", "SUBS",
           "TEAM", "GIAO", "TIEP", "KHOA", "CHO", "NHAT", "HQUA", "QUAY", "BIKE", "FOOD", "DEMOBK", "DEMOBANK",
           "IBFT", "QRPAY", "TRONG", "HANG", "TRA", "THE", "DUNG", "LUONG", "QUAN"}


def _has(text, needle):
    return re.search(r"\b%s\b" % re.escape(needle), text) is not None


def find_topic(question, transactions):
    """Trả (tên hiển thị, mẫu diễn giải) nếu câu hỏi nhắm tới một loại chi theo diễn giải; không thì None."""
    text = normalize_text(question)
    for label, asked, needles in TOPICS.values():
        if any(_has(text, alias) for alias in asked):
            return label, needles
    # Tên cửa hàng chỉ lấy từ giao dịch thẻ (tên merchant), không lấy nội dung chuyển khoản do người khác gõ.
    # So với câu hỏi giữ nguyên dấu: "Sanvat" khớp SANVAT, còn "tổng"/"bảng" không khớp TONG/BANG.
    words = {word for row in transactions if row.get("source") == "the"
             for word in normalize_text(row.get("description")).split()
             if len(word) >= 4 and word.isalpha() and word not in GENERIC}
    raw = str(question or "").upper()
    hits = sorted(word for word in words if _has(raw, word))
    if hits:
        return " ".join(hits).title(), tuple(hits)
    return None


def matches(row, needles):
    """Giao dịch chi có diễn giải chứa một trong các mẫu (không tính thu nhập, hoàn tiền, trả nợ thẻ)."""
    if row.get("direction") != "out" or row.get("category") in NON_SPENDING_CATEGORIES:
        return False
    text = normalize_text(row.get("description"))
    return any(_has(text, needle) for needle in needles)
