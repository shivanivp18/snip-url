
import getpass

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.auth.security import generate_api_key, hash_api_key
from app.core.db import SessionLocal
from app.models import ApiClient


def main() -> None:
    name = input("Enter API client name: ").strip()

    if not name or len(name) > 100:
        print("Client name must contain 1 to 100 characters.")
        return

    api_key = generate_api_key()
    key_hash = hash_api_key(api_key)

    with SessionLocal() as db:
        try:
            client = ApiClient(
                name=name,
                key_hash=key_hash,
            )

            db.add(client)
            db.commit()
            db.refresh(client)

        except IntegrityError:
            db.rollback()
            print("Could not register API client.")
            return

    print(f"\nAPI client registered successfully!")
    print(f"Client ID: {client.id}")
    print(f"Client name: {client.name}")
    print(f"API key: {api_key}")
    print("\nSAVE THIS KEY SECURELY.")
    print("It will not be stored in plaintext in MySQL.")


if __name__ == "__main__":
    main()
