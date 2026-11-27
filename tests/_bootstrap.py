import os
import sys
from pathlib import Path

# Unit tests must never call the paid API configured in .env.
os.environ["MODEL_PROVIDER"] = "fake"

ROOT = Path(__file__).resolve().parents[1]
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))


def use_user(user_id):
    os.environ["DEMO_USER_ID"] = user_id
