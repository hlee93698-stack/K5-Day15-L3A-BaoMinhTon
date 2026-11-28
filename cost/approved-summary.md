# Phân tích chi phí với tỷ lệ đạt CP4

Nguồn token: `cost/simulate-1.csv`, run ID `simulate-1@20261128-123231`.

Tính lại từ CSV bằng cùng hàm summarize của khung, không gọi lại API. Giữ nguyên CSV, trace và bản tóm tắt gốc dùng tỷ lệ run-2; bảng này dùng tỷ lệ run-3 đã chấm và cấu hình cost/personas.yaml.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| xem_it | 23 | 1 | 730 | 97 | 1.0 | 2.8 |
| xem_vua | 16 | 2 | 1281 | 206 | 1.9 | 5.1 |
| xem_nhieu | 11 | 3 | 1990 | 282 | 3.2 | 8.4 |

Tỉ lệ đạt dùng để tính: 23/29 (79%) — lượt run-3@20261128-122738

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-3.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (1.000 người) | Chi phí / tháng — cao (10.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-luna (vào 0.1 · ra 0.5 $/1M) | $0.00020 | $0.00026 | $0.00015 | $0.0834 | $0.8341 | $8.34 | $0.00083 |
| gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.00028 | $0.00035 | $0.00020 | $0.1146 | $1.15 | $11.46 | $0.0011 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.8) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-6-luna. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.

Giá gpt-6-luna là giả định chưa xác minh cho 9router; hàng gpt-4o-mini chỉ đối chiếu giá trên token đo từ Luna. Đây không phải hóa đơn của endpoint. Nguồn và giả định: cost/assumptions.md.
