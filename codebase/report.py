"""Dựng facts và bảng kết quả bằng code."""
from datetime import date


def money(value):
    return format(int(value), ",").replace(",", ".") + "đ"


def percent(value):
    return ("%.1f" % value).replace(".", ",") + "%"


def display_date(value):
    return date.fromisoformat(value).strftime("%d/%m/%Y")


def _tx_index(transactions):
    return {row["tx_id"]: row for row in transactions}


def _tx_data(row):
    """Một giao dịch ở dạng frontend hiển thị được; số giữ nguyên số nguyên đồng."""
    return {"tx_id": row["tx_id"], "date": row["date"], "description": row["description"] or "",
            "amount": row["amount"], "fee": row["fee"], "source": row["source"],
            "category": row.get("category")}


def summary_context(from_date, to_date, summary, transactions, category=None, duplicates=None):
    index = _tx_index(transactions)
    groups = summary["nhom"]
    groups = ([row for row in groups if row["nhom"] == category] if category
              else [row for row in groups if row["nhom"] != "khong_ro"][:3])
    allowed_money = {summary["tong_chi"], summary["khong_ro"]["tong_tien"]}
    allowed_percent = set()
    period = "%s–%s" % (display_date(from_date), display_date(to_date))
    facts = ["Khoảng %s, tổng chi %s." % (period, money(summary["tong_chi"]))]
    lines = ["### %s" % ("Chi tiết nhóm chi" if category else "Top nhóm chi"), "",
             "Khoảng dữ liệu: **%s**" % period,
             "Tổng chi: **%s**" % money(summary["tong_chi"]), "",
             "| Nhóm | Số tiền | Tỷ lệ |", "|---|---:|---:|"]
    evidence_ids = []
    group_data = []
    for row in groups:
        group_data.append({"nhom": row["nhom"], "tong_tien": row["tong_tien"], "phan_tram": row["phan_tram"],
                           "so_giao_dich": len(row["tx_ids"])})
        allowed_money.add(row["tong_tien"])
        allowed_percent.add(row["phan_tram"])
        facts.append("%s: %s, %s." % (row["nhom"], money(row["tong_tien"]), percent(row["phan_tram"])))
        lines.append("| %s | %s | %s |" % (row["nhom"], money(row["tong_tien"]), percent(row["phan_tram"])))
        chosen = sorted(row["tx_ids"], key=lambda tx_id: (index[tx_id]["date"], index[tx_id]["time"], tx_id))
        evidence_ids.extend(chosen if category else sorted(chosen, key=lambda tx_id: index[tx_id]["amount"], reverse=True)[:5])
        if category:
            facts.append("%s có %d giao dịch." % (row["nhom"], len(row["tx_ids"])))
            lines.append("")
            lines.append("Số giao dịch: **%d**" % len(row["tx_ids"]))
    lines.extend(["", "### Giao dịch làm căn cứ", "", "| Mã | Ngày | Diễn giải | Số tiền thanh toán | Phí |",
                  "|---|---|---|---:|---:|"])
    for tx_id in evidence_ids[:50]:
        row = index[tx_id]
        allowed_money.add(row["amount"])
        allowed_money.add(row["fee"])
        lines.append("| %s | %s | %s | %s | %s |" %
                     (tx_id, display_date(row["date"]), row["description"] or "(trống)",
                      money(row["amount"]), money(row["fee"])))
    unknown_ids = summary["khong_ro"]["tx_ids"]
    if unknown_ids and category != "khong_ro":
        facts.append("Không rõ: %s." % money(summary["khong_ro"]["tong_tien"]))
        lines.extend(["", "### Khoản không rõ · %s · %d giao dịch" %
                      (money(summary["khong_ro"]["tong_tien"]), len(unknown_ids)), ""])
        for tx_id in unknown_ids[:10]:
            row = index[tx_id]
            allowed_money.add(row["amount"])
            lines.append("- %s · %s · %s · %s" %
                         (tx_id, display_date(row["date"]), row["description"] or "(trống)", money(row["amount"])))
    excluded = [(name, amount) for name, amount in summary["khong_tinh"].items() if amount]
    if excluded:
        lines.extend(["", "### Không tính vào tổng chi", "",
                      "Lương, hoàn tiền và trả nợ thẻ được ghi riêng. Hoàn tiền không trừ ngược nhóm giao dịch gốc; "
                      "trả nợ thẻ không được cộng lại để tránh đếm đôi.", ""])
        for name, amount in excluded:
            allowed_money.add(amount)
            lines.append("- %s: %s" % (name, money(amount)))
    if duplicates:
        lines.extend(["", "### Khoản nghi trừ hai lần", "",
                      "Đây chỉ là dấu hiệu cần kiểm tra với ngân hàng; các khoản vẫn nằm trong tổng chi.", ""])
        for group in duplicates:
            allowed_money.add(group["so_tien"])
            lines.append("- %s · %s · %s · %s" %
                         (", ".join(group["tx_ids"]), display_date(group["ngay"]), group["mo_ta"], money(group["so_tien"])))
    evidence = [_tx_data(index[tx_id]) for tx_id in evidence_ids[:50]]
    data = {
        "kind": "mot_nhom" if category else "tong_hop",
        "period": {"from": from_date, "to": to_date},
        "total": summary["tong_chi"], "count": summary["so_giao_dich"], "category": category,
        "groups": [{"nhom": row["nhom"], "tong_tien": row["tong_tien"], "phan_tram": row["phan_tram"],
                    "so_giao_dich": len(row["tx_ids"])} for row in groups],
        "unknown": {"tong_tien": summary["khong_ro"]["tong_tien"],
                    "items": [_tx_data(index[tx_id]) for tx_id in unknown_ids]},
        "largest": None if category or not evidence else max(evidence, key=lambda row: row["amount"]),
        "evidence": evidence,
        "excluded": dict(summary["khong_tinh"]),
        "duplicates": duplicates or [],
    }
    return {"facts": "\n".join(facts), "report": "\n".join(lines), "data": data,
            "allowed_money": allowed_money, "allowed_percent": allowed_percent}


def search_context(from_date, to_date, label, rows, total_spending):
    """Các khoản chi khớp diễn giải: tổng, số khoản, gộp theo diễn giải, danh sách đầy đủ — đều do code tính."""
    rows = sorted(rows, key=lambda row: (row["date"], row["time"], row["tx_id"]))
    total = sum(row["amount"] for row in rows)
    share = round(total * 100.0 / total_spending, 1) if total_spending else 0.0
    by_text = {}
    for row in rows:
        key = row["description"] or "(trống)"
        entry = by_text.setdefault(key, {"description": key, "tong_tien": 0, "so_giao_dich": 0})
        entry["tong_tien"] += row["amount"]
        entry["so_giao_dich"] += 1
    merchants = sorted(by_text.values(), key=lambda entry: (-entry["tong_tien"], entry["description"]))
    period = "%s–%s" % (display_date(from_date), display_date(to_date))
    allowed_money = {total, total_spending} | {row["amount"] for row in rows} | {m["tong_tien"] for m in merchants}
    facts = ["Khoảng %s. %s: %s, %d giao dịch, %s tổng chi %s." %
             (period, label, money(total), len(rows), percent(share), money(total_spending))]
    lines = ["### %s" % label, "", "Khoảng dữ liệu: **%s**" % period,
             "Tổng: **%s** · %d giao dịch · %s tổng chi" % (money(total), len(rows), percent(share)), ""]
    if not rows:
        lines.append("Không có giao dịch chi nào có diễn giải khớp trong khoảng này.")
    else:
        lines.extend(["| Mã | Ngày | Diễn giải | Số tiền |", "|---|---|---|---:|"])
        for row in rows:
            lines.append("| %s | %s | %s | %s |" % (row["tx_id"], display_date(row["date"]),
                                                    row["description"] or "(trống)", money(row["amount"])))
    data = {"kind": "tim_kiem", "period": {"from": from_date, "to": to_date}, "label": label,
            "total": total, "count": len(rows), "share": share, "total_spending": total_spending,
            "merchants": merchants, "items": [_tx_data(row) for row in rows]}
    return {"facts": "\n".join(facts), "report": "\n".join(lines), "data": data,
            "allowed_money": allowed_money, "allowed_percent": {share}}


def duplicates_context(from_date, to_date, summary, duplicates):
    allowed_money = {summary["tong_chi"]}
    shown_from, shown_to = display_date(from_date), display_date(to_date)
    facts = ["Khoảng %s–%s, tổng chi %s." % (shown_from, shown_to, money(summary["tong_chi"]))]
    lines = ["### Giao dịch nghi trừ hai lần", "", "Khoảng dữ liệu: **%s–%s**" % (shown_from, shown_to), "",
             "Đây chỉ là dấu hiệu cần kiểm tra với ngân hàng; không khẳng định giao dịch sai và không tự loại khỏi tổng.", ""]
    if not duplicates:
        lines.append("Không tìm thấy cặp giao dịch trùng theo cùng nguồn, ngày, mô tả và số tiền.")
    for group in duplicates:
        allowed_money.add(group["so_tien"])
        facts.append("Nghi trùng %s: %s, %s." %
                     (", ".join(group["tx_ids"]), group["mo_ta"], money(group["so_tien"])))
        lines.extend(["- Mã: **%s**" % ", ".join(group["tx_ids"]),
                      "  - Ngày: %s" % display_date(group["ngay"]), "  - Mô tả: %s" % group["mo_ta"],
                      "  - Mỗi khoản: %s" % money(group["so_tien"])])
    lines.extend(["", "Tổng chi vẫn là **%s**." % money(summary["tong_chi"])])
    data = {"kind": "kiem_trung", "period": {"from": from_date, "to": to_date},
            "total": summary["tong_chi"], "duplicates": duplicates}
    return {"facts": "\n".join(facts), "report": "\n".join(lines), "data": data,
            "allowed_money": allowed_money, "allowed_percent": set()}


def comparison_context(result):
    left, right = result["thang_1"], result["thang_2"]
    left_groups = {row["nhom"]: row["tong_tien"] for row in left["nhom"]}
    right_groups = {row["nhom"]: row["tong_tien"] for row in right["nhom"]}
    total_delta = right["tong_chi"] - left["tong_chi"]
    allowed_money = {left["tong_chi"], right["tong_chi"], abs(total_delta)}
    allowed_percent = set()
    facts = ["Cửa sổ %s." % result["cua_so"], "%s: %s." % (left["month"], money(left["tong_chi"])),
             "%s: %s." % (right["month"], money(right["tong_chi"]))]
    lines = ["### So sánh chi tiêu", "", "Cửa sổ: `%s`" % result["cua_so"], "",
             "| Tháng | Tổng chi |", "|---|---:|", "| %s | %s |" % (left["month"], money(left["tong_chi"])),
             "| %s | %s |" % (right["month"], money(right["tong_chi"])), "",
             "Chênh lệch tổng: **%s%s**" % ("+" if total_delta > 0 else "-" if total_delta < 0 else "",
                                             money(abs(total_delta))),
             "", "### Ba nhóm tăng nhiều nhất", "",
             "| Nhóm | %s | %s | Chênh lệch | Tỷ lệ so với tháng đầu |" % (left["month"], right["month"]),
             "|---|---:|---:|---:|---:|"]
    increases = [row for row in result["chenh_lech"] if row["tien"] > 0][:3]
    increase_data = []
    for row in increases:
        increase_data.append({"nhom": row["nhom"], "truoc": left_groups.get(row["nhom"], 0),
                              "sau": right_groups.get(row["nhom"], 0), "tien": row["tien"],
                              "phan_tram": row["phan_tram"]})
        before, after = left_groups.get(row["nhom"], 0), right_groups.get(row["nhom"], 0)
        allowed_money.update((before, after))
        allowed_money.add(abs(row["tien"]))
        if row["phan_tram"] is not None:
            allowed_percent.add(row["phan_tram"])
            allowed_percent.add(abs(row["phan_tram"]))
        sign = "+" if row["tien"] > 0 else "-" if row["tien"] < 0 else ""
        pct = "—" if row["phan_tram"] is None else ("+" if row["phan_tram"] > 0 else "") + percent(row["phan_tram"])
        lines.append("| %s | %s | %s | %s%s | %s |" %
                     (row["nhom"], money(before), money(after), sign, money(abs(row["tien"])), pct))
        facts.append("%s: %s lên %s, chênh %s%s." %
                     (row["nhom"], money(before), money(after), sign, money(abs(row["tien"]))))
    decreases = [row for row in result["chenh_lech"] if row["tien"] < 0]
    drop = min(decreases, key=lambda row: row["tien"]) if decreases else None
    data = {
        "kind": "so_sanh", "window": result["cua_so"],
        "months": [{"month": side["month"], "from": side["from_date"], "to": side["to_date"],
                    "total": side["tong_chi"]} for side in (left, right)],
        "delta": total_delta, "increases": increase_data,
        "biggest_drop": None if not drop else {
            "nhom": drop["nhom"], "truoc": left_groups.get(drop["nhom"], 0),
            "sau": right_groups.get(drop["nhom"], 0), "tien": drop["tien"]},
    }
    return {"facts": "\n".join(facts), "report": "\n".join(lines), "data": data,
            "allowed_money": allowed_money, "allowed_percent": allowed_percent}
