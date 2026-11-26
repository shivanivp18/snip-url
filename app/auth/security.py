
import hashlib
import secrets


def generate_api_key() -> str:
    """Generate a cryptographically secure API key."""
    return secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    """Return a SHA-256 hexadecimal hash of an API key."""
    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()
