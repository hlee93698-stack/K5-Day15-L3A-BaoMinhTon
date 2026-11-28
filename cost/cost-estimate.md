# Chi phí khi dùng thật — CP4

**Người phụ trách: Đinh Thị Hường · 28/11/2026.**

## 1. Đầu vào và nguồn

Token được đo bằng model thật `gpt-6-luna` qua endpoint 9router trên cùng code sau cải tiến của run-3. Cấu hình: `cost/personas.yaml`; nguồn và cách tính persona: [assumptions.md](assumptions.md).

Ba persona lấy từ 13 phiếu khảo sát người đi làm dưới 3 năm đã từng xem lại chi tiêu: xem ít 6/13, xem vừa 4/13, xem nhiều 3/13. Số phiên/người/tháng lần lượt 5/6, 9/4 và 8, là trung bình số lần tự khai trong từng nhóm. Tần suất trung bình có trọng số là 38/13 ≈ 2,9231 lần/người/tháng. Chuyển hành vi xem app sang dùng chatbot là giả định mô phỏng, chưa có số liệu sử dụng sản phẩm.

Số lượt hỏi/phiên 1/2/3 và quy mô thấp/cơ sở/cao 100/1.000/10.000 người là **tự ước tính**, không phải số khách hàng hiện có. Không suy quy mô thị trường từ 13 phiếu.

Hai kịch bản giá, đơn vị USD/1 triệu token:

| Kịch bản | Đầu vào | Đầu ra | Nguồn và ý nghĩa |
|---|---:|---:|---|
| gpt-6-luna | 0,10 | 0,50 | Tự ước tính theo mức người phụ trách cung cấp ngày 28/11; chưa xác minh phí của host 9router |
| gpt-4o-mini | 0,15 | 0,60 | [Trang model chính thức](https://developers.openai.com/api/docs/models/gpt-4o-mini), đọc 28/11/2026; chỉ tái định giá cùng token đo ở Luna |

Không áp dụng giảm giá cache, credit gói ChatGPT hoặc tỷ giá VND khi chưa có phép đo/nguồn phù hợp. Bảng không phải hóa đơn của endpoint và chưa gồm máy chủ, lưu trữ, hỗ trợ hay kiểm tra thủ công. Đo trên model Luna không chứng minh số token hoặc chất lượng của GPT-4o mini sẽ giống nhau.

## 2. Lượt đo và khả năng chạy lại

Lượt `simulate-1@20261128-123231`, seed 42, **50 phiên tổng hợp**, 88 lượt hỏi, 89 lần gọi model và 238 lần gọi công cụ. Tổng token **59.170 vào / 8.627 ra**, 0 phiên lỗi. Có 5 phiên 0 token do kết thúc ở nhánh code trước khi gọi model; 0 token không đồng nghĩa trả lời đạt.

Đây là 50 phiên chạy thật qua code/API khi cần, không phải 50 người dùng thật. Các câu lấy ngẫu nhiên từ benchmark loại thường/khó; các lượt trong phiên độc lập, không mô phỏng hội thoại có trí nhớ.

```text
python run.py simulate --rate-from eval/run-2.csv
python cost/analyze.py cost/simulate-1.csv --rate-from eval/run-3.csv
```

CSV gốc: `cost/simulate-1.csv`; trace: `traces/simulate-1.jsonl`. Lệnh đầu khởi chạy khi run-3 chưa chấm xong nên bản tóm tắt gốc `simulate-1-summary.md` dùng tỷ lệ run-2 (21/29). Sau khi chấm run-3, lệnh thứ hai dùng chính token đã đo và cùng hàm summarize của khung để tính lại theo **23/29 (79,3%)**, ghi `approved-summary.md`; không gọi API lại và không sửa các artifact gốc.

Chạy mô phỏng mới trực tiếp với tỷ lệ hiện tại bằng `python run.py simulate --rate-from eval/run-3.csv`; khung sẽ tạo lượt mới. Bảng dưới lấy từ `approved-summary.md`.

## 3. Kết quả

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


Giá Luna trong bảng là giả định chưa xác minh; hàng GPT-4o mini là đối chiếu giá trên cùng lượng token. Hai hàng không phải hai lượt đo model khác nhau.

Theo công thức của khung, chi phí/task thành công = chi phí trung bình một phiên / tỷ lệ đạt trên benchmark. Đây là chỉ số quy đổi, **không phải đo tỷ lệ mọi lượt trong phiên đều đúng**. Vì mỗi phiên có nhiều lượt, bảng còn đưa chi phí/câu hỏi đạt để đọc đúng đơn vị.

Tỷ lệ 23/29 lấy từ benchmark đầy đủ, có 6 câu từ chối, trong khi tải mô phỏng chỉ lấy thường/khó. Nếu dùng riêng tỷ lệ thường/khó 17/23 (73,9%), giá Luna cho chi phí/phiên quy đổi theo thành công khoảng 0,000277 USD, cao hơn mức 0,000258 USD tính bằng 23/29. Đây là độ nhạy của cách chọn tỷ lệ, không phải chấm riêng 50 phiên.

## 4. So với tác động và kết luận

Khảo sát ghi nhận 8/13 người dùng chính xem xong chỉ biết một phần hoặc bỏ dở; mẫu nhỏ và tự khai. Chưa đo thời gian tiết kiệm, số tiền tiết kiệm hoặc tỷ lệ người dùng giải quyết xong nhu cầu bằng sản phẩm, nên chưa quy đổi lợi ích sang USD hay khẳng định hoàn vốn.

Với kịch bản 1.000 người, tiền token ước tính theo giá Luna là khoảng 0,8341 USD/tháng; đối chiếu giá GPT-4o mini khoảng 1,15 USD/tháng. Chi phí token trong các giả định này thấp, nhưng chưa phải tổng chi phí vận hành hoặc báo giá thực của 9router.

**Kết luận:** có thể tiếp tục thử nghiệm ở quy mô nhỏ, nhưng chưa đủ cơ sở triển khai rộng: độ đúng sau cải tiến mới 23/29, dưới chuẩn 95%, và lỗi hỏi lại còn tồn tại. Cần ưu tiên chất lượng và đo giá trị người dùng trước khi tối ưu thêm tiền token.

## 5. Đánh đổi của cải tiến

Cùng bộ 29 câu và cùng model, run-2 → run-3 tăng từ 21 lên 23 câu đạt, nhưng tổng token tăng từ 6.769 lên 23.619. Theo giá Luna giả định, chi phí toàn bộ eval tăng từ 0,0013609 lên 0,0036283 USD. Đây là tính lại từ token usage, không phải hóa đơn. Gửi thêm căn cứ giúp B10/B11 nhất quán hơn nhưng làm prompt dài hơn; chưa kết luận đây là phương án tối ưu.

Bộ thử và phép đo nhỏ; chưa đo tải đồng thời, nhiều lần chạy hay biến động mạng. Số người dùng, lượt hỏi/phiên, giá Luna và việc chuyển hành vi xem app thành sử dụng chatbot đều cần kiểm chứng thêm.
