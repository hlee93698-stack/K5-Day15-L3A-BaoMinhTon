# Nội dung cập nhật CP4 cho spec và slide

Người phụ trách đánh giá/chi phí: Đinh Thị Hường · 28/11/2026.

## Kết quả đánh giá

Cặp so sánh cùng model gpt-6-luna, cùng benchmark/metric: run-2 21/29 (72,4%) → run-3 23/29 (79,3%), tăng 2 câu và 6,9 điểm phần trăm. Run ID sau cải tiến: run-3@20261128-122738. Còn trượt B07/B08/B21/B22/B24/B25; chưa đạt chuẩn 95%.

Một cải tiến: gửi thêm bảng căn cứ code vào dữ liệu cho bước viết giải thích, kèm hướng dẫn không làm theo lệnh trong mô tả giao dịch. B10 và B11 chuyển sang đạt. Không đổi phép tính, guard, intent, verifier, benchmark hoặc metric. Tổng token eval tăng từ 6.769 lên 23.619; đây là đánh đổi của việc cấp thêm căn cứ.

## Dòng changelog để Hạ cập nhật spec §10

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 28/11/2026 — CP4 | Bước viết giải thích nhận thêm bảng căn cứ code dưới dạng JSON; giữ nguyên bộ thử và chuẩn đạt | B10/B11 run-2 thiếu/mâu thuẫn căn cứ; sau cải tiến run-3 đạt 23/29 so với 21/29 |

## Chi phí và giới hạn cần thể hiện trên slide

Bảng cuối cùng: cost/cost-estimate.md. Token đo qua model thật trên 50 phiên tổng hợp; không phải 50 người dùng thật. Persona lấy từ 13 phiếu khảo sát nhóm đi làm dưới 3 năm. Tần suất trung bình 38/13 ≈ 2,9231 lần/người/tháng là hành vi xem app hiện tại; chuyển sang dùng chatbot là giả định.

Số lượt hỏi/phiên 1/2/3 và quy mô 100/1000/10000 tự ước tính. Giá Luna 0,10/0,50 USD mỗi triệu token vào/ra là giả định theo mức người phụ trách cung cấp, chưa xác minh phí host 9router; giá GPT-4o mini 0,15/0,60 được đối chiếu trang model chính thức, chỉ dùng tái định giá token Luna. Không gọi các số này là hóa đơn thực.

Hạ là người sửa spec theo phân công; tài liệu này cung cấp nội dung để cập nhật §8 và §10. Không sửa chuẩn đạt ở §7. Việc chấm thử độc lập 5 câu run-1 của Minh nằm trên nhánh minh-cp4, commit be01c3a: khớp 4/5, khác B09; không coi đó là chấm độc lập run-3.


## Số đưa vào spec §8

Lượt mô phỏng simulate-1@20261128-123231: 50 phiên, 88 lượt hỏi, 59.170 token vào và 8.627 token ra, 0 lỗi. Tỷ lệ đạt dùng trong bảng phân tích cuối: run-3 23/29 (79,3%).

| Kịch bản giá | Chi phí/phiên | Chi phí/task thành công quy đổi | Tháng thấp 100 người | Tháng cơ sở 1.000 người | Tháng cao 10.000 người |
|---|---:|---:|---:|---:|---:|
| Luna — giá giả định chưa xác minh 9router | $0.00020 | $0.00026 | $0.0834 | $0.8341 | $8.34 |
| GPT-4o mini — tái định giá token Luna | $0.00028 | $0.00035 | $0.1146 | $1.15 | $11.46 |

Bản tóm tắt do khung sinh dùng run-2 vì lượt đo bắt đầu trước khi chốt run-3. Bảng cuối được tính lại từ chính CSV bằng cost/analyze.py, dùng cùng hàm summarize và tỷ lệ run-3, không sửa artifact gốc. Chi tiết ở cost/cost-estimate.md và cost/approved-summary.md.

Kết luận đề nghị: chi phí token theo giả định thấp, nhưng chưa đủ điều kiện triển khai rộng vì độ đúng 79,3% dưới chuẩn 95%; chưa có số liệu tiết kiệm thời gian/tiền để tính ROI. Giá Luna, số người dùng và lượt hỏi/phiên còn cần kiểm chứng.
