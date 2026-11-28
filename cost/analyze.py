"""Tính lại bảng chi phí từ token đã đo, không gọi API hoặc sửa artifact gốc.

python cost/analyze.py cost/simulate-1.csv --rate-from eval/run-3.csv
"""
import argparse
import csv
import json
from pathlib import Path

import simulate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path")
    parser.add_argument("--rate-from", required=True)
    parser.add_argument("--output", default="cost/approved-summary.md")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source = (root / args.csv_path).resolve()
    output = (root / args.output).resolve()
    if output == source or output.name.startswith("simulate-"):
        parser.error("Không ghi đè CSV hoặc bản tóm tắt simulate-* do khung sinh.")
    cfg, warnings = simulate.load_config()
    if warnings:
        parser.error("; ".join(warnings))
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for field in ("turns", "tokens_in", "tokens_out", "model_calls", "tool_calls"):
            row[field] = int(row[field])
        row["by_model"] = json.loads(row["tokens_by_model"])
    if len(rows) < 50 or any(row["error"] for row in rows):
        parser.error("Cần ít nhất 50 phiên hoàn tất không lỗi để lập bảng này.")
    models = simulate.measured_models(rows)
    graded, other = simulate.pick_rate(models, args.rate_from)
    if graded["models"] != models:
        parser.error("Lượt chấm và lượt đo token phải dùng cùng model.")
    lines = [
        "# Phân tích chi phí với tỷ lệ đạt CP4",
        "",
        "Nguồn token: `%s`, run ID `%s`." % (args.csv_path, rows[0]["run_id"]),
        "",
        "Tính lại từ CSV bằng cùng hàm summarize của khung, không gọi lại API. "
        "Giữ nguyên CSV, trace và bản tóm tắt gốc dùng tỷ lệ run-2; "
        "bảng này dùng tỷ lệ run-3 đã chấm và cấu hình cost/personas.yaml.",
        "",
    ]
    lines.extend(simulate.summarize(cfg, rows, graded, other))
    lines.extend([
        "",
        "Giá gpt-6-luna là giả định chưa xác minh cho 9router; "
        "hàng gpt-4o-mini chỉ đối chiếu giá trên token đo từ Luna. "
        "Đây không phải hóa đơn của endpoint. Nguồn và giả định: cost/assumptions.md.",
        "",
    ])
    output.write_text("\n".join(lines), encoding="utf-8")
    print("Đã ghi %s, dùng %d phiên và tỷ lệ %d/%d." % (
        args.output, len(rows), graded["passed"], graded["total"]))


if __name__ == "__main__":
    main()
