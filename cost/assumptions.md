# Cơ sở persona và giá CP4

Người phụ trách: Đinh Thị Hường · 28/11/2026.

## Persona

Nguồn: evidence/survey/results.csv. Chọn vai Đi làm dưới 3 năm, loại người chọn Chưa bao giờ ở lan_gan_nhat: n=13. Không loại phiếu báo 0 lần trong tháng vì người đó đã từng xem lại. Share là tỷ lệ trong 13 phiếu, không phải ước lượng thị trường.

| Persona | Mã phiếu | Số lần/tháng | Share | Trung bình lần/tháng | Lượt hỏi/phiên |
|---|---|---|---|---|---|
| xem_it | 4, 15, 16, 17, 18, 21 | 0, 1, 1, 1, 1, 1 | 6/13 | 0.833333 | 1 (tự ước tính) |
| xem_vua | 11, 12, 13, 22 | 3, 2, 2, 2 | 4/13 | 2.250000 | 2 (tự ước tính) |
| xem_nhieu | 9, 14, 19 | 4, 10, 10 | 3/13 | 8.000000 | 3 (tự ước tính) |

Số phiên/người/tháng trung bình có trọng số = (5 + 9 + 24) / 13 = 38/13 ≈ 2,9231. Đây là tần suất xem lại trong app hiện tại; chuyển sang sử dụng chatbot là giả định mô phỏng, chưa có dữ liệu sử dụng sản phẩm.

Lượt hỏi/phiên 1/2/3 và quy mô 100/1000/10000 đều là tự ước tính. Phỏng vấn P1 khoảng 2–3 lần, P2 khoảng 1–2 lần, P3 khoảng 3 lần hỗ trợ sự khác nhau về tần suất, không dùng n=3 để suy tỷ lệ dân số.

Mỗi phiên lấy câu hỏi ngẫu nhiên từ benchmark loại thuong/kho theo khung. Đây là tải tổng hợp, không phải 50 người thật dùng thử. Các lượt trong một phiên độc lập, không mô phỏng lịch sử hội thoại.

## Giá và giới hạn

- GPT-6 Luna: giả định 0,10 USD/1M input và 0,50 USD/1M output theo nội dung người phụ trách cung cấp ngày 28/11. Chưa có hóa đơn hoặc bảng giá xác thực của host 9router đang cấu hình. Dùng làm kịch bản tính, không gọi là phí thực tế.
- GPT-4o mini: trang chính thức https://developers.openai.com/api/docs/models/gpt-4o-mini được đọc ngày 28/11/2026, mục Pricing: Text tokens Per 1M tokens, Input $0.15, Cached input $0.075, Output $0.60. Mô phỏng dùng input thường 0,15 và output 0,60; không giả định cache.
- Tất cả token đo thực trên gpt-6-luna qua endpoint hiện có. Hàng gpt-4o-mini chỉ là tái định giá cùng token, không phải chạy hay đo lại model đó.
- Không quy đổi credit Codex/ChatGPT Plus/Pro sang USD/token; đó là cơ chế tính khác. Không dùng suy đoán cache hit 70–85%, RTK hoặc Caveman khi trace không đo những yếu tố đó.
- Không quy đổi sang VND vì chưa chọn nguồn tỷ giá. Chi phí chưa gồm máy chủ, lưu trữ, hỗ trợ và kiểm tra thủ công.
