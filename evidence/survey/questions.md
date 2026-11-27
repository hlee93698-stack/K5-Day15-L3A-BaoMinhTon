# Khảo sát — bộ câu hỏi và cách gửi

- **Tên form:** Lần gần nhất bạn xem tiền mình đi đâu (Google Form)
- **Link:** https://docs.google.com/forms/d/e/1FAIpQLSejL8ix66FTy4pC0IqqLXal-7QFIvRXqpBG60-qLM94RzgaZQ/viewform
- **Mô tả trên form:** Nhóm mình đang tìm hiểu cách mọi người xem lại chi tiêu cuối tháng. Khảo sát khoảng 3 phút, ẩn danh. Form không hỏi thu nhập, số dư hay số tiền cụ thể, và không thu email.
- **Người phụ trách:** Hoàng Lam Minh (tổng hợp) · Lê Xuân Hạ (tạo form)

## Gửi ở đâu, khi nào

| Kênh đã gửi (vd: nhóm Zalo lớp L3B, Facebook cá nhân, nhóm đồng nghiệp) | Giờ gửi | Ghi chú |
|---|---|---|
| __ | __ | __ |
| __ | __ | __ |

- **Giờ mở form:** 27/11/2026, phiếu đầu tiên lúc 14:55
- **Bản chụp đang dùng:** 27/11/2026 17:37 — 22 phiếu (form vẫn mở)
- **Giờ chốt (ngừng nhận để đếm):** __/11/2026 __:__
- **Tổng số câu trả lời lúc chốt:** __ · trong đó người trong nhóm (loại ra): 0 *(đã hỏi cả nhóm 27/11: không thành viên nào điền form)* · còn lại: __

## Bộ câu hỏi (chép nguyên văn từ form)

| # | Câu hỏi | Kiểu | Lựa chọn |
|---|---|---|---|
| 1 | Bạn hiện là * | Chọn một | Sinh viên · Đi làm dưới 3 năm · Đi làm từ 3 năm trở lên · Người lo chi tiêu cả nhà · Mục khác |
| 2 | Bạn chi tiêu hằng ngày chủ yếu qua * | Chọn nhiều | Ví điện tử · App ngân hàng · Thẻ tín dụng · Tiền mặt |
| 3 | Lần gần nhất bạn ngồi xem lại tiền của mình đã đi vào những khoản nào là khi nào? * | Chọn một | Tuần này · Tuần trước · Đầu tháng này · Hơn 1 tháng trước · Chưa bao giờ |
| 4 | Trong 1 tháng qua, bạn xem lại chi tiêu như vậy mấy lần? (ghi số, ví dụ 0, 1, 3) * | Số | — |
| 5 | Lần gần nhất đó, bạn đã làm thế nào? * | Chọn nhiều | Kéo xem lịch sử giao dịch trong app · Xem biểu đồ/thống kê có sẵn trong app · Chép ra Excel/Google Sheets · Dùng app quản lý chi tiêu riêng · Cộng nhẩm/ghi giấy · Hỏi ChatGPT/AI · Bỏ qua, không xem nữa · Mục khác |
| 6 | Lần đó mất khoảng bao lâu? * | Chọn một | Dưới 5 phút · 5–15 phút · 15–30 phút · Trên 30 phút |
| 7 | Lần đó bạn có biết được tiền đã đi đâu không? * | Chọn một | Có, rõ ràng · Được một phần · Không, bỏ dở |
| 8 | Lần đó có khoản nào bạn không nhận ra là khoản gì không (chuyển khoản không ghi nội dung, tên cửa hàng khó hiểu…)? * | Chọn một | Có, nhiều khoản · Có, vài khoản · Không có · Không nhớ |
| 9 | Điều gì khó chịu nhất ở lần đó? | Đoạn văn (không bắt buộc) | — |
| 10 | Bạn có sẵn lòng cho nhóm hỏi thêm 10 phút không? Nếu có, để lại cách liên hệ | Đoạn ngắn (không bắt buộc) | — |

`*` = bắt buộc.

## Xử lý trước khi commit `results.csv`

- Xoá cột **Dấu thời gian** và cột **câu 10** (liên hệ). Bản gốc còn liên hệ giữ riêng, **không commit**.
- Thêm cột `phieu` đánh số 1, 2, 3… để trích dẫn ("phiếu #4").
- Loại phiếu của người trong nhóm (nếu có), ghi số phiếu đã loại ở bảng trên.

## Sửa form trong lúc chạy (nếu có)

- __ (vd: 27/11 17:10 bỏ bắt buộc câu 4–8 cho người chọn "Chưa bao giờ" — có __ phiếu trả lời trước khi sửa)
