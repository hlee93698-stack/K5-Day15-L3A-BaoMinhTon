"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
SHOW_RAW = (os.environ.get("SHOW_RAW") or "").strip().lower() in ("1", "true", "yes")


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON bằng thư viện chuẩn và trả JSON phản hồi."""
    request = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers))
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")[:500]
        raise RuntimeError("HTTP %d: %s" % (error.code, detail))
    except urllib.error.URLError as error:
        raise RuntimeError("Không kết nối được model API: %s" % error.reason)
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def _require_config(require_key=True):
    if not MODEL_NAME:
        raise RuntimeError("MODEL_NAME đang trống trong .env")
    if require_key and not API_KEY:
        raise RuntimeError("API_KEY đang trống trong .env")


def call_openai(system, user):
    _require_config()
    url = (os.environ.get("MODEL_URL") or "https://api.openai.com/v1/chat/completions").strip()
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {"Authorization": "Bearer " + API_KEY}, {"model": MODEL_NAME, "messages": messages})
    usage = data["usage"]
    return {"text": data["choices"][0]["message"]["content"],
            "tokens_in": usage["prompt_tokens"], "tokens_out": usage["completion_tokens"]}


def call_claude(system, user):
    _require_config()
    url = (os.environ.get("MODEL_URL") or "https://api.anthropic.com/v1/messages").strip()
    data = post_json(url, {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME, "max_tokens": 1024, "system": system or "",
                      "messages": [{"role": "user", "content": user}]})
    text = "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text")
    usage = data["usage"]
    return {"text": text, "tokens_in": usage["input_tokens"], "tokens_out": usage["output_tokens"]}


def call_ollama(system, user):
    _require_config(require_key=False)
    url = (os.environ.get("MODEL_URL") or "http://localhost:11434/api/chat").strip()
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {"text": data["message"]["content"], "tokens_in": data.get("prompt_eval_count", 0),
            "tokens_out": data.get("eval_count", 0)}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if MODEL_PROVIDER in ("openai", "openai_compatible", "deepseek"):
        result = call_openai(system, user)
    elif MODEL_PROVIDER in ("anthropic", "claude"):
        result = call_claude(system, user)
    elif MODEL_PROVIDER == "ollama":
        result = call_ollama(system, user)
    else:
        raise RuntimeError("MODEL_PROVIDER không được hỗ trợ: %s" % MODEL_PROVIDER)
    return {"text": result["text"], "model": MODEL_NAME,
            "tokens_in": int(result["tokens_in"]), "tokens_out": int(result["tokens_out"])}
