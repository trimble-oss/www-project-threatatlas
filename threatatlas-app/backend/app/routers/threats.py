from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Threat as ThreatModel, Framework as FrameworkModel
from app.schemas import Threat, ThreatCreate, ThreatUpdate

router = APIRouter(prefix="/threats", tags=["threats"])


@router.get("/", response_model=list[Threat])
def list_threats(
    framework_id: int | None = None,
    is_custom: bool | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all threats, optionally filtered by framework and custom flag."""
    query = db.query(ThreatModel)
    if framework_id is not None:
        query = query.filter(ThreatModel.framework_id == framework_id)
    if is_custom is not None:
        query = query.filter(ThreatModel.is_custom == is_custom)
    threats = query.offset(skip).limit(limit).all()
    return threats


@router.get("/{threat_id}", response_model=Threat)
def get_threat(threat_id: int, db: Session = Depends(get_db)):
    """Get a threat by ID."""
    threat = db.query(ThreatModel).filter(ThreatModel.id == threat_id).first()
    if not threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Threat with id {threat_id} not found"
        )
    return threat


@router.post("/", response_model=Threat, status_code=status.HTTP_201_CREATED)
def create_threat(threat: ThreatCreate, db: Session = Depends(get_db)):
    """Create a new threat."""
    # Check if framework exists
    framework = db.query(FrameworkModel).filter(FrameworkModel.id == threat.framework_id).first()
    if not framework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Framework with id {threat.framework_id} not found"
        )

    db_threat = ThreatModel(**threat.model_dump())
    db.add(db_threat)
    db.commit()
    db.refresh(db_threat)
    return db_threat


@router.put("/{threat_id}", response_model=Threat)
def update_threat(
    threat_id: int,
    threat: ThreatUpdate,
    db: Session = Depends(get_db)
):
    """Update a threat."""
    db_threat = db.query(ThreatModel).filter(ThreatModel.id == threat_id).first()
    if not db_threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Threat with id {threat_id} not found"
        )

    update_data = threat.model_dump(exclude_unset=True)

    # If framework_id is being updated, verify it exists
    if "framework_id" in update_data:
        framework = db.query(FrameworkModel).filter(FrameworkModel.id == update_data["framework_id"]).first()
        if not framework:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Framework with id {update_data['framework_id']} not found"
            )

    for field, value in update_data.items():
        setattr(db_threat, field, value)

    db.commit()
    db.refresh(db_threat)
    return db_threat


@router.delete("/{threat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_threat(threat_id: int, db: Session = Depends(get_db)):
    """Delete a threat."""
    db_threat = db.query(ThreatModel).filter(ThreatModel.id == threat_id).first()
    if not db_threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Threat with id {threat_id} not found"
        )

    db.delete(db_threat)
    db.commit()
    return None
