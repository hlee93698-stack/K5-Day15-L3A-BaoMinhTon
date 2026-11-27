"""Đếm kết quả khảo sát từ evidence/survey/results.csv (bản đã xoá dấu thời gian + liên hệ).

Chạy:  python evidence/survey/count.py
Quy ước đếm (khớp evidence/hypothesis.md):
- Loại phiếu chọn "Chưa bao giờ" ở câu 3 khỏi mẫu số của câu 4–8 (họ không có "lần gần nhất").
- Loại các phiếu ghi trong LOAI_RA (phiếu của người trong nhóm, nếu có).
- Đếm cho tất cả và riêng nhóm "Đi làm dưới 3 năm" (người dùng chính).
"""
import csv
import statistics
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
FILE = Path(__file__).with_name("results.csv")
LOAI_RA: set[int] = set()  # số phiếu của người trong nhóm, vd {3, 7}
NGUOI_DUNG_CHINH = "Đi làm dưới 3 năm"


def pct(x, n):
    return f"{x}/{n} ({round(100 * x / n)}%)" if n >= 10 else f"{x}/{n}"


rows = [r for r in csv.DictReader(open(FILE, encoding="utf-8")) if int(r["phieu"]) not in LOAI_RA]
print(f"Tổng phiếu hợp lệ: N = {len(rows)} (đã loại {len(LOAI_RA)} phiếu người trong nhóm)")

vai = {}
for r in rows:
    vai[r["vai"]] = vai.get(r["vai"], 0) + 1
print("Câu 1 · Vai:", ", ".join(f"{k} {v}" for k, v in sorted(vai.items(), key=lambda kv: -kv[1])))
chua = [r for r in rows if r["lan_gan_nhat"] == "Chưa bao giờ"]
print(f"Câu 3 · Chưa bao giờ xem lại: {len(chua)} phiếu → loại khỏi mẫu số câu 4–8\n")

CHI_TIEU = [
    ("Câu 3 · Xem lại trong khoảng 1 tháng gần đây (tuần này / tuần trước / đầu tháng này)",
     lambda r: r["lan_gan_nhat"] in ("Tuần này", "Tuần trước", "Đầu tháng này")),
    ("Câu 5 · Kéo xem lịch sử giao dịch trong app", lambda r: "Kéo xem lịch sử giao dịch" in r["cach_lam"]),
    ("Câu 5 · Xem biểu đồ/thống kê có sẵn trong app", lambda r: "biểu đồ/thống kê" in r["cach_lam"]),
    ("Câu 5 · Cộng nhẩm/ghi giấy", lambda r: "Cộng nhẩm" in r["cach_lam"]),
    ("Câu 6 · Mất ≥15 phút (15–30 + trên 30 phút)", lambda r: r["thoi_gian"] in ("15–30 phút", "Trên 30 phút")),
    ("Câu 7 · Chỉ biết một phần hoặc bỏ dở", lambda r: r["biet_tien_di_dau"] in ("Được một phần", "Không, bỏ dở")),
    ("Câu 6 hoặc 7 · Mất ≥15 phút HOẶC không biết rõ (ngưỡng 1 của giả thuyết)",
     lambda r: r["thoi_gian"] in ("15–30 phút", "Trên 30 phút") or r["biet_tien_di_dau"] in ("Được một phần", "Không, bỏ dở")),
    ("Câu 8 · Có khoản không nhận ra (nhiều + vài khoản) (ngưỡng 2 của giả thuyết)",
     lambda r: r["khoan_khong_nhan_ra"] in ("Có, nhiều khoản", "Có, vài khoản")),
]

da_xem = [r for r in rows if r["lan_gan_nhat"] != "Chưa bao giờ"]
chinh = [r for r in da_xem if r["vai"] == NGUOI_DUNG_CHINH]
print(f"Mẫu số: tất cả đã từng xem lại n = {len(da_xem)} · riêng '{NGUOI_DUNG_CHINH}' n = {len(chinh)}\n")
print("| Đếm gì | Tất cả | Đi làm dưới 3 năm |")
print("|---|---|---|")
for ten, f in CHI_TIEU:
    print(f"| {ten} | {pct(sum(map(f, da_xem)), len(da_xem))} | {pct(sum(map(f, chinh)), len(chinh))} |")


def so_lan(rs):
    v = [int(r["so_lan_1_thang"]) for r in rs if r["so_lan_1_thang"].strip().isdigit()]
    return f"trung vị {statistics.median(v):g} lần (min {min(v)}, max {max(v)})"


print(f"| Câu 4 · Số lần xem lại / 1 tháng qua | {so_lan(da_xem)} | {so_lan(chinh)} |")

print("\nCâu 9 · Trả lời nguyên văn:")
for r in rows:
    if r["kho_chiu_nhat"].strip():
        print(f'- phiếu #{r["phieu"]} ({r["vai"]}): "{r["kho_chiu_nhat"].strip()}"')
