from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:3000",
]


def set_default_cors_policy(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
