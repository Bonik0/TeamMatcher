import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
EMAIL_SENDER_ROOT = BACKEND_ROOT / "email_sender_service"


if str(EMAIL_SENDER_ROOT) not in sys.path:
    sys.path.insert(0, str(EMAIL_SENDER_ROOT))
