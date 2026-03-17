#!/usr/bin/env python3
"""Script to seed the database with knowledge base data (STRIDE and PASTA frameworks)."""

import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Framework, Threat, Mitigation
from app.seed_data import (
    FRAMEWORKS,
    STRIDE_THREATS,
    STRIDE_MITIGATIONS,
    PASTA_THREATS,
    PASTA_MITIGATIONS,
)


def seed_database():
    """Seed the database with frameworks, threats, and mitigations."""
    db: Session = SessionLocal()

    try:
        # Check if frameworks already exist
        existing_frameworks = db.query(Framework).filter(
            Framework.name.in_(["STRIDE", "PASTA"])
        ).all()

        if existing_frameworks:
            print("Knowledge base already seeded. Skipping...")
            return

        print("Seeding knowledge base...")

        # Create frameworks
        stride_framework = Framework(
            name=FRAMEWORKS[0]["name"],
            description=FRAMEWORKS[0]["description"]
        )
        pasta_framework = Framework(
            name=FRAMEWORKS[1]["name"],
            description=FRAMEWORKS[1]["description"]
        )

        db.add(stride_framework)
        db.add(pasta_framework)
        db.commit()
        db.refresh(stride_framework)
        db.refresh(pasta_framework)

        print(f"✓ Created frameworks: {stride_framework.name}, {pasta_framework.name}")

        # Create STRIDE threats
        for threat_data in STRIDE_THREATS:
            threat = Threat(
                framework_id=stride_framework.id,
                name=threat_data["name"],
                description=threat_data["description"],
                category=threat_data["category"],
                is_custom=False
            )
            db.add(threat)

        db.commit()
        print(f"✓ Created {len(STRIDE_THREATS)} STRIDE threats")

        # Create STRIDE mitigations
        for mitigation_data in STRIDE_MITIGATIONS:
            mitigation = Mitigation(
                framework_id=stride_framework.id,
                name=mitigation_data["name"],
                description=mitigation_data["description"],
                category=mitigation_data["category"],
                is_custom=False
            )
            db.add(mitigation)

        db.commit()
        print(f"✓ Created {len(STRIDE_MITIGATIONS)} STRIDE mitigations")

        # Create PASTA threats
        for threat_data in PASTA_THREATS:
            threat = Threat(
                framework_id=pasta_framework.id,
                name=threat_data["name"],
                description=threat_data["description"],
                category=threat_data["category"],
                is_custom=False
            )
            db.add(threat)

        db.commit()
        print(f"✓ Created {len(PASTA_THREATS)} PASTA threats")

        # Create PASTA mitigations
        for mitigation_data in PASTA_MITIGATIONS:
            mitigation = Mitigation(
                framework_id=pasta_framework.id,
                name=mitigation_data["name"],
                description=mitigation_data["description"],
                category=mitigation_data["category"],
                is_custom=False
            )
            db.add(mitigation)

        db.commit()
        print(f"✓ Created {len(PASTA_MITIGATIONS)} PASTA mitigations")

        print("\n✓ Knowledge base seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
