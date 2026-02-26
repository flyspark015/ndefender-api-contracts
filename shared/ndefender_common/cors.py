from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def install_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        max_age=86400,
    )
