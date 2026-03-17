from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Framework as FrameworkModel, User as UserModel
from app.schemas import Framework, FrameworkCreate, FrameworkUpdate
from app.auth.dependencies import get_current_user
from app.auth.permissions import require_standard_or_admin

router = APIRouter(prefix="/frameworks", tags=["frameworks"])


@router.get("/", response_model=list[Framework])
def list_frameworks(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all frameworks."""
    frameworks = db.query(FrameworkModel).offset(skip).limit(limit).all()
    return frameworks


@router.get("/{framework_id}", response_model=Framework)
def get_framework(
    framework_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a framework by ID."""
    framework = db.query(FrameworkModel).filter(FrameworkModel.id == framework_id).first()
    if not framework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Framework with id {framework_id} not found"
        )
    return framework


@router.post("/", response_model=Framework, status_code=status.HTTP_201_CREATED)
def create_framework(
    framework: FrameworkCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new framework."""
    # Require write access
    require_standard_or_admin(current_user)

    # Check if framework with same name exists
    existing = db.query(FrameworkModel).filter(FrameworkModel.name == framework.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Framework with name '{framework.name}' already exists"
        )

    db_framework = FrameworkModel(**framework.model_dump())
    db.add(db_framework)
    db.commit()
    db.refresh(db_framework)
    return db_framework


@router.put("/{framework_id}", response_model=Framework)
def update_framework(
    framework_id: int,
    framework: FrameworkUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a framework."""
    # Require write access
    require_standard_or_admin(current_user)

    db_framework = db.query(FrameworkModel).filter(FrameworkModel.id == framework_id).first()
    if not db_framework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Framework with id {framework_id} not found"
        )

    update_data = framework.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_framework, field, value)

    db.commit()
    db.refresh(db_framework)
    return db_framework


@router.delete("/{framework_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_framework(
    framework_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a framework."""
    # Require write access
    require_standard_or_admin(current_user)

    db_framework = db.query(FrameworkModel).filter(FrameworkModel.id == framework_id).first()
    if not db_framework:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Framework with id {framework_id} not found"
        )

    db.delete(db_framework)
    db.commit()
    return None
