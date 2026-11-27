# Model không tính tiền

**Trạng thái: đã chốt (27/11/2026).**

Luồng chạy cố định: code chặn phạm vi, đọc giao dịch của người dùng phiên, loại giao dịch không phải chi, tính tổng và phần trăm; model chỉ hiểu câu hỏi, gán nhóm khi đủ căn cứ và viết lời giải thích từ facts có cấu trúc. Code kiểm mọi con số trước khi trả kết quả, thử viết lại một lần nếu lệch và dùng bảng do code dựng nếu vẫn lệch. Nhóm chọn cách này thay cho agent tự chọn công cụ vì một câu trả lời trôi chảy nhưng sai số tiền nguy hiểm hơn một câu trả lời ngắn.
