# Tổng hợp bằng chứng pain

> Xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1. Người phụ trách: Hoàng Lam Minh.
> Tối thiểu **≥1 nguồn đạt ngưỡng**. Nhóm dùng: khảo sát (nguồn chính) + phỏng vấn (kiểm lại vì sao).
> Giả thuyết viết trước: [hypothesis.md](hypothesis.md).
> **Trạng thái:** số khảo sát là bản chụp lúc **27/11 17:37 (22 phiếu)**, form vẫn đang mở. Bản chốt sẽ cập nhật bằng cách tải lại `results.csv` và chạy lại `python evidence/survey/count.py`.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data — review Google Play (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☐ (chưa làm) | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ 0/3 | [P1](interviews/P1.md) · [P2](interviews/P2.md) · [P3](interviews/P3.md) |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ n = 22 *(chờ xác nhận không có phiếu của thành viên nhóm)* | [questions.md](survey/questions.md) · [results.csv](survey/results.csv) · [count.py](survey/count.py) |

## 2. Số chính

### Khảo sát (đếm bằng `python evidence/survey/count.py` trên `survey/results.csv`)

- Tổng phiếu hợp lệ: **N = 22** · vai: 14 đi làm dưới 3 năm · 7 sinh viên · 1 đi làm từ 3 năm trở lên.
- 1 phiếu chọn "Chưa bao giờ" ở câu 3 → loại khỏi mẫu số câu 4–8. Mẫu số: **tất cả đã từng xem lại n = 21** · **"Đi làm dưới 3 năm" (người dùng chính) n = 13**.

| Đếm gì | Tất cả: x/21 (%) | Đi làm dưới 3 năm: x/13 (%) |
|---|---|---|
| Câu 3 · Xem lại trong khoảng 1 tháng gần đây (tuần này / tuần trước / đầu tháng này) | 17/21 (81%) | 9/13 (69%) |
| Câu 5 · Cách làm phổ biến nhất: "Kéo xem lịch sử giao dịch trong app" | 17/21 (81%) | 11/13 (85%) |
| Câu 5 · Cộng nhẩm / ghi giấy | 9/21 (43%) | 7/13 (54%) |
| Câu 5 · Xem biểu đồ / thống kê có sẵn trong app | 6/21 (29%) | 6/13 (46%) |
| Câu 6 · Mất ≥15 phút (15–30 phút + trên 30 phút) | 5/21 (24%) | 3/13 (23%) |
| Câu 7 · Chỉ biết một phần hoặc bỏ dở | 15/21 (71%) | 8/13 (62%) |
| Câu 6 hoặc 7 · Mất ≥15 phút **hoặc** không biết rõ *(ngưỡng 1 của giả thuyết: ≥50%)* | **16/21 (76%)** | **9/13 (69%)** |
| Câu 8 · Có khoản không nhận ra (nhiều + vài khoản) *(ngưỡng 2: ≥50%)* | **19/21 (90%)** | **13/13 (100%)** |
| Câu 4 · Số lần xem lại / 1 tháng qua | trung vị 2 lần (0–10) | trung vị 2 lần (0–10) |

### Phỏng vấn

- __/3 người gặp khó khăn khi xem lại chi tiêu *(n nhỏ, không ghi %)*
- Số lần / tháng: P1 __, P2 __, P3 __ · lần gần nhất mất __–__ phút

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |

## 3. ≥5 trích dẫn nguyên văn (có nguồn, bỏ tên)

*Từ câu 9 của form ("Điều gì khó chịu nhất ở lần đó?"), chép đúng chữ. 7/22 phiếu có trả lời câu này.*

1. "Qúa nhiều giao dịch, có những giao dịch mà tôi quên hoàn toàn, không có cách nào nhớ ra được" — phiếu #12 (đi làm dưới 3 năm)
2. "Tốn thời gian lọc lại quá lâu mặc dù cuối cùng vẫn lọc ra được" — phiếu #11 (đi làm dưới 3 năm)
3. "Không nhớ ra tiêu vào cái gì" — phiếu #4 (đi làm dưới 3 năm)
4. "Mình chi tiêu quá nhiều khoản lặt vặt, không thể nhớ, không thể biết rằng hôm ý mình đã mua gì ntn" — phiếu #8 (đi làm từ 3 năm trở lên)
5. "Không thể hiểu hết là mình đã trả tiền cho những khoản gì, mất thời gian ngồi nhớ lại" — phiếu #7 (sinh viên)
6. "Không thể nhớ được là đã dùng vào việc gì" — phiếu #2 (sinh viên)
7. "Là phải ngồi nhớ lại số tiền" — phiếu #3 (sinh viên)

*(Thêm 1–2 trích dẫn từ P1–P3 sau khi phỏng vấn.)*

## 4. Các nguồn có khớp nhau không

Khảo sát nói: phần lớn **không biết rõ tiền đi đâu** (71%) và **gặp khoản không nhận ra** (90%), nhưng **ít người mất ≥15 phút** (24%) — đa số xem 5–15 phút rồi dừng khi mới hiểu một phần. 6/7 câu trả lời nguyên văn nói về **không nhớ / không nhận ra khoản gì**, chỉ 1 câu nói về tốn thời gian.
Phỏng vấn nói: __ (→ hỏi kỹ: vì sao dừng ở 5–15 phút mà chưa hiểu hết? lúc gặp khoản lạ thì làm gì?)

## 5. Kết luận *(tạm thời — theo bản chụp 22 phiếu, chốt lại khi đóng form + có phỏng vấn)*

Giả thuyết ở `evidence/hypothesis.md`: **đúng một phần, phải đổi trọng tâm**.
- **Đạt** ngưỡng 1: 16/21 (76%) mất ≥15 phút hoặc không biết rõ (ngưỡng ≥50%) — nhưng gần như toàn bộ nhờ vế "không biết rõ" (15/21), vế "mất ≥15 phút" chỉ 5/21 (24%).
- **Đạt** ngưỡng 2: 19/21 (90%) gặp khoản không nhận ra (ngưỡng ≥50%); ở người dùng chính là 13/13.
- **Phải đổi:** pain chính **không phải "tốn 20–30 phút"** như giả thuyết ban đầu, mà là **xem xong vẫn không biết tiền đi đâu vì không nhận ra / không nhớ các khoản**. Số "20–30 phút / lần" ở `spec.md` §1–§2 không được khảo sát ủng hộ.

Điều vẫn chưa biết: vì sao họ dừng khi mới hiểu một phần (bỏ cuộc? chấp nhận?); khoản không nhận ra chủ yếu là loại nào (chuyển khoản không nội dung / tên cửa hàng lạ / khoản nhỏ lặt vặt).
Giới hạn: mẫu từ người quen và học viên AI20K (rành công nghệ); 7/22 là sinh viên, không phải người dùng chính; câu 4–8 tự khai theo trí nhớ.

## Lịch hẹn phỏng vấn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| | Vai | Giờ hẹn | Hình thức | Đã xong? |
|---|---|---|---|---|
| P1 | | | | ☐ |
| P2 | | | | ☐ |
| P3 | | | | ☐ |
