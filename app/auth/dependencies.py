
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.security import hash_api_key
from app.core.db import get_db
from app.models import ApiClient


api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


def get_current_client(
    api_key: Annotated[str | None, Security(api_key_header)],
    db: Annotated[Session, Depends(get_db)],
) -> ApiClient:
    """Authenticate a request using its API key."""

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    key_hash = hash_api_key(api_key)

    client = db.scalar(
        select(ApiClient).where(
            ApiClient.key_hash == key_hash
        )
    )

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return client
