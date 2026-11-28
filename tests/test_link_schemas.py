
from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from app.schemas.link import LinkCreate


def test_valid_url():
    link = LinkCreate(long_url="https://www.python.org/")
    assert str(link.long_url) == "https://www.python.org/"


def test_valid_custom_alias():
    link = LinkCreate(
        long_url="https://example.com",
        custom_alias="python2026",
    )
    assert link.custom_alias == "python2026"


@pytest.mark.parametrize(
    "alias",
    ["abc", "a" * 17, "invalid alias", "invalid!"],
)
def test_invalid_alias(alias):
    with pytest.raises(ValidationError):
        LinkCreate(
            long_url="https://example.com",
            custom_alias=alias,
        )


def test_invalid_url():
    with pytest.raises(ValidationError):
        LinkCreate(long_url="not-a-valid-url")


def test_past_expiration():
    with pytest.raises(ValidationError):
        LinkCreate(
            long_url="https://example.com",
            expires_at=datetime.now(timezone.utc)
            - timedelta(days=1),
        )


def test_future_expiration():
    future = datetime.now(timezone.utc) + timedelta(days=1)
    link = LinkCreate(
        long_url="https://example.com",
        expires_at=future,
    )
    assert link.expires_at == future


def test_expiration_requires_timezone():
    with pytest.raises(ValidationError):
        LinkCreate(
            long_url="https://example.com",
            expires_at=datetime(2027, 1, 1),
        )


def test_url_exceeds_database_limit():
    with pytest.raises(ValidationError):
        LinkCreate(
            long_url="https://example.com/" + "a" * 2050,
        )
