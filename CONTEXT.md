# Giải thích chi tiêu cuối tháng từ sao kê

Hệ thống đọc giao dịch (tài khoản thanh toán + thẻ tín dụng) của người dùng đang đăng nhập và trả lời câu hỏi "tiền đi đâu?" bằng số do code tính, kèm giao dịch làm căn cứ. Model chỉ hiểu câu hỏi, gán nhóm cho khoản luật chưa nhận ra và viết lời giải thích. Bản hackathon dùng **dữ liệu giả có seed** của ngân hàng dựng `DEMOBANK` — không có sao kê hay ngân hàng thật.

Thiết kế: `spec.md` §4 · cách code: `docs/implementation-plan.md` · quyết định: `docs/adr/`.

## Ngôn ngữ

**Sao kê**:
Danh sách giao dịch của một tài khoản thanh toán hoặc một thẻ tín dụng trong một khoảng ngày. Bản hackathon: `data/transactions_bank.csv`, `data/transactions_card.csv`, `data/card_statements.csv`.
_Tránh dùng_: File giao dịch, bảng ngân hàng

**Giao dịch**:
Một dòng đã chuẩn hoá từ sao kê, thuộc đúng một người dùng, có `direction` là `out` (tiền ra) hoặc `in` (tiền vào) và `amount` là số nguyên VND dương.
_Tránh dùng_: Record, entry

**Người dùng phiên**:
`user_id` do code gán theo phiên (`DEMO_USER_ID`, mặc định `U1`). Công cụ tự lấy giá trị này; model không truyền và không đổi được.
_Tránh dùng_: user_id trong prompt

**Nhóm chi**:
Nhãn mục đích của một giao dịch tiền ra: `an_uong`, `di_lai`, `mua_sam`, `hoa_don`, `nha_o`, `giai_tri`, `suc_khoe`, `giao_duc`, `tien_mat`, `gia_dinh`, `khong_ro`.
_Tránh dùng_: Loại tiền, tag

**Không rõ** (`khong_ro`):
Nhóm của giao dịch không đủ căn cứ để gán (chuyển khoản không nội dung, QR/POS không tên). Hệ thống không đoán; người dùng tự chọn nhóm. Vẫn tính vào tổng chi nhưng không vào top 3.
_Tránh dùng_: Khác, linh tinh

**Giao dịch không phải chi**:
`thu_nhap` (lương), `hoan_tien` (hoàn tiền), `noi_bo` (trả nợ thẻ của chính mình). Luật trong code nhận, không tính vào tổng chi. Trả nợ thẻ mà tính vào chi là **đếm 2 lần**, vì từng khoản chi đã nằm trong giao dịch thẻ.
_Tránh dùng_: Chi tiêu âm

**Tổng chi**:
Tổng `amount` của giao dịch `out` có nhóm chi (gồm `khong_ro`), trong khoảng ngày đang xem.
_Tránh dùng_: Số tiền đã tiêu ước tính

**Điều chỉnh nhóm chi**:
Thay đổi nhóm chi do người dùng bấm. Hệ thống giữ nhóm cũ và nhóm mới để hoàn tác. Model không bao giờ tự điều chỉnh.
_Tránh dùng_: AI sửa giao dịch, tự học nhãn

**Cửa sổ so sánh**:
Khoảng ngày giống nhau ở hai tháng đem so. Dữ liệu tháng 11 dừng ở ngày 25 thì so ngày 01–25 của cả hai tháng.
_Tránh dùng_: So cả tháng khi một tháng chưa kết thúc

**Facts**:
Các con số do công cụ tính, đã định dạng sẵn, là nguồn duy nhất model được chép số. Mọi số tiền / % trong câu trả lời phải có trong facts (R7).
_Tránh dùng_: Ngữ cảnh, gợi ý cho model

**Ngoài lát cắt** *(không làm trong hackathon — xem implementation-plan §11)*:
Ngân sách, baseline, đánh giá "có quá tay không", nhập PDF / OCR, cơ sở dữ liệu, tư vấn đầu tư, giao dịch thay.
