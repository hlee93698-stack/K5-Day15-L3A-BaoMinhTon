"""Ngữ cảnh phiên demo. Model không được truyền hoặc đổi user_id."""
import os
from datetime import date

ALLOWED_USERS = {"U1", "U2"}
REFERENCE_DATE = date(2026, 11, 25)
DATA_START = date(2026, 9, 1)


def current_user_id():
    """Trả user_id tin cậy của phiên demo."""
    user_id = (os.environ.get("DEMO_USER_ID") or "U1").strip().upper()
    if user_id not in ALLOWED_USERS:
        raise ValueError("DEMO_USER_ID chỉ nhận U1 hoặc U2")
    return user_id
