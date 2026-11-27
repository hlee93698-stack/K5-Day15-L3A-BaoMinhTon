# PostgreSQL lưu dữ liệu sao kê đã xác nhận

**Trạng thái: hoãn (27/11/2026)** — lõi hackathon chạy trên CSV theo [ADR 0003](0003-core-runs-on-csv-stdlib.md). Giữ ADR này làm thiết kế cho phần mở rộng "lưu qua phiên" (implementation-plan §11); nếu làm trong hackathon thì dùng SQLite có sẵn trong Python thay PostgreSQL.

Hệ thống lưu giao dịch đã chuẩn hóa, điều chỉnh nhóm chi và trạng thái hội thoại theo `user_id`. File sao kê chỉ tồn tại trong lúc đọc và xem trước; sau khi người dùng xác nhận, hệ thống giữ checksum cùng metadata lần nhập và xóa file tạm. Cách này đổi lấy khả năng hỏi qua nhiều phiên, chống nhập trùng và cô lập dữ liệu giữa người dùng, nhưng không biến database thành kho lưu tài liệu ngân hàng thô.

Mỗi truy vấn dữ liệu nhận `user_id` từ phiên đăng nhập, không lấy từ prompt hoặc output của model. Bản hackathon dùng tài khoản synthetic và biến `DEMO_USER_ID` để mô phỏng phiên đã đăng nhập; dự án không tự xây hệ thống mật khẩu.
