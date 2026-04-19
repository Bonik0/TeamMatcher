import os
import sys
from pathlib import Path


def _ensure_core_settings_env() -> None:
    defaults = {
        "POSTGRES_DB": "test",
        "POSTGRES_USER": "test",
        "POSTGRES_PASSWORD": "test",
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "5432",
        "REDIS_PASSWORD": "test",
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "RABBITMQ_USER": "test",
        "RABBITMQ_PASSWORD": "test",
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "5672",
        "RABBITMQ_VHOST": "/",
    }
    for key, value in defaults.items():
        os.environ.setdefault(key, value)


_ensure_core_settings_env()

BACKEND_ROOT = Path(__file__).resolve().parents[1]

if str(BACKEND_ROOT) not in sys.path:
    sys.path.append(str(BACKEND_ROOT))
