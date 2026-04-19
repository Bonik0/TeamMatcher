import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
USER_SERVICE_ROOT = BACKEND_ROOT / "user_service"

if str(USER_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(USER_SERVICE_ROOT))
