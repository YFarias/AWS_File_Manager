from __future__ import annotations

import jwt
from jwt import InvalidTokenError
from pydantic import BaseModel, Field

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings
from app.core.exceptions import BaseAppException

security_scheme = HTTPBearer(auto_error=False)


class AuthenticatedUser(BaseModel):
    user_id: str
    scopes: list[str] = Field(default_factory=list)


def _decode_token(token: str) -> dict[str, object]:
    settings = get_settings()
    decode_kwargs: dict[str, object] = {}
    options = {"verify_aud": bool(settings.jwt_audience)}

    if settings.jwt_audience:
        decode_kwargs["audience"] = settings.jwt_audience
    if settings.jwt_issuer:
        decode_kwargs["issuer"] = settings.jwt_issuer

    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        options=options,
        **decode_kwargs,
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
) -> AuthenticatedUser:
    if credentials is None:
        raise BaseAppException(
            message="Authentication token is required.",
            code="UNAUTHORIZED",
            status_code=401,
        )

    token = credentials.credentials
    try:
        payload = _decode_token(token)
    except InvalidTokenError as exc:
        raise BaseAppException(
            message="Invalid authentication token.",
            code="INVALID_TOKEN",
            status_code=401,
        ) from exc

    user_id = payload.get("sub") or payload.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        raise BaseAppException(
            message="Token does not include a valid subject.",
            code="INVALID_TOKEN_SUBJECT",
            status_code=401,
        )

    raw_scopes = payload.get("scopes", [])
    if isinstance(raw_scopes, str):
        scopes = [raw_scopes]
    elif isinstance(raw_scopes, list):
        scopes = [str(scope) for scope in raw_scopes]
    else:
        scopes = []

    return AuthenticatedUser(user_id=user_id, scopes=scopes)
