from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Mitigation as MitigationModel, Framework as FrameworkModel
from app.schemas import Mitigation, MitigationCreate, MitigationUpdate

router = APIRouter(prefix="/mitigations", tags=["mitigations"])


@router.get("/", response_model=list[Mitigation])
def list_mitigations(
    framework_id: int | None = None,
    is_custom: bool | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all mitigations, optionally filtered by framework and custom flag."""
    query = db.query(MitigationModel)
    if framework_id is not None:
        query = query.filter(MitigationModel.framework_id == framework_id)
    if is_custom is not None:
        query = query.filter(MitigationModel.is_custom == is_custom)
    mitigations = query.offset(skip).limit(limit).all()
    return mitigations


@router.get("/{mitigation_id}", response_model=Mitigation)
def get_mitigation(mitigation_id: int, db: Session = Depends(get_db)):
    """Get a mitigation by ID."""
    mitigation = db.query(MitigationModel).filter(MitigationModel.id == mitigation_id).first()
    if not mitigation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mitigation with id {mitigation_id} not found"
        )
    return mitigation


@router.post("/", response_model=Mitigation, status_code=status.HTTP_201_CREATED)
def create_mitigation(mitigation: MitigationCreate, db: Session = Depends(get_db)):
    """Create a new mitigation."""
    # Check if framework exists
    framework = db.query(FrameworkModel).filter(FrameworkModel.id == mitigation.framework_id).first()
    if not framework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Framework with id {mitigation.framework_id} not found"
        )

    db_mitigation = MitigationModel(**mitigation.model_dump())
    db.add(db_mitigation)
    db.commit()
    db.refresh(db_mitigation)
    return db_mitigation


@router.put("/{mitigation_id}", response_model=Mitigation)
def update_mitigation(
    mitigation_id: int,
    mitigation: MitigationUpdate,
    db: Session = Depends(get_db)
):
    """Update a mitigation."""
    db_mitigation = db.query(MitigationModel).filter(MitigationModel.id == mitigation_id).first()
    if not db_mitigation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mitigation with id {mitigation_id} not found"
        )

    update_data = mitigation.model_dump(exclude_unset=True)

    # If framework_id is being updated, verify it exists
    if "framework_id" in update_data:
        framework = db.query(FrameworkModel).filter(FrameworkModel.id == update_data["framework_id"]).first()
        if not framework:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Framework with id {update_data['framework_id']} not found"
            )

    for field, value in update_data.items():
        setattr(db_mitigation, field, value)

    db.commit()
    db.refresh(db_mitigation)
    return db_mitigation


@router.delete("/{mitigation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mitigation(mitigation_id: int, db: Session = Depends(get_db)):
    """Delete a mitigation."""
    db_mitigation = db.query(MitigationModel).filter(MitigationModel.id == mitigation_id).first()
    if not db_mitigation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mitigation with id {mitigation_id} not found"
        )

    db.delete(db_mitigation)
    db.commit()
    return None
