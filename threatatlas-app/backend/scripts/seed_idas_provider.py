#!/usr/bin/env python3
"""Seed an `idas` OIDC provider from environment variables.

This script is intended for local/staging use. It will create an OIDC provider
record if one with the same `name` does not already exist.

Usage:
  TRIMBLE_IDAS_ISSUER=https://id.trimble.com \
  TRIMBLE_IDAS_CLIENT_ID=... \
  TRIMBLE_IDAS_CLIENT_SECRET=... \
  python3 threatatlas-app/backend/scripts/seed_idas_provider.py
"""

import os
import sys
from pathlib import Path

# Allow importing app modules from repository
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import OIDCProviderConfig
from app.auth.secrets import encrypt_secret


def main():
    name = os.environ.get("TRIMBLE_IDAS_NAME", "idas")
    display_name = os.environ.get("TRIMBLE_IDAS_DISPLAY_NAME", "Trimble IDAS")
    issuer = os.environ.get("TRIMBLE_IDAS_ISSUER")
    metadata_url = os.environ.get("TRIMBLE_IDAS_METADATA_URL")
    client_id = os.environ.get("TRIMBLE_IDAS_CLIENT_ID")
    client_secret = os.environ.get("TRIMBLE_IDAS_CLIENT_SECRET")
    scopes = os.environ.get("TRIMBLE_IDAS_SCOPES", "openid email profile")
    is_enabled = os.environ.get("TRIMBLE_IDAS_ENABLED", "true").lower() in ("1", "true", "yes")

    missing = [k for k, v in (
        ("TRIMBLE_IDAS_ISSUER", issuer),
        ("TRIMBLE_IDAS_CLIENT_ID", client_id),
        ("TRIMBLE_IDAS_CLIENT_SECRET", client_secret),
    ) if not v]

    if missing:
        print("Missing required environment variables:", ", ".join(missing))
        print("Set the variables and re-run. No changes were made.")
        return

    db: Session = SessionLocal()
    try:
        existing = db.query(OIDCProviderConfig).filter(OIDCProviderConfig.name == name).first()
        if existing:
            print(f"Provider '{name}' already exists (id={existing.id}) — skipping.")
            return

        provider = OIDCProviderConfig(
            name=name,
            display_name=display_name,
            issuer=issuer.rstrip("/"),
            metadata_url=(metadata_url or None),
            client_id=client_id,
            client_secret_encrypted=encrypt_secret(client_secret),
            scopes=scopes,
            is_enabled=is_enabled,
        )
        db.add(provider)
        db.commit()
        db.refresh(provider)
        print(f"Created provider '{name}' (id={provider.id})")

    except Exception as e:
        print("Error creating provider:", e)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
