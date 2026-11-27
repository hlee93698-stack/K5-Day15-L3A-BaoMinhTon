# AI SPEC — [Tên lát cắt] · Nhóm [tên nhóm] · Phòng [XXX] · Zone [X]

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [ ] A · [ ] B · [ ] C · [ ] D · [ ] E — bài toán: [đề gợi ý trong file track, hoặc bài toán nhóm tự mở rộng] __
Data BTC cấp đã dùng (nếu có — không commit nguyên file): __

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại của việc này, trong khoá hoặc trên app thật (3–5 bước; ảnh chụp từ tài khoản của mình, đã che thông tin):
- Công cụ / AI đang được dùng cho việc này (nếu có) + nguồn. Không kiểm được thì ghi "chưa kiểm":

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể):
- Việc họ cố làm xong (`động từ + đối tượng + bối cảnh`, không có chữ AI):
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ:
- Pain (KHÔNG chữ AI): ai — đang làm gì — vướng đâu — hậu quả gì:
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): __

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

- **Impact / tháng** của hướng chọn = __ người × __ lần × __ phút = __ — nguồn từng thừa số: __ (không có nguồn thì ghi rõ *(tự ước tính)*)
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá):
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8):

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả):
- Không làm (≥3 điều):
- **Sơ đồ** — flow tổng thể từ câu hỏi của người dùng đến kết thúc (bản nháp, chốt ở CP2):

  ```mermaid
  flowchart TD
      U(["👤 Nhân viên văn phòng hỏi:<br/>'Tháng này tiền đi đâu hết vậy?'"]) --> APP["App chat<br/>(codebase/app.py)"]
      APP --> GUARD{"Chặn phạm vi<br/>(quy tắc trong code + AI phân loại)"}

      GUARD -->|"Xin tư vấn đầu tư / xin giao dịch thay /<br/>hỏi chi tiêu người khác / xin OTP"| REFUSE["Từ chối lịch sự,<br/>nói rõ giới hạn, gợi ý việc làm được"]
      REFUSE --> END

      GUARD -->|"Câu hỏi về chi tiêu của mình"| PARSE["AI hiểu câu hỏi:<br/>khoảng thời gian + loại câu hỏi<br/>(tổng hợp / so 2 tháng / 1 nhóm chi)"]
      PARSE --> CLEAR{"Đủ rõ?"}
      CLEAR -->|"Mơ hồ ('dạo này', từ lóng không hiểu)"| ASK["Hỏi lại ĐÚNG 1 câu<br/>(vd: 'Bạn muốn xem tháng 11 phải không?')"]
      ASK --> U

      CLEAR -->|"Rõ"| GET["🔧 get_transactions(user, from, to)<br/>đọc dữ liệu giả có seed (data/)"]
      GET --> HAS{"Có dữ liệu<br/>khoảng đó?"}
      HAS -->|"Không (tháng tương lai / chưa có)"| MISSING["Nói rõ thiếu dữ liệu,<br/>không ước số"]
      MISSING --> END

      HAS -->|"Có"| CAT["🔧 categorize(tx)<br/>B1: luật chuẩn hoá tên nơi bán (code)<br/>B2: AI gán nhóm cho khoản còn lại"]
      CAT --> SURE{"AI chắc chắn?"}
      SURE -->|"Không (CK không nội dung, tên lạ)"| UNK["Gán nhóm 'không rõ'<br/>— không đoán"]
      SURE -->|"Có"| GROUP["Gán nhóm chi"]
      UNK --> SUM
      GROUP --> SUM["🔧 sum_by_category / compare_months<br/>CODE cộng, tính %, xếp hạng"]

      SUM --> WRITE["AI viết câu trả lời<br/>CHỈ chép số từ output công cụ"]
      WRITE --> VERIFY{"Code kiểm: mọi con số trong<br/>câu trả lời khớp output công cụ?"}
      VERIFY -->|"Lệch"| RETRY["Viết lại 1 lần;<br/>vẫn lệch → trả bảng số thuần từ code"]
      RETRY --> SHOW
      VERIFY -->|"Khớp 100%"| SHOW["Hiện cho người dùng:<br/>• Top 3 nhóm chi + số tiền + %<br/>• Bảng giao dịch làm căn cứ<br/>• Danh sách khoản 'không rõ'"]

      SHOW --> FIX{"Người dùng sửa nhóm<br/>khoản 'không rõ'?"}
      FIX -->|"Có — người bấm chọn"| UPD["🔧 update_category(tx, nhóm)<br/>ghi lại, đảo được"]
      UPD --> SUM
      FIX -->|"Không / đã xong"| END(["✅ Người dùng biết tiền đi đâu,<br/>có căn cứ, con số đúng"])

      APP -.-> LOG[("tracing: log mọi lượt gọi<br/>model + công cụ → eval/, cost/")]
  ```

  **Đọc sơ đồ:** ô có 🔧 là công cụ trong `codebase/tools.py`. **AI chỉ quyết 3 việc**: hiểu câu hỏi và khoảng thời gian, gán nhóm (hoặc "không rõ") cho giao dịch mơ hồ, và viết lời giải thích. **Mọi phép tính do code làm**, có code kiểm lại trước khi hiện. **Đổi nhóm chi do người dùng bấm**, AI không tự đổi. Bốn nhánh dừng sớm (từ chối, hỏi lại, thiếu dữ liệu, số lệch) ứng với §5–§6.
- **Hình dạng:** [ ] workflow cố định · [ ] một agent · [ ] nhiều agent — 2 dòng lý do, và vì sao **không** chọn hình dạng phức tạp hơn:
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  |  |  |  |  |

- **Mức tự động:** [ ] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — lý do (sai thì ai chịu gì, sửa đắt hay rẻ):
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì):
- **Chỗ người duyệt** (việc AI không được tự làm):
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc |  |
  |  |  |
  |  |  |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật:

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ __% câu qua, và __"
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"): __
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`):
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
