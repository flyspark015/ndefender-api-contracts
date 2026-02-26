from __future__ import annotations

from fastapi import HTTPException


def http_error(detail: str, status_code: int) -> HTTPException:
    # Contract-compliant FastAPI error body: {"detail":"..."}
    return HTTPException(status_code=status_code, detail=detail)
