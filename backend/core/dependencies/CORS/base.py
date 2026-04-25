from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def _get_origins_default() -> list[str]:
    return [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
    ]


def set_default_cors_policy(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_get_origins_default(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
