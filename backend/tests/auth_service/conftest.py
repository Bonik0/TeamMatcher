import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
AUTH_SERVICE_ROOT = BACKEND_ROOT / "auth_service"


if str(AUTH_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(AUTH_SERVICE_ROOT))
