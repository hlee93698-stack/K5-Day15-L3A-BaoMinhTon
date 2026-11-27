# Tổng hợp bằng chứng pain

> Xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1. Người phụ trách: Hoàng Lam Minh.
> Tối thiểu **≥1 nguồn đạt ngưỡng**. Nhóm dùng: khảo sát (nguồn chính) + phỏng vấn (kiểm lại vì sao).
> Giả thuyết viết trước: [hypothesis.md](hypothesis.md).
> **Trạng thái:** số khảo sát là bản chụp lúc **27/11 17:37 (22 phiếu)**, form vẫn đang mở. Bản chốt sẽ cập nhật bằng cách tải lại `results.csv` và chạy lại `python evidence/survey/count.py`.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data — review Google Play (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☐ (chưa làm) | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ 3/3 người ngoài nhóm (P2 đúng nhóm người dùng chính; P1 "đi làm vài năm", chưa rõ số năm; P3 đi làm ~4 năm) | [P1](interviews/P1.md) · [P2](interviews/P2.md) · [P3](interviews/P3.md) |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ n = 22 (đã xác nhận với cả nhóm: không có phiếu của thành viên nhóm) | [questions.md](survey/questions.md) · [results.csv](survey/results.csv) · [count.py](survey/count.py) |

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

- **3/3 người** kể được một lần cụ thể trong tháng qua xem xong **chỉ biết một phần** (không có con số theo nhóm) *(n nhỏ, không ghi %)*
- **3/3** gặp khoản không nhận ra (khoản nhỏ, tên cửa hàng lạ) → thử nhớ / tra nhanh, không ra thì **bỏ qua**
- **3/3 không muốn nhập tay**: P1, P2 đã tải rồi bỏ app quản lý chi tiêu vì phải nhập từng khoản; P3 thử thống kê có sẵn trong app ngân hàng nhưng thấy phân loại chưa đúng ý
- Số lần / tháng: P1 2–3, P2 1–2, P3 ~3 · lần gần nhất mất 10–30 phút (P1 20–30, P2 10, P3 15)

| | Vai | Hình thức | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|---|
| P1 | nhân viên văn phòng, đi làm vài năm | nhắn tin Zalo · 27/11 22:30 | Có — biết sơ bộ, không có con số; khoản nhỏ không nhớ | 2–3 | 20–30 phút | lịch sử giao dịch app ngân hàng + app ví (đã bỏ app quản lý chi tiêu) |
| P2 | nhân viên văn phòng, đi làm 2 năm | trực tiếp · 27/11 21:00 | Một phần — biết sơ bộ, nhưng không coi là vấn đề thường xuyên | 1–2 | 10 phút | lịch sử giao dịch app ngân hàng (đã bỏ app quản lý chi tiêu) |
| P3 | nhân viên văn phòng, đi làm ~4 năm | gọi video · 27/11 21:30 | Một phần — kiểm tra thường xuyên nhưng không ghép thành bức tranh cả tháng | ~3 | 15 phút | lịch sử app ngân hàng, đôi khi ví, tra Google / tin nhắn (đã thử thống kê trong app) |

*Cách ghi: P1 là ghi chép đã viết lại bằng AI, không phải nguyên văn; P2 là người hỏi ghi lại sau buổi nói chuyện; P3 do người hỏi ghi nguyên văn. Chi tiết ở từng file.*

## 3. ≥5 trích dẫn nguyên văn (có nguồn, bỏ tên)

*Từ câu 9 của form ("Điều gì khó chịu nhất ở lần đó?"), chép đúng chữ. 7/22 phiếu có trả lời câu này.*

1. "Qúa nhiều giao dịch, có những giao dịch mà tôi quên hoàn toàn, không có cách nào nhớ ra được" — phiếu #12 (đi làm dưới 3 năm)
2. "Tốn thời gian lọc lại quá lâu mặc dù cuối cùng vẫn lọc ra được" — phiếu #11 (đi làm dưới 3 năm)
3. "Không nhớ ra tiêu vào cái gì" — phiếu #4 (đi làm dưới 3 năm)
4. "Mình chi tiêu quá nhiều khoản lặt vặt, không thể nhớ, không thể biết rằng hôm ý mình đã mua gì ntn" — phiếu #8 (đi làm từ 3 năm trở lên)
5. "Không thể hiểu hết là mình đã trả tiền cho những khoản gì, mất thời gian ngồi nhớ lại" — phiếu #7 (sinh viên)
6. "Không thể nhớ được là đã dùng vào việc gì" — phiếu #2 (sinh viên)
7. "Là phải ngồi nhớ lại số tiền" — phiếu #3 (sinh viên)

**Từ phỏng vấn:**

8. "Mình muốn nhìn được tháng này khoản nào tăng lên so với bình thường, chứ mở lịch sử giao dịch thì chỉ thấy từng khoản riêng lẻ thôi." — P3 (nguyên văn theo ghi chép của người hỏi)
9. "Mình không muốn biến việc chi tiêu hàng ngày thành một việc phải làm thêm." — P3
10. "Mình chỉ muốn biết gần đây có tiêu gì nhiều quá không thôi, chứ bình thường cũng không nghĩ phải theo dõi chi tiết từng khoản." — P2 (theo ghi chép của người hỏi)

*P1 không có trích nguyên văn (ghi chép đã viết lại) — ý chính: xem xong chỉ có cảm giác tiêu hơi quá, không có con số cụ thể.*

## 4. Các nguồn có khớp nhau không

Khảo sát nói: phần lớn **không biết rõ tiền đi đâu** (71%) và **gặp khoản không nhận ra** (90%), nhưng **ít người mất ≥15 phút** (24%) — đa số xem 5–15 phút rồi dừng khi mới hiểu một phần. 6/7 câu trả lời nguyên văn nói về **không nhớ / không nhận ra khoản gì**, chỉ 1 câu nói về tốn thời gian.
Phỏng vấn nói: **khớp** ở chỗ cả 3 chỉ biết một phần và đều gặp khoản không nhận ra, gặp thì bỏ qua. Phỏng vấn **giải thích vì sao dừng giữa chừng**: mục tiêu của họ không phải tổng kết chính xác, mà là *"xem gần đây có tiêu gì quá tay không"* (P2, P3) — xem đủ để yên tâm thì dừng, tự cộng thì mất công.
**Lệch / thêm:**
- Thời gian: P1 mất 20–30 phút (khảo sát: chỉ 24% mất ≥15 phút) — thời gian dao động lớn theo người, không phải pain chính.
- **Không muốn nhập tay** (3/3) — khảo sát không hỏi trực tiếp, phỏng vấn cho thấy rõ: giải pháp phải dùng dữ liệu giao dịch có sẵn.
- **Muốn thấy thay đổi bất thường** hơn là chi tiết từng khoản (P2, P3; P1 cũng muốn biết "có khoản nào tiêu quá mức mà không nhận ra") — khảo sát chưa hỏi điều này.

## 5. Kết luận *(khảo sát: bản chụp 22 phiếu, chốt lại khi đóng form · phỏng vấn: 3/3 đã xong)*

Giả thuyết ở `evidence/hypothesis.md`: **đúng một phần, phải đổi trọng tâm**.
- **Đạt** ngưỡng 1: 16/21 (76%) mất ≥15 phút hoặc không biết rõ (ngưỡng ≥50%) — nhưng gần như toàn bộ nhờ vế "không biết rõ" (15/21), vế "mất ≥15 phút" chỉ 5/21 (24%).
- **Đạt** ngưỡng 2: 19/21 (90%) gặp khoản không nhận ra (ngưỡng ≥50%); ở người dùng chính là 13/13.
- **Đạt** ngưỡng 3: 3/3 người phỏng vấn kể được một lần cụ thể trong tháng qua không hiểu hết các khoản (ngưỡng ≥2/3) — nhưng chỉ P1 mất nhiều thời gian.
- **Phải đổi:** pain chính **không phải "tốn 20–30 phút"** như giả thuyết ban đầu, mà là **xem xong vẫn không biết tiền đi đâu vì không nhận ra / không nhớ các khoản**. Số "20–30 phút / lần" ở `spec.md` §1–§2 không được khảo sát ủng hộ.

**Gợi ý cho thiết kế (từ phỏng vấn, chưa đo bằng khảo sát):** (1) không bắt nhập tay — đọc giao dịch có sẵn; (2) ngoài bảng theo nhóm, nên trả lời nhanh được câu *"tháng này khoản nào tăng so với bình thường / có gì tiêu quá tay"*; (3) thống kê có sẵn trong app bị chê vì phân loại không đúng ý → cho người dùng sửa nhóm là đúng hướng.

Điều vẫn chưa biết: khoản không nhận ra chủ yếu là loại nào (phỏng vấn: khoản nhỏ vài chục nghìn, tên cửa hàng lạ — chưa có số); bao nhiêu người muốn "xem nhanh bất thường" so với "bảng chi tiết" (mới 2/3 phỏng vấn, khảo sát chưa hỏi).
Giới hạn: mẫu từ người quen và học viên AI20K (rành công nghệ); 7/22 phiếu là sinh viên, không phải người dùng chính; câu 4–8 tự khai theo trí nhớ; phỏng vấn chỉ 3 người, P3 ngoài nhóm 1–3 năm đi làm, P1 chưa rõ số năm; ghi chép P1 đã viết lại bằng AI.

## Lịch hẹn phỏng vấn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| | Vai | Giờ hẹn | Hình thức | Đã xong? |
|---|---|---|---|---|
| P1 | nhân viên văn phòng, đi làm vài năm | 27/11 22:30 | nhắn tin Zalo | ☑ |
| P2 | nhân viên văn phòng, đi làm 2 năm | 27/11 21:00 | trực tiếp | ☑ |
| P3 | nhân viên văn phòng, đi làm ~4 năm | 27/11 21:30 | gọi video | ☑ |
