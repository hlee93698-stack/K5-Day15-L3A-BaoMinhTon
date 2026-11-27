# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | | | | |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | | | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).

## Đánh giá CP3 ngày 27/11/2026

Người phụ trách: Đinh Hường.

Công cụ AI hỗ trợ rà code nhánh Hạ `ce9842c`, cấu hình kết nối model, tổng hợp lỗi và soạn bản chấm/báo cáo. Hường duyệt bản chấm trước khi áp dụng vào pass/ghi_chu. Kết quả chạy thật dùng `gpt-6-luna` qua 9router; token lấy từ usage API. Cấu hình unit test dùng fake để tránh gọi API thật.

Lượt bổ sung `run-2@20261127-225323` đạt 21/29 (72,4%). Chỉ cập nhật pass/ghi_chu; không sửa output, expected, token hoặc trace. Không tạo thêm phỏng vấn, trích dẫn hay số liệu khảo sát. Minh chưa chấm độc lập 5 ca theo phân công.
