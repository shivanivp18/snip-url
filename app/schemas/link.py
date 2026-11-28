
from datetime import datetime, timezone

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)


class LinkCreate(BaseModel):
    """Validate incoming requests to create short links."""

    long_url: HttpUrl
    custom_alias: str | None = Field(
        default=None,
        min_length=8,
        max_length=16,
        pattern=r"^[A-Za-z0-9_-]+$",
    )
    expires_at: datetime | None = None

    @field_validator("long_url")
    @classmethod
    def validate_url_length(cls, value: HttpUrl) -> HttpUrl:
        if len(str(value)) > 2048:
            raise ValueError("URL must not exceed 2048 characters")
        return value

    @model_validator(mode="after")
    def validate_expiration(self):
        if self.expires_at is not None:
            if self.expires_at.tzinfo is None:
                raise ValueError(
                    "Expiration must include a timezone"
                )

            if self.expires_at <= datetime.now(timezone.utc):
                raise ValueError(
                    "Expiration must be in the future"
                )

        return self


class LinkResponse(BaseModel):
    id: int
    code: str
    long_url: str
    short_url: str
    expires_at: datetime | None = None
    created_at: datetime
