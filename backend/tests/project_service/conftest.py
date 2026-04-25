import os
import sys
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
PROJECT_SERVICE_ROOT = BACKEND_ROOT / "project_service"

if str(PROJECT_SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_SERVICE_ROOT))


def _ensure_match_settings_env() -> None:
    defaults = {
        "MATCH_QUANTIZE": "0.01",
        "MATCH_LOW_LEVEL_VALUE": "0.5",
        "MATCH_MIDDLE_LEVEL_VALUE": "0.75",
        "MATCH_HIGH_LEVEL_VALUE": "1.0",
        "MATCH_DESIRDED_ROLE_COEFF": "1.0",
        "MATCH_ROLE_PRIORITY_BONUS_COEFF": "1.0",
    }
    for key, value in defaults.items():
        os.environ.setdefault(key, value)


_ensure_match_settings_env()
