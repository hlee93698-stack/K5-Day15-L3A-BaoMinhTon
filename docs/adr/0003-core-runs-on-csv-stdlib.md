# Lõi chạy trên CSV giả, chỉ thư viện chuẩn Python

**Trạng thái: đã chốt (27/11/2026)** — thay [ADR 0001](0001-postgresql-owns-confirmed-statement-data.md) cho phần lõi.

Lõi đọc giao dịch từ `data/transactions_bank.csv` và `data/transactions_card.csv` (dữ liệu giả có seed, ngân hàng dựng `DEMOBANK`), chỉ dùng thư viện chuẩn Python; nhãn người dùng sửa ghi vào `runtime/overrides.json` (không commit). Bộ chấm gọi `python run.py eval` trên máy bất kỳ — lõi phụ thuộc PostgreSQL, Docker hay Tesseract thì eval hỏng khi thiếu một trong số đó, và còn khoảng 15 giờ tới CP3. Nhóm đổi khả năng nhập sao kê và lưu qua phiên lấy một lát cắt chạy được, đo được ở mọi máy.

Hệ quả: không đọc sao kê thật, không mang tên hay bố cục tài liệu của ngân hàng thật, không commit ảnh / PDF sao kê thật. Nhập PDF giả và lưu bằng SQLite là phần mở rộng sau CP3 (implementation-plan §11).
