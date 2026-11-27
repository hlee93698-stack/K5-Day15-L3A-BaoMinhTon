"""Web app của bản chạy thử: phục vụ web/ tĩnh và /api/* — chỉ thư viện chuẩn.

Chạy:  python codebase/server.py            (mặc định http://127.0.0.1:8000)
       python codebase/server.py --port 8080

API (JSON, cùng origin):
  POST /api/ask                    { text }      → { output, data, meta }   gọi agent.answer()
  GET  /api/range                                → khoảng dữ liệu, nguồn, người dùng phiên
  GET  /api/categories                           → nhóm chi + tên hiển thị
  POST /api/categories/undo                      → { tx_id, ve }             hoàn tác lần sửa gần nhất
  POST /api/categories/{tx_id}     { category }  → { tx_id, cu, moi }        người dùng chọn nhóm
Không endpoint nào nhận user_id: người dùng luôn lấy từ phiên (DEMO_USER_ID).
"""
import argparse
import json
import os
import re
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import agent  # noqa: E402
import ai  # noqa: E402
import data_access  # noqa: E402
import tracing  # noqa: E402
from rules import CATEGORY_LABELS, SPENDING_CATEGORIES  # noqa: E402
from session import current_user_id  # noqa: E402

WEB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")
STATIC = {"/": ("index.html", "text/html; charset=utf-8"),
          "/index.html": ("index.html", "text/html; charset=utf-8")}
# tracing giữ trạng thái toàn cục: mỗi lúc chỉ xử lý một lượt hỏi.
LOCK = threading.Lock()
MAX_BODY = 16 * 1024


class Handler(BaseHTTPRequestHandler):
    server_version = "TienDiDau/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("[web] %s\n" % (fmt % args))

    def _send(self, status, body, content_type="application/json; charset=utf-8"):
        raw = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(raw)

    def _body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            raise ValueError("Nội dung gửi lên quá dài")
        if not length:
            return {}
        value = json.loads(self.rfile.read(length).decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError("Cần một JSON object")
        return value

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in STATIC:
            name, content_type = STATIC[path]
            with open(os.path.join(WEB, name), "rb") as handle:
                return self._send(200, handle.read(), content_type)
        if path == "/api/range":
            start, end = data_access.available_range()
            return self._send(200, {"from": start, "to": end, "user_id": current_user_id(),
                                    "model": ai.MODEL_PROVIDER,
                                    "sources": ["Tài khoản thanh toán", "Thẻ tín dụng"]})
        if path == "/api/categories":
            return self._send(200, [{"id": c, "label": CATEGORY_LABELS[c]} for c in SPENDING_CATEGORIES]
                              + [{"id": c, "label": CATEGORY_LABELS[c], "spending": False}
                                 for c in CATEGORY_LABELS if c not in SPENDING_CATEGORIES])
        return self._send(404, {"error": "Không có trang này"})

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        try:
            body = self._body()
        except ValueError as e:
            return self._send(400, {"error": str(e)})
        try:
            if path == "/api/ask":
                text = str(body.get("text") or "").strip()
                if not text:
                    return self._send(400, {"error": "Câu hỏi trống"})
                return self._send(200, self._ask(text[:500]))
            if path == "/api/categories/undo":
                with LOCK:
                    undone = agent.undo_category()
                if not undone:
                    return self._send(409, {"error": "Chưa có lần sửa nhóm nào để hoàn tác."})
                return self._send(200, undone)
            match = re.fullmatch(r"/api/categories/(U[12]-(?:BA|CC)-\d{4})", path)
            if match:
                with LOCK:
                    changed = agent.set_category(match.group(1), str(body.get("category") or ""))
                return self._send(200, {"tx_id": changed["tx_id"], "cu": changed["cu"], "moi": changed["moi"]})
        except ValueError as e:
            return self._send(400, {"error": str(e)})
        except Exception as e:  # lỗi gọi model, mạng…: báo gọn cho giao diện
            return self._send(502, {"error": "%s: %s" % (type(e).__name__, e)})
        return self._send(404, {"error": "Không có API này"})

    @staticmethod
    def _ask(text):
        with LOCK:
            tracing.begin("web")
            try:
                result = agent.answer(text)
            finally:
                summary, _ = tracing.end()
        data = result.get("data") or {}
        period = data.get("period") or {}
        sys.stderr.write("[ask] %r → %s %s\n" % (text, data.get("kind"),
                         "%s..%s" % (period.get("from"), period.get("to")) if period else ""))
        return {"output": result.get("output", ""), "data": result.get("data"),
                "meta": {"models": summary["models"], "model_calls": summary["model_calls"],
                         "tool_calls": summary["tool_calls"], "tokens_in": summary["tokens_in"],
                         "tokens_out": summary["tokens_out"]}}


def main():
    parser = argparse.ArgumentParser(description="Web app của bản chạy thử")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT") or 8000))
    args = parser.parse_args()
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print("Web app: http://%s:%d  (model: %s · người dùng phiên: %s) — Ctrl+C để dừng"
          % (args.host, args.port, ai.MODEL_PROVIDER, current_user_id()))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
