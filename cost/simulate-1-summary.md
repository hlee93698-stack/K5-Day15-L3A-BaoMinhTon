# Tóm tắt mô phỏng simulate-1@20261128-123231

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| xem_it | 23 | 1 | 730 | 97 | 1.0 | 2.8 |
| xem_vua | 16 | 2 | 1281 | 206 | 1.9 | 5.1 |
| xem_nhieu | 11 | 3 | 1990 | 282 | 3.2 | 8.4 |

Tỉ lệ đạt dùng để tính: 21/29 (72%) — lượt run-2@20261127-225323

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (1.000 người) | Chi phí / tháng — cao (10.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-6-luna (vào 0.1 · ra 0.5 $/1M) | $0.00020 | $0.00028 | $0.00016 | $0.0834 | $0.8341 | $8.34 | $0.00083 |
| gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.00028 | $0.00039 | $0.00022 | $0.1146 | $1.15 | $11.46 | $0.0011 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.8) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-6-luna. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
