from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User as UserModel
from app.schemas.user import User, UserUpdate, UserCreateByAdmin, PasswordChange, AdminUserUpdate
from app.auth.dependencies import get_current_user
from app.auth.password import get_password_hash, verify_password
from app.auth.permissions import require_admin

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
def list_users(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all users (admin only).

    Args:
        current_user: Current authenticated user (must be admin)
        db: Database session

    Returns:
        List of all users

    Raises:
        HTTPException: If user is not admin
    """
    require_admin(current_user)

    users = db.query(UserModel).all()
    return users


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreateByAdmin,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new user (admin only).

    Args:
        user_data: User creation data
        current_user: Current authenticated user (must be admin)
        db: Database session

    Returns:
        Created user object

    Raises:
        HTTPException: If user is not admin, or email/username already exists
    """
    require_admin(current_user)

    # Check if email already exists
    if db.query(UserModel).filter(UserModel.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if username already exists
    if db.query(UserModel).filter(UserModel.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create new user
    new_user = UserModel(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/me", response_model=User)
def get_current_user_profile(current_user: UserModel = Depends(get_current_user)):
    """
    Get current user profile.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user object
    """
    return current_user


@router.put("/me", response_model=User)
def update_current_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile.

    Args:
        user_update: User update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user object

    Raises:
        HTTPException: If email is already taken by another user
    """
    update_data = user_update.model_dump(exclude_unset=True)

    # Check if email is being changed and is already taken
    if "email" in update_data and update_data["email"] != current_user.email:
        existing_user = db.query(UserModel).filter(
            UserModel.email == update_data["email"]
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    # Hash password if being updated
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Apply updates
    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user


@router.put("/me/password", response_model=dict)
def change_password(
    password_data: PasswordChange,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change current user's password.

    Args:
        password_data: Password change data (current and new password)
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If current password is incorrect
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Update password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}


@router.put("/{user_id}", response_model=User)
def admin_update_user(
    user_id: int,
    user_update: AdminUserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update any user's profile (admin only).
    """
    require_admin(current_user)

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    update_data = user_update.model_dump(exclude_unset=True)

    # Check email uniqueness if being changed
    if "email" in update_data and update_data["email"] != user.email:
        if db.query(UserModel).filter(UserModel.email == update_data["email"]).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    # Check username uniqueness if being changed
    if "username" in update_data and update_data["username"] != user.username:
        if db.query(UserModel).filter(UserModel.username == update_data["username"]).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

    # Hash password if being set
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Apply updates
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a user (admin only).
    """
    require_admin(current_user)

    # Prevent self-deletion
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return None
