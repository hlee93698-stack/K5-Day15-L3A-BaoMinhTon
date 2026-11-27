# Kế hoạch triển khai — Giải thích chi tiêu cuối tháng từ sao kê (v2)

Trạng thái: **v2, 27/11/2026** — sửa từ bản v1 của Duy (nhánh `duy`, commit `c53dd00`). Nguồn sự thật về thiết kế là `spec.md` §4; file này là hướng dẫn **code**. Hai file lệch nhau thì sửa cho khớp, không tự chọn một bên.

## 0. Đổi gì so với v1 và vì sao

| v1 | v2 | Vì sao |
|---|---|---|
| Sản phẩm "BIDV statement assistant", PDF dựng theo mẫu BIDV | Ngân hàng dựng `DEMOBANK`, không mang tên hay mẫu của ngân hàng thật | Track E: tên sản phẩm thật chỉ để hình dung bối cảnh, nơi bán / ngân hàng dùng tên dựng. Bắt chước tài liệu của tổ chức thật là rủi ro |
| Ảnh sao kê thật `BIDV.jpg`, `VISA_MB.png` trong repo | **Không đưa vào repo** | README đề: repo có dữ liệu cá nhân thật → trừ 10 điểm. Track E cấm dùng sao kê thật kể cả của thành viên |
| `.markdown-collab/.mcp-server.json` (có token) | Đưa vào `.gitignore` | File bí mật sinh tự động, không commit |
| Lõi bắt buộc PostgreSQL + Docker + Tesseract | Lõi chạy bằng **thư viện chuẩn Python + CSV**; lưu trữ / PDF là mở rộng sau CP3 | Bộ chấm gọi `python run.py eval`; máy không có DB thì eval không chạy được. Còn ~15 giờ tới CP3 |
| Ngân sách, baseline, "tôi có quá tay không?" là lõi | **Ngoài lát cắt** (là hướng E2 đã loại ở spec §2) | Lát cắt nộp CP1 là 1 câu hỏi → 3 nhóm chi + căn cứ + sửa nhóm. Chưa có bằng chứng nào cho ngân sách |
| Chỉ tài khoản thanh toán, bỏ thẻ tín dụng | Giữ **tài khoản + thẻ** | Mất bẫy "trả nợ thẻ bị đếm 2 lần" — kịch bản nhóm sợ nhất ở spec §5 |
| `pytest` | `unittest` (thư viện chuẩn) | Không thêm thư viện cho lõi |
| ✅ Model không tính tiền, code kiểm số | **Giữ nguyên** (ADR 0002) | Khớp spec §4, R7 |
| ✅ `user_id` lấy từ phiên, không từ model | **Giữ, làm chặt hơn**: công cụ không có tham số `user_id` | Khớp spec §4, Input |
| ✅ So tháng dở dùng cùng cửa sổ ngày | **Giữ** — thêm vào spec §5–§6 | Dữ liệu T11 dừng ở ngày 25: so cả tháng T10 với 25 ngày T11 là sai |
| ✅ Bộ test bảo mật (U1 không đọc U2, lệnh chèn là dữ liệu) | **Giữ** | Khớp câu thử tấn công spec §5 |

Quyết định kiến trúc: [ADR 0002](adr/0002-model-does-not-compute-money.md) (giữ) · [ADR 0003](adr/0003-core-runs-on-csv-stdlib.md) (mới, thay 0001 cho lõi) · [ADR 0001](adr/0001-postgresql-owns-confirmed-statement-data.md) (hoãn).

## 1. Kết quả cần đạt (lát cắt — không đổi so với CP1)

Một nhân viên văn phòng hỏi "tháng này tiền đi đâu hết vậy?" → thấy **3 nhóm chi lớn nhất** (không tính "không rõ") kèm số tiền, %, **giao dịch làm căn cứ**, danh sách khoản **"không rõ"** và sửa được nhóm của chúng. Ba loại câu hỏi: tổng hợp 1 tháng · so 2 tháng · xem 1 nhóm chi.

## 2. Phạm vi

| Trong lát cắt (bắt buộc tới CP3) | Ngoài lát cắt |
|---|---|
| Dữ liệu CSV giả có seed: 2 người dùng, TK + thẻ, 09/2026 → 25/11/2026 | Kết nối ngân hàng / ví thật, đọc sao kê thật |
| Workflow cố định: guard → hiểu câu hỏi → lấy giao dịch → phân nhóm → code tính → viết → code kiểm số | Agent tự chọn công cụ, nhiều agent |
| 5 công cụ (§5), chặn rủi ro R1–R7 (spec §4) | Ngân sách, baseline, cảnh báo (hướng E2) |
| So 2 tháng cùng cửa sổ ngày | Tư vấn đầu tư, giao dịch thay |
| Sửa nhóm chi do người dùng bấm, hoàn tác được | Đăng nhập / mật khẩu thật |
| CLI `python run.py` + `answer(text)` cho eval | Docker, PostgreSQL, OCR *(mở rộng sau CP3, §11)* |

## 3. Cấu trúc code

Chỉ thư viện chuẩn Python. File khung (`tracing.py`, `run.py`, `eval/run_eval.py`, `cost/simulate.py`) **không sửa**.

| File | Ai | Trách nhiệm |
|---|---|---|
| `codebase/session.py` | Duy | `current_user_id()` đọc `DEMO_USER_ID` (mặc định `U1`), chỉ nhận `U1`/`U2`. `REFERENCE_DATE` = `2026-11-25` (ngày cuối có dữ liệu — "tháng này" = 11/2026) |
| `codebase/data_access.py` | Duy | Đọc `data/transactions_bank.csv` + `data/transactions_card.csv` → giao dịch chuẩn hoá (§4). **Không bao giờ mở** `labels.csv`, `summary_truth.csv` |
| `codebase/rules.py` | Duy | Chuẩn hoá tên nơi bán, luật gán nhóm, luật nhận giao dịch không phải chi (§6) |
| `codebase/guard.py` | Duy | R1: chặn từ khoá ngoài phạm vi trước khi gọi model (§7) |
| `codebase/intent.py` | Duy | Hiểu câu hỏi: luật cho câu rõ ("tháng này", "tháng 10", "so tháng 10 với 11") + model cho phần còn lại; trả JSON đã kiểm (§7) |
| `codebase/tools.py` | Duy | 5 công cụ có `@tool` (§5) |
| `codebase/verifier.py` | Duy | R7: kiểm mọi số tiền / % trong câu trả lời có trong facts (§8) |
| `codebase/report.py` | Duy | Dựng bảng kết quả bằng code — dùng cho cả phần căn cứ lẫn fallback khi R7 lệch |
| `codebase/agent.py` | Duy (Hạ review) | `answer(text) -> {"output": str}`: nối các bước đúng sơ đồ spec §4 |
| `codebase/ai.py` | Duy | Nối model thật theo `docs/connect-model.md`; chế độ `fake` vẫn chạy hết luồng |
| `tests/test_*.py` | Hường (Duy hỗ trợ) | `python -m unittest discover tests` (§10) |
| `runtime/` | — | Nhãn người dùng sửa (`overrides.json`). Đã `.gitignore`, eval chạy với thư mục trống |

## 4. Giao dịch chuẩn hoá

```text
{tx_id, user_id, source: "tai_khoan"|"the", date: "YYYY-MM-DD", time: "HH:MM:SS"|"",
 description: str (nguyên văn), amount: int VND > 0, direction: "out"|"in", fee: int}
```

- Tài khoản: `phat_sinh_no > 0` → `out`, amount = nợ · `phat_sinh_co > 0` → `in`, amount = có.
- Thẻ: `so_tien_thanh_toan > 0` → `out` · `< 0` → `in` (hoàn tiền), amount = giá trị tuyệt đối. Ngày theo `ngay_gd`. Tiền ngoại tệ: dùng `so_tien_thanh_toan` (đã gồm phí), không dùng `so_tien_gd_goc`.
- Tiền là `int`, không dùng `float`.

## 5. Hợp đồng công cụ

`user_id` **không** là tham số của công cụ nào — công cụ tự gọi `session.current_user_id()`. Model không có đường nào đọc dữ liệu người khác.

| Công cụ | Input | Output | Tác động ra ngoài |
|---|---|---|---|
| `get_transactions(from_date, to_date)` | `YYYY-MM-DD`, cả hai đầu tính | danh sách giao dịch §4 của người dùng phiên, sắp theo thời gian; `[]` nếu không có | Không |
| `categorize(transactions)` | danh sách §4 | mỗi giao dịch thêm `category`, `method: "luat"|"ai"|"mac_dinh"` | Không |
| `sum_by_category(transactions)` | danh sách đã phân nhóm | `{tong_chi, so_giao_dich, nhom: [{nhom, tong_tien, phan_tram, hang, tx_ids}], khong_ro: {tong_tien, tx_ids}, khong_tinh: {thu_nhap, hoan_tien, noi_bo}}` | Không |
| `compare_months(month_1, month_2)` | `YYYY-MM` | `{cua_so: "01–25", thang_1: {...}, thang_2: {...}, chenh_lech: [{nhom, tien, phan_tram}]}` — cùng cửa sổ ngày | Không |
| `update_category(tx_id, category)` | nhóm người dùng chọn | `{tx_id, cu, moi}`; ghi `runtime/overrides.json` | **Có** — chỉ gọi từ thao tác người dùng, không bao giờ từ model; hoàn tác = gọi lại với nhóm cũ |

**Quy tắc tính** (khớp `data/DATA_CARD.md`):
- `tong_chi` = tổng `amount` của giao dịch `out` có nhóm chi tiêu. Không cộng `thu_nhap`, `hoan_tien`, `noi_bo`.
- `phan_tram` = `tong_tien * 100 / tong_chi`, làm tròn 1 chữ số thập phân.
- Top 3 lấy từ nhóm chi tiêu **trừ `khong_ro`**; `khong_ro` hiện riêng.
- **Cửa sổ so sánh:** gọi `D` = ngày cuối có dữ liệu của tháng chưa trọn (T11 → 25). Nếu một trong hai tháng chưa trọn, cả hai tháng chỉ lấy ngày 01..D. Cả hai đều trọn thì so cả tháng.

## 6. Phân nhóm

**Nhóm chi tiêu (11):** `an_uong` · `di_lai` · `mua_sam` · `hoa_don` · `nha_o` · `giai_tri` · `suc_khoe` · `giao_duc` · `tien_mat` · `gia_dinh` · `khong_ro`. **Không phải chi (3):** `thu_nhap` · `hoan_tien` · `noi_bo`.

Thứ tự:
1. **Luật (code)** — chạy trước, luôn thắng:
   - Mọi giao dịch `in` → `thu_nhap` (lương) hoặc `hoan_tien` (mô tả có `HOAN TIEN` hoặc tiền thẻ âm). **AI không bao giờ gán nhóm cho giao dịch `in`.**
   - `TT THE TIN DUNG` → `noi_bo`.
   - Chuẩn hoá tên: bỏ dấu, viết hoa, bỏ ký tự `* . - _`, gộp khoảng trắng → so với bảng nơi bán (`XEMAU BIKE`/`XE MAU` → `di_lai`; `XEMAU FOOD` → `an_uong` — **kiểm `FOOD` trước `XE MAU`**; `GIO NAM`/`GIONAM` → `an_uong`; `RUT TIEN ATM` → `tien_mat`…).
   - Nhãn người dùng đã sửa trong `runtime/overrides.json` thắng mọi luật.
2. **AI** — chỉ cho giao dịch `out` luật chưa nhận ra. Gửi theo lô, mỗi mô tả nằm trong khối dữ liệu có đánh dấu (R4), model trả JSON `{tx_id: nhom}`. Nhóm không thuộc 11 nhóm chi, thiếu `tx_id`, hay JSON hỏng → `khong_ro`.
3. **Mặc định** — chế độ `fake` hoặc model lỗi → `khong_ro` (`method: "mac_dinh"`).

## 7. Guard và hiểu câu hỏi

**R1 — guard bằng code** (chạy trước model, không gọi model nếu chặn):
- Đầu tư: `co phieu`, `chung khoan`, `coin`, `crypto`, `dau tu`, `vang`… · Giao dịch thay: `chuyen giup`, `chuyen tien cho`, `thanh toan giup`… · Bí mật: `otp`, `mat khau`, `so the`… · Người khác: `cua vo`, `cua chong`, `cua ban`, `user 2`, `nguoi khac`…
- So khớp trên câu đã bỏ dấu, viết thường. Chặn → trả câu từ chối dựng sẵn, nói rõ giới hạn + gợi ý việc làm được.

**Hiểu câu hỏi** — luật trước, model sau. Kết quả phải đúng dạng:
```json
{"in_scope": true, "intent": "tong_hop|so_sanh|mot_nhom", "months": ["2026-11"], "category": null, "clarify": null}
```
- Luật nhận được: "tháng này" → `2026-11` · "tháng trước" → `2026-10` · "tháng N" → `2026-NN` · "so tháng A với B" → `so_sanh`. Khi luật nhận đủ thì **không gọi model** (rẻ hơn, chắc hơn).
- Model chỉ dùng khi luật không nhận ra; output phải qua kiểm: `months` đúng dạng, `intent` thuộc 3 giá trị, `category` thuộc 11 nhóm hoặc `null`. Hỏng → coi là mơ hồ.
- Mơ hồ ("dạo này", không có mốc thời gian, từ lóng không hiểu) → `clarify` = **đúng 1 câu hỏi lại**, không có con số.
- Tháng ngoài dữ liệu (trước 09/2026 hoặc sau 11/2026) → R3: nói chưa có dữ liệu, nêu khoảng đang có (01/09/2026 – 25/11/2026), không ước.

## 8. Viết câu trả lời và kiểm số (R7)

1. Code dựng **facts** từ output công cụ (số đã định dạng sẵn, vd `4.500.000đ`, `29,1%`).
2. Model viết lời giải thích ngắn từ facts; prompt cấm tính toán, cấm số không có trong facts.
3. `verifier.py` trích mọi **số tiền** (≥ 4 chữ số, có thể có dấu `.`/`,`, hoặc kèm `đ`, `k`, `tr`, `triệu`) và mọi **phần trăm** trong câu trả lời, chuẩn hoá về số nguyên / 1 chữ số thập phân, so với tập số trong facts. Bỏ qua ngày, tháng, năm, số thứ tự, số giao dịch đếm được có trong facts.
4. Lệch → viết lại 1 lần. Vẫn lệch → chỉ trả bảng do `report.py` dựng. Ghi `note("R7: …")` vào trace.
5. Output cuối luôn có: phần lời (nếu qua R7) + **bảng căn cứ do code dựng** (không qua model).

## 9. Thứ tự làm và cổng kiểm

### Cổng A — CP2, 19:30 Thứ Sáu 27/11
- [ ] Hạ: spec §4–§7 khớp file này (đã cập nhật cùng commit v2).
- [ ] Hường + Minh: ≥10 câu trong `eval/benchmark.csv` (xoá B01–B03), ≥3 metric trong `eval/metric_spec.yaml`, **chốt ngưỡng §7 và commit trước 19:30**.
- [ ] Duy: `session.py`, `data_access.py`, `rules.py`, `guard.py`, 5 công cụ, `agent.py` nối đủ bước với AI `fake` → `python run.py` đi hết luồng.
- [ ] `python run.py check` không còn cảnh báo dòng mẫu / metric.

### Cổng B — tối Thứ Sáu (nên xong trước khi ngủ)
- [ ] Duy: nối model thật trong `ai.py`; `intent.py` + bước AI của `categorize`; `verifier.py`, `report.py`.
- [ ] Hường: `tests/` (§10) chạy xanh.
- [ ] Cổng đạt khi: câu "tháng 11 so với tháng 10 tiêu nhiều hơn ở đâu?" dùng cửa sổ 01–25, số khớp `data/summary_truth.csv` tính lại theo cửa sổ; U1 không đọc được dòng nào của U2.

### Cổng C — CP3, 10:00 Thứ Bảy 28/11
- [ ] Hường: 20–30 câu (≥5 `kho`, ≥2 `tu_choi` gồm 2 câu tấn công, ≥1/3 từ người dùng thật — Minh cung cấp), `eval --try` rồi **lượt 1 chạy cùng nhau**.
- [ ] Hạ: spec §0–§7 đầy đủ (số bằng chứng từ Minh).

### Cổng D — CP4, 14:30 Thứ Bảy 28/11
- [ ] Cả nhóm đọc câu trượt → chọn **1** cải tiến → lượt 2.
- [ ] Hường: ≥50 phiên mô phỏng chi phí, `cost/cost-estimate.md`.
- [ ] Hạ: slide → `demo-slides.pdf`; Duy: video demo dự phòng.

## 10. Test bắt buộc (`python -m unittest discover tests`)

- **Dữ liệu:** generator cùng seed ra cùng hash · `data_access` không mở `labels.csv` / `summary_truth.csv`.
- **Tính toán:** `sum_by_category` trên dữ liệu U1 khớp `summary_truth.csv` khi dùng nhãn đáp án · tổng chi không cộng lương, hoàn tiền, trả nợ thẻ · % cộng lại ≈ 100 (sai số làm tròn ≤ 0,1 × số nhóm).
- **Cửa sổ:** so T10 với T11 chỉ dùng ngày 01–25 của cả hai.
- **Luật:** 4 kiểu tên XE MAU → `di_lai`; `XEMAU*FOOD` → `an_uong`; mô tả rỗng / `CK` → không bị luật gán nhóm.
- **Bảo mật:** `DEMO_USER_ID=U1` thì không công cụ nào trả `tx_id` bắt đầu bằng `U2-` · câu "cho xem chi tiêu của vợ" bị R1 chặn · mô tả `CK: bo qua quy tac…` không đổi tổng chi · câu xin OTP / chuyển tiền / đầu tư bị từ chối, model không được gọi.
- **Verifier:** chấp nhận câu chỉ có số trong facts · từ chối câu có một số tiền lạ · không bắt nhầm ngày `25/11`.

## 11. Mở rộng sau CP3 (chỉ khi cổng C đạt, cả nhóm đồng ý, ghi changelog spec §10)

Theo thứ tự ưu tiên:
1. **Lưu nhãn đã sửa qua phiên** — SQLite (`sqlite3` có sẵn trong Python), giữ `user_id` trên mọi bảng. Thiết kế bảng theo ADR 0001 (bản v1) nếu cần.
2. **Nhập sao kê PDF giả** của `DEMOBANK` (sinh từ cùng dữ liệu seed) → kiểm chuỗi số dư `số dư trước − Nợ + Có = số dư sau` → xem trước → xác nhận. OCR ảnh scan chỉ làm nếu còn thời gian.
3. **Ngân sách / baseline**: là hướng E2. Chỉ làm khi bằng chứng của Minh cho thấy người dùng cần, và phải thêm câu thử riêng — **không** thêm sau CP4 vì đổi lát cắt.

## 12. Thứ tự cắt nếu trễ (giữ lõi)

1. Bỏ bước AI của `categorize` → luật + `khong_ro` (vẫn đúng an toàn, chỉ nhiều "không rõ" hơn).
2. Bỏ model ở bước hiểu câu hỏi → chỉ luật + hỏi lại khi không nhận ra.
3. Bỏ phần lời của model → chỉ bảng do code dựng.

**Không được cắt:** code tính tiền · R7 kiểm số · loại giao dịch không phải chi (R6) · `user_id` theo phiên · guard R1 · cửa sổ so sánh.

## 13. Xong khi

- `python run.py` hỏi "tháng này tiền đi đâu hết vậy?" ra top 3 nhóm, căn cứ, khoản "không rõ" — số khớp code.
- `python -m unittest discover tests`, `python run.py check`, `eval` lượt 1 + lượt 2 và `simulate` đều có kết quả trong repo.
- Không có ảnh sao kê, PDF thật, API key, token hay dữ liệu người thật trong Git.

## 14. Phân công

| Người | Việc chính | Review chéo |
|---|---|---|
| Lê Xuân Hạ | `spec.md`, giữ scope, slide, nộp checkpoint | Review `agent.py` khớp sơ đồ §4 |
| Đỗ Đắc Duy | `codebase/` (session, data_access, rules, guard, intent, tools, verifier, report, agent, ai) | Review metric và test với Hường |
| Đinh Hường | `eval/`, `tests/`, `cost/` | Chạy test độc lập trên code của Duy |
| Hoàng Lam Minh | `evidence/`, câu người dùng thật cho benchmark, `validation/` | Chấm thử 5 output, review giọng trả lời |

Cặp Duy + Hạ khoá bản chạy thử. Cặp Hường + Minh không sửa code khi chấm lượt 1; ghi lỗi thành nhóm trước khi đề nghị thay đổi.
