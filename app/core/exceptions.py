from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class BaseAppException(Exception):
    def __init__(self, message: str, code: str, status_code: int) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

    def to_response(self) -> dict[str, object]:
        return {
            "success": False,
            "error": {
                "message": self.message,
                "code": self.code,
            },
        }


async def app_exception_handler(_: Request, exc: BaseAppException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.to_response())


async def unhandled_exception_handler(_: Request, __: Exception) -> JSONResponse:
    fallback = BaseAppException(
        message="An unexpected error occurred.",
        code="INTERNAL_SERVER_ERROR",
        status_code=500,
    )
    return JSONResponse(status_code=fallback.status_code, content=fallback.to_response())


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BaseAppException, app_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
