
from sqlalchemy import select

from app.auth.security import generate_api_key, hash_api_key
from app.core.db import SessionLocal
from app.models import ApiClient


def main() -> None:
    client_id = 1

    with SessionLocal() as db:
        client = db.scalar(
            select(ApiClient)
            .where(ApiClient.id == client_id)
            .with_for_update()
        )

        if client is None:
            print("Client ID 1 not found. No changes made.")
            return

        print(f"Client ID: {client.id}")
        print(f"Client name: {client.name}")

        confirmation = input(
            "Rotate this client's API key? Type YES: "
        )

        if confirmation != "YES":
            print("Cancelled. No changes made.")
            return

        new_api_key = generate_api_key()
        client.key_hash = hash_api_key(new_api_key)

        try:
            db.commit()
        except Exception:
            db.rollback()
            print("Database update failed. No new key issued.")
            raise

        print("\nAPI key rotated successfully!")
        print(f"New API key: {new_api_key}")
        print("\nSave this key securely.")
        print("The previous API key is now invalid.")


if __name__ == "__main__":
    main()
